import time
import sys
import keyboard
import threading
from rich.table import Table
from rich.console import Console, Group 
from rich.columns import Columns
from rich.live import Live
from rich.prompt import Prompt
from rich.panel import Panel
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



def generate_user_table() -> Table:
    # creating user and battle field
    user_table = Table(title="YOUR SHIPS", title_style="bold", expand=True, width=46, box=None)
    # adding empyy column head
    user_table.add_column(no_wrap=True, justify="center")
    for i in range(0, 10):
        # 65 is when unicode for capital english alphbet starts
        user_table.add_column(ratio=1, header=chr(65 + i), no_wrap=True, justify="center")
    for i in range(0, 11):
        user_table.add_row(f"{i + 1}", "-","-","-","-","-","-","-","-","-","-")

    enemy_table = Table(title="ENEMY SHIPS", title_style="bold", expand=True, width=46, box=None)
    # adding empyy column head
    enemy_table.add_column(no_wrap=True, justify="center")
    for i in range(0, 10):
        # 65 is when unicode for capital english alphbet starts
        enemy_table.add_column(ratio=1, header=chr(65 + i), no_wrap=True, justify="center")
    for i in range(0, 11):
        enemy_table.add_row(f"{i + 1}", "-","-","-","-","-","-","-","-","-","-")

def update_display() -> Table:
    # creating user and battle field
    user_table = Table(title="YOUR SHIPS", title_style="bold", expand=True, width=46, box=None)
    # adding empyy column head
    user_table.add_column(no_wrap=True, justify="center")
    for i in range(0, 10):
        # 65 is when unicode for capital english alphbet starts
        user_table.add_column(ratio=1, header=chr(65 + i), no_wrap=True, justify="center")
    for i in range(0, 11):
        user_table.add_row(f"{i + 1}", "-","-","-","-","-","-","-","-","-","-")

    enemy_table = Table(title="ENEMY SHIPS", title_style="bold", expand=True, width=46, box=None)
    # adding empyy column head
    enemy_table.add_column(no_wrap=True, justify="center")
    for i in range(0, 10):
        # 65 is when unicode for capital english alphbet starts
        enemy_table.add_column(ratio=1, header=chr(65 + i), no_wrap=True, justify="center")
    for i in range(0, 11):
        enemy_table.add_row(f"{i + 1}", "0","0","0","0","0","0","0","0","0","0")

    new_final_table = Columns([user_table, enemy_table],padding=(0,5,0,5))
    return new_final_table


# main function
if __name__ == "__main__":

    # Prompt the user without a newline
    sys.stdout.write("Enter your username: ")
    sys.stdout.flush()

    # Read user input and remove the newline character
    username = sys.stdin.readline().replace("\n", "").replace("\r", "")  # Remove both newlines

    # Overwrite the line with a greeting
    sys.stdout.write("\rHello, " + username + "! Welcome!\n\n")
    sys.stdout.flush()

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
    sys.stdout.flush()

    # # creating user and battle field
    # user_table = Table(title="YOUR SHIPS", title_style="bold", expand=True, width=45, box=None)
    # # adding empyy column head
    # user_table.add_column(no_wrap=True, justify="center")
    # for i in range(0, 10):
    #     # 65 is when unicode for capital english alphbet starts
    #     user_table.add_column(ratio=1, header=chr(65 + i), no_wrap=True, justify="center")
    # for i in range(0, 10):
    #     user_table.add_row(f"{i + 1}", "-","-","-","-","-","-","-","-","-","-")

    # enemy_table = Table(title="ENEMY SHIPS", title_style="bold", expand=True, width=45, box=None)
    # # adding empyy column head
    # enemy_table.add_column(no_wrap=True, justify="center")
    # for i in range(0, 10):
    #     # 65 is when unicode for capital english alphbet starts
    #     enemy_table.add_column(ratio=1, header=chr(65 + i), no_wrap=True, justify="center")
    # for i in range(0, 10):
    #     enemy_table.add_row(f"{i + 1}", "-","-","-","-","-","-","-","-","-","-")

    # final_table = Columns([user_table, enemy_table], padding=(0,5,0,5))

    # panel_group = Group(
    #     final_table,
    #     Panel("Hello\nHello\nHello",  title="text panel", width=93, padding=(1,1,1,1)),
    # )


    # # keyboard_listener()
    # console = Console()
    # user_input_buffer = "+"
    # sys.stdout.write(user_input_buffer)
    # with Live(panel_group, auto_refresh=False) as live:
    #     while True:
    #         sys.stdout.write("\x1b[20B")
    #         sys.stdout.flush()
    #         if (user_input_buffer == "bruh"):
    #             print("\nx pressed")
    #             live.update(update_display())
    #             exit_flag = True
    #             sys.exit(0)

    # wait for keyboard_listener_thread to finish (when x for exit is pressed)

    sys.stdout.write("\nExiting!")
    sys.stdout.flush()
    sys.exit(0)

