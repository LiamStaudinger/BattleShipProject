'''
File: battleship.py
Author: Liam Staudinger
Course: CSC 120, Spring 2024
Purpose: This program simulates a game of battleship. The program reads in two
files, one containing the placement of the ships and the other containing the 
guesses. The program will output the board after each guess and will print out 
the result of the guess. The program will also print out if a ship has been 
sunk and if all ships have been sunk. The program will also print out if a 
guess is illegal or if a placement causes an error. The program will exit if
all ships have been sunk.
'''
import sys

class GridPos:
    '''
    This class represents a postion on the game board.
    It includes methods for guessing a position, checking if a position has 
    been guessed or hit,and managing the ship at a position.

    Attributes:
        - x (int): The x-coordinate of the position.
        - y (int): The y-coordinate of the position.
        - ship (Ship): The ship at the position.
        - guessed (bool): True if the position has been guessed, False
        otherwise.
        - hit (bool): True if the position has been hit, False otherwise.
    '''
    def __init__(self, x, y, ship = None):
        '''
        Constructor for the GridPos class.

        Parameters:
            - x (int): The x-coordinate of the position.
            - y (int): The y-coordinate of the position.
            - ship (Ship): The ship at the position.
        Returns:
            - None
        '''
        self._x = x
        self._y = x
        self._ship = ship
        self._guessed = False
        self._hit = False
    def guess(self):
        '''
        Records that the position has been guessed.

        Parameters:
            - None
        Returns:
            - None
        '''
        self._guessed = True
    def guessed(self):
        '''
        Returns whether the position has been guessed.

        Parameters:
            - None
        Returns:
            - bool: True if the position has been guessed, False otherwise.
        '''
        return self._guessed
    def hit(self):
        '''
        Marks the position as hit.
    
        Parameters:
            - None
        Returns:
            - None
        '''
        self._hit = True
    def is_hit(self):
        '''
        Returns whether the position has been hit.

        Parameters:
            - None
        Returns:
            - bool: True if the position has been hit, False otherwise.
        '''
        return self._hit
    def __str__(self):
        '''
        Returns a string representation of the position.

        Parameters:
            - None
        Returns:
            - str: A string representation of the position.
        '''
        if self._ship == None:
            return '.'
        else:
            return str(self._ship)
    def ship(self):
        '''
        Returns the ship at the position.

        Parameters:
            - None
        Returns:
            - Ship: The ship at the position.
        '''
        return self._ship
    def place_ship(self, ship):
        '''
        Places a ship at the position.

        Parameters:
            - ship (Ship): The ship to place at the position.
        Returns:
            - None
        '''
        self._ship = ship
    def remove_ship(self):
        '''
        Removes the ship from the position.

        Parameters:
            - None
        Returns:
            - None
        '''
        self._ship = None
    __repr__ = __str__
    
