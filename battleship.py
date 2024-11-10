import time
import sys
import threading 
import re
# MOST OF THE ITEMS HERE WRITE STUFF TO TERMINAL REGARDLESS. MUCH ASSUMPTIONS ARE MADE
# AS TO THE LOCATION OF THE CURSOR AT MANY POINTS. PLEASE KEEP TRACK OF THESE ASSUMPTIONS 
# AND CHANGE THEM AS NEEDED

# this creates a hover effect where the ship blinks over the would-be area. Naturally, it is non-blocking
# Why a class? because we need a wait to 
def run_hover_animation(row: int, col: int, ship: str, length: int, orientation: str):
    # we first generate the row or rows of text of associated with animation frame and then cycle through them. 

    # generating regular row frame
    normal_row_frame = "" 
    # user row
    normal_row_frame += f"\u001b[1m{row + 1}\u001b[0m  "
    for i in range(0, 10):
        normal_row_frame += f" {user_board[row][i]} "
    # space between rows
    normal_row_frame += "   "
    # enemy row
    normal_row_frame += f"\u001b[1m{row + 1}\u001b[0m  "
    for i in range(0, 10):
        normal_row_frame += f" {enemy_board[row][i]} "

    # generating row frame with hover effect
    blink_row_frame = ""
    # user row
    blink_row_frame += f"\u001b[1m{row + 1}\u001b[0m  "
    for i in range(0, 10):
        # injecting ship into section of row 
        if (i in range(col, col + length)):
            # inserting first letter of ship name
            blink_row_frame += f" {ship[0]} "
        else:
            blink_row_frame += f" {user_board[row][i]} "

    # space between rows
    blink_row_frame += "   "
    # enemy row
    blink_row_frame += f"\u001b[1m{row + 1}\u001b[0m  "
    for i in range(0, 10):
        blink_row_frame += f" {enemy_board[row][i]} "

    # list used to cycle through
    frames = [normal_row_frame, blink_row_frame]


    # cycling through the animation frames
    start_time = time.time()

    sys.stdout.write(
    # saving and moving cursor
    f"\033[s\r\033[{14 - row}A"
    # writing frame of row normally len()
    + frames[i % len(frames)]
    # restoring cursor
    + "\033[u")
    sys.stdout.flush()
    while True:
        for i in range(1, 11):
            # if we need to keep track of more vent threading. Event may be useful
            # returns True if notified False if timed out

            time.sleep(0.1)

            if (not stop_anim_event.is_set() and ((i % 5) == 0)):
                sys.stdout.write(
                # saving and moving cursor
                f"\033[s\r\033[{14 - row}A"
                # writing frame of row normally len()
                + frames[i % len(frames)]
                # restoring cursor
                + "\033[u")
                sys.stdout.flush()
            elif (stop_anim_event.is_set()):
                # making sure it ends on the normal frame
                sys.stdout.write(
                # saving and moving cursor
                f"\033[s\r\033[{14 - row}A"
                # writing frame of row
                + frames[0]
                # restoring cursor
                + "\033[u")
                sys.stdout.flush()
                sys.exit()

