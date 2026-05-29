from mlx import Mlx
from time import time
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

    def vis_maze(self, controller: Controller, frame: Image, wall: Image, ft: Image):
        from MazeGenerator import Maze

        config = parser("config.txt")
        if (config):
            if config["SEED"]:
                random.seed(42)
            maze = Maze(
                config["HEIGHT"],
                config["WIDTH"],
                config["ENTRY"],
                config["EXIT"],
                config["PERFECT"],
            )
        self.mlx.mlx_clear_window(self.mlx_con, self.win_con)
        frame.fill_color(0xcf3a93ff)
        maze.gen_Maze()
        self.vis_grid(maze, frame, wall, ft)
        maze.output("meow.txt")

    def vis_grid(self, maze: Any, frame: Image, wall: Image, ft: Image,
                 entry: Any = None, exit: Any = None) -> None:
        size = (maze.width, maze.height)
        for row in maze.grid:
            for cell in row:
                if cell.is_42:
                    self.vis_cell(cell, size, frame, ft)
                else:
                    self.vis_cell(cell, size, frame, wall)

    def vis_cell(self, cell: Any, size: tuple[int, int], frame: Image, wall: Image) -> None:
        tile = 16
        anchor = (100, 100)

        if cell.north:
            frame.put_image(wall, (anchor[0] + cell.col * tile * 2,
                                   anchor[1] + cell.row * tile * 2 - tile))
            frame.put_image(wall, (anchor[0] + cell.col * tile * 2 + tile,
                                   anchor[1] + cell.row * tile * 2 - tile))

        if cell.east:
            frame.put_image(wall, (anchor[0] + cell.col * tile * 2 + tile,
                                   anchor[1] + cell.row * tile * 2))
            frame.put_image(wall, (anchor[0] + cell.col * tile * 2 + tile,
                                   anchor[1] + cell.row * tile * 2 + tile))

        if cell.south and cell.row == size[1] - 1:
            frame.put_image(wall, (anchor[0] + cell.col * tile * 2,
                                   anchor[1] + cell.row * tile * 2 + tile))
            frame.put_image(wall, (anchor[0] + cell.col * tile * 2 - tile,
                                   anchor[1] + cell.row * tile * 2 + tile))

        if cell.west and cell.col == 0:
            frame.put_image(wall, (anchor[0] + cell.col * tile * 2 - tile,
                                   anchor[1] + cell.row * tile * 2))
            frame.put_image(wall, (anchor[0] + cell.col * tile * 2 - tile,
                                   anchor[1] + cell.row * tile * 2 - tile))

def mouse_listener(button: int, x: int, y: int, params: dict[Any]) -> None:
    print("the left click value is : ", button)


def key_listener(keycode: int, params: dict[Any]) -> None:
    wall = params["wall"]
    ft = params["42"]
    frame = params["frame"]
    controller: Controller = params["controller"]

    print("keycode value is : ", keycode)
    if keycode == key_bindings["esc"] or keycode == key_bindings["4"]:
        controller.close_win()
    elif keycode == key_bindings["1"]:
        controller.vis_maze(controller, frame, wall, ft, bg)


