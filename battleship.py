import time
import sys
import keyboard
import threading
from rich.table import Table
from rich.console import Console 
from rich.columns import Columns
from rich.style import Style
from rich.text import Text
from rich import box, print


# printing out some instructions before user is done
sys.stdout.write("press x and enter to leave (Yes, it would be nicer if you didn't\n\
have to press enter, but that would requires some black magic)\n\n")
sys.stdout.flush()

exit_flag = False

def keyboard_listener():
    while True:
        event = keyboard.read_event()
        if (event.event_type == keyboard.KEY_DOWN and event.name == "x"):
            sys.stdout.write("\nx pressed")
            sys.stdout.flush()
            exit_flag = True
            sys.exit(0)


# naturally must be nonblocking
# def run_animation():
#     animation = "|/-\\"
#     start_time = time.time()
#     while True:
#         for i in range(4):
#             time.sleep(0.1)
#             sys.stdout.write("\r" + animation[i % len(animation)])
#             sys.stdout.flush()
#             if (exit_flag == True):
#                 sys.exit(0)


# main function
if __name__ == "__main__":
    # printing title of game 
    sys.stdout.write("\
______       _   _   _           _     _\n\
| ___ \     | | | | | |         | |   (_)\n\
| |_/ / __ _| |_| |_| | ___  ___| |__  _ _ __  \n\
| ___ \/ _` | __| __| |/ _ \/ __| '_ \| | '_ \ \n\
| |_/ / (_| | |_| |_| |  __/\__ \ | | | | |_) |\n\
\____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/\n\
                                        | |\n\
                                        |_|\n\n")

    # start animation thread
    # run_animation_thread = threading.Thread(target=run_animation)
    # run_animation_thread.daemon = True
    # run_animation_thread.start()
    
    # start keyboard listener thread
    keyboard_listener_thread = threading.Thread(target=keyboard_listener)
    keyboard_listener_thread.start()

    # Prompt the user without a newline
    sys.stdout.write("Enter your username: ")
    sys.stdout.flush()

    # Read user input and remove the newline character
    username = sys.stdin.readline().replace("\n", "").replace("\r", "")  # Remove both newlines

    # Overwrite the line with a greeting
    sys.stdout.write("\rHello, " + username + "! Welcome!\n\n")
    sys.stdout.flush()


    # creating user and battle field
    user_table = Table(title="Your ships", expand=True, width=41, box=box.SIMPLE_HEAD)
    for i in range(0, 10):
        user_table.add_column(ratio=1, header=chr(65 + i), no_wrap=True, justify="center")
    for i in range(0, 11):
        user_table.add_row("-","-","-","-","-","-","-","-","-","-")
    
    # creating enemy battle field
    enemy_table = Table(title="Enemy ships", expand=True, width=41, box=box.SIMPLE_HEAD)
    # SIMPLE_HEAD
    for i in range(0, 10):
        # 65 is when unicode for capital english alphbet starts
        enemy_table.add_column(ratio=1, header=chr(65 + i), no_wrap=True, justify="center")
    for i in range(0, 11):
        enemy_table.add_row("-",Text("-", style="blink red"),"-","-","-","-","-","-","-","-")

    final_table = Columns([user_table, enemy_table], padding=(0,10,0,10))
    print(final_table)


    # wait for keyboard_listener_thread to finish (when x for exit is pressed)
    keyboard_listener_thread.join()

    sys.stdout.write("\nExiting!")
    sys.stdout.flush()
    sys.exit(0)

