import json
import uuid


def get_contents(filename : str) -> str:
    try:
        with open(filename, "r") as file:
            data = file.read()
    except FileNotFoundError:
        data = '{"users":[], "profiles":[]}'

    return data


def read_json() -> dict:
    return json.loads(get_contents("data.json"))


def write_json(contents) -> bool:
    try:
        with open("data.json", "w") as file:
            file.write(json.dumps(contents, indent=4))
        return True
    except Exception:
        return False
