from typing import Any, cast
import random
from queue import Queue
from parser import parser


random.seed(42)


class MazeError(Exception):
    def __init__(self, m: str = "error generating maze"):
        super().__init__(m)


class Cell:

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.is_visited = False
        self.is_42 = False
        self.path = " "
        self.north = True
        self.east = True
        self.west = True
        self.south = True

    def has_unvisited_n(self, grid: list[list["Cell"]]) -> list["Cell"]:
        my_n = []
        if self.row - 1 >= 0:
            top = grid[self.row - 1][self.col]
            if (not top.is_visited):
                my_n.append(top)
        if self.row + 1 < len(grid):
            bottom = grid[self.row + 1][self.col]
            if (not bottom.is_visited):
                my_n.append(bottom)
        if self.col - 1 >= 0:
            left = grid[self.row][self.col - 1]
            if (not left.is_visited):
                my_n.append(left)
        if self.col + 1 < len(grid[0]):
            right = grid[self.row][self.col + 1]
            if (not right.is_visited):
                my_n.append(right)
        return my_n

    def open_path(c1: "Cell", c2: "Cell") -> None:
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

    def get_acc(self, grid: list[list["Cell"]]) -> list["Cell"]:
        open = []
        if (not self.north and self.path[-1] != "S"):
            new = grid[self.row - 1][self.col]
            new.path = self.path + "N"
            open.append(new)
        if (not self.south and self.path[-1] != "N"):
            new = grid[self.row + 1][self.col]
            new.path = self.path + "S"
            open.append(new)
        if (not self.east and self.path[-1] != "W"):
            new = grid[self.row][self.col + 1]
            new.path = self.path + "E"
            open.append(new)
        if (not self.west and self.path[-1] != "E"):
            new = grid[self.row][self.col - 1]
            new.path = self.path + "W"
            open.append(new)
        random.shuffle(open)
        return open

    def get_value(self) -> int:
        value = 0
        if self.north:
            value += 1
        if self.east:
            value += 2
        if self.south:
            value += 4
        if self.west:
            value += 8
        return value


class Maze:
    def __init__(self, height: int, width: int, ENTRY: tuple[int, int],
                 EXIT: tuple[int, int], PERFECT: bool):
        self.height = height
        self.width = width
        self.entry = ENTRY
        self.exit = EXIT
        self.perfect = PERFECT
        self.grid = self.grid_build(height, width)
        if (self.grid[ENTRY[0]][ENTRY[1]].is_visited):
            raise MazeError("entry is a 42 point")
        elif (self.grid[EXIT[0]][EXIT[1]].is_visited):
            raise MazeError("exit is a 42 point")

    def grid_build(self, height: int, width: int) -> list[list[Cell]]:
        grid = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Cell(i, j))
            grid.append(row)
        return grid

    def reserve_42(self) -> None:
        height = self.height // 2
        width = self.width // 2
        cell42 = [
            self.grid[height][width + 1],
            self.grid[height][width + 2],
            self.grid[height][width + 3],
            self.grid[height][width - 1],
            self.grid[height][width - 2],
            self.grid[height][width - 3],
            self.grid[height + 1][width + 1],
            self.grid[height + 1][width - 1],
            self.grid[height + 2][width - 1],
            self.grid[height + 2][width + 1],
            self.grid[height + 2][width + 2],
            self.grid[height + 2][width + 3],
            self.grid[height - 1][width + 3],
            self.grid[height - 1][width - 3],
            self.grid[height - 2][width + 1],
            self.grid[height - 2][width + 2],
            self.grid[height - 2][width + 3],
            self.grid[height - 2][width - 3]
        ]
        for cell in cell42:
            cell.is_42 = True
            cell.is_visited = True

    def open_loop(self, c1: Cell) -> bool:
        col = c1.col
        row = c1.row
        grid = self.grid
        if col - 1 >= 0:
            n_cell = grid[row][col - 1]
            if n_cell.east is True and not n_cell.is_42:
                c1.open_path(n_cell)
                return True
        if col + 1 <= self.width - 1:
            n_cell = grid[row][col + 1]
            if n_cell.west is True and not n_cell.is_42:
                c1.open_path(n_cell)
                return True
        if row - 1 >= 0:
            n_cell = grid[row - 1][col]
            if n_cell.south is True and not n_cell.is_42:
                c1.open_path(n_cell)
                return True
        if row + 1 <= self.height - 1:
            n_cell = grid[row + 1][col]
            if n_cell.north is True and not n_cell.is_42:
                c1.open_path(n_cell)
                return True
        return False

    def gen_Maze(self) -> None:
        if self.height <= 5 or self.width <= 7:
            raise ValueError("Maze size is too small")
        self.reserve_42()
        st_row = self.entry[0]
        st_col = self.entry[1]
        stack = []
        stack.append(self.grid[st_row][st_col])
        while len(stack):
            cur = stack[-1]
            cur.is_visited = True
            n = cur.has_unvisited_n(self.grid)
            if len(n) == 0:
                stack.pop()
                continue
            rand_cell = random.choice(n)
            cur.open_path(rand_cell)
            stack.append(rand_cell)
        if not self.perfect:
            while True:
                loop_cell = random.choice(random.choice(self.grid))
                if self.open_loop(loop_cell):
                    break

    def find_path(self) -> str:
        q: Queue[Any] = Queue()
        entry = self.grid[self.entry[0]][self.entry[1]]
        exit = self.grid[self.exit[0]][self.exit[1]]
        q.put(entry)
        while not q.empty():
            cur = q.get()
            if (cur == exit):
                return cast(str, cur.path[1:])
            for x in cur.get_acc(self.grid):
                q.put(x)
        return "exit not found"

    def to_hex(self) -> str:
        hexa = ""
        for row in self.grid:
            for cell in row:
                hexa += hex(cell.get_value())[2:].upper()
            hexa += "\n"
        return hexa

    def output(self, file_name: str) -> None:
        self.gen_Maze()
        with open(file_name, "w") as f:
            f.write(self.to_hex())
            f.write("\n")
            f.write(str(self.entry[0]) + "," + str(self.entry[1]) + "\n")
            f.write(str(self.exit[0]) + "," + str(self.exit[1]) + "\n")
            f.write(self.find_path() + "\n")


if __name__ == "__main__":
    config = parser("config.txt")
    if (config):
        maze = Maze(
            config["HEIGHT"],
            config["WIDTH"],
            config["ENTRY"],
            config["EXIT"],
            config["PERFECT"]
        )
        maze.output("meow.txt")