class Board:
    '''
    This class represents the game board. It includes methods for validating
    coordinates and ship sizes, checking fleet composition, and placing ships 
    on the board. It also includes methods for processing guesses and checking
    if a guess is legal. The class also includes methods for getting and 
    setting cells on the board.

    Attributes:
        - ships (set): A set of the ships on the board.
        - ship_counts (dict): A dictionary of the counts of each ship on the 
        board.
        - board (list): A 2D list of GridPos objects representing the game 
        board.
    '''
    def __init__(self):
        '''
        Constructor for the Board class.

        Parameters:
            - None
        Returns:
            - None
        '''
        self._ships = {'A', 'B', 'S', 'D', 'P'}
        self._ship_counts = {'A': 0, 'B': 0, 'S': 0, 'D': 0, 'P': 0}
        self._board = []
        for i in range(10):
            row = []
            for j in range(10):
                row.append(GridPos(i, j))
            self._board.append(row)
    def validate_coordinates(self, x1, y1, x2, y2, string):
        '''
        Validates that the given coordinates are within bounds and either
        horizontal or vertical.

        Parameters:
            - x1 (int): The x-coordinate of the first position.
            - y1 (int): The y-coordinate of the first position.
            - x2 (int): The x-coordinate of the second position.
            - y2 (int): The y-coordinate of the second position.
            - string (str): The string representation of the ship.
        Returns:
            - None
        '''
        if x1 < 0 or x1 > 9 or y1 < 0 or y1 > 9 or \
        x2 < 0 or x2 > 9 or y2 < 0 or y2 > 9:
            print("ERROR: ship out-of-bounds: " + string)
            sys.exit(0)
        if x1 != x2 and y1 != y2:
            print("ERROR: ship not horizontal or vertical: " + string)
            sys.exit(0)
    def validate_ship_size(self, x1, y1, x2, y2, ship, string):
        '''
        Validates that the size of the ship matches the distance between the
        given coordinates.

        Parameters:
            - x1 (int): The x-coordinate of the first position.
            - y1 (int): The y-coordinate of the first position.
            - x2 (int): The x-coordinate of the second position.
            - y2 (int): The y-coordinate of the second position.
            - ship (Ship): The ship to validate.
            - string (str): The string representation of the ship.
        Returns:
            - None
        '''
        if x1 == x2 and max(y1-y2, y2-y1) + 1 != ship.size() or \
        y1 == y2 and max(x1-x2, x2-x1) + 1 != ship.size():
            print("ERROR: incorrect ship size: " + string)
            sys.exit(0)
    def check_fleet_composition(self):
        '''
        Checks that the total number of ships is correct.

        Parameters:
            - None
        Returns:
            - None
        '''
        if sum(self._ship_counts.values()) != 5:
            print("ERROR: fleet composition incorrect")
            sys.exit(0)
    def place_ship_on_board(self, x1, y1, x2, y2, ship, string):
        '''
        Places a ship on the board over the given coordinates.

        Parameters:
            - x1 (int): The x-coordinate of the first position.
            - y1 (int): The y-coordinate of the first position.
            - x2 (int): The x-coordinate of the second position.
            - y2 (int): The y-coordinate of the second position.
            - ship (Ship): The ship to place.
            - string (str): The string representation of the ship.
        Returns:
            - None
        '''
        # If the ship is vertical
        if x1 == x2:
            # Ensure y1 is the smaller coordinate
            if y1 > y2:
                y1, y2 = y2, y1
            for i in range(y1, y2 + 1):
                # If there's already a ship at the position
                if self._board[i][x1].ship() is not None:
                    print("ERROR: overlapping ship: " + string)
                    sys.exit(0)
                self._board[i][x1].place_ship(ship)
                ship.add_position(x1, i)
        # If the ship is horizontal        
        else:
            # Ensure x1 is the smaller coordinate
            if x1 > x2:
                x1, x2 = x2, x1
            for i in range(x1, x2 + 1):
                # If there's already a ship at the position
                if self._board[y1][i].ship() is not None:
                    print("ERROR: overlapping ship: " + string)
                    sys.exit(0)
                self._board[y1][i].place_ship(ship)
                ship.add_position(i, y1)
    def place_one_ship(self, string):
        '''
        Places a single ship on the board.

        Parameters:
            - string (str): A string containing the ship type and its
            coordinates.

        Returns:
            - None
        '''
        ship_info  = string.split()
        ship_type = ship_info[0]
        x1 = int(ship_info[1])
        y1 = int(ship_info[2])
        x2 = int(ship_info[3])
        y2 = int(ship_info[4])
        ship = Ship(ship_type)

        self.validate_coordinates(x1, y1, x2, y2, string)
        self.validate_ship_size(x1, y1, x2, y2, ship, string)
        self.place_ship_on_board(x1, y1, x2, y2, ship, string)
        self._ship_counts[ship.type()] += 1        
    def process_guess(self, x, y):
        '''
        Processes a guess at the given coordinates.

        Parameters:
            - x (int): The x-coordinate of the guess.
            - y (int): The y-coordinate of the guess.
        Returns:
            - None
        '''
        cell = self.get_cell(x, y)
        if cell.ship() is None:
            self.process_miss(cell)
        else:
            self.process_hit(cell)

    def process_miss(self, cell):
        '''
        Processes a miss at the given cell.

        Parameters:
            - cell (GridPos): The cell to process.
        Returns:
            - None
        '''
        # If the cell has already been guessed
        if cell.guessed():
            print('miss (again)')
        else:
            print('miss')
            # Mark the cell as guessed
            cell.guess()

    def process_hit(self, cell):
        '''
        Processes a hit at the given cell.

        Parameters: 
            - cell (GridPos): The cell to process.
        Returns:
            - None
        '''
        ship = cell.ship()
        # If the cell has already been guessed
        if cell.guessed():
            print('hit (again)')
        else:
            # Mark the cell as guessed and hit
            cell.guess()
            cell.hit()
            # If all the ship's positions have been hit
            if ship.hit():
                self.process_sunk(ship, cell)
            else:
                print('hit')

    def process_sunk(self, ship, cell):
        '''
        Processes a sunk ship.

        Parameters:
            - ship (Ship): The ship that was sunk.
            - cell (GridPos): The cell that was hit.
        Returns:
            - None
        '''
        print(f'{ship.type()} sunk')
        cell.remove_ship()
        self._ships.remove(ship.type())
        # If all ships have been sunk, exit the game
        if len(self._ships) == 0:
            print('all ships sunk: game over') 
            sys.exit(0)

    def check_guess(self, guess):
        '''
        Checks if a guess is legal and processes the guess.

        Parameters:
            - guess (str): A string containing the guess.
        Returns:
            - None
        '''
        guess = guess.split()
        x = int(guess[0])
        y = int(guess[1])
        # If the guess is legal
        if x <= 9 and y <= 9:
            self.process_guess(x, y)
        else:   
            print('illegal guess')
        return self
    def get_cell(self, x, y):
        '''
        Returns the cell at the given coordinates.

        Parameters:
            - x (int): The x-coordinate of the cell.
            - y (int): The y-coordinate of the cell.
        Returns:
            - GridPos: The cell at the given coordinates.
        '''
        return self._board[y][x]
    def __str__(self):
        '''
        Returns a string representation of the board.

        Parameters: 
            - None
        Returns:
            - board_str (str): A string representation of the board.
        '''
        board_str = ''
        # Loop through each row in the board in reverse order
        for i, row in enumerate(self._board[::-1]):
            for cell in row:
                board_str += str(cell) + ' '        
            if i < len(self._board) - 1: 
                board_str += '\n'
        return board_str
    def __repr__(self):
        return str(self._board)

