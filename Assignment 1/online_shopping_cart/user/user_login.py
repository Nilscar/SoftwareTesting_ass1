from online_shopping_cart.user.user_authentication import UserAuthenticator, PasswordValidator
from online_shopping_cart.user.user_interface import UserInterface
from online_shopping_cart.user.user_data import UserDataManager

########################
# USER LOGIN FUNCTIONS #
########################

def is_quit(input_argument: str) -> bool:
    return input_argument.lower() == 'q'

def login() -> dict[str, str | float] | None:
    username: str = UserInterface.get_user_input(prompt="Enter your username (or 'q' to quit): ")
    if is_quit(input_argument=username):
        exit(0)  # The user has quit

    password: str = UserInterface.get_user_input(prompt="Enter your password (or 'q' to quit): ")
    if is_quit(input_argument=password):
        exit(0)   # The user has quit

    is_authentic_user: dict[str, str | float] = UserAuthenticator().login(
        username=username,
        password=password,
        data=UserDataManager.load_users()
    )
    if is_authentic_user is not None:
        return is_authentic_user

    # TODO: Task 1: prompt user to register when not found
    # Prompt user to register when not found
    if is_authentic_user is None:
        print('User is not registered.')
        register_choice = UserInterface.get_user_input(prompt="Would you like to register? (yes/no): ").strip().lower()
        if register_choice in ["yes", "y"]:
            while True:
                new_password: str = UserInterface.get_user_input(prompt="Enter a password for registration: ").strip()
                if PasswordValidator.is_valid(new_password):
                    UserAuthenticator.register(username=username, password=new_password, data=UserDataManager.load_users())
                    print(f"User '{username}' successfully registered.")
                    return {"username": username, "wallet": 0.0}
                else:
                    print(
                        "Invalid password. It must be at least 8 characters long, contain one capital letter, and one special character.")

        else:
            print("Registration skipped.")
    return None