class Run_hover_animation(threading.Thread):
    # we first generate the row or rows of text of associated with animation frame and then cycle through them. 
    def __init__(self, row: int, col: int, ship: str, length: int, orientation: str):
        super().__init__()

        # generating regular row frame
        normal_row_frame = "" 
        # user row
        normal_row_frame += f"\u001b[1m{row + 1}\u001b[0m  "
        for i in range(0, 10):
            normal_row_frame += f" {user_board[row][i]} "
        # space between rows
        normal_row_frame += "   "
        # enemy row
        normal_row_frame += f"\u001b[1m{row + 1}\u001b[0m  "
        for i in range(0, 10):
            normal_row_frame += f" {enemy_board[row][i]} "
        self.normal_row_frame = normal_row_frame
        
        # generating row frame with hover effect
        blink_row_frame = ""
        # user row
        blink_row_frame += f"\u001b[1m{row + 1}\u001b[0m  "
        for i in range(0, 10):
            # injecting ship into section of row 
            if (i in range(col, col + length)):
                # inserting first letter of ship name
                blink_row_frame += f" {ship[0]} "
            else:
                blink_row_frame += f" {user_board[row][i]} "
        # space between rows
        blink_row_frame += "   "
        # enemy row
        blink_row_frame += f"\u001b[1m{row + 1}\u001b[0m  "
        for i in range(0, 10):
            blink_row_frame += f" {enemy_board[row][i]} "
        self.blink_row_frame = blink_row_frame 

        # list used to cycle through for animation
        self.frames = [normal_row_frame, blink_row_frame]

        # threading event
        self.stop_anim_event = threading.Event()
        
        # initializing thread
        self.thread = threading.Thread(target=self.run)

        # other attributes
        self.row = row
        self.col = col
        self.length = length
        self.ship = ship
        self.orientation = orientation

    def run(self):
        # write first before animation loop starts to make hover startup fast
        sys.stdout.write(
        # saving and moving cursor
        f"\033[s\r\033[{14 - self.row}A"
        # writing frame of blink row
        + self.frames[1]
        # restoring cursor
        + "\033[u")
        sys.stdout.flush()
        # cycling through the animation frames
        start_time = time.time()

        while True:
            for i in range(1, 11):
                # if we need to keep track of more vent threading. Event may be useful
                # returns True if notified False if timed out

                time.sleep(0.1)

                if (not self.stop_anim_event.is_set() and i % 5 == 0):
                    sys.stdout.write(
                    # saving and moving cursor
                    f"\033[s\r\033[{14 - self.row}A"
                    # writing frame of row
                    + self.frames[i % len(self.frames)]
                    # restoring cursor
                    + "\033[u")
                    sys.stdout.flush()
                elif (self.stop_anim_event.is_set()):
                    # making sure it ends on the normal frame
                    sys.stdout.write(
                    # saving and moving cursor
                    f"\033[s\r\033[{14 - self.row}A"
                    # writing frame of row
                    + self.frames[0]
                    # restoring cursor
                    + "\033[u")
                    sys.stdout.flush()
                    sys.exit()

    def end_animation(self):
        self.stop_anim_event.set()

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

    # Tables' Titles
    sys.stdout.write("\u001b[1m             Your Board")
    sys.stdout.write("                         ")
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
        # number ten naturally messes up col alignment. need to format accordingly. 
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

    # how many lines or characters away is the origin of some table from first line of text below tables
    ship_classes = {"Carrier": 5, "Battleship": 4, "Destroyer": 3, "Submarine": 3, "Patrol Boat": 2}



    # instructions for how to place stuff
    sys.stdout.write("\u001b[2K'l' or 'r' to rotate left or right respectively around pivot. will not rotate if impossilbe.\n"
    "Enter with no input to confirm placement.\n"
    "'A1', 'h10', etc to hover elsewhere.\n")

    table_origin_row_offset = 14

    # prompting users to place ships
    for ship, length in ship_classes.items():
        hover_row = 0
        hover_col = 0

        while True:
            # prompt user. we must move cursor to beginning despite newline in previous write otherwise format is off.
            sys.stdout.write((f"\u001b[2K\u001b[0GPlace \u001b[34m{ship}\u001b[0m of length \u001b[34m{length}\u001b[0m: "))
            sys.stdout.flush()

            # starting hover animation
            hover_animation = Run_hover_animation(hover_row, hover_col, ship, length, "r")
            # to properly escape code execution
            hover_animation.daemon = True
            hover_animation.start()

            # taking and trimming input
            instruction = sys.stdin.readline().replace("\n", "")
            instruction = instruction.replace("\r", "")

            # stopping animation
            hover_animation.end_animation()

            # clearing previous prompt and user inpout with white space
            sys.stdout.write(f"\u001b[1A\u001b[2K")
            sys.stdout.flush()

            # checking user input
            if (re.search("^[a-jA-J]([1-9]|10)$", instruction) ): # input is valid. adding 
                # why minus by one? we multiply by column and row offsets to get distance from table origin.
                row_num = int(instruction[1:]) - 1
                if (ord(instruction[0]) in range(65, 75)):
                    col_num = ord(instruction[0]) - 65
                else:
                    col_num = ord(instruction[0]) - 97

                hover_col = col_num 
                hover_row = row_num
            elif (instruction == ""):
                # refreshing entire row of both boards. because formatting may be unpredictable otherwise must use both info from both boards.
                # moving cursor to the right place 
                # sys.stdout.write(f"\u001b[{table_origin_row_offset - row_num}A\u001b[2K")

                # generating actual user row. all these row accesses might be inefficient, but it's simple 
                # sys.stdout.write(f"\u001b[1m{row_num + 1}\u001b[0m  ")
                # for i in range(0, 10):
                #     sys.stdout.write(f" {user_board[row_num][i]} ")
                # sys.stdout.write(f"   ")
                # # enemy row
                # sys.stdout.write(f"\u001b[1m{row_num + 1}\u001b[0m  ")
                # for i in range(0, 10):
                #     sys.stdout.write(f" {enemy_board[row_num][i]} ")
                # sys.stdout.flush()

                # moving cursor back to prompt area
                # sys.stdout.write(f"\u001b[{table_origin_row_offset - row_num}B\u001b[0G")
                # sys.stdout.flush()
                break
            elif (instruction == "x"):
                break
        
        if (instruction == "x"):
            break

    # clearing previous input
    sys.stdout.write(f"\u001b[1A\u001b[2K\u001b[1A\u001b[2K\u001b[1A\u001b[2K")
    sys.stdout.flush()

    # since prompt area is different
    table_origin_row_offset = 11

    # prompting users for where to place the bomb
    while True:
        # prompt user 
        sys.stdout.write(f"\u001b[2KShoot where? ")
        sys.stdout.flush()

        # taking and trimming input
        instruction = sys.stdin.readline().replace("\n", "")
        instruction = instruction.replace("\r", "")
        
        # clearing previous prompt and user input with white space
        sys.stdout.write(f"\u001b[1A\u001b[2K")

        sys.stdout.flush()

        # checking if user-given input is valid
        if (re.search("^[a-jA-J]([1-9]|10)$", instruction) ): # input is valid.
            # why minus by one? we multiply by column and row offsets to get distance from table origin.
            row_num = int(instruction[1:]) - 1
            if (ord(instruction[0]) in range(65, 75)):
                col_num = ord(instruction[0]) - 65
            else:
                col_num = ord(instruction[0]) - 97
            
            enemy_board[row_num][col_num] = "0"
            
            # refreshing entire row of both boards. because formatting may be unpredictable otherwise must use both info from both boards.
            # moving cursor to the right place 
            sys.stdout.write(f"\u001b[{table_origin_row_offset - row_num}A\u001b[2K")

            # generating actual user row. all these row accesses might be inefficient, but I don't care. 
            sys.stdout.write(f"\u001b[1m{row_num + 1}\u001b[0m  ")
            for i in range(0, 10):
                sys.stdout.write(f" {user_board[row_num][i]} ")
            sys.stdout.write(f"   ")
            # enemy row
            sys.stdout.write(f"\u001b[1m{row_num + 1}\u001b[0m  ")
            for i in range(0, 10):
                sys.stdout.write(f" {enemy_board[row_num][i]} ")
            sys.stdout.flush()

            sys.stdout.flush()
            # moving cursor back to prompt area
            sys.stdout.write(f"\u001b[{table_origin_row_offset - row_num}B\u001b[0G")
            sys.stdout.flush()
        elif (instruction == "\n"):
            print("\n\n accepted")
        elif (instruction == "x"):
            break 
        # get user input for board
            
    # exiting
    sys.stdout.write("EXITING!\n\n")
    sys.stdout.flush()
    sys.exit(0)

