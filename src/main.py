import curses
import os
from lib.rsa import RSAHandler
from ui import display_ascii_art, menu_navigation
from key_management import _ensure_keys_folder, _handle_generate_keys
from message_handlers import _handle_encrypt_message, _handle_decrypt_message
from file_handlers import _handle_encrypt_file, _handle_decrypt_file
from network import act_as_client, act_as_server

# main app loop
def main(stdscr):
    # init curses settings
    curses.curs_set(0) # hide cursor
    curses.start_color() # enable colors
    # define color pair 1: black text on white background (for highlighted menu)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 

    rsa_handler = RSAHandler()
    # init history with ascii art (display_ascii_art doesn't need stdscr if art is static)
    history = [display_ascii_art(None)] 
    last_encrypted_message = None # store last message encrypted in session
    keys_folder = None # track current path to .keys folder

    menu_items = [ # define menu items
        "generate rsa keypairs",
        "encrypt message",
        "decrypt message",
        "encrypt file",
        "decrypt file",
        "act as server",
        "act as client",
        "quit",
    ]
    
    while True: # main program loop
        # display menu and get user's selection
        selected_index = menu_navigation(stdscr, menu_items, history)

        if selected_index is None:  # quit condition (from menu_navigation for "quit")
            break

        # actions requiring keys folder need validation
        actions_needing_keys = [1, 2, 3, 4, 5] # indices for enc/dec msg/file, server
        
        if selected_index in actions_needing_keys:
            # if keys_folder not set or path is no longer valid, prompt user
            if not keys_folder or not os.path.exists(keys_folder):
                if keys_folder: # if path was set but now invalid
                    history.append(f"warn: keys folder '{keys_folder}' no longer valid.")
                else: # path was never set
                    history.append("keys folder not set.")
                
                # attempt to set/update keys_folder
                potential_keys_folder = _ensure_keys_folder(stdscr, history, keys_folder, menu_items)
                if potential_keys_folder:
                    keys_folder = potential_keys_folder # update with valid path
                else: # user opted to retry or path was invalid
                    history.append("action cancelled: keys folder required and not set.")
                    stdscr.refresh() # ensure message is shown
                    continue # skip to next menu iteration

        # dispatch to appropriate action handler based on selection
        if selected_index == 0: # generate keys
            new_keys_folder = _handle_generate_keys(stdscr, rsa_handler, history, menu_items)
            if new_keys_folder: # if key generation was successful
                keys_folder = new_keys_folder # update main keys_folder path
        elif selected_index == 1: # encrypt message
            if keys_folder: # ensure keys_folder is valid
                 last_encrypted_message = _handle_encrypt_message(stdscr, rsa_handler, history, keys_folder, last_encrypted_message, menu_items)
        elif selected_index == 2: # decrypt message
            if keys_folder:
                # handler returns None on successful decrypt (to clear), or old message on fail/no message
                updated_message_state = _handle_decrypt_message(stdscr, rsa_handler, history, keys_folder, last_encrypted_message, menu_items)
                if last_encrypted_message is not None and updated_message_state is None:
                    history.append("last encrypted message cleared after decryption.")
                last_encrypted_message = updated_message_state
        elif selected_index == 3: # encrypt file
            if keys_folder:
                _handle_encrypt_file(stdscr, rsa_handler, history, keys_folder, menu_items)
        elif selected_index == 4: # decrypt file
            if keys_folder:
                _handle_decrypt_file(stdscr, rsa_handler, history, keys_folder, menu_items)
        elif selected_index == 5: # act as server
            if keys_folder: # server needs keys
                act_as_server(stdscr, rsa_handler, keys_folder, history)
            # if keys_folder is None here, the check above should have prompted or skipped
        elif selected_index == 6: # act as client
            act_as_client(stdscr, rsa_handler, history, menu_items) # pass menu_items for its get_user_input calls
        else: # should not happen if menu_navigation is correct
            history.append(f"warn: unhandled menu index {selected_index}")

        stdscr.refresh() # refresh display after each action to show history updates


if __name__ == "__main__":
    curses.wrapper(main) # initialize curses and run main