class Ship:
    '''
    This class represents a ship in the game. It includes methods for hitting
    a ship, adding a position to a ship, and getting the type and size of a
    ship.

    Attributes:
        - type (str): The type of the ship.
        - hits (int): The number of hits the ship has taken.
        - size (int): The size of the ship.
        - positions (list): A list of the positions of the ship.
    '''
    def __init__(self, type):
        '''
        Constructor for the Ship class.

        Parameters:
            - type (str): The type of the ship.
        Returns:
            - None
        '''
        self._type = type
        self._hits = 0 
        self._positions = []
        if self._type == 'A':
            self._size = 5
        elif self._type == 'B':
            self._size = 4
        elif self._type == 'S':
            self._size = 3
        elif self._type == 'D':
            self._size = 3
        elif self._type == 'P':
            self._size = 2
    def hit(self):
        '''
        Increments the number of hits the ship has taken.
        Returns True if the ship has been sunk.

        Parameters:
            - None
        Returns:
            - bool: True if the ship has been sunk, False otherwise.
        '''
        self._hits += 1
        # If the number of hits equals the size of the ship, it has been sunk
        if self._hits == self._size:
            return True
    def add_position(self, x, y):
        '''
        Adds a position that the ship occupies to the ship

        Parameters:
            - x (int): The x-coordinate of the position.
            - y (int): The y-coordinate of the position.
        Returns:
            - None
        '''
        self._positions.append((x, y))
    def type(self):
        '''
        Returns the type of the ship.

        Parameters:
            - None
        Returns:
            - str: The type of the ship.
        '''
        return self._type
    def size(self):
        '''
        Returns the size of the ship.

        Parameters:
            - None
        Returns:
            - int: The size of the ship.
        '''
        return self._size
    def __str__(self):
        '''
        Returns a string representation of the ship.

        Parameters:
            - None
        Returns:
            - str: A string representation of the ship.
        '''
        return str(self._type)
    def __repr__(self):
        '''
        Returns a string representation of the ship for debugging purposes.
        
        Parameters:
            - None
        Returns:
            - str: A string representation of the ship for debugging purposes.
        '''
        return str(self._type) + str(self._hits) + str(self._positions)

def open_placement_file():
    '''
    This function reads in the placement file and returns the data.

    Parameters:
        - None
    Returns:
        - player1_data (list): A list of the ships in the placement file.
    '''
    player1_filename = input()
    player1_file = open(player1_filename, 'r')
    player1_data = []
    for line in player1_file:
        ship = line.strip()
        player1_data.append(ship)
    player1_file.close()
    return player1_data

def open_guess_file():
    '''
    This function reads in the guess file and returns the data.

    Parameters:
        - None
    Returns:
        - player2_data (list): A list of the guesses in the guess file.
    '''
    player2_filename = input()
    player2_file = open(player2_filename, 'r')
    player2_data = []
    for line in player2_file:
        guess = line.strip()
        player2_data.append(guess)
    player2_file.close()
    return player2_data

def main():
    '''
    Main function that runs the game.

    Parameters:
        - None
    Returns:
        - None
    '''
    board = Board()
    player1_data = open_placement_file()
    for ship in player1_data:
        board.place_one_ship(ship)
    board.check_fleet_composition()
    player_2_data = open_guess_file()
    for guess in player_2_data:
        guess = guess.strip()
        if guess:
            board.check_guess(guess)
main()  