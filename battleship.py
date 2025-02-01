import sys
import threading 
import re
import socket
from ship_hover_animation import Run_hover_animation
from board import Ship, Board
from server_code import server_func
from client_code import client_func

buffer_lock = threading.Lock()


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
                                        |_|\n\n\
\n\u001b[1A")
    sys.stdout.flush()

    instruction = ""
    while instruction != "c" or instruction != "j":
        instruction = input("create game (c) or join game (j): ")
        sys.stdout.write("\u001b[1A\u001b[2K")
        sys.stdout.flush()

        if instruction == "c":
            # create new game
            server_func()
        elif instruction == "j":
            # join game
            break


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
    user_board = Board()

    # generating state for enemy board. NOTE enemy position unknown to user and vice versa
    enemy_board = Board()

    # how many lines or characters away is the origin of some table from first line of text below tables
    ships = [Ship(0, 0, "Carrier", 5, "horizontal"), 
            Ship(0, 0, "Battleship", 4, "horizontal"),
            Ship(0, 0, "Destroyer", 3, "horizontal"),
            Ship(0, 0, "Submarine", 3, "horizontal"),
            Ship(0, 0, "Patrol Boat", 2, "horizontal")]

    # instructions for how to place stuff
    sys.stdout.write("\u001b[2K'v' for vertical orientation or 'h', for horizontal orientation.\n"
    "Enter with no input to confirm placement.\n"
    "'A1', 'h10', etc to hover elsewhere.\n")

    # how high from cursor the table origin is 
    table_origin_row_offset = 14

    # creating extra spacing on bottom to help with presentation
    # moving cursor clearing previous prompt and user inpout with white space
    sys.stdout.write(f"\n\n\u001b[2A")
    sys.stdout.flush()


    # prompting users to place ships
    for ship in ships:
        hover_col = 0
        hover_row = 0

        while True:
            # prompt user. we must move cursor to beginning despite newline in previous write otherwise format is off.
            buffer_lock.acquire()
            sys.stdout.write(f"\u001b[2K\u001b[0GPlace \u001b[34m{ship.ship_name}\u001b[0m of length \u001b[34m{ship.length}\u001b[0m: \u001b[s")
            sys.stdout.flush()
            buffer_lock.release()

            hover_animation = Run_hover_animation(ship, user_board, buffer_lock)
            # daemon to escape so we can easily escape code execution 
            hover_animation.daemon = True
            hover_animation.start()

            # one might expect input to create some problems as it creates a newline, and if the cursor is 
            # not moved to the previous row before a switch to the animation thread the animation might be thrown off
            # because it relies on precise cursor positioning to work. However, using the default python function 
            # actually seems to "solve" this issue after some manual testing. I'm not sure if this eliminates the
            # issue or just makes it unlikely. In any case, using system writes and flushes cause this to happen more easily.    
            instruction = input()
            instruction = instruction.replace("\r", "")

            # moving cursor clearing previous prompt and user input with white space
            buffer_lock.acquire()
            sys.stdout.write(f"\u001b[1A\u001b[2K")
            sys.stdout.flush()
            buffer_lock.release()

            # checking user input. we end animation after each conditional as it relies on info processed here
            if (re.search("^[a-jA-J]([1-9]|10)$", instruction) ):  
                # why minus by one? we multiply by column and row offsets to get distance from table origin.
                row_num = int(instruction[1:]) - 1
                if (ord(instruction[0]) in range(65, 75)):
                    col_num = ord(instruction[0]) - 65
                else:
                    col_num = ord(instruction[0]) - 97

                
                ship.row = row_num 
                ship.col = col_num  

                # stopping blinking animation
                hover_animation.end_animation()

            # confirms that an item is put in place
            elif (instruction == ""):
                if (user_board.can_place_ship(ship)):
                    user_board.add_ship(ship)
                    hover_animation.end_animation()
                    break
                hover_animation.end_animation()

                # consider making it so that hover animation continues and doesn't create another thread
            elif (instruction == "v"):
                ship.orientation = "vertical"
                hover_animation.end_animation()

            elif (instruction == "h"):
                ship.orientation = "horizontal"
                hover_animation.end_animation()
            elif (instruction == "x"):
                sys.exit()
            # stopping blinking animation
            hover_animation.end_animation()

    # making sure that end animation does not mess stuff up due to threading and cursor positioning
    hover_animation.join()

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
            # get indexes from input. why minus by one? we multiply by column and row offsets 
            # to get distance from table origin
            row_num = int(instruction[1:]) - 1
            if (ord(instruction[0]) in range(65, 75)):
                col_num = ord(instruction[0]) - 65
            else:
                col_num = ord(instruction[0]) - 97
            
            enemy_board.drop_bomb[row_num, col_num]
            
            # refreshing entire row of both boards. because formatting may be unpredictable otherwise must 
            # use both info from both boards. moving cursor to the right place 
            buffer_lock.acquire()
            sys.stdout.write(f"\u001b[{table_origin_row_offset - row_num}A\u001b[2K")

            # generating actual user row. all these row accesses might be inefficient, but I can't
            #  be arsed at this point
            sys.stdout.write(f"\u001b[1m{row_num + 1}\u001b[0m" + ("  " if row_num < 9 else " "))
            for i in range(0, 10):
                sys.stdout.write(f" {user_board[row_num][i]} ")
            sys.stdout.write(f"   ")
            # enemy row
            sys.stdout.write(f"\u001b[1m{row_num + 1}\u001b[0m" + ("  " if row_num < 9 else " "))
            for i in range(0, 10):
                sys.stdout.write(f" {enemy_board[row_num][i]} ")

            # moving cursor back to prompt area
            sys.stdout.write(f"\u001b[{table_origin_row_offset - row_num}B\u001b[0G")
            sys.stdout.flush()
            buffer_lock.release()

        elif (instruction == "\n"):
            # must check if can be added in place
            if (ship):
                continue
            elif (False):
                user_board.add_ship(ship)
                break

        elif (instruction == "x"):
            break 
        # get user input for board
            
    # exiting
    sys.stdout.write("EXITING!\n\n")
    sys.stdout.flush()
    sys.exit(0)

