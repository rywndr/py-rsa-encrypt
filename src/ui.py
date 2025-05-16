import curses

# display ascii art
def display_ascii_art(stdscr):
    art = r"""
  ___ ___   ____     _____
 /   |   \ /  _ \   /     \
/    ~    \>  _ </\/  \ /  \
\    Y    /  <_\ \/    Y    \
 \___|_  /\_____\ \____|__  /
       \/        \/       \/
__________  _________   _____    ___________ _______  ________________________.___._____________________
\______   \/   _____/  /  _  \   \_   _____/ \      \ \_   ___ \______   \__  |   |\\______   \__    ___/
 |       _/\_____  \  /  /_\  \   |    __)_  /   |   \/    \  \/|       _//   |   | |     ___/ |    |   
 |    |   \/        \/    |    \  |        \/    |    \     \___|    |   \\____   | |    |     |    |   
 |____|_  /_______  /\____|__  / /_______  /\____|__  /\______  /____|_  // ______| |____|     |____|   
        \/        \/         \/          \/         \/        \/       \/ \/
"""
    return art

# manage history list size
def manage_history(history, max_entries=8):
    # keep first entry (art) and most recent entries
    if len(history) > max_entries:
        # keep art and tail of history
        return [history[0]] + history[-max_entries:]
    return history

# navigate menu and display history
def menu_navigation(stdscr, menu, history):
    # manage history before display
    history = manage_history(history)

    current_row = 0
    max_y, max_x = stdscr.getmaxyx()

    # split screen based on history[0] (ascii art)
    ascii_art_lines = history[0].split("\n") 
    ascii_art_height = len(ascii_art_lines)

    # calc screen layout
    menu_width = max_x // 3  # menu on left third
    history_width = max_x - menu_width  # history on right two-thirds

    while True:
        stdscr.clear() # clear screen for redraw

        # display art at top, full width
        for i, line in enumerate(ascii_art_lines):
            try:
                stdscr.addstr(i, 0, line[: max_x - 1]) # prevent writing past screen edge
            except curses.error:
                pass  # ignore screen boundary errs if window resized small

        # display menu section (left side)
        menu_start_y = ascii_art_height + 1 # below art
        menu_border_top = " ╔═════Menu═════════════════════╗"
        stdscr.addstr(menu_start_y, 0, menu_border_top)

        for idx, row in enumerate(menu):
            display_string = f"║ {row}" # menu item format
            if idx == current_row: # highlight selected item
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(menu_start_y + idx + 1, 1, display_string) 
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(menu_start_y + idx + 1, 1, display_string)
        
        menu_border_bottom = " ╚══════════════════════════════╝"
        stdscr.addstr(menu_start_y + len(menu) + 1, 0, menu_border_bottom)

        # display messages section (right side)
        messages_start_y = menu_start_y # align with menu
        messages_border_top = "══════Messages══════════════════════════"
        messages_border_bottom = "═════════════════════════════════════════" # border for messages

        stdscr.addstr(messages_start_y, menu_width, messages_border_top)
        stdscr.addstr(messages_start_y + len(menu) + 1, menu_width, messages_border_bottom)

        # display history entries in messages section
        max_history_lines = len(menu) # fit history display within menu height
        # get relevant history slice (excluding art)
        display_history = history[1 : max_history_lines + 1] if len(history) > 1 else []

        for i, hist_entry in enumerate(display_history):
            try:
                truncated_entry = hist_entry[: history_width - 4] # truncate long lines
                stdscr.addstr(messages_start_y + i + 1, menu_width + 1, truncated_entry)
            except curses.error: # stop if run out of screen space
                break  

        stdscr.refresh() # update physical screen

        key = stdscr.getch() # get user input for navigation
        if key in [curses.KEY_UP, ord("k")]:
            current_row = (current_row - 1 + len(menu)) % len(menu) # navigate up, wrap
        elif key in [curses.KEY_DOWN, ord("j")]:
            current_row = (current_row + 1) % len(menu) # navigate down, wrap
        elif key in [10, ord("\n")]:  # enter key selects
            # return index unless it's the "quit" option (last item)
            return current_row if current_row != len(menu) - 1 else None 

# get user input with preserved layout
def get_user_input(stdscr, prompt, history, menu_items_for_layout): # added menu_items_for_layout
    # manage history
    history = manage_history(history)
    max_y, max_x = stdscr.getmaxyx() # get current screen dimensions

    ascii_art_lines = history[0].split("\n")
    ascii_art_height = len(ascii_art_lines)

    menu_width = max_x // 3
    history_width = max_x - menu_width

    input_prompt_y = max_y - 3 # position for prompt message
    input_y = max_y - 2        # position for user input field

    # clear previous prompt and input lines
    stdscr.addstr(input_prompt_y, 0, " " * (max_x -1)) 
    stdscr.addstr(input_y, 0, " " * (max_x-1))      

    # display new prompt
    stdscr.addstr(input_prompt_y, 0, prompt)

    # redraw ascii art (to keep consistent view during input)
    for i, line in enumerate(ascii_art_lines):
        try:
            stdscr.addstr(i, 0, line[: max_x - 1])
        except curses.error:
            pass # ignore errs if screen too small

    # redraw menu section
    menu_start_y = ascii_art_height + 1
    stdscr.addstr(menu_start_y, 0, " ╔═════Menu═════════════════════╗")
    for idx, row in enumerate(menu_items_for_layout): # use passed menu items
        stdscr.addstr(menu_start_y + idx + 1, 1, f"║ {row}")
    stdscr.addstr(menu_start_y + len(menu_items_for_layout) + 1, 0, " ╚══════════════════════════════╝")

    # redraw messages section
    messages_start_y = menu_start_y
    stdscr.addstr(messages_start_y, menu_width, "══════Messages══════════════════════════")
    stdscr.addstr(messages_start_y + len(menu_items_for_layout) + 1, menu_width, "═════════════════════════════════════════")

    max_history_lines = len(menu_items_for_layout)
    display_history = history[1 : max_history_lines + 1] if len(history) > 1 else []
    for i, hist_entry in enumerate(display_history):
        try:
            truncated_entry = hist_entry[: history_width - 4]
            stdscr.addstr(messages_start_y + i + 1, menu_width + 1, truncated_entry)
        except curses.error:
            break # stop if out of space
    
    stdscr.refresh() # update screen before getting input

    curses.echo() # enable echoing characters
    curses.curs_set(1) # show cursor

    stdscr.move(input_y, 0) # move cursor to input field
    # get string from user, limit length to screen width
    user_input = stdscr.getstr(input_y, 0, max_x - 2).decode("utf-8").strip()

    curses.noecho() # disable echoing
    curses.curs_set(0) # hide cursor
    return user_input
