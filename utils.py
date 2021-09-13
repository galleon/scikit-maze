from collections import deque
from random import choice
from copy import deepcopy
import matplotlib.pyplot as plt

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
    
    def get_image(self, x, y):
        """
        Return an image from the Maze
        x, y: current position in the maze
        """
        maze_ = deepcopy(self.maze)
        
        maze_[x][y] = 0.3
        plt.ioff()
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')  # set the x and y axes to the same scale
        plt.xticks([])  # remove the tick marks by setting to an empty list
        plt.yticks([])  # remove the tick marks by setting to an empty list
        ax.invert_yaxis()  # invert the y-axis so the first row of data is at the top
        plt.ion()
        fig.canvas.header_visible = False
        fig.canvas.footer_visible = False
        fig.canvas.resizable = False
        fig.set_dpi(1)
        fig.set_figwidth(600)
        fig.set_figheight(600)
        return ax.imshow(maze_)