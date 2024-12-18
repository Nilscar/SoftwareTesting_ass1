# test_user_functions.py
import builtins

import pytest
from unittest.mock import patch, MagicMock
from online_shopping_cart.user.user_login import login
from online_shopping_cart.user.user_authentication import UserAuthenticator, PasswordValidator
from online_shopping_cart.user.user_data import UserDataManager
from online_shopping_cart.user.user_interface import UserInterface
from online_shopping_cart.user.user_logout import logout


###########################
# MOCK DATA FOR TESTING
###########################
@pytest.fixture
def mock_user_data():
    return [
        {"username": "testuser", "password": "Valid123!", "wallet": 100.0},
        {"username": "existinguser", "password": "Secretpass!23", "wallet": 500.0},
        {"username": "anotheruser", "password": "Apassword1@", "wallet": 11.7}
    ]

###########################
# PASSWORD VALIDATOR TESTS
###########################
def test_valid_password():
    assert PasswordValidator.is_valid("Valid123!") is True

def test_invalid_password_no_special_char():
    assert PasswordValidator.is_valid("Valid123") is False

def test_invalid_password_no_capital():
    assert PasswordValidator.is_valid("valid123!") is False

def test_invalid_password_too_short():
    assert PasswordValidator.is_valid("V1!") is False

def test_invalid_password_empty():
    assert PasswordValidator.is_valid("") is False

def test_invalid_input_integer():
    assert PasswordValidator.is_valid(12345678) is False

def test_invalid_input_float():
    assert PasswordValidator.is_valid(1234567.8) is False

def test_invalid_input_list():
    assert PasswordValidator.is_valid(["V","a","l","i","p","a","s","s","1","!"]) is False

#############################
# USER LOGIN TESTS
#############################
def test_user_login_success(mock_user_data):

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data), \
    patch.object(UserInterface, 'get_user_input', side_effect=["testuser", "Valid123!"]):
        with patch.object(UserAuthenticator, 'login') as login_called:
            login()
            login_called.assert_called_once_with(username="testuser", password="Valid123!", data=mock_user_data)
        with patch("builtins.print") as mock_print:
            result = UserAuthenticator.login("testuser", "Valid123!", mock_user_data)
            assert result is not None
            mock_print.assert_called_with('Successfully logged in.')
            assert result["username"] == "testuser"


def test_user_login_failure_wrong_password(mock_user_data):

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data), \
    patch.object(UserInterface, 'get_user_input', side_effect=["testuser", "wrongpass"]):
        with patch.object(UserAuthenticator, 'login') as login_called:
            login()
            login_called.assert_called_once_with(username="testuser", password="wrongpass", data=mock_user_data)
        with patch("builtins.print") as mock_print:
            result = UserAuthenticator.login("testuser", "wrongpass", mock_user_data)
            assert result is None
            mock_print.assert_called_with('Login failed.')


def test_user_login_failure_non_existent_user(mock_user_data):

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data), \
    patch.object(UserInterface, 'get_user_input', side_effect=["nouser", "anypassword"]):
        with patch.object(UserAuthenticator, 'login') as login_called, \
        patch("builtins.input") as mock_input:
            login()
            login_called.assert_called_once_with(username="nouser", password="anypassword", data=mock_user_data)
            #mock_input.assert_any_call("Would you like to register? (yes/no): ")
        with patch("builtins.print") as mock_print:
            result = UserAuthenticator.login("nouser", "anypassword", mock_user_data)
            assert result is None
            mock_print.assert_called_with('User is not registered.')


def test_login_failure_no_user_no_password(mock_user_data):
    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        result = UserAuthenticator.login("", "", mock_user_data)
        assert result is None

def test_login_failure_invalid_input_integer(mock_user_data):
    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        result = UserAuthenticator.login(1234, "", mock_user_data)
        assert result is None

#############################
# USER REGISTER TESTS
#############################
def test_register_valid_new_user(mock_user_data):
    new_user_data = mock_user_data.copy()

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        with patch.object(UserDataManager, 'save_users') as mock_save:
            UserAuthenticator.register("newuser", "ValidPass123!", new_user_data)
            mock_save.assert_called_once()  # Ensures save_users was called once as it should

    assert {"username": "newuser", "password": "ValidPass123!", "wallet": 0.0} in new_user_data


def test_register_existing_user(mock_user_data):
    new_user_data = mock_user_data.copy()

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        with patch.object(UserDataManager, 'save_users') as mock_save:
            UserAuthenticator.register("existinguser", "Secretpass!23", new_user_data)
            mock_save.assert_not_called()  # Save should not happen

    assert {"username": "existinguser", "password": "Secretpass!23", "wallet": 0.0} not in new_user_data


def test_register_invalid_password(mock_user_data):
    new_user_data = mock_user_data.copy()

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        with patch.object(UserDataManager, 'save_users') as mock_save:
            UserAuthenticator.register("newuser", "short", new_user_data)
            mock_save.assert_not_called()

    assert {"username": "newuser", "password": "short", "wallet": 0.0} not in new_user_data


def test_register_invalid_input_username(mock_user_data):
    new_user_data = mock_user_data.copy()

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        with patch.object(UserDataManager, 'save_users') as mock_save:
            UserAuthenticator.register(12345, "ValidPass123!", new_user_data)
            mock_save.assert_not_called()

    assert {"username": 12345, "password": "ValidPass123!", "wallet": 0.0} in new_user_data

def test_register_invalid_input_password(mock_user_data):
    new_user_data = mock_user_data.copy()

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        with patch.object(UserDataManager, 'save_users') as mock_save:
            UserAuthenticator.register("newuser", 12345, new_user_data)
            mock_save.assert_not_called()

    assert {"username": "newuser", "password": 12345, "wallet": 0.0} in new_user_data

def test_register_invalid_input_data(mock_user_data):
    new_user_data = mock_user_data.copy()

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        with patch.object(UserDataManager, 'save_users') as mock_save:
            UserAuthenticator.register("newuser", "ValidPass123!", 12345)
            mock_save.assert_not_called()

    assert {"username": "newuser", "password": "ValidPass123!", "wallet": 0.0} in new_user_data

#############################
# USER LOGOUT TESTS
#############################
def test_logout_with_empty_cart():
    cart = MagicMock()
    cart.is_empty.return_value = True

    with patch.object(UserInterface, 'get_user_input', return_value="y"), \
            patch("builtins.print") as mock_print:
        result = logout(cart)

        assert result is True
        mock_print.assert_called_with('You have been logged out.')


def test_logout_with_items_in_cart():
    cart = MagicMock()
    cart.is_empty.return_value = False
    cart.retrieve_items.return_value = ["item1", "item2"]

    with patch.object(UserInterface, 'get_user_input', return_value="n"), \
            patch("builtins.print") as mock_print:
        result = logout(cart)

        assert result is False
        mock_print.assert_any_call("Your cart is not empty. You have the following items:")
        mock_print.assert_any_call("item1")
        mock_print.assert_any_call("item2")


def test_logout_cart_error_handling():
    cart = MagicMock()
    cart.is_empty.side_effect = AttributeError("is_empty method not found")

    with patch.object(UserInterface, 'get_user_input', return_value="y"), \
            patch("builtins.print") as mock_print:
        with pytest.raises(AttributeError):
            logout(cart)