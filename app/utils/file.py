from os import path


def get_name(file_path: str) -> str:
    file_name = path.basename(file_path)
    name = file_name.split('.')[0].capitalize()
    return name
