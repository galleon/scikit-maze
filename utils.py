from collections import deque
from random import choice

class Maze(object):
    odd_row_pattern = "+-"
    odd_row_end_cell = "+"
    even_row_pattern = "| "
    even_row_end_cell = "|"
    empty_cell = " "

    deltas_neighbour = [
        (0, 2),
        (2, 0),
        (0, -2),
        (-2, 0),
    ]


    def __init__(self, width, height):
        self.width = width
        self.height = height


    def get_neighbours(self, cell):
        i, j = cell
        # all potential neighbours
        neighbours = [(i + di, j +dj) for (di, dj) in Maze.deltas_neighbour]
        # remove illicit neighbours
        neighbours = [(i, j) for (i, j) in neighbours 
                      if (i>0) and (i<self.height) and (j>0) and (j<self.width)]
        return neighbours

    def get_str(self):
        """Generate a maze string with given width and height.
        
        Width and height are assumed to be odd so that the maze is surrounded by a wall
        and 1 charcter over 2 is a cell followed by a connexion or a wall.
        
        """
        semiwidth = self.width // 2
        semiheight = self.height // 2 
        odd_row = list(Maze.odd_row_pattern) * semiwidth + [Maze.odd_row_end_cell]
        even_row = list(Maze.even_row_pattern) * semiwidth + [Maze.even_row_end_cell]
        maze = [list(row) for _ in range(semiheight) for row in (odd_row, even_row)] + [list(odd_row)]
    
        first_cell = (1, 1)
        stack = deque([first_cell])
        visited = {first_cell}
        while len(stack) > 0:
            current_cell = stack.pop()
            unvisited_neighbours = [cell for cell in self.get_neighbours(current_cell) if cell not in visited]
            if len(unvisited_neighbours) > 0:
                stack.append(current_cell)
                next_cell = choice(unvisited_neighbours)
                i1, j1 = current_cell
                i2, j2 = next_cell
                wall_to_remove = ()
                maze[(i1 + i2) // 2][(j1 + j2) // 2] = Maze.empty_cell
                visited.add(next_cell)
                stack.append(next_cell)
    
        return "\n".join(["".join(row) for row in maze])
