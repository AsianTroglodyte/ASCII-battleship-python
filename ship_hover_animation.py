import threading
import sys
from board import Board, Ship 


# MOST OF THE ITEMS HERE WRITE STUFF TO TERMINAL REGARDLESS. MUCH ASSUMPTIONS ARE MADE
# AS TO THE LOCATION OF THE CURSOR AT MANY POINTS. PLEASE KEEP TRACK OF THESE ASSUMPTIONS 
# AND CHANGE THEM AS NEEDED

# this creates a hover effect where the ship blinks over the would-be area. Naturally, it is non-blocking, and thus a thread.
# Why subclassing? when we are getting user input while running an animation, we run a loop that loops on each user "enter".
# the end_animation() method via subclassing allows us to create several threads at a time 
# and terminate them individually without waiting for them to complete
# locks for flushes because several threads manipulate the console cursor, which *might* lead to unexpected behavior
class Run_hover_animation(threading.Thread):
    # we first generate the row or rows of text of associated with animation frame and then cycle through them by callin run(). 
    def __init__(self, ship: Ship, board : Board, buffer_lock : threading):
        super().__init__()

        # of course set basic attributes
        self.row = ship.row
        self.col = ship.col
        self.ship_name = ship.ship_name
        self.length = ship.length
        self.orientation = ship.orientation

        self.board = board

        self.buffer_lock = buffer_lock

        # generating regular row frame
        normal_row_frame = "" 
        # user row
        if (self.orientation == "horizontal"):
            normal_row_frame += f"\u001b[1m{self.row + 1}\u001b[0m" + ("  " if self.row < 9 else " ")
                
            for i in range(0, 10):
                normal_row_frame += f" {self.board[self.row][i]} "
        elif (self.orientation == "vertical"):
            # use min to make sure that row 
            for row in range(self.row, self.row + self.length):
                # making sure access does not go out of bounds
                if 9 < row:
                    break

                normal_row_frame += f"\u001b[1m{row + 1}\u001b[0m" + ("  " if row < 9 else " ")
                for col in range(0, 10):
                    normal_row_frame += f" {self.board[row][col]} "
                normal_row_frame += f"\n"


        # generating row frame with hover effect
        blink_row_frame = ""
        # user row
        if (self.orientation == "horizontal"):
            # row num
            blink_row_frame += f"\u001b[1m{self.row + 1}\u001b[0m" + ("  " if self.row < 9 else " ")

            for i in range(0, 10):
                # injecting ship into section of row 
                if (i in range(self.col, self.col + self.length)):
                    # inserting first letter of ship name
                    blink_row_frame += f" \u001b[1m{self.ship_name[0]}\u001b[0m "
                # rest existing ships and blank spaces 
                else:
                    blink_row_frame += f" {self.board[self.row][i]} "
        elif (self.orientation == "vertical"):
            for row in range(self.row, self.row + self.length):
                # making sure access does not go out of bounds
                if 9 < row:
                    break
                blink_row_frame += f"\u001b[1m{row + 1}\u001b[0m" + ("  " if row < 9 else " ")
                for col in range(0, 10):
                    # injecting ship into section of row 
                    if (col == self.col):
                        # inserting first letter of ship name
                        blink_row_frame += f" \u001b[1m{self.ship_name[0]}\u001b[0m "
                    # rest existing ships and blank spaces 
                    else:
                        blink_row_frame += f" {self.board[row][col]} "
                blink_row_frame += f"\n"


        # list used to cycle through for animation
        self.frames = [normal_row_frame, blink_row_frame]

        # running subclasses method as a thread. This allows for threads to terminate self nicely
        self.stop_anim_event = threading.Event()
        self.thread = threading.Thread(target=self.run)
        self.sleep_timer = threading.Event()

    # note that run is specifically for overloading in thread subclasses: https://docs.python.org/3/library/threading.html
    def run(self):
        # write first before animation loop starts to make hover startup fast
        self.buffer_lock.acquire()

        # saving and moving cursor. writing frame of blink row. done first to make startup fast
        sys.stdout.write(f"\033[s\r\033[{14 - self.row}A" + self.frames[1] + "\033[u")
        sys.stdout.flush()
        self.buffer_lock.release()
        # cycling through the animation frames

        # variable for determining which frame to put
        cur_frame = 0

        # range and the modulo determines time between each frame. how it works with different vals can be subtle.
        while True:
            for i in range(1, 11):
                # any sleep time below 0.1 causes shenanigans bcuz of python. its weird
                self.sleep_timer.wait(timeout = 0.1)

                if (not self.stop_anim_event.is_set() and (i % 5 == 0)):
                    self.buffer_lock.acquire()
                    # saving and moving cursor
                    sys.stdout.write(f"\033[s\r\033[{14 - self.row}A" + self.frames[cur_frame]+ "\033[u")
                    sys.stdout.flush()
                    self.buffer_lock.release()

                    # determining next frame
                    cur_frame = (cur_frame + 1) % 2
                elif (self.stop_anim_event.is_set()):
                    # uses board to keep view up-to-date. board is updated if a ship is placed.
                    # the below uses board to determine the final frame the animation ends on. 
                    # Thus making sure that the view is kept up to date with the model (board) 
                    final_frame = "" 
                    if self.orientation == "horizontal":
                        # board final stuff
                        final_frame += f"\u001b[1m{self.row + 1}\u001b[0m  "
                        for i in range(0, 10):
                            final_frame += f" {self.board[self.row][i]} "
                    elif self.orientation == "vertical":
                        for row in range(self.row, self.row + self.length):
                        # making sure access is 
                            if 9 < row:
                                break
                            final_frame += f"\u001b[1m{row + 1}\u001b[0m" + ("  " if row < 9 else " ")
                            for col in range(0, 10):
                                # injecting ship into section of row 
                                final_frame += f" {self.board[row][col]} "
                            final_frame += f"\n"

                    # making sure it ends on correct frame
                    self.buffer_lock.acquire()
                    sys.stdout.write(f"\033[s\r\033[{14 - self.row}A" + final_frame + "\033[u")
                    sys.stdout.flush()
                    self.buffer_lock.release()
                    sys.exit()

    def end_animation(self):
        self.stop_anim_event.set()
        self.sleep_timer.set()
