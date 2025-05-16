import os
from ui import get_user_input

# handle file encryption
def _handle_encrypt_file(stdscr, rsa_handler, history, keys_folder, menu_items_for_layout):
    file_prompt = "enter file name to encrypt: "
    filename = get_user_input(stdscr, file_prompt, history, menu_items_for_layout)

    if not filename: # check for empty input
        history.append("no filename entered for encryption.")
        return
        
    if not os.path.exists(filename) or not os.path.isfile(filename):
        history.append(f"err: file '{filename}' not found.")
        return

    try:
        public_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep.pub"))
        # read file content (ensure utf-8 for text files)
        with open(filename, "r", encoding="utf-8") as f: 
            message = f.read()
        encrypted_message = rsa_handler.encrypt(public_key, message)
        
        output_filename = filename + ".enc" # append .enc extension
        with open(output_filename, "wb") as f: # write in binary mode
            f.write(encrypted_message)
        history.append(f"file encrypted as {output_filename}")
    except FileNotFoundError: # key not found
        history.append(f"err: public key not found in {keys_folder}.")
    except UnicodeDecodeError: # file might not be utf-8 text
        history.append(f"err: could not read '{filename}' as text. ensure it's utf-8 encoded.")
    except Exception as e:
        history.append(f"err encrypting file: {str(e)}")

# handle file decryption
def _handle_decrypt_file(stdscr, rsa_handler, history, keys_folder, menu_items_for_layout):
    file_prompt = "enter file name to decrypt (e.g., file.txt.enc): "
    filename = get_user_input(stdscr, file_prompt, history, menu_items_for_layout)

    if not filename: # check for empty input
        history.append("no filename entered for decryption.")
        return

    if not os.path.exists(filename) or not os.path.isfile(filename):
        history.append(f"err: file '{filename}' not found.")
        return

    try:
        private_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep"))
        with open(filename, "rb") as f: # read encrypted file in binary
            encrypted_message = f.read()
        decrypted_message = rsa_handler.decrypt(private_key, encrypted_message)
        
        output_filename = filename 
        if filename.endswith(".enc"): # if it has .enc, remove it
            output_filename = filename[:-4] 
        output_filename += ".dec" # always add .dec suffix to decrypted file

        with open(output_filename, "w", encoding="utf-8") as f: # write decrypted text
            f.write(decrypted_message)
        history.append(f"file decrypted as {output_filename}")
    except FileNotFoundError: # key not found
        history.append(f"err: private key not found in {keys_folder}.")
    except ValueError: # decryption err (wrong key, corrupted data)
        history.append("err: incorrect private key or data, unable to decrypt file.")
    except Exception as e:
        history.append(f"err decrypting file: {str(e)}")
