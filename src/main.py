import curses
import os
import select
import socket

from lib.rsa import RSAHandler


def receive_all(sock, length):
    """
    Ensure that exactly length bytes are read from the socket.
    """
    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:  # Connection closed
            raise ConnectionError("Socket connection closed before receiving all data.")
        data += chunk
    return data


def act_as_client(stdscr, rsa_handler, history):
    host = get_user_input(stdscr, "Enter server IP address: ", history)
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)

    try:
        client_socket.connect((host, port))
    except BlockingIOError:
        pass

    history.append(f"Connecting to {host}:{port}")
    stdscr.refresh()

    # Wait for server's public key
    server_public_key_bytes = None
    while not server_public_key_bytes:
        try:
            readable, _, _ = select.select([client_socket], [], [], 5)
            if readable:
                server_public_key_bytes = client_socket.recv(4096)
                history.append("Received server's public key")
        except Exception as e:
            history.append(f"Error during public key exchange: {str(e)}")
            client_socket.close()
            return

    if not server_public_key_bytes:
        history.append("Failed to receive server's public key")
        client_socket.close()
        return

    # Load server's public key
    server_public_key = rsa_handler.import_key(server_public_key_bytes)

    try:
        # Get message to send
        message = get_user_input(stdscr, "Enter message to encrypt: ", history)
        encrypted_message = rsa_handler.encrypt(server_public_key, message)

        # Send encrypted message
        message_length = len(encrypted_message).to_bytes(4, "big")
        client_socket.sendall(message_length + encrypted_message)
        history.append(
            f"Sent encrypted message: {truncate_ciphertext(encrypted_message)}"
        )
    except BrokenPipeError:
        history.append("Connection closed by server.")
    except Exception as e:
        history.append(f"Error sending message: {str(e)}")
    finally:
        client_socket.close()


def act_as_server(stdscr, rsa_handler, keys_folder, history):
    host = "0.0.0.0"
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    server_socket.setblocking(False)

    public_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep.pub"))
    private_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep"))

    history.append(f"Server listening on {host}:{port}")
    stdscr.refresh()

    inputs = [server_socket]
    try:
        while True:
            readable, _, _ = select.select(inputs, [], [], 1)  # 1-second timeout
            for s in readable:
                if s is server_socket:
                    conn, address = server_socket.accept()
                    conn.setblocking(False)
                    inputs.append(conn)
                    history.append(f"Connection from: {address}")
                    stdscr.refresh()

                    # Send public key immediately after connection
                    public_key_bytes = public_key.export_key()
                    conn.sendall(public_key_bytes)
                else:
                    try:
                        # Read length of incoming message
                        if s in readable:
                            length_bytes = s.recv(4)
                            if not length_bytes:
                                raise ConnectionError("Client disconnected.")

                            message_length = int.from_bytes(length_bytes, "big")
                            encrypted_message = receive_all(s, message_length)

                            # Decrypt the message
                            decrypted_message = rsa_handler.decrypt(
                                private_key, encrypted_message
                            )
                            history.append(
                                f"Received and decrypted message: {decrypted_message}"
                            )
                            stdscr.refresh()

                            # Send response
                            response = f"Server received: {decrypted_message}"
                            response_encrypted = rsa_handler.encrypt(
                                public_key, response
                            )
                            response_length = len(response_encrypted).to_bytes(4, "big")
                            s.sendall(response_length + response_encrypted)
                    except BlockingIOError:
                        # No data available, continue to the next socket
                        continue
                    except ConnectionError as e:
                        history.append(f"Connection closed: {str(e)}")
                        inputs.remove(s)
                        s.close()
                    except Exception as e:
                        history.append(f"Error: {str(e)}")
                        inputs.remove(s)
                        s.close()
    except KeyboardInterrupt:
        history.append("Server shutting down")
        stdscr.refresh()
    finally:
        server_socket.close()


