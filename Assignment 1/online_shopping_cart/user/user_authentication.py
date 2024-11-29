from online_shopping_cart.user.user_data import UserDataManager
###############################
# USER AUTHENTICATION CLASSES #
###############################


class PasswordValidator:

    @staticmethod
    def is_valid(password) -> bool:
        # TODO: Task 1: validate password for registration
        if password is not str:
            return False
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return False
        if not any(char.isupper() for char in password):
            print("Password must contain at least one uppercase letter.")
            return False
        if not any(char in "!@#$%^&*" for char in password):
            print("Password must contain at least one special symbol (!@#$%^&*).")
            return False
        return True


class UserAuthenticator:

    @staticmethod
    def login(username, password, data) -> dict[str, str | float] | None:
        is_user_registered: bool = False

        for entry in data:
            if entry['username'].lower() == username.lower():
                is_user_registered = True
            if is_user_registered:
                if entry['password'].lower() == password.lower():
                    print('Successfully logged in.')
                    return {
                        'username': entry['username'],
                        'wallet': entry['wallet']
                    }
                break

        if not is_user_registered:
            print('User is not registered.')
        else:
            print('Login failed.')
        return None

    @staticmethod
    def register(username, password, data) -> None:
        # TODO: Task 1: register username and password as new user to file with 0.0 wallet funds
        # Check if username already exists
        for entry in data:
            if entry['username'].lower() == username.lower():
                print(f"Username '{username}' is already taken.")
                return

        # Validate password
        if not PasswordValidator.is_valid(password):
            print("Registration failed due to invalid password.")
            return
        # Add new user
        new_user = {
            "username": username,
            "password": password,
            "wallet": 0.0
        }
        data.append(new_user)
        UserDataManager.save_users(data)
        print(f"User '{username}' successfully registered.")
