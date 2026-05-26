from mlx import Mlx
from time import sleep
from typing import Any


class GUIError(Exception):
    def __init__(self, m: str = "GUI Error"):
        super().__init__(m)

#  the value of lift click is 1
#  the value of right click is 3
#  the value of the middle click is 2


def close_win(button: int, x: int, y: int, params: dict[Any]) -> None:
    print("the left click value is : ", button)
    mlx = params["mlx"]
    mlx_con = params["mlx_con"]
    win_con = params["win_con"]
    mlx.mlx_destroy_window(mlx_con, win_con)
    mlx.mlx_loop_exit(mlx_con)


def put_pixel(keycode: int, params: dict[Any]):
    print("'a' keycode value is : ", keycode)
    mlx = params["mlx"]
    mlx_con = params["mlx_con"]
    win_con = params["win_con"]
    for x in range(16):
        for y in range(16):
            mlx.mlx_pixel_put(mlx_con, win_con, 100 + x, 100 + y, 0xffffffff)


def main():
    try:
        # MLX Initialization
        mlx = Mlx()
        mlx_con = mlx.mlx_init()
        if not mlx_con:
            raise GUIError("Error establishing the Graphics Connection")

        win_con = mlx.mlx_new_window(mlx_con, 1920, 1080, "hello khashan")
        if not win_con:
            raise GUIError("Error creating the window")

        mlx.mlx_mouse_hook(win_con, close_win, {"mlx": mlx,
                                                "mlx_con": mlx_con,
                                                "win_con": win_con
                                                })
        mlx.mlx_key_hook(win_con, put_pixel, {"mlx": mlx,
                                              "mlx_con": mlx_con,
                                              "win_con": win_con
                                              })
        cat1, w, h = mlx.mlx_xpm_file_to_image(mlx_con, r"resources/cat1.xpm")
        mlx.mlx_put_image_to_window(mlx_con, win_con, cat1, 100, 100)
        mlx.mlx_loop(mlx_con)
        mlx.mlx_destroy_window(mlx_con, win_con)

        # to end the program, release all resources
        mlx.mlx_release(mlx_con)
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    main()
