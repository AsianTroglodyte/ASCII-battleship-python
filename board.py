import sys

class Ship():
    def __init__(self, row: int, col: int, ship_name: str, length: int, orientation: str):
        self.row = row
        self.col = col
        self.ship_name = ship_name
        self.length = length
        self.orientation = orientation

class Board():
    # this allows for access like this: board[i][j]. while only storing strings. 
    # notice how the __getitem__() method accesses items in string
    class Row(str):
        def __init__(self, row_num: int):
            self.row_string = ("\u001b[1m" + str(row_num + 1) + "\u001b[0m") + ("  " if row_num < 9 else " ") + " - " * 10

        def __getitem__(self, key: int):
            # 12 + probably because of ANSI escape codes
            return self.row_string[12 + (key * 3)]

        def __str__(self):
            return self.row_string

        def __setitem__(self, key, value):
            # recall that strings are immutable and cannot be changed
            new_row = self.row_string[ :(12 + (key * 3))] + value + self.row_string[(12 + (key * 3)) + 1: ]
            self.row_string = new_row


    def __init__(self):
        self.board_headers = "    "
        for j in range(0, 10):
            # 65 when unicode for capital eng alphabet starts.abs
            # concatenating with beginning of ANSI esc code for bold strings (kinda hacky) 
            self.board_headers += "  \u001b[1m" + chr(65 + j) + "\u001b[0m"

        # generating state for user board. NOTE user position unknown to enemy and vice versa
        self.board = [self.Row(i) for i in range(0,10)]

        self.board_string = ""
        for row in self.board:
            # str() makes sure that __str__ is used. could use __add__ but I'm lazy
            self.board_string += str(row) + "\n"

        # boats
        self.ships_list = []
    
    def add_ship(self, ship):
        
        if (not self.can_place_ship(ship)):
            return

        self.ships_list.append(ship)
        
        if (ship.orientation == "horizontal"):
            for i in range(0, ship.length):
                self.board[ship.row][ship.col + i] = ship.ship_name[0]
        
        elif (ship.orientation == "vertical"):
            for i in range(0, ship.length):
                self.board[ship.row + i][ship.col] = ship.ship_name[0]
    
    def can_place_ship(self, ship : Ship):
        # we pass in ship class objects. and then do all the processing here: 
        # - check if valid placement.
        #   - ship out of bound
        if (ship.orientation  == "horizontal"):
            if (10 < (ship.col + ship.length)):
                return False
        elif (ship.orientation == "vertical"):
            if (10 < (ship.row + ship.length)):
                return False
        #   - collision with other ships
        if (ship.orientation  == "horizontal"):
            for i in range(0, ship.length):
                if (self.board[ship.row][ship.col + i] != "-"):
                    return False
        elif (ship.orientation == "vertical"):
            for i in range(0, ship.length):
                if (self.board[ship.row + i][ship.col] != "-"):
                    return False
        return True
    
    def drop_bomb(self, row : int, col : int):
        # refreshing entire row of both boards. because formatting may be unpredictable otherwise must use both info from both boards.
        # moving cursor to the right place 
        miss = True 
        if (True):
            self.board[row][col] = "O"
        else:
            self.board[row][col] = "X"
        

    def change_ship_pos(self, new_pos):
        print("ship positions changed")

    def __str__(self):
        # update overall string. for some reason first row has extra whitespace at beginning 
        # can't figure out how to do this thing. 
        self.board_string = ""
        for row in self.board:
            self.board_string += str(row) + "\n"
        return self.board_string

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        self.board[key] = value