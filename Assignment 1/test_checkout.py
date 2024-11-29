import pytest
from unittest.mock import patch, MagicMock
from online_shopping_cart.checkout.checkout_process import checkout_and_payment
from online_shopping_cart.product.product import Product
from online_shopping_cart.checkout.shopping_cart import ShoppingCart
import logging

logging.basicConfig(level=logging.DEBUG)

# Mock login information
login_info_rich_user = {"username":"user","wallet": 10**52}
login_info_full_wallet = {"username": "user", "wallet": 100}
login_info_low_wallet = {"username": "user", "wallet": 20}
login_info_negative_wallet = {"username":"user","wallet": -10}
login_info_decimal_wallet = {"username": "user", "wallet": 50.50}

############################### 
# Fixtures for Mocked Objects #
###############################

@pytest.fixture
def mock_cart_empty():
    cart = ShoppingCart()  
    with patch('online_shopping_cart.checkout.checkout_process.global_cart', cart):
        yield cart

@pytest.fixture
def mock_cart_with_items():
    cart = ShoppingCart()

    product1 = Product(name="Product 1", price=25, units=1) 
    product2 = Product(name="Product 2", price=25, units=1)

    cart.add_item(product1)
    cart.add_item(product2)
    

    with patch('online_shopping_cart.checkout.checkout_process.global_cart', cart):
        yield cart


@pytest.fixture
def mock_products():
    mock_products_list = [
        Product(name="Product 1", price=25, units=5),  
        Product(name="Product 2", price=20, units=3),
        Product(name="Product 3", price=15, units=5),
        Product(name="Product 4", price=20, units=0)
    ]
    with patch('online_shopping_cart.checkout.checkout_process.get_products', return_value=mock_products_list):
        with patch('online_shopping_cart.checkout.checkout_process.global_products', mock_products_list):
            yield mock_products_list

