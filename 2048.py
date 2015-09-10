"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def swipe(self, seq):
        seq_length = len(seq)
        new_seq = self.strip(seq)
        new_seq = self.merge(new_seq)
        new_seq = self.strip(new_seq)
        new_seq.extend([0] * (seq_length - len(new_seq)))
        if seq != new_seq:
            self.did_not_merge += 1
        
        return new_seq

    def merge(self, seq):
      
        for i in range(len(seq)):
            if i != 0:
                if seq[i - 1] == seq[i]:
                    seq[i - 1] += seq[i]
                    seq[i] = 0
        
        return seq

    def strip(self, seq):
        new_seq = [elem for elem in seq if elem != 0]
        
        return new_seq

    def __init__(self, grid_height, grid_width):
        
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.grid = []
        self.did_not_merge = 0
        self.STARTING_TILES = {UP:(0,0), LEFT:(0, 0), DOWN:(grid_height - 1, grid_width - 1), RIGHT:(0, grid_width - 1)} 
        
        #Simplify with loop
        self.compute_starting_tiles(UP)
        self.compute_starting_tiles(DOWN)
        self.compute_starting_tiles(LEFT)
        self.compute_starting_tiles(RIGHT)
        
        self.reset()
        
    def compute_starting_tiles(self, direction):   
        if direction == UP:
            starting_tiles = [(0, i) for i in range(self.grid_width)]
            self.STARTING_TILES[direction] = starting_tiles
            
        elif direction == DOWN:
            starting_tiles = [(self.grid_height - 1, -i + (self.grid_width - 1)) for i in range(self.grid_width)]
            self.STARTING_TILES[direction] = starting_tiles
            
        elif direction == RIGHT:
            starting_tiles = [(i, self.grid_width - 1) for i in range(self.grid_width)]
            self.STARTING_TILES[direction] = starting_tiles
            
        else:
            starting_tiles = [(i, 0) for i in range(self.grid_height)]
            self.STARTING_TILES[direction] = starting_tiles

    def reset(self):
        self.grid = [[0 for dummy_col in range(0, self.grid_width)]for dummy_rows in range(0, self.grid_height)]
        
        #For starting tile computation:
        #[self.compute__starting_tiles() for self.STARTING_TILES[UP] in range(3)] 
        
        self.new_tile()
        self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        
        while True:
        
            r = random.randint(0, self.get_grid_height() - 1)
            c = random.randint(0, self.get_grid_width() - 1)
            
            if self.get_tile(r, c) == 0:
                rand_num = random.randint(1, 10)
                if rand_num != 1:
                    value = 2
                    self.grid[r][c] = value
                    print "New tile: " + str(value) + " at position " + str(r) + ", " + str(c)
                elif rand_num == 1:
                    value = 4
                    self.grid[r][c] = value
                    print "New tile: " + str(value) + " at position " + str(r) + ", " + str(c)
                break

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        
        return self.grid[row][col]
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
    
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        
        return self.grid_width

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return [[str(self.get_tile(dummy_row, dummy_col))for dummy_col in range(0, self.grid_width)]for dummy_row in range(0, self.grid_height)]

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction == UP or direction == DOWN:
            run_length = self.grid_height
        else:
            run_length = self.grid_width
        
        """
        - INCORPORATE MERGE FUNCTION
        - SET TILE
        - ...
        """
        new_grid = []
        for tile in self.STARTING_TILES[direction]:
            merged_list = self.swipe(self.traverse_grid(tile, OFFSETS[direction], run_length))
            print "Merged List: " + str(merged_list)
            new_grid.append(merged_list)
            
        self.grid = new_grid
        
        if self.did_not_merge != 0:
            self.new_tile()
        
        print new_grid
        new_new_grid = []
        for tile in self.STARTING_TILES[direction]:
            merged_list = self.traverse_grid(tile, OFFSETS[direction], run_length)
            new_new_grid.append(merged_list)
             
            
        self.grid = new_new_grid
         

    def traverse_grid(self, start_tile, direction, run_length):
        temp_list = []
        for index in range(run_length):
            row = start_tile[0] + index * direction[0]
            col = start_tile[1] + index * direction[1]
            temp_list.append(self.get_tile(row, col))
                   
        return temp_list


poc_2048_gui.run_gui(TwentyFortyEight(3, 3))
x = TwentyFortyEight(3, 3)
print x.STARTING_TILES
print x.grid
x.move(DOWN)
print x.grid