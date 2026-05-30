from mlx import Mlx
from MazeGenerator import Maze, Cell
from parser import parser
from typing import Any
import random
from time import sleep

key_bindings = {
    "a": 97,
    "esc": 65307,
    "1": 48 + 1,
    "2": 48 + 2,
    "3": 48 + 3,
    "4": 48 + 4
}

mouse_bindings = {
    "LC": 1,  # Left Click
    "MC": 2,  # Middle Click
    "RC": 3,  # Right Click
    "SU": 4,  # Scroll Up
    "SD": 5  # Scroll Down
}


class GUIError(Exception):
    def __init__(self, m: str = "GUI Error"):
        super().__init__(m)


class Controller:
    def __init__(self, mlx: Any, mlx_con: Any, win_con: Any):
        self.mlx: Mlx = mlx
        self.mlx_con = mlx_con
        self.win_con = win_con

    def close_win(self):
        self.mlx.mlx_destroy_window(self.mlx_con, self.win_con)
        self.mlx.mlx_loop_exit(self.mlx_con)

    def vis_grid(self, maze: Maze, wall: Any, ft: Any,
                 entry: Any = None, exit: Any = None, bg: Any = None) -> None:
        size = (maze.width, maze.height)
        self.mlx.mlx_sync(self.mlx_con, 1, wall)
        self.mlx.mlx_sync(self.mlx_con, 1, ft)
        self.mlx.mlx_clear_window(self.mlx_con, self.win_con)
        cell_obj = []
        for row in maze.grid:
            for cell in row:
                if cell.is_42:
                    cell_obj.append(self.vis_cell(cell, maze, size, ft))
                    # self.vis_cell(cell, size, ft)
                else:
                    cell_obj.append(self.vis_cell(cell, maze, size, wall))
                    # self.vis_cell(cell, size, wall)
        print(cell_obj)
        random.shuffle(cell_obj)
        max_size = len(cell_obj)
        self.mlx.mlx_clear_window(self.mlx_con, self.win_con)
        while len(cell_obj):
            cell = cell_obj.pop(0)
            if cell:
                for wal in cell:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_con,
                        self.win_con,
                        wal["img"],
                        wal["x"],
                        wal["y"]
                    )
                    self.mlx.mlx_do_sync(self.mlx_con)
                sleep((len(cell_obj) + 1) / max_size * 0.000001)
                self.mlx.mlx_do_sync(self.mlx_con)
        self.mlx.mlx_do_sync(self.mlx_con)

    def vis_cell(self, cell: Cell, maze: Maze, size: tuple[int, int], img: Any) -> list[dict]:
        tile = 16
        anchor = (100, 100)
        _42_n = cell.has_42_neighbour(maze.grid)
        wall_obj = []

        base_x = anchor[0] + cell.col * tile * 2
        base_y = anchor[1] + cell.row * tile * 2

        if cell.is_42:
            wall_obj.append({"img": img, "x": base_x - tile,
                             "y": base_y - tile})
            wall_obj.append({"img": img, "x": base_x + tile,
                             "y": base_y - tile})
            wall_obj.append({"img": img, "x": base_x - tile,
                             "y": base_y + tile})
            wall_obj.append({"img": img, "x": base_x + tile,
                             "y": base_y + tile})
            wall_obj.append({"img": img, "x": base_x, "y": base_y - tile})
            wall_obj.append({"img": img, "x": base_x, "y": base_y + tile})
            wall_obj.append({"img": img, "x": base_x + tile, "y": base_y})
            wall_obj.append({"img": img, "x": base_x - tile, "y": base_y})
            
            return wall_obj
        
        if not any(d in _42_n for d in ["nw", "n", "w"]):
            wall_obj.append({"img": img, "x": base_x - tile,
                             "y": base_y - tile})

        if cell.col == size[0] - 1:
            wall_obj.append({"img": img, "x": base_x + tile,
                             "y": base_y - tile})
            
        if cell.row == size[1] - 1:
            wall_obj.append({"img": img,
                             "x": base_x - tile, "y": base_y + tile})
            
        if cell.col == size[0] - 1 and cell.row == size[1] - 1:
            wall_obj.append({"img": img, "x": base_x + tile,
                             "y": base_y + tile})

        if cell.north and not ("n" in _42_n):
            wall_obj.append({"img": img, "x": base_x, "y": base_y - tile})

        if cell.east and not ("e" in _42_n):
            wall_obj.append({"img": img, "x": base_x + tile, "y": base_y})

        if cell.row == size[1] - 1:
            wall_obj.append({"img": img, "x": base_x, "y": base_y + tile})

        if cell.col == 0:
            wall_obj.append({"img": img, "x": base_x - tile, "y": base_y})

        return wall_obj
    
    def color_cell(self, loc: tuple, color, h, w):
        row = loc[0]
        col = loc[1]
        for r in range(0, h):
            for c in range(0, w):
                self.mlx.mlx_pixel_put(self.mlx_con, self.win_con,
                                       col + c,
                                       row + r,
                                       color)
 
    def vis_start_end(self, start, end):
        tile = 16
        anchor = (100, 100)
        st = (anchor[0] + 2 * tile * start[0], anchor[1] + 2 * tile * start[1])
        ed = (anchor[0] + 2 * tile * end[0], anchor[1] + 2 * tile * end[1])
        self.color_cell(st, 0xFF00FF00, tile, tile)
        self.color_cell(ed, 0xFFFF0000, tile, tile)
        self.mlx.mlx_do_sync(self.mlx_con)

    # SSENNESSENNESSSENENWNEEEEESSWNWWSESEESESENENESEENENNENESSSWSWSSWSSESEESSWSWNNWWSWNNNNENNWWSSWNWWWNWSWWSEESEESSSSSWSEEENESSWSESESWSEENENNEENWWNEENESSSSWWSSENES

    def vis_path(self, start, path: str, color=0xFF0000FF):
        tile = 16
        anchor = (100, 100)
        st = [anchor[0] + 2 * tile * start[0], anchor[1] + 2 * tile * start[1]]
        for i in range(len(path)):
            if path[i] == "N":
                if not i == len(path) - 1:
                    st[0] -= 2 * tile
                    self.color_cell(st, color, w=tile, h=tile * 2)
                else:
                    self.color_cell(st, color, w=tile, h=tile)
            elif path[i] == "S":
                st[0] += tile
                if not i == len(path) - 1:
                    self.color_cell(st, color, w=tile, h=tile * 2)
                    st[0] += tile
                else:
                    self.color_cell(st, color, w=tile, h=tile)
            elif path[i] == "E":
                if not i == len(path) - 1:
                    st[1] += tile
                    self.color_cell(st, color, w=tile * 2, h=tile)
                    st[1] += tile
                else:
                    self.color_cell(st, color, w=tile, h=tile)
                
            elif path[i] == "W":
                if not i == len(path) - 1:
                    st[1] -= 2 * tile
                    self.color_cell(st, color, w=tile * 2, h=tile)
                else:
                    self.color_cell(st, color, w=tile, h=tile)
        self.mlx.mlx_do_sync(self.mlx_con)







