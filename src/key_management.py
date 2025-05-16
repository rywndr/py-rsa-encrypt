import os
from ui import get_user_input

# ensure keys folder is set, prompt if not
def _ensure_keys_folder(stdscr, history, current_keys_folder, menu_items_for_layout):
    # if folder exists and is valid, return it
    if current_keys_folder and os.path.exists(current_keys_folder) and os.path.isdir(current_keys_folder):
        return current_keys_folder
    
    prompt_message = "input path to .keys folder or (R)etry to generate keys: "
    user_path = get_user_input(stdscr, prompt_message, history, menu_items_for_layout)

    if user_path.lower() in ["r", "retry"]:
        history.append("retry: please generate keys first or provide a valid path.")
        return None # indicate retry or need for key generation

    if not os.path.exists(user_path) or not os.path.isdir(user_path):
        history.append(f"err: folder '{user_path}' not found or not a directory.")
        return None # path invalid
            
    history.append(f"using keys folder: {user_path}")
    return user_path

# handle rsa keypair generation
def _handle_generate_keys(stdscr, rsa_handler, history, menu_items_for_layout):
    save_path_prompt = "input path to save keypair (default: current directory): "
    save_path = get_user_input(stdscr, save_path_prompt, history, menu_items_for_layout)
    save_path = save_path if save_path else os.getcwd() # default to current working dir

    keys_folder = os.path.join(save_path, ".keys") # standard subfolder for keys
    try:
        os.makedirs(keys_folder, exist_ok=True) # create if not exists
        
        public_key, private_key = rsa_handler.generate_keypair()
        # save keys to standard filenames
        rsa_handler.save_key(public_key, os.path.join(keys_folder, "rsa_pkcs1_oaep.pub"))
        rsa_handler.save_key(private_key, os.path.join(keys_folder, "rsa_pkcs1_oaep"))
        
        history.append(f"keys saved in {keys_folder}.")
        return keys_folder # return new path for main loop to update
    except Exception as e:
        history.append(f"err generating keys: {str(e)}")
        return None # indicate failure
