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

    # Tables' Titles
    sys.stdout.write("\u001b[1m            Your Board")
    sys.stdout.write("                          ")
    sys.stdout.write("Enemy Board\u001b[0m\n")
    sys.stdout.flush()


    # Table Column Headers
    sys.stdout.write("  ")
    for i in range(0, 2):
        for j in range(0, 10):
            # 65 when unicode for capital eng alphabet starts.abs
            # concatenating with beginning of ANSI esc code for bold strings (kinda hacky) 
            sys.stdout.write("  \u001b[1m" + chr(65 + j))
        sys.stdout.write(" " * 6)
    sys.stdout.write("\n")
    sys.stdout.flush()

    # Table Body + Table Row Headers
    for i in range(0, 10):
        if (i < 9):
            # User table
            sys.stdout.write(f"\u001b[1m{i + 1}\u001b[0m   -  -  -  -  -  -  -  -  -  -")
            sys.stdout.write(" " * 4)
            # enemy table
            sys.stdout.write(f"\u001b[1m{i + 1}\u001b[0m   -  -  -  -  -  -  -  -  -  -\n")
        else:
            # User table
            sys.stdout.write(f"\u001b[1m{i + 1}\u001b[0m  -  -  -  -  -  -  -  -  -  -")
            sys.stdout.write(" " * 4)
            # enemy table
            sys.stdout.write(f"\u001b[1m{i + 1}\u001b[0m  -  -  -  -  -  -  -  -  -  -\n")
    # moving cursor further down
    sys.stdout.write("\n")
    sys.stdout.flush()

    # generating state for user board. NOTE user position unknown to enemy and vice versa
    user_board = [["-" for i in range(0,10)] for i in range(0,10)]
    # generating state for enemy board. NOTE enemy position unknown to user and vice versa
    enemy_board = [["-" for i in range(0,10)] for i in range(0,10)]

    USER_PROMPT_ROW = 19
    USER_PROMPT_COLUMN = 20

    # origin is considered top left most item
    USER_BOARD_ORIGIN_ROW = 8
    USER_BOARD_ORIGIN_COLUMN = 5

    ENEMY_BOARD_ORIGIN_ROW = 8
    ENEMY_BOARD_ORIGIN_COLUMN = 41

    COLUMN_OFFSET = 2
    ROW_OFFSET = 1

    ships_placed = False
    ship_classes = {"Carrier": 5, "Battleship": 4, "Destroyer": 3, "Submarine": 3, "Patrol Boat": 2}

    # Prompting user input
    while True:
        if (not ships_placed):
            # taking and trimming input
            instruction = sys.stdin.readline().replace("\n", "")
            instruction = instruction.replace("\r", "")
            
            # clearing previous prompt and user input with white space
            sys.stdout.write("\r\u001b[1A\u001b[2K")
            sys.stdout.flush()
        elif (ships_placed):
            # taking and trimming input
            instruction = sys.stdin.readline().replace("\n", "")
            instruction = instruction.replace("\r", "")
            
            # clearing previous prompt and user input with white space
            sys.stdout.write("\r\u001b[1A\u001b[2K")
            sys.stdout.flush()

            # processing input
            if (instruction == "x"):
                break
            
            elif (instruction == "user"):
                sys.stdout.write(f"\u001b[{USER_BOARD_ORIGIN_ROW};{USER_BOARD_ORIGIN_COLUMN}H0")
                # moving cursor back to user prompt location
                sys.stdout.write(f"\u001b[{USER_PROMPT_ROW};{USER_PROMPT_COLUMN}H")
            elif (instruction == "enemy"):
                # moving position to 
                sys.stdout.write(f"\u001b[{ENEMY_BOARD_ORIGIN_ROW};{ENEMY_BOARD_ORIGIN_COLUMN}H0")
                # moving cursor back to user prompt location
                sys.stdout.write(f"\u001b[{USER_PROMPT_ROW};{USER_PROMPT_COLUMN}H")
            # get user input for board
            
    # exiting
    sys.stdout.write("\nExiting!")
    sys.stdout.flush()
    sys.exit(0)

