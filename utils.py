from collections import deque
from random import choice
from copy import deepcopy
import numpy as np

class Maze(object):
    odd_row_pattern = [1, 1]
    row_end_cell = 1
    even_row_pattern = [1, 0]
    empty_cell = 0

    deltas_neighbour = [
        (0, 2),
        (2, 0),
        (0, -2),
        (-2, 0),
    ]


    def __init__(self, width, height):
        """Generate a maze string with given width and height.
        
        Width and height are assumed to be odd so that the maze is surrounded by a wall
        and 1 charcter over 2 is a cell followed by a connexion or a wall.
        
        """
        self.width = width
        self.height = height

        semiwidth = self.width // 2
        semiheight = self.height // 2 
        odd_row = list(Maze.odd_row_pattern) * semiwidth + [Maze.row_end_cell]
        even_row = list(Maze.even_row_pattern) * semiwidth + [Maze.row_end_cell]
        self.maze = [list(row) for _ in range(semiheight) for row in (odd_row, even_row)] + [list(odd_row)]
    
        first_cell = (1, 1)
        stack = deque([first_cell])
        visited = {first_cell}
        while len(stack) > 0:
            current_cell = stack.pop()
            
            i, j = current_cell
            # all potential neighbours
            neighbours = [(i + di, j + dj) for (di, dj) in Maze.deltas_neighbour]
            # remove illicit neighbours
            neighbours = [(i, j) for (i, j) in neighbours if (i>0) and (i<self.height) and (j>0) and (j<self.width)]

            unvisited_neighbours = [cell for cell in neighbours if cell not in visited]
            if len(unvisited_neighbours) > 0:
                stack.append(current_cell)
                next_cell = choice(unvisited_neighbours)
                i1, j1 = current_cell
                i2, j2 = next_cell
                wall_to_remove = ()
                self.maze[(i1 + i2) // 2][(j1 + j2) // 2] = Maze.empty_cell
                visited.add(next_cell)
                stack.append(next_cell)

    def is_an_empty_cell(self, i, j):
        return self.maze[i][j] == 0
    
    def get_image(self, x=1, y=1):
        """
        Return an image from the Maze
        x, y: current position in the maze
        """
        maze_ = 255*np.array(self.maze).astype('uint8')
        
        maze_[x, y] = 77

        return maze_
