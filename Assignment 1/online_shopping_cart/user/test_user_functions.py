# test_user_functions.py
import pytest
from unittest.mock import patch
from online_shopping_cart.user.user_authentication import UserAuthenticator, PasswordValidator
from online_shopping_cart.user.user_data import UserDataManager


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


#############################
# USER AUTHENTICATOR TESTS
#############################
def test_login_success(mock_user_data):
    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        result = UserAuthenticator.login("testuser", "Valid123!", mock_user_data)
        assert result is not None
        assert result["username"] == "testuser"


def test_login_failure_wrong_password(mock_user_data):
    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        result = UserAuthenticator.login("testuser", "WrongPass!", mock_user_data)
        assert result is None


def test_register_valid_new_user(mock_user_data):
    new_user_data = mock_user_data.copy()

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        with patch.object(UserDataManager, 'save_users') as mock_save:
            UserAuthenticator.register("newuser", "NewPass123!", new_user_data)
            mock_save.assert_called_once()  # Ensures save_users was called once as it should

    assert {"username": "newuser", "password": "NewPass123!", "wallet": 0.0} in new_user_data


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
            UserAuthenticator.register("invalnewuser", "short", new_user_data)
            mock_save.assert_not_called()

    assert {"username": "invalnewuser", "password": "short", "wallet": 0.0} not in new_user_data


def test_register_edge_case_username(mock_user_data):
    new_user_data = mock_user_data.copy()

    with patch.object(UserDataManager, 'load_users', return_value=mock_user_data):
        with patch.object(UserDataManager, 'save_users') as mock_save:
            UserAuthenticator.register("New_User!@#", "EdgePass@123", new_user_data)
            mock_save.assert_called_once()

    assert {"username": "New_User!@#", "password": "EdgePass@123", "wallet": 0.0} in new_user_data

