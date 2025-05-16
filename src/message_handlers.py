import os
from ui import get_user_input

# truncate long ciphertexts for display
def truncate_ciphertext(encrypted_message):
    hex_message = encrypted_message.hex() # convert bytes to hex string
    if len(hex_message) > 70: # if hex string is too long
        # show beginning and end
        return f"{hex_message[:30]}...{hex_message[-30:]}"
    return hex_message

# handle message encryption
def _handle_encrypt_message(stdscr, rsa_handler, history, keys_folder, last_encrypted_message, menu_items_for_layout):
    message_prompt = "enter message to encrypt: "
    message_to_encrypt = get_user_input(stdscr, message_prompt, history, menu_items_for_layout)
    
    if not message_to_encrypt: # check for empty input
        history.append("no message entered for encryption.")
        return last_encrypted_message # return previous state

    try:
        public_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep.pub"))
        encrypted_message = rsa_handler.encrypt(public_key, message_to_encrypt)
        
        history.append(f"encrypted (hex): {encrypted_message.hex()}") # show full hex
        history.append(f"truncated: {truncate_ciphertext(encrypted_message)}") # show truncated
        
        save_option = get_user_input(stdscr, "save encrypted message? (y/n): ", history, menu_items_for_layout)
        if save_option.lower() == 'y':
            encrypted_dir = os.path.join(os.getcwd(), "encrypted_messages") # dedicated dir
            os.makedirs(encrypted_dir, exist_ok=True)
            # generic filename for saved message
            encrypted_file_path = os.path.join(encrypted_dir, "encrypted_message.txt") 
            with open(encrypted_file_path, "wb") as f:
                f.write(encrypted_message)
            history.append(f"encrypted message saved to {encrypted_file_path}")
        return encrypted_message # return new encrypted message for potential immediate decryption
    except FileNotFoundError:
        history.append(f"err: public key not found in {keys_folder}.")
    except Exception as e:
        history.append(f"err encrypting message: {str(e)}")
    return last_encrypted_message # return old state if err

# handle message decryption
def _handle_decrypt_message(stdscr, rsa_handler, history, keys_folder, last_encrypted_message, menu_items_for_layout):
    if last_encrypted_message is None:
        history.append("err: no encrypted message available. encrypt a message first.")
        return None # no message to decrypt, effectively clearing/keeping it None

    try:
        private_key = rsa_handler.load_key(os.path.join(keys_folder, "rsa_pkcs1_oaep"))
        decrypted_message = rsa_handler.decrypt(private_key, last_encrypted_message)
        history.append(f"decrypted message: {decrypted_message}")
        return None # clear last_encrypted_message in main loop after successful decryption
    except FileNotFoundError:
        history.append(f"err: private key not found in {keys_folder}.")
    except ValueError: # often indicates wrong key or corrupted data for decryption
        history.append("err: incorrect private key or data, unable to decrypt.")
    except Exception as e:
        history.append(f"err decrypting message: {str(e)}")
    return last_encrypted_message # return original message if decryption failed, allowing retry