def mouse_listener(button: int, x: int, y: int, params: dict[Any]) -> None:
    print("the left click value is : ", button)
    mlx = params["mlx"]
    mlx_con = params["mlx_con"]
    win_con = params["win_con"]





def key_listener(keycode: int, params: dict[Any]) -> None:
    mlx = params["mlx"]
    mlx_con = params["mlx_con"]
    win_con = params["win_con"]
    controller = Controller(mlx, mlx_con, win_con)

    print("keycode value is : ", keycode)
    if keycode == key_bindings["esc"] or keycode == key_bindings["4"]:
        controller.close_win()
    elif keycode == key_bindings["1"]:
        vis_maze(params)


def vis_maze(params: dict):
    mlx: Mlx = params["mlx"]
    mlx_con = params["mlx_con"]
    win_con = params["win_con"]
    wall = params["wall"]
    ft = params["42"]

    config = parser("config.txt")
    if (config):
        if config["SEED"]:
            random.seed(42)
        maze = Maze(
            config["HEIGHT"],
            config["WIDTH"],
            config["ENTRY"],
            config["EXIT"],
            config["PERFECT"]
        )
        maze.output("meow.txt")

    mlx.mlx_clear_window(mlx_con, win_con)
    controller = Controller(mlx, mlx_con, win_con)
    controller.vis_grid(maze, wall, ft)
    path = maze.find_path()
    controller.vis_start_end(config["ENTRY"], config["EXIT"])
    controller.vis_path(config["ENTRY"], path, 0xFF0000FF)



def main():
    try:
        # MLX Initialization
        mlx = Mlx()
        mlx_con = mlx.mlx_init()
        if not mlx_con:
            raise GUIError("Error establishing the Graphics Connection")

        win_con = mlx.mlx_new_window(mlx_con, 1920, 1080, "A_meow_ing")
        if not win_con:
            raise GUIError("Error creating the window")

        cat1, _, _ = mlx.mlx_xpm_file_to_image(mlx_con, "resources/cat1.xpm")
        cat2, _, _ = mlx.mlx_xpm_file_to_image(mlx_con, "resources/cat2.xpm")
        mlx.mlx_mouse_hook(win_con,
                           mouse_listener,
                           {"mlx": mlx,
                            "mlx_con": mlx_con,
                            "win_con": win_con
                            })

        mlx.mlx_key_hook(win_con,
                         key_listener,
                         {
                            "mlx": mlx,
                            "mlx_con": mlx_con,
                            "win_con": win_con,
                            "wall": cat1,
                            "42": cat2
                          }
                         )

        # mlx.mlx_loop_hook(
        #     mlx_con,
        #     vis_maze,
        #     {
        #         "mlx": mlx,
        #         "mlx_con": mlx_con,
        #         "win_con": win_con,
        #         "wall": cat1,
        #         "42": cat2
        #     }
        # )
        vis_maze({
                    "mlx": mlx,
                    "mlx_con": mlx_con,
                    "win_con": win_con,
                    "wall": cat1,
                    "42": cat2
        })
        mlx.mlx_loop(mlx_con)

        # to end the program, release all resources
        mlx.mlx_release(mlx_con)
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    main()
