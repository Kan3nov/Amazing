from mlx import Mlx
from MazeGenerator import Maze, Cell
from parser import parser
from typing import Any
import random

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
        for row in maze.grid:
            for cell in row:
                if cell.is_42:
                    self.vis_cell(cell, size, ft)
                else:
                    self.vis_cell(cell, size, wall)
        self.mlx.mlx_do_sync(self.mlx_con)

    def vis_cell(self, cell: Cell, size: tuple[int, int], img: Any) -> None:
        tile = 16
        anchor = (100, 100)

        if cell.north:
            self.mlx.mlx_put_image_to_window(
                self.mlx_con,
                self.win_con,
                img,
                (anchor[0] + cell.col * tile * 2),
                (anchor[1] + cell.row * tile * 2) - tile
            )
            self.mlx.mlx_put_image_to_window(
                self.mlx_con,
                self.win_con,
                img,
                (anchor[0] + cell.col * tile * 2) + tile,
                (anchor[1] + cell.row * tile * 2) - tile
            )

        if cell.east:
            self.mlx.mlx_put_image_to_window(
                self.mlx_con,
                self.win_con,
                img,
                (anchor[0] + cell.col * tile * 2) + tile,
                (anchor[1] + cell.row * tile * 2)
            )
            self.mlx.mlx_put_image_to_window(
                self.mlx_con,
                self.win_con,
                img,
                (anchor[0] + cell.col * tile * 2) + tile,
                (anchor[1] + cell.row * tile * 2) + tile
            )

        if cell.south and cell.row == size[1] - 1:
            self.mlx.mlx_put_image_to_window(
                self.mlx_con,
                self.win_con,
                img,
                (anchor[0] + cell.col * tile * 2),
                (anchor[1] + cell.row * tile * 2) + tile
            )
            self.mlx.mlx_put_image_to_window(
                self.mlx_con,
                self.win_con,
                img,
                (anchor[0] + cell.col * tile * 2) - tile,
                (anchor[1] + cell.row * tile * 2) + tile
            )

        if cell.west and cell.col == 0:
            self.mlx.mlx_put_image_to_window(
                self.mlx_con,
                self.win_con,
                img,
                (anchor[0] + cell.col * tile * 2) - tile,
                (anchor[1] + cell.row * tile * 2)
            )
            self.mlx.mlx_put_image_to_window(
                self.mlx_con,
                self.win_con,
                img,
                (anchor[0] + cell.col * tile * 2) - tile,
                (anchor[1] + cell.row * tile * 2) - tile
            )


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