class Image:
    def __init__(self, ptr: Any, width: int, height: int, controller: Controller) -> None:
        self.ptr = ptr
        self.width = width
        self.height = height
        self.controller = controller

    def fill_color(self, rgba: int) -> None:
        a = rgba & 0xff
        print("a : ", hex(a))
        b = (rgba >> 8) & 0xff
        print("b : ", hex(b))
        g = (rgba >> 16) & 0xff
        print("g : ", hex(g))
        r = (rgba >> 24) & 0xff
        print("r : ", hex(r))

        buf, _, line_size, _ = self.controller.mlx.mlx_get_data_addr(self.ptr)
        for line in range(self.height):
            pos_byte = line_size * line
            for x in range(0, self.width * 4, 4):
                buf[pos_byte + x] = b
                buf[pos_byte + x + 1] = g
                buf[pos_byte + x + 2] = r
                buf[pos_byte + x + 3] = a

    def put_image(self: Image, other: Image, pos: tuple[int, int]) -> None:
        if other.width + pos[0] > self.width or\
                                other.height + pos[1] > self.height:
            raise GUIError("Image to be put is out of bounds")

        mlx = self.controller.mlx
        img1 = self.ptr
        img2 = other.ptr

        buf1, bytes_pix1, line_size1, _ = mlx.mlx_get_data_addr(img1)
        bytes_pix1 //= 8
        buf2, bytes_pix2, line_size2, _ = mlx.mlx_get_data_addr(img2)
        bytes_pix2 //= 8
        for line in range(0, other.height):
            pos1_byte = (pos[1] + line) * line_size1 + pos[0] * bytes_pix1
            for x in range((other.width - 1) * bytes_pix1):
                buf1[pos1_byte + x] = buf2[line * line_size2 + x]

    def sub_patch(self: Image, other: Image, pos: tuple[int, int],
                  size: tuple[int, int]):
        if self.width != other.width or self.height != self.height:
            raise GUIError("Image to be put is out of bounds")

        mlx = self.controller.mlx
        img1 = self.ptr
        img2 = other.ptr

        buf1, bytes_pix1, line_size1, _ = mlx.mlx_get_data_addr(img1)
        bytes_pix1 //= 8
        buf2, bytes_pix2, line_size2, _ = mlx.mlx_get_data_addr(img2)
        bytes_pix2 //= 8

        for line in range(0, size[1]):
            pos1_byte = (pos[1] + line) * line_size1 + pos[0] * bytes_pix1
            pos2_byte = (pos[1] + line) * line_size2 + pos[0] * bytes_pix2
            for x in range(size[0] * bytes_pix1):
                buf1[pos1_byte + x] = buf2[pos2_byte + x]


time1 = time()


def loop(params: dict[Any]):  # runs every 16ms
    global time1
    print("time gap : ", round(time() - time1, 3), "s")
    controller: Controller = params["controller"]
    frame = params["frame"]
    time1 = time()
    controller.mlx.mlx_put_image_to_window(controller.mlx_con,
                                           controller.win_con, frame.ptr, 0, 0)
    print("time to show image : ", round(time() - time1, 3), "s")
    time1 = time()


def main():
    # try:
        # MLX Initialization
        mlx = Mlx()
        mlx_con = mlx.mlx_init()
        if not mlx_con:
            raise GUIError("Error establishing the Graphics Connection")

        win_con = mlx.mlx_new_window(mlx_con, 1920, 1080, "A_meow_ing")
        if not win_con:
            raise GUIError("Error creating the window")
        controller = Controller(mlx, mlx_con, win_con)

        cat1 = Image(*mlx.mlx_xpm_file_to_image(mlx_con, "resources/cat1.xpm"), controller)
        cat2 = Image(*mlx.mlx_xpm_file_to_image(mlx_con, "resources/cat2.xpm"), controller)
        mlx.mlx_sync(mlx_con, 3, win_con)

        canvas = Image(mlx.mlx_new_image(mlx_con, 1960, 1080), 1960, 1080, controller)
        canvas.fill_color(0xcf3a93ff)

        bg = Image(mlx.mlx_new_image(mlx_con, 1960, 1080), 1960, 1080, controller)
        bg.fill_color(0xcf3a93ff)

        params = {
            "controller": controller,
            "wall": cat1,
            "42": cat2,
            "frame": canvas,
            "bg": bg
        }

        mlx.mlx_mouse_hook(win_con, mouse_listener, params)
        mlx.mlx_key_hook(win_con, key_listener, params)
        mlx.mlx_loop_hook(mlx_con, loop, params)

        controller.vis_maze(controller, canvas, cat1, cat2)
        #controller.vis_maze(cat1, cat2)
        mlx.mlx_loop(mlx_con)


        # to end the program, release all resources
        mlx.mlx_release(mlx_con)
    # except Exception as e:
    #     print("Error: ", e)


if __name__ == "__main__":
    main()
