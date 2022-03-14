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


def main():
    data = read_json()
    while True:
        resp = input("To register, enter 'r'.\nTo log in, enter 'l'.\nInput: ")
        print()

        if resp == "r":
            while True:
                print("Note: login and password must consist only of numbers and latin letters.")
                user_login = input("Enter new login: ")
                password = input("Enter new password: ")
                
                user_id = register(data, user_login, password)
                
                if user_id is None:
                    print("Incorrect input or this login is in use. Please, try again.")
                    print()
                else:
                    print("Success.")
                    print()
                    break
            break

        elif resp == "l":
            while True:
                user_login = input("Enter login: ")
                password = input("Enter password: ")

                user_id = login(data, user_login, password)

                if user_id is None:
                    print("Wrong login or password. Try again.")
                    print()
                else:
                    print("Success.")
                    print()
                    break
            break

        else:
            print("Wrong response. Try again.")

    while True:
        resp = input("To display userdata, enter 'u'.\nTo display profile, enter 'p'\n\
To change profile field, enter 'c'.\nInput: ")

        if resp == "u":
            print()
            display_user(data, user_id)
            print()

        elif resp == "p":
            print()
            display_profile(data, user_id)
            print()

        elif resp == "c":
            print()
            print("user_id and profile_id are unchangeable.")

            field = input("Enter field name: ")
            contents = input("Enter new value (if numeric, must consist only of numbers): ")

            if change_profile(data, user_id, field, contents):
                print("Success.")
            else:
                print("Error. Data remains unchanged.")
            print()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
