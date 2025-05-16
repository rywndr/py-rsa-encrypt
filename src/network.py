import socket
import select
import os

# act as client
def act_as_client(stdscr, rsa_handler, history, keys_folder, menu_items_for_layout):
    from ui import get_user_input # late import to avoid circular dependency
    host = get_user_input(stdscr, "enter server ip: ", history, menu_items_for_layout)
    port_str = get_user_input(stdscr, "enter server port: ", history, menu_items_for_layout)
    try:
        port = int(port_str)
    except ValueError:
        history.append("invalid port number.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        history.append(f"connected to server at {host}:{port}")

        # send public key to server
        public_key_path = os.path.join(keys_folder, "rsa_pkcs1_oaep.pub")
        with open(public_key_path, "rb") as f:
            public_key_pem = f.read()
        client_socket.sendall(public_key_pem)
        history.append("public key sent to server.")

        # receive encrypted message from server
        encrypted_message = receive_all(client_socket, 4096) # buffer size for key
        history.append("encrypted message received from server.")

        # decrypt message
        private_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep"))
        decrypted_message = rsa_handler.decrypt(private_key, encrypted_message)
        history.append(f"decrypted message: {decrypted_message}")

        client_socket.close()
    except ConnectionRefusedError:
        history.append(f"err: connection refused by server at {host}:{port}.")
    except socket.gaierror: # getaddrinfo error
        history.append(f"err: invalid host or ip address: {host}.")
    except Exception as e:
        history.append(f"client err: {str(e)}")

# act as server
def act_as_server(stdscr, rsa_handler, history, keys_folder, menu_items_for_layout):
    from ui import get_user_input # late import
    host = "0.0.0.0" # listen on all available interfaces
    port_str = get_user_input(stdscr, "enter port to listen on: ", history, menu_items_for_layout)
    try:
        port = int(port_str)
    except ValueError:
        history.append("invalid port number.")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow reuse of address
    try:
        server_socket.bind((host, port))
        server_socket.listen(1) # listen for one connection
        history.append(f"server listening on {host}:{port}. waiting for connection...")
        stdscr.refresh() # ensure message is displayed

        # use select for non-blocking accept with timeout
        readable, _, _ = select.select([server_socket], [], [], 15) # 15 sec timeout
        if not readable:
            history.append("server timeout: no connection received.")
            server_socket.close()
            return

        conn, addr = server_socket.accept()
        history.append(f"connection from {addr}")

        # receive public key from client
        client_public_key_pem = receive_all(conn, 1024) # buffer for key
        client_public_key = rsa_handler.deserialize_key(client_public_key_pem)
        history.append("public key received from client.")

        # get message to encrypt and send
        message_to_encrypt = get_user_input(stdscr, "enter message to send to client: ", history, menu_items_for_layout)
        encrypted_message = rsa_handler.encrypt(client_public_key, message_to_encrypt)
        conn.sendall(encrypted_message)
        history.append("encrypted message sent to client.")

        conn.close()
    except socket.error as e:
        history.append(f"server socket err: {str(e)}")
    except Exception as e:
        history.append(f"server err: {str(e)}")
    finally:
        server_socket.close()

# receive all data from socket
def receive_all(sock, buffer_size):
    data = b""
    while True:
        part = sock.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            # either 0 or end of data
            break
        elif not part: # explicitly check for empty bytes if connection closed prematurely
            raise ConnectionError("socket connection closed before receiving all data.")
    return data
