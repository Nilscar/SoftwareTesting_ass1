import pytest
from online_shopping_cart.checkout.shopping_cart import ShoppingCart  # Correct path for ShoppingCart
from online_shopping_cart.product.product import Product  # Correct path for Product


# Correct path for Product


class User:
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet


def check_cart(user, cart):
    # Check if user has sufficient funds
    total_price = cart.get_total_price()
    if total_price > user.wallet:
        raise ValueError("Insufficient funds")

    # Check for invalid product prices
    for product in cart.retrieve_items():
        if product.price < 0:
            raise ValueError("Invalid product price")

    return True  # Cart is valid if no issues


# Valid Test Case 1: Single product, sufficient funds
def test_valid_cart_case_1():
    user = User("Alice", 50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Book", price=20.0, units=1))
    assert check_cart(user, cart) == True


# Valid Test Case 2: Multiple products, sufficient funds
def test_valid_cart_case_2():
    user = User("Bob", 100.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Pen", price=5.0, units=4))
    cart.add_item(Product(name="Notebook", price=10.0, units=3))
    assert check_cart(user, cart) == True


# Valid Test Case 3: Cart with multiple units of one product, sufficient funds
def test_valid_cart_case_3():
    user = User("Charlie", 50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Mug", price=5.0, units=10))
    assert check_cart(user, cart) == True


# Valid Test Case 4: Single product with exact wallet balance
def test_valid_cart_case_4():
    user = User("Diana", 30.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Shirt", price=30.0, units=1))
    assert check_cart(user, cart) == True


# Valid Test Case 5: Empty cart, no money needed
def test_valid_cart_case_5():
    user = User("Eve", 100.0)
    cart = ShoppingCart()
    assert check_cart(user, cart) == True


# Valid Test Case 6: Cart with fractional product prices, sufficient funds
def test_valid_cart_case_6():
    user = User("Frank", 20.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Chocolate", price=2.5, units=4))
    cart.add_item(Product(name="Candy", price=1.5, units=6))
    assert check_cart(user, cart) == True


# Valid Test Case 7: Product removal with correct price calculation
def test_valid_cart_case_7():
    user = User("Grace", 100.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Shoes", price=40.0, units=3))
    cart.remove_item(Product(name="Shoes", price=40.0, units=1))
    assert check_cart(user, cart) == True


# Valid Test Case 8: Multiple products, total within budget
def test_valid_cart_case_8():
    user = User("Hannah", 150.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Backpack", price=30.0, units=2))
    cart.add_item(Product(name="Laptop", price=90.0, units=1))
    assert check_cart(user, cart) == True


# Valid Test Case 9: High wallet balance, multiple products
def test_valid_cart_case_9():
    user = User("Ivy", 5000.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Luxury Watch", price=2500.0, units=1))
    cart.add_item(Product(name="Gift Box", price=500.0, units=2))
    assert check_cart(user, cart) == True


# Valid Test Case 10: Cart with no negative prices
def test_valid_cart_case_10():
    user = User("Jack", 50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Smartphone", price=300.0, units=1))
    cart.add_item(Product(name="Earphones", price=50.0, units=1))
    assert check_cart(user, cart) == True

# Invalid Test Case 1: Insufficient funds
def test_invalid_cart_case_1():
    user = User("Liam", 20.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Watch", price=50.0, units=1))
    with pytest.raises(ValueError):
        check_cart(user, cart)

# Invalid Test Case 2: Negative product price
def test_invalid_cart_case_2():
    user = User("Mason", 100.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Glitch Item", price=-10.0, units=1))
    with pytest.raises(ValueError):
        check_cart(user, cart)

# Invalid Test Case 3: Cart is None (invalid cart object)
def test_invalid_cart_case_3():
    user = User("Noah", 100.0)
    cart = None
    with pytest.raises(AttributeError):
        check_cart(user, cart)

# Invalid Test Case 4: User with missing wallet attribute
def test_invalid_cart_case_4():
    cart = ShoppingCart()
    invalid_user = object()  # User object does not have 'wallet' attribute
    with pytest.raises(AttributeError):
        check_cart(invalid_user, cart)
