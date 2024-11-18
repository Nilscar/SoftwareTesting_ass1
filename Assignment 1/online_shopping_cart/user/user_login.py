from online_shopping_cart.user.user_authentication import UserAuthenticator
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

    return None