def display_ascii_art(stdscr):
    """
    Display ASCII art at the start of the program.
    """
    art = r"""
  ___ ___   ____     _____                                                                              
 /   |   \ /  _ \   /     \                                                                             
/    ~    \>  _ </\/  \ /  \                                                                            
\    Y    /  <_\ \/    Y    \                                                                           
 \___|_  /\_____\ \____|__  /                                                                           
       \/        \/       \/                                                                            
__________  _________   _____    ___________ _______  ________________________.___._____________________
\______   \/   _____/  /  _  \   \_   _____/ \      \ \_   ___ \______   \__  |   |\______   \__    ___/
 |       _/\_____  \  /  /_\  \   |    __)_  /   |   \/    \  \/|       _//   |   | |     ___/ |    |   
 |    |   \/        \/    |    \  |        \/    |    \     \___|    |   \\____   | |    |     |    |   
 |____|_  /_______  /\____|__  / /_______  /\____|__  /\______  /____|_  // ______| |____|     |____|   
        \/        \/         \/          \/         \/        \/       \/ \/                            
"""
    return art


def manage_history(history, max_entries=8):
    """
    Manage the history list to prevent it from growing too large.

    Args:
        history (list): List of history entries
        max_entries (int, optional): Maximum number of entries to keep. Defaults to 8.

    Returns:
        list: Managed history list
    """
    # Always keep the first entry (ASCII art)
    if len(history) > max_entries:
        # Keep the first entry (ASCII art) and the most recent entries
        return [history[0]] + history[-max_entries:]
    return history


