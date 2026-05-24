from typing import Union


class ArgsFillingError(Exception):
    """This Exception raised when some args value or the args itself is missing or incorrect.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def int_case(value: str) -> int:
    """ This func handle the case when the agrs value is int

        Args:
            value (str): The value before being processed

        Returns:
            int: The processed value, if valid
    """
    striped_value = value.strip()
    int_value = int(striped_value)
    return int_value


def list_case(value: str) -> list:
    """ This func handle the case when the agrs value is x, y

        Args:
            value (str): The value before being processed

        Returns:
            List[x, y]: The processed value, if valid
    """
    x, y = value.split(",")
    int_x = int(x.strip())
    int_y = int(y.strip())
    return [int_x, int_y]


def str_case(value: str) -> str:
    """ This func handle the case when the agrs value is str(File path)

        Args:
            value (str): The value before being processed

        Returns:
            str: The processed value, if valid
    """
    string = value.strip()
    return string


def bool_case(value: str) -> bool:
    """ This func handle the case when the agrs value is str(bool)

        Args:
            value (str): The value before being processed

        Returns:
            bool: The processed value, if valid
    """
    processed_value = value.strip().lower()
    if processed_value in ["yes", "true"]:
        return True
    elif processed_value in ["no", "false"]:
        return False
    else:
        raise ValueError("The PERFECT values ​​are not recognized")


def value_handler(value: str, key: str) -> Union[list, int, str, bool]:
    """This function forward each value to its custom func

        Args:
            value (str): The value before being processed
            key (str): The args type, each value forward based on it

        Returns:
            Union[list, int, str, bool]: The processed value, if valid
    """
    keys = {
        "WIDTH": "int",
        "HEIGHT": "int",
        "ENTRY": "list",
        "EXIT": "list",
        "OUTPUT_FILE": "str",
        "PERFECT": "bool",
    }
    try:
        if keys[key] == "int":
            result = int_case(value)
        elif keys[key] == "list":
            result = list_case(value)
        elif keys[key] == "str":
            result = str_case(value)
        elif keys[key] == "bool":
             result = bool_case(value)
    except ValueError as e:
        print(f"Erorr: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return result


def parser(file: str) -> dict:
    """This function Parse the config file and return it as dict

        This function try to read the file passed and search across each line
        about the predefined config and try to process it's value

        Args:
            file (str): File path

        Returns:
            Dict["args_name": value]: dict of args and thier values
    """
    args = {
        "WIDTH": "",
        "HEIGHT": "",
        "ENTRY": "",
        "EXIT": "",
        "OUTPUT_FILE": "",
        "PERFECT": "",
    }
    total_received_args = 0
    try:
        with open(file, "r") as f:
            for line in f:
                key, value = line.split("=")
                key = key.strip().upper()
                if key in args.keys():
                    args[key] = value_handler(value= value, key= key)
                    total_received_args += 1
            if total_received_args != 6:
                 raise ArgsFillingError("one of args are missing")
    except ArgsFillingError as e:
         print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return args


if __name__ == "__main__":
    my_dict = parser(r"C:\Users\User\OneDrive\42 core\m3python\A_maze_ing\Amazing\config.txt")
    print(my_dict)