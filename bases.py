from typing import Tuple, List
import random
import copy


class cell:

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.is_visited = False
        self.north =  True
        self.east = True
        self.west = True
        self.south = True

    def has_unvisited_n(self, grid: List[List["cell"]]) -> List["cell"]:
        my_n = []
        if self.row - 1 > 0:
            top = grid[self.row - 1, self.col]
            my_n.append(top)
        if self.row + 1 < len(grid):
            bottom = grid[self.row - 1, self.col]
            my_n.append(bottom)
        if self.col - 1 > 0:
            left = grid[self.row - 1, self.col]
            my_n.append(left)
        if self.col + 1 < len(grid[0]):
            right = grid[self.row - 1, self.col]
            my_n.append(right)
        return my_n


    def open_path(c1: "cell", c2: "cell") -> None:
        if c1.col - c2.col == 1:
            c1.west = False
            c2.east = False
        elif c1.col - c2.col == -1:
            c2.west = False
            c1.east = False
        elif c1.row - c2.row == 1:
            c1.north = False
            c2.south = False
        elif c1.row - c2.row == -1:
            c2.north = False
            c1.south = False


#def visit(grid: List[list], stack: list, cur_cell: cell) -> tuple:
#    cur_cell.is_visitted = True
#    stack.append(cur_cell)
#    candidate_n_index = [(cur_cell.row_index - 1,cur_cell.col_index),(cur_cell.row_index,cur_cell.col_index + 1),
#               (cur_cell.row_index + 1,cur_cell.col_index),(cur_cell.row_index,cur_cell.col_index - 1)]
#    n_index = []
#    for i in range(4):
#        if (candidate_n_index[i][0] > 0 and candidate_n_index[i][1] > 0 and
#           grid[candidate_n_index[i][0]][candidate_n_index[i][1]].is_visitted is False):
#            n_index.append(candidate_n_index[i])
#    return (stack, random.choice(n_index))



class maze:
    def __int__(self, height: int, width: int, ENTRY: Tuple[int], EXIT: Tuple[int],
                PERFECT: bool):
        self.height = height
        self.width = width
        self.ENTRY = ENTRY
        self.EXIT = EXIT
        self.PERFECT = PERFECT
        self.grid = self.grid_build(height, width)


    def grid_build(height: int, width: int) -> List[List[cell]]:
        grid = []
        for i in range (height):
            row = []
            for j in range (width):
                row.append(cell(i, j))
            grid.append(row)
        return grid

    def reserve_42(self) -> None:
        height = self.height // 2
        width = self.width // 2
        self.grid[height][width + 1].is_visited = True
        self.grid[height][width + 2].is_visited = True
        self.grid[height][width + 3].is_visited = True
        self.grid[height][width - 1].is_visited = True
        self.grid[height][width - 2].is_visited = True
        self.grid[height][width - 3].is_visited = True
        self.grid[height + 1][width + 1].is_visited = True
        self.grid[height + 1][width - 1].is_visited = True
        self.grid[height + 2][width - 1].is_visited = True
        self.grid[height + 2][width + 1].is_visited = True
        self.grid[height + 2][width + 2].is_visited = True
        self.grid[height + 2][width + 3].is_visited = True
        self.grid[height - 1][width + 1].is_visited = True
        self.grid[height - 1][width - 1].is_visited = True
        self.grid[height - 2][width + 1].is_visited = True
        self.grid[height - 2][width + 2].is_visited = True
        self.grid[height - 2][width + 3].is_visited = True
        self.grid[height - 2][width - 1].is_visited = True


    def gen_maze(self):
        if self.height <= 5 or self.width <= 7:
            raise ValueError("The maze size is too small")
        self.reserve_42()
        st_row= random.randint(0, self.height - 1)
        st_col= random.randint(0, self.width - 1)
        stack = []
        stack.append(self.grid[st_row, st_col])
        while len(stack):
            cur =  stack[-1]
            cur.is_visited = True
            n = cur.has_unvisited_n()
            if len(n) == 0:
                stack.pop()
                continue
            rand_cell = random.choice(n)
            cur.open_path(rand_cell)
            stack.append(rand_cell)


        """
        1 - vistied
        2 - return n by has_unvisited_n if not pop and repeat
        3 - choose random n
        4 -  breaks walls and push cell and repeat 
        """

