import os
from typing import List, Union, Tuple


def get_main_project_path() -> str:
    """
    Get the main project directory path
    Returns:
        str: The path to the main project directory
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_path_to_file(relative_path_params: Union[Tuple[str], List[str]]) -> str:
    """
    Get the path to a file
    Args:
        relative_path_params (Union[Tuple[str], List[str]]): The relative path to the file
    Returns:
        str: The path to the file
    """
    return os.path.join(get_main_project_path(), *relative_path_params)
