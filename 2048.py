"""
--------------------- 2048 -------------------------

How to start and stop the game:

Click the 'play' button at the top left corner of
CodeSkulptor to start the game. A popout window will appear
with a menu. Simply click the menu to begin.

To stop, exit the popout window and click the 'reset'
button (to the right of the folder icon).

Controls:

Use arrow keys to shift the tiles in any
vertical or horizontal direction

Click 'New Game' tp start a new game.

                      shift-up
                         ^
                         |
         shift-left <--- | ---> shift-right
                         |
                         v
                    shift-down

NOTE:
    There is one gripe that I have with this game and that
    is that there are no animations when the tiles merge
    or new ones appear. This creates the appearance that
    tiles may not move or might simply appear. Just know
    that everything has been debugged 'under the hood'
    and that any '..wait what?' moments are most likely
    an illusion due to there being no merge or new tile
    animations.

For the curious:
    Feel free to skim over the code and see what's going on.
    If you'd like to change the code up be sure to save
    your work by clicking the floppy disk in the left
    corner of CodeSkulptor and then saving the url somewhere.
    This will NOT affect the version that is presented to you
    from the website.
"""

# Import libraries
import poc_2048_gui
import random

# Constants for direction (DO NOT change these)
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# (Do not change these)
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, board_height, board_width):
        """
        Initializes a game of 2048

        Arguments:
        grid_height(int): height of grid
        grid_width(int): width of grid
        """
        #Initialize grid
        self.board_height = board_height
        self.board_width = board_width
        self.tile_spaces = board_width * board_height
        self.board = []
        self.tile_count = 0
        self.did_not_merge = 0
        self.game_over = False
        self.starting_tiles = {UP:(0, 0), LEFT:(0, 0), DOWN:(board_height - 1, board_width - 1), RIGHT:(0, board_width - 1)}

        #Compute starting tiles
        self.compute_starting_tiles(UP)
        self.compute_starting_tiles(DOWN)
        self.compute_starting_tiles(LEFT)
        self.compute_starting_tiles(RIGHT)

        self.reset()

    def merge(self, seq):

        """
        Merge the current sequence by stripping all zeros from the
        initial incoming sequence, adding adjacent tiles together
        (if present) and then then stripping zeros from the new
        sequence.

        Arguments:
        seq(list): list of current tile values

        Returns:
        new_seq(list): list of newly merged tile values
        """

        seq_length = len(seq)

        # strip zeros for merge processing
        new_seq = self.strip(seq)

        # Merges tiles
        for i in range(len(new_seq)):
            if i != 0:
                # If adjacent tiles are the same, add them together
                if new_seq[i - 1] == new_seq[i]:
                    new_seq[i - 1] += new_seq[i]
                    new_seq[i] = 0

        # slide filled tiles down
        new_seq = self.strip(new_seq)

        # Append zeros to stripped sequence
        new_seq.extend([0] * (seq_length - len(new_seq)))

        '''
        if seq != new_seq:
            self.did_not_merge = False
        else:
            self.did_not_merge = True
        '''

        return new_seq

    def strip(self, seq):
        """
        Removes zeros from incoming sequence list

        Arguments:
        seq(list): list of original tile values

        Returns:
        stripped_seq(list): list of tile values without zeros
        """

        stripped_seq = [elem for elem in seq if elem != 0]

        return stripped_seq

    def compute_starting_tiles(self, direction):

        """
        Computes the starting tiles for a single instance of 2048

        Arguments:
        direction(tuple): offset for computing tile indecies for each direction
        """
        if direction == UP:
            starting_tiles = [(0, i) for i in range(self.board_width)]
            self.starting_tiles[direction] = starting_tiles

        elif direction == DOWN:
            starting_tiles = [(self.board_height - 1, -i + (self.board_width - 1)) for i in range(self.board_width)]
            self.starting_tiles[direction] = starting_tiles

        elif direction == RIGHT:
            starting_tiles = [(i, self.board_width - 1) for i in range(self.board_width)]
            self.starting_tiles[direction] = starting_tiles

        else:
            starting_tiles = [(i, 0) for i in range(self.board_height)]
            self.starting_tiles[direction] = starting_tiles


    def reset(self):
        """
        Resets grid
        """

        self.board = [[0 for dummy_col in range(0, self.board_width)] for dummy_rows in range(0, self.board_height)]

        #For starting tile computation:
        #[self.compute__starting_tiles() for self.STARTING_TILES[UP] in range(3)]

        self.new_tile()
        self.new_tile()

    def new_tile(self):
        """
        Creates a new tile in a randomly selected empty square.
        Tiles are 2 90% of the time and 4 10% of the time.
        """

        while True:

            # Randomly set row and column coordinate
            r = random.randint(0, self.get_grid_height() - 1)
            c = random.randint(0, self.get_grid_width() - 1)

            # Set values for tiles
            if self.get_tile(r, c) == 0:
                rand_num = random.randint(1, 10)
                # Value is 2 if not within the 10th percentile
                if rand_num != 1:
                    value = 2
                    self.board[r][c] = value
                    print "New tile: " + str(value) + " at position " + str(r) + ", " + str(c)
                # Value is 4 if within 10th percentile
                elif rand_num == 1:
                    value = 4
                    self.board[r][c] = value
                    print "New tile: " + str(value) + " at position " + str(r) + ", " + str(c)
                # Break loop after new tile is generated
                break

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """

        return self.board[row][col]

    def get_grid_height(self):
        """
        Get the height of the board.
        """

        return self.board_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """

        return self.board_width

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.board[row][col] = value

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return [[str(self.get_tile(dummy_row, dummy_col)) for dummy_col in range(0, self.board_width)] for dummy_row in range(0, self.board_height)]

    def move(self, direction):
        """
        Moves all tiles in the given direction and adds
        a new tile if any tiles moved.

        Aruments:
        direction(tuple): offset for computing tile indecies for each direction
        """

        start_tiles = self.starting_tiles.get(direction)
        offset = OFFSETS.get(direction)
        changed = False

                                #### CAN BE SIMPLIFIED ####

        # Traverse through grid
        for row, col in start_tiles:
            temp_list = []
            # While within bounds of board
            while (row >= 0 and row < self.board_height) and (col >= 0 and col < self.board_width):
                # Build temporary list from current board
                temp_list.append(self.get_tile(row, col))
                row += offset[0]
                col += offset[1]
            # Process temporary list
            result_list = self.merge(temp_list)

            # Reverse and transform list
            result_list.reverse()
            for entry in result_list:
                row -= offset[0]
                col -= offset[1]

                # If board state has changed
                if entry != self.board[row][col]:
                        changed = True

                self.set_tile(row, col, entry)

        # Generate new tiles if board state has changed
        if changed == True:
            self.new_tile()

    def check_for_gameOver(self):
        """
        Checks if any potential moves are available when tile count reaches maximum

        Return:
        True (boolean): No potential moves, game is over.

        """

        for row in range(self.board_height):
            for col in range(self.board_width - 1):
                if self.get_tile(row, col) == self.get_tile(row, col + 1):
                    return False

        for col in range(self.board_width):
            for row in range(self.board_height - 1):
                if self.get_tile(row, col) == self.get_tile(row + 1, col):
                    return False

        print "No more moves. Game over. Press 'New Game' to try again."
        self.game_over = True


# Create single instance of 2048 in GUI
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))