def menu_navigation(stdscr, menu, history):
    """
    Display menu on the left side and history on the right side with a labeled messages section.

    Modify the function to use the new history management
    """
    # Manage history before display
    history = manage_history(history)

    current_row = 0
    max_y, max_x = stdscr.getmaxyx()

    # Split the screen into sections
    ascii_art_lines = history[0].split("\n")
    ascii_art_height = len(ascii_art_lines)

    # Calculate screen layout
    menu_width = max_x // 3  # Left third of the screen for menu
    history_width = max_x - menu_width  # Right two-thirds for history

    while True:
        stdscr.clear()

        # Display ASCII art at the top across full width
        for i, line in enumerate(ascii_art_lines):
            try:
                stdscr.addstr(i, 0, line[: max_x - 1])
            except curses.error:
                pass  # Ignore potential screen boundary errors

        # Menu section (left side)
        menu_start_y = ascii_art_height + 1
        menu_border = " ╔═════Menu═════════════════════╗"
        stdscr.addstr(menu_start_y, 0, menu_border)

        for idx, row in enumerate(menu):
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(menu_start_y + idx + 1, 1, f"║ {row}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(menu_start_y + idx + 1, 1, f"║ {row}")

        menu_border = " ╚══════════════════════════════╝"
        stdscr.addstr(menu_start_y + len(menu) + 1, 0, menu_border)

        # Messages section (right side)
        messages_start_y = menu_start_y
        messages_border = "══════Messages══════════════════════════"
        messages_end_border = "═════════════════════════════════════════"

        # Draw messages border
        stdscr.addstr(messages_start_y, menu_width, messages_border)
        stdscr.addstr(messages_start_y + len(menu) + 1, menu_width, messages_end_border)

        # Display history in the messages section
        max_history_lines = len(menu)
        display_history = history[1 : max_history_lines + 1] if len(history) > 1 else []

        for i, hist_entry in enumerate(display_history):
            try:
                # Truncate long lines to prevent wrapping
                truncated_entry = hist_entry[: history_width - 4]
                stdscr.addstr(messages_start_y + i + 1, menu_width + 1, truncated_entry)
            except curses.error:
                break  # Stop if we run out of screen space

        stdscr.refresh()

        key = stdscr.getch()
        if key in [curses.KEY_UP, ord("k")]:
            current_row = (current_row - 1) % len(menu)
        elif key in [curses.KEY_DOWN, ord("j")]:
            current_row = (current_row + 1) % len(menu)
        elif key in [10, ord("\n")]:  # Enter key
            if current_row == len(menu) - 1:
                return None
            return current_row


def get_user_input(stdscr, prompt, history):
    """
    Display a prompt and get user input while preserving menu and history layout.
    """

    history = manage_history(history)
    # Calculate screen dimensions
    max_y, max_x = stdscr.getmaxyx()

    # Calculate ASCII art height
    ascii_art_lines = history[0].split("\n")
    ascii_art_height = len(ascii_art_lines)

    menu = [
        "Generate RSA keypairs",
        "Encrypt message",
        "Decrypt message",
        "Encrypt file",
        "Decrypt file",
        "Acts as a server",
        "Acts as a client",
        "Quit",
    ]

    # Split the screen into sections
    menu_width = max_x // 3  # Left third of the screen for menu
    history_width = max_x - menu_width  # Right two-thirds for history

    # Calculate input start position
    input_prompt_y = max_y - 3
    input_y = max_y - 2

    # Clear the input lines
    stdscr.addstr(input_prompt_y, 0, " " * max_x)
    stdscr.addstr(input_y, 0, " " * max_x)

    # Display prompt for input
    stdscr.addstr(input_prompt_y, 0, prompt)

    # Preserve previous screen layout
    # Redraw ASCII art
    for i, line in enumerate(ascii_art_lines):
        try:
            stdscr.addstr(i, 0, line[: max_x - 1])
        except curses.error:
            pass  # Ignore potential screen boundary errors

    # Redraw menu section (left side)
    menu_start_y = ascii_art_height + 1
    menu_border = " ╔═════Menu═════════════════════╗"
    stdscr.addstr(menu_start_y, 0, menu_border)

    for idx, row in enumerate(menu):
        stdscr.addstr(menu_start_y + idx + 1, 1, f"║ {row}")

    menu_border = " ╚══════════════════════════════╝"
    stdscr.addstr(menu_start_y + len(menu) + 1, 0, menu_border)

    # Redraw Messages section (right side)
    messages_start_y = menu_start_y
    messages_border = "══════Messages══════════════════════════"
    messages_end_border = "═════════════════════════════════════════"

    # Draw messages border
    stdscr.addstr(messages_start_y, menu_width, messages_border)
    stdscr.addstr(messages_start_y + len(menu) + 1, menu_width, messages_end_border)

    # Display history in the messages section
    max_history_lines = len(menu)
    display_history = history[1 : max_history_lines + 1] if len(history) > 1 else []

    for i, hist_entry in enumerate(display_history):
        try:
            # Truncate long lines to prevent wrapping
            truncated_entry = hist_entry[: history_width - 4]
            stdscr.addstr(messages_start_y + i + 1, menu_width + 1, truncated_entry)
        except curses.error:
            break  # Stop if we run out of screen space

    # Move cursor to input line and get input
    stdscr.refresh()

    curses.echo()
    curses.curs_set(1)

    # Get user input on the line below the prompt
    stdscr.move(input_y, 0)
    user_input = stdscr.getstr(input_y, 0, max_x - 1).decode("utf-8").strip()

    curses.noecho()
    curses.curs_set(0)
    return user_input


def truncate_ciphertext(encrypted_message):
    """
    Truncate long ciphertexts to improve display readability.

    Args:
        encrypted_message (bytes): Encrypted message to potentially truncate

    Returns:
        str: Truncated hexadecimal representation of the ciphertext
    """
    hex_message = encrypted_message.hex()
    if len(hex_message) > 70:
        return f"{hex_message[:30]}...{hex_message[-30:]}"
    return hex_message


def main(stdscr):
    """
    Main function for interactive RSA Cryptography program.
    """
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    rsa_handler = RSAHandler()
    history = [display_ascii_art(stdscr)]  # Initialize history with ASCII art
    last_encrypted_message = None
    keys_folder = None

    menu = [
        "Generate RSA keypairs",
        "Encrypt message",
        "Decrypt message",
        "Encrypt file",
        "Decrypt file",
        "Acts as a server",
        "Acts as a client",
        "Quit",
    ]

    while True:
        selected = menu_navigation(stdscr, menu, history)

        if selected == 0:  # Generate RSA keypairs
            save_path = get_user_input(
                stdscr,
                "Input path to save keypair (default: current directory): ",
                history,
            )
            save_path = save_path if save_path else os.getcwd()
            keys_folder = os.path.join(save_path, ".keys")
            os.makedirs(keys_folder, exist_ok=True)

            public_key, private_key = rsa_handler.generate_keypair()
            rsa_handler.save_key(
                public_key, os.path.join(keys_folder, "rsa_pkcs1_oaep.pub")
            )
            rsa_handler.save_key(
                private_key, os.path.join(keys_folder, "rsa_pkcs1_oaep")
            )
            message = f"Keys saved in {keys_folder}."
            history.append(message)

        elif selected in range(1, 7):  # Encryption/Decryption options
            if selected == 6:  # Acts as a client
                act_as_client(stdscr, rsa_handler, history)
                continue

            if keys_folder is None:
                message = get_user_input(
                    stdscr,
                    "Input path folder .keys atau ketik (R)etry jika Anda belum men-generate keypair: ",
                    history,
                )
                if message.lower() == "r" or message.lower() == "retry":
                    continue

                if not os.path.exists(message):
                    history.append("Error: Folder does not exist.")
                    continue

                keys_folder = message
                selected = selected

            elif selected == 1:  # Encrypt message
                message = get_user_input(stdscr, "Enter message to encrypt: ", history)
                public_key = rsa_handler.load_key(
                    os.path.join(keys_folder, "rsa_pkcs1_oaep.pub")
                )
                encrypted_message = rsa_handler.encrypt(public_key, message)
                last_encrypted_message = encrypted_message
                untrunked_message = f"Encrypted message: {encrypted_message}"
                result = f"Truncated message: {truncate_ciphertext(encrypted_message)}"
                history.append(untrunked_message)
                history.append(result)

                # Ask if user wants to save the encrypted message
                save_option = get_user_input(
                    stdscr,
                    "Do you want to save the encrypted message? (y/N): ",
                    history,
                )

                if save_option.lower() == "y":
                    # Create a directory for encrypted messages if it doesn't exist
                    encrypted_dir = os.path.join(os.getcwd(), "encrypted_messages")
                    os.makedirs(encrypted_dir, exist_ok=True)

                    # Save the encrypted message to a file
                    encrypted_file_path = os.path.join(encrypted_dir, "encrypted.txt")
                    with open(encrypted_file_path, "wb") as f:
                        f.write(encrypted_message)

                    # Add to history
                    history.append(f"Encrypted message saved to {encrypted_file_path}")
                else:
                    continue

            elif selected == 2:  # Decrypt message
                try:
                    if last_encrypted_message is None:
                        history.append(
                            "Error: No encrypted message available. Encrypt a message first."
                        )
                        continue

                    private_key = rsa_handler.load_key(
                        os.path.join(keys_folder, "rsa_pkcs1_oaep")
                    )
                    decrypted_message = rsa_handler.decrypt(
                        private_key, last_encrypted_message
                    )
                    result = f"Decrypted Message: {decrypted_message}"
                    history.append(result)
                    last_encrypted_message = None

                except ValueError as e:
                    history.append(f"Incorrect Private key unable to decrypt: {str(e)}")
                    continue

            elif selected == 3:  # Encrypt file
                filename = get_user_input(
                    stdscr, "Enter file name to encrypt: ", history
                )
                public_key = rsa_handler.load_key(
                    os.path.join(keys_folder, "rsa_pkcs1_oaep.pub")
                )
                with open(filename, "r") as f:
                    message = f.read()
                encrypted_message = rsa_handler.encrypt(public_key, message)
                with open(filename + ".enc", "wb") as f:
                    f.write(encrypted_message)
                result = f"File encrypted as {filename}.enc"
                history.append(result)

            elif selected == 4:  # Decrypt file
                filename = get_user_input(
                    stdscr, "Enter file name to decrypt: ", history
                )
                private_key = rsa_handler.load_key(
                    os.path.join(keys_folder, "rsa_pkcs1_oaep")
                )
                with open(filename, "rb") as f:
                    encrypted_message = f.read()
                decrypted_message = rsa_handler.decrypt(private_key, encrypted_message)
                with open(filename + ".dec", "w") as f:
                    f.write(decrypted_message)
                result = f"File decrypted as {filename}.dec"
                history.append(result)

            elif selected == 5:  # Acts as a server
                act_as_server(stdscr, rsa_handler, keys_folder, history)

        if selected is None:  # Quit condition
            break


if __name__ == "__main__":
    curses.wrapper(main)
