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


def register(data : dict, user_login : str, password : str) -> str | None:
    if not (user_login.isalnum() and password.isalnum()):
        return None

    for user in data["users"]:
        if user["login"] == user_login:
            return None
    
    user_id = str(uuid.uuid4())
    profile_id = str(uuid.uuid4())
    data["users"].append(
            {
                "user_id": user_id,
                "login": user_login,
                "password": password
            }
    )
    data["profiles"].append(
            {
                "profile_id": profile_id,
                "user_id": user_id,
                "level": 1
            }
    )

    write_json(data)

    return user_id


def login(data : dict, user_login : str, password : str) -> str | None:
    for user in data["users"]:
        if user["login"] == user_login and user["password"] == password:
            return user["user_id"]

    return None