@pytest.fixture
def mock_user_input():
    with patch('online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock:
        yield mock

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock:
        yield mock

@pytest.fixture
def mock_update_wallet():
    with patch('online_shopping_cart.user.user_data.UserDataManager.update_wallet') as mock:
        yield mock

######################################
# Test Cases for invalid input types #
######################################

def test_checkout_with_invalid_int_input():
    invalid_login_info = 12345  

    with pytest.raises(TypeError):
        checkout_and_payment(invalid_login_info)
    
def test_checkout_with_invalid_float_input():
    invalid_login_info = 12.4  

    with pytest.raises(TypeError):
        checkout_and_payment(invalid_login_info)
        
def test_checkout_with_invalid_string_input():
    invalid_login_info = "user"  

    with pytest.raises(TypeError):
        checkout_and_payment(invalid_login_info)
        
def test_checkout_with_invalid_list_input():
    invalid_login_info = ["user","123"]  

    with pytest.raises(TypeError):
        checkout_and_payment(invalid_login_info)

############################
# Test Cases for Scenarios #
############################

def test_display_products(mock_products, mock_user_input, mock_print):
    mock_user_input.side_effect= ["d","l","y"]
    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass
    
    mock_print.assert_any_call('\nAvailable products for purchase:')
    mock_print.assert_any_call('1. Product 1 - $25 - Units: 5')
    mock_print.assert_any_call('2. Product 2 - $20 - Units: 3')
    mock_print.assert_any_call('3. Product 3 - $15 - Units: 5')
    mock_print.assert_any_call('You have been logged out.')

def test_empty_cart(mock_cart_empty, mock_products, mock_user_input, mock_print, mock_update_wallet):
    mock_user_input.side_effect = ["c", "l", "y"]

    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass

    mock_print.assert_any_call("\nItems in the cart:")
    mock_update_wallet.assert_not_called()
    assert mock_cart_empty.is_empty()
    mock_print.assert_any_call("You have been logged out.")

def test_log_out(mock_cart_empty, mock_products, mock_user_input, mock_print, mock_update_wallet):
    mock_user_input.side_effect = ['l','y']
    
    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass
    
    mock_print.assert_any_call("You have been logged out.")
    mock_update_wallet.assert_not_called()
    assert mock_cart_empty.is_empty()

def test_add_out_of_stock_product(mock_products, mock_user_input, mock_print):
    mock_user_input.side_effect = ["4", "l", "y"]  

    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass

    mock_print.assert_any_call("Sorry, Product 4 is out of stock.")
    mock_print.assert_any_call("You have been logged out.")
    
def test_add_non_existent_product(mock_products, mock_user_input, mock_print):
    mock_user_input.side_effect = ["38", "l", "y"]  

    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass

    mock_print.assert_any_call("Invalid input. Please try again.")
    mock_print.assert_any_call("You have been logged out.")

def test_insufficient_funds(mock_cart_with_items, mock_products, mock_user_input, mock_print):
    mock_user_input.side_effect = ["c", "y", "l", "y"]

    try:
        checkout_and_payment(login_info_low_wallet)
    except SystemExit:
        pass

    mock_print.assert_any_call("You don't have enough money to complete the purchase. Please try again!")
    
    assert not mock_cart_with_items.is_empty()
    assert mock_cart_with_items.get_total_price() == 50

def test_checkout_exceeding_funds_by_very_small_amount(mock_cart_empty, mock_products, mock_user_input, mock_print):
    product_1 = Product(name="Product 1", price=49.99, units=1)
    product_2 = Product(name="Product 2", price=0.529999999999999999999999999999999999999999, units=1)
    mock_cart_empty.add_item(product_1)
    mock_cart_empty.add_item(product_2)

    mock_user_input.side_effect = ["c", "y", "l", "y"]

    try:
        checkout_and_payment(login_info_decimal_wallet)
    except SystemExit:
        pass

    mock_print.assert_any_call("You don't have enough money to complete the purchase. Please try again!")
    assert not mock_cart_empty.is_empty()
    

def test_add_multiple_units_no_checkout(mock_products, mock_user_input, mock_cart_empty, mock_print):
    mock_user_input.side_effect = ["3", "3", "l", "y"]

    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass

    assert len(mock_cart_empty.items) == 1
    product = mock_cart_empty.items[0]
    assert product.name == "Product 3"
    assert product.units == 2
    
    mock_print.assert_any_call('Product 3 added to your cart.')
    mock_print.assert_any_call('You have been logged out.')

    assert not mock_cart_empty.is_empty()

def test_invalid_remove(mock_products, mock_user_input, mock_cart_with_items, mock_print):
    mock_user_input.side_effect = ['c', 'n', 'y', '4', 'c', 'n', 'l', 'y']

    assert len(mock_cart_with_items.items) == 2
    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass
    
    assert len(mock_cart_with_items.items) == 2
    mock_print.assert_any_call('Invalid input. Please try again.')

def test_remove(mock_products, mock_user_input, mock_cart_with_items, mock_print):
    mock_user_input.side_effect = ['c', 'n', 'y', '1', 'l', 'y']
    assert len(mock_cart_with_items.items) == 2
    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass
    
    assert len(mock_cart_with_items.items) == 1
    remaining_item_names = [item.name for item in mock_cart_with_items.items]
    assert 'Product 1' not in remaining_item_names

def test_checkout_after_cancel(mock_cart_with_items, mock_products, mock_user_input, mock_print, mock_update_wallet):
    mock_user_input.side_effect = ["c", "n", "n", "c", "y", "l", "y"]

    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass

    mock_print.assert_any_call("Thank you for your purchase, user! Your remaining balance is 50")
    assert mock_cart_with_items.is_empty()

def test_successful_checkout(mock_cart_with_items, mock_products, mock_user_input, mock_print, mock_update_wallet):
    mock_user_input.side_effect = ["c", "y", "l", "y"]

    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass
   
    mock_print.assert_any_call('Thank you for your purchase, user! Your remaining balance is 50')
    mock_update_wallet.assert_called_once_with("user", 50.0)
    
    assert mock_cart_with_items.is_empty()
    assert mock_cart_with_items.get_total_price() == 0

def test_checkout_with_decimal_wallet(mock_cart_with_items, mock_products, mock_user_input, mock_print, mock_update_wallet):
    mock_user_input.side_effect = ["c", "y", "l", "y"]
    logger = logging.getLogger("logger")
    try:
        checkout_and_payment(login_info_decimal_wallet)
    except SystemExit:
        pass
    
    logger.debug("Logging all print calls:")
    for call in mock_print.call_args_list:
        logger.debug(call)

    mock_print.assert_any_call('Thank you for your purchase, user! Your remaining balance is 0.5')
    mock_update_wallet.assert_called_once_with("user", 0.50)
    assert mock_cart_with_items.is_empty()

def test_checkout_very_expensive(mock_cart_empty, mock_products, mock_user_input, mock_print, mock_update_wallet):
    expensive_product = Product(name="Crazy Rolex", price=10**50, units=1)
    mock_cart_empty.add_item(expensive_product)

    mock_user_input.side_effect = ["c", "y", "l", "y"]

    try:
        checkout_and_payment(login_info_rich_user)
    except SystemExit:
        pass

    mock_print.assert_any_call("Thank you for your purchase, user! Your remaining balance is " + str(10**52 - 10**50))
    mock_update_wallet.assert_called_once_with("user", 10**52 - 10**50)

def test_checkout_very_large_quantity(mock_cart_empty, mock_products, mock_user_input, mock_print, mock_update_wallet):
    product = Product(name="Product", price=1, units=10**50)
    mock_cart_empty.add_item(product)

    mock_user_input.side_effect = ["c", "y", "l", "y"]

    try:
        checkout_and_payment(login_info_rich_user)
    except SystemExit:
        pass

    mock_print.assert_any_call("Thank you for your purchase, user! Your remaining balance is " + str(10**52 - 10**50))
    mock_update_wallet.assert_called_once_with("user", 10**52 - 10**50)

def test_add_item_checkout(mock_cart_with_items, mock_products, mock_user_input, mock_print, mock_update_wallet):
    cart = mock_cart_with_items  
    mock_user_input.side_effect = ["1", "c", "y", "l", "y"]
    assert len(cart.items) == 2
    
    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass
    
    mock_print.assert_any_call('Product 1 added to your cart.')
    mock_print.assert_any_call('1. Product 1 - $25 - Units: 2')  ## was 1 unit before add
    mock_print.assert_any_call('Thank you for your purchase, user! Your remaining balance is 25')
    
    mock_update_wallet.assert_called_once_with("user", 25)
     
    assert cart.is_empty()
    assert cart.get_total_price() == 0

def test_multiple_items_checkout_even_zero_checkout(mock_cart_with_items, mock_products, mock_user_input, mock_print, mock_update_wallet):
    cart = mock_cart_with_items  
    mock_user_input.side_effect = ["1", "2", "c", "y", "l", "y"]
    assert len(cart.items) == 2
    
    try:
        checkout_and_payment(login_info_full_wallet)
    except SystemExit:
        pass
    
    mock_print.assert_any_call('Product 1 added to your cart.')
    mock_print.assert_any_call('Product 2 added to your cart.')
    mock_print.assert_any_call('Thank you for your purchase, user! Your remaining balance is 0')
    
    mock_update_wallet.assert_called_once_with("user", 0)
     
    assert cart.is_empty()
    assert cart.get_total_price() == 0

def test_negative_wallet_checkout(mock_cart_with_items, mock_products, mock_user_input, mock_print, mock_update_wallet):
    mock_user_input.side_effect = ["c", "y", "l", "y"]

    try:
        checkout_and_payment(login_info_negative_wallet)
    except SystemExit:
        pass
    
    assert not mock_cart_with_items.is_empty()
    assert mock_cart_with_items.get_total_price() == 50
    mock_print.assert_any_call("You don't have enough money to complete the purchase. Please try again!")
    mock_print.assert_any_call("You have been logged out.")
