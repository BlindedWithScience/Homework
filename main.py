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


def change_profile(data : dict, user_id : str, field : str, contents) -> bool:
    if field == "profile_id" or field == "user_id":
        return False

    for profile in data["profiles"]:
        if profile["user_id"] == user_id and field in profile:

            if type(profile[field]) is int:
                try:
                    contents = int(contents)
                except:
                    return False

            if type(profile[field]) == type(contents):
                profile[field] = contents
                write_json(data) 
                return True

            else:
                return False


def get_field(data : dict, field : str, user_id : str) -> str | None:
    for item in data[field]:
        if item["user_id"] == user_id:
            return item

    return None


def get_user(data : dict, user_id : str) -> str | None:
    return get_field(data, "users", user_id)
   

def get_profile(data : dict, user_id : str) -> str | None:
    return get_field(data, "profiles", user_id)


def display_user(data : dict, user_id : str):
    user = get_user(data, user_id)

    if user is None:
        print("User does not exist")
    
    else:
        print(f"user_id: {user_id} \nlogin: {user['login']}")


def display_profile(data : dict, user_id : str):
    profile = get_profile(data, user_id)

    if profile is None:
        print("User does not exist")
    
    else:
        print(f"user_id: {user_id} \nprofile_id: {profile['profile_id']} \nlevel: {profile['level']}")
