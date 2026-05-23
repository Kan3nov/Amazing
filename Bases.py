from typing import Tuple, List
import random
import copy

class cell:

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.is_visitted = False
        self.north =  True
        self.east = True
        self.west = True
        self.south = True
        self.is42 = False

    def has_unvisited_n(self, grid: List[list]) -> bool:
        if self.row - 1 > 0:
            top = grid[self.row - 1, self.col]
        else:
            top = False
        if self.row - 1 > 0:
            bottom = grid[self.row - 1, self.col]
        else:
            bottom = False
        if self.row - 1 > 0:
            right = grid[self.row - 1, self.col]
        else:
            right = False
        if self.row - 1 > 0:
            left = grid[self.row - 1, self.col]
        else:
            left = False


def visit(grid: List[list], stack: list, cur_cell: cell) -> tuple:
    cur_cell.is_visitted = True
    stack.append(cur_cell)
    candidate_n_index = [(cur_cell.row_index - 1,cur_cell.col_index),(cur_cell.row_index,cur_cell.col_index + 1),
               (cur_cell.row_index + 1,cur_cell.col_index),(cur_cell.row_index,cur_cell.col_index - 1)]
    n_index = []
    for i in range(4):
        if (candidate_n_index[i][0] > 0 and candidate_n_index[i][1] > 0 and
           grid[candidate_n_index[i][0]][candidate_n_index[i][1]].is_visitted is False):
            n_index.append(candidate_n_index[i])
    return (stack, random.choice(n_index))



class maze:
    def __int__(self, height: int, width: int, ENTRY: Tuple[int], EXIT: Tuple[int],
                PERFECT: bool):
        self.height = height
        self.width = width
        self.ENTRY = ENTRY
        self.EXIT = EXIT
        self.PERFECT = PERFECT
        self.grid = self.grid_build(height, width)


    def grid_build(height: int, width: int) -> List[list]:
        grid = []
        width //= 2
        height //= 2
        for i in range (height):
            row = []
            for j in range (width):
                row.append(cell(i, j))
            grid.append(row)
        return grid


    def gen_maze(self):
        if self.height <= 5 or self.width <= 7:
            raise ValueError()
        st_row= random.randint(0, self.height)
        st_col= random.randint(0, self.width)
        unvisited_cell = self.height * self.width
        while unvisited_cell:
            """
            1-
            2-
            """
