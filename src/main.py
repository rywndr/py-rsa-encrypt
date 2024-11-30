import curses
import os
import select
import socket

from lib.rsa import RSAHandler


def act_as_server(stdscr, rsa_handler, keys_folder, history):
    host = "0.0.0.0"
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    server_socket.setblocking(False)

    # Load server's public key to send to client
    public_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep.pub"))
    private_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep"))

    history.append(f"Server listening on {host}:{port}")

    stdscr.refresh()

    inputs = [server_socket]
    try:
        while True:
            readable, _, _ = select.select(inputs, [], [], 1)

            if server_socket in readable:
                conn, address = server_socket.accept()
                conn.setblocking(False)
                inputs.append(conn)
                history.append(f"Connection from: {address}")

                # Send public key to client
                conn.send(public_key.encode())
                stdscr.refresh()

            for s in readable:
                if s is not server_socket:
                    try:
                        data = s.recv(4096)
                        if not data:
                            inputs.remove(s)
                            s.close()
                            continue

                        # Decrypt the received message
                        decrypted_message = rsa_handler.decrypt(private_key, data)
                        history.append(f"Received and decrypted: {decrypted_message}")
                        stdscr.refresh()

                        # Optional: send back an acknowledgment
                        response = f"Server received: {decrypted_message}"
                        encrypted_response = rsa_handler.encrypt(public_key, response)
                        s.send(encrypted_response)

                    except Exception as e:
                        history.append(f"Error processing client message: {str(e)}")
                        inputs.remove(s)
                        s.close()

    except KeyboardInterrupt:
        history.append("Server shutting down")
    finally:
        server_socket.close()


def act_as_client(stdscr, rsa_handler, keys_folder, history):
    host = get_user_input(stdscr, "Enter server IP address: ", history)
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)

    # Load client's keys
    public_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep.pub"))
    private_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep"))

    try:
        client_socket.connect((host, port))
    except socket.error as e:
        if e.errno != 115:  # Not in progress
            history.append(f"Connection error: {str(e)}")
            return

    history.append(f"Connecting to {host}:{port}")
    stdscr.refresh()

    # Wait for server's public key
    server_public_key = None
    while not server_public_key:
        readable, _, _ = select.select([client_socket], [], [], 5)
        if readable:
            server_public_key = client_socket.recv(4096).decode()
            history.append("Received server's public key")
            break

    if not server_public_key:
        history.append("Failed to receive server's public key")
        client_socket.close()
        return

    # Get message to send
    message = get_user_input(stdscr, "Enter message to encrypt: ", history)

    # Encrypt and send message
    encrypted_message = rsa_handler.encrypt(server_public_key, message)
    client_socket.send(encrypted_message)

    history.append(f"Sent encrypted message: {truncate_ciphertext(encrypted_message)}")
    stdscr.refresh()

    # Wait for server response
    try:
        readable, _, _ = select.select([client_socket], [], [], 5)
        if readable:
            response = client_socket.recv(4096)
            decrypted_response = rsa_handler.decrypt(private_key, response)
            history.append(f"Server response: {decrypted_response}")
    except Exception as e:
        history.append(f"Error receiving server response: {str(e)}")

    client_socket.close()


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


def menu_navigation(stdscr, menu, history):
    """
    Display menu and allow navigation using arrow keys or vim keys.
    """
    current_row = 0
    max_y, max_x = stdscr.getmaxyx()

    # Split the screen into sections
    ascii_art_lines = history[0].split("\n")
    ascii_art_height = len(ascii_art_lines)

    # Calculate available space for history
    max_history_lines = (
        max_y - ascii_art_height - len(menu) - 4
    )  # Reserve space for menu and input

    while True:
        stdscr.clear()

        # Display ASCII art at the top
        for i, line in enumerate(ascii_art_lines):
            try:
                stdscr.addstr(i, 0, line)
            except curses.error:
                pass  # Ignore potential screen boundary errors

        # Display menu below ASCII art
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

        # Display history below menu
        history_start_y = menu_start_y + len(menu) + 2

        # Limit history to available space
        display_history = history[1 : max_history_lines + 1] if len(history) > 1 else []

        for i, hist_entry in enumerate(display_history):
            try:
                # Truncate long lines to prevent wrapping
                truncated_entry = hist_entry[: max_x - 1]
                stdscr.addstr(history_start_y + i, 0, truncated_entry)
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
    Display a prompt and get user input with proper spacing and no overlapping.
    """
    # Calculate screen dimensions
    max_y, max_x = stdscr.getmaxyx()

    # Calculate ASCII art height
    ascii_art_lines = history[0].split("\n")
    ascii_art_height = len(ascii_art_lines)

    stdscr.clear()

    # Display ASCII art at the top
    for i, line in enumerate(ascii_art_lines):
        try:
            stdscr.addstr(i, 0, line)
        except curses.error:
            pass  # Ignore potential screen boundary errors

    # Calculate available space for history
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
    max_history_lines = (
        max_y - ascii_art_height - len(menu) - 4
    )  # Reserve space for menu and input

    # Display history
    history_start_y = ascii_art_height + 1

    # Limit history to available space
    display_history = history[1 : max_history_lines + 1] if len(history) > 1 else []

    for i, hist_entry in enumerate(display_history):
        try:
            # Truncate long lines to prevent wrapping
            truncated_entry = hist_entry[: max_x - 1]
            stdscr.addstr(history_start_y + i, 0, truncated_entry)
        except curses.error:
            break  # Stop if we run out of screen space

    # Calculate input start position
    input_prompt_y = max_y - 3
    input_y = max_y - 2

    # Clear the lines we'll use for input
    stdscr.addstr(input_prompt_y, 0, " " * max_x)
    stdscr.addstr(input_y, 0, " " * max_x)

    # Display prompt for input at the bottom of the screen
    stdscr.addstr(input_prompt_y, 0, prompt)
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
                result = f"Encrypted Message: {truncate_ciphertext(encrypted_message)}"
                history.append(result)

                # Ask if user wants to save the encrypted message
                save_option = get_user_input(
                    stdscr,
                    "Do you want to save the encrypted message? (y/n): ",
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
            elif selected == 2:  # Decrypt message
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

            elif selected == 6:  # Acts as a client
                act_as_client(stdscr, rsa_handler, keys_folder, history)

        if selected is None:  # Quit condition
            break


if __name__ == "__main__":
    curses.wrapper(main)
