'''
Developers: Oğuzhan Umut Bek , Seymen Alper , Rıza Arslan , Mehmet Enes Polat
'''
import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the game grid
import numpy as np  # fundamental Python module for scientific computing
import copy
from point import Point
import pygame
import os
# Class used for modelling the game grid
from tile import Tile

# Draws the game screen
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create the tile matrix to store the tiles placed on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # game_over flag shows whether the game is over/completed or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(15, 15, 15)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(54, 54, 54)
        self.boundary_color = Color(28, 15, 69)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.002
        self.box_thickness = 8 * self.line_thickness
        # Keeps total game score
        self.score = 0

        self.pos = Point()
        # Keeps the default value of game speed
        self.game_speed = 250
        # It maintains another score information to update the speed based on the total score.
        self.last_updated = 0

        # Initializes the necessary variables from pygame to play background.
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

    # Method used for displaying the game grid
    def display(self):
        # Checks if value of last_updated is > 500, if yes, increases the game speed

        # clear the background canvas to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current (active) tetromino
        if self.current_tetromino is not None and self.next_tetromino is not None:
            self.current_tetromino.draw()
            self.next_tetromino.draw()

        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = game_speed ms
        stddraw.show(self.game_speed)

    # Method for drawing the cells and the lines of the grid
    def draw_grid(self):
        # draw each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                  self.tile_matrix[row][col].draw()

        # Draws the stop button
        stddraw.setPenColor(Color(238, 130, 238))
        stddraw.filledRectangle(12.5, 18.5, .6, .6)
        stddraw.setPenRadius(100)
        stddraw.setPenColor(Color(255, 255, 255))

        stddraw.text(12.8, 18.8, "||")

        # Draws the main score on the top right of the main game screen
        self.show_score(self.score)
        # Displays total number of count how many times the speed increased
        self.show_next_tetromino()

        # draw the inner lines of the grid
        stddraw.setPenColor(Color(  0, 255, 255))
        stddraw.setPenRadius(self.line_thickness)

        # x and y ranges for the game grid
        start_x, end_x = -0.5, 12 - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # A method used checking whether the grid cell with the given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # return False if the cell is out of the grid
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # A method that locks the tiles of a landed tetromino on the grid checking
    # if the game is over due to having any tile above the topmost grid row.
    # (This method returns True when the game is over and False otherwise.)
    def update_grid(self, tiles_to_place):
        # place all the tiles of the stopped tetromino onto the game grid
        n_rows, n_cols = len(tiles_to_place), len(tiles_to_place[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each occupied tile onto the game grid
                if tiles_to_place[row][col] is not None:
                    pos = tiles_to_place[row][col].get_position()
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_place[row][col]
                    # the game is over if any placed tile is out of the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over





    # shows next tetromino by using next_tetromino parameter
    def show_next_tetromino(self):
        stddraw.setPenRadius(150)
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.text(15.8, 5, "NEXT TETROMINO : ")
    # Shows the main score
    def show_score(self, score=0):
        stddraw.setPenRadius(150)
        stddraw.setFontSize(25)
        stddraw.setPenColor(Color(255,255,255))
        stddraw.text(15.8, 18.8, "Score: " + str(score))

        # Takes list of free tile (tiles which is not connected others), send them one unit down
    def handle_free_tiles(self, free_tiles):
            for row in range(self.grid_height):  # excluding the bottommost row
                for col in range(self.grid_width):
                    if free_tiles[row][col]:
                        free_tile_copy = copy.deepcopy(self.tile_matrix[row][col])
                        self.tile_matrix[row - 1][col] = free_tile_copy
                        dx, dy = 0, -1  # change of the position in x and y directions
                        self.tile_matrix[row - 1][col].move(dx, dy)
                        self.tile_matrix[row][col] = None
    def set_next(self, next_tetromino):
        self.next_tetromino = next_tetromino