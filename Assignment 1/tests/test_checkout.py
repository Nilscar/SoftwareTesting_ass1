import pytest

class User:
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet

class Product:
    def __init__(self, name, price, units):
        self.name = name
        self.price = price
        self.units = units

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product):
        self.items.append(product)

    def total_cost(self):
        return sum(item.price * item.units for item in self.items)

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = []

def checkout(user, cart):
    if cart.is_empty():
        return  # No action needed for an empty cart
    total_cost = cart.total_cost()
    if user.wallet >= total_cost:
        user.wallet -= total_cost
        cart.clear()


@pytest.fixture
def valid_cart():
    return {"1": 2, "2": 1}  # 2 Apples, 1 Banana

@pytest.fixture
def product_catalog():
    return {
        "1": {"price": 1.0, "stock": 100},
        "2": {"price": 0.5, "stock": 50},
    }
def test_checkout_with_valid_items_in_cart():
    user = User(name="John", wallet=100.0)
    cart = ShoppingCart()
    product1 = Product(name="Apple", price=10.0, units=2)
    cart.add_item(product1)
    checkout(user, cart)
    assert user.wallet == 80.0
    assert cart.is_empty()

def test_checkout_with_exact_wallet_amount():
    user = User(name="Jane", wallet=20.0)
    cart = ShoppingCart()
    product1 = Product(name="Banana", price=20.0, units=1)
    cart.add_item(product1)
    checkout(user, cart)
    assert user.wallet == 0.0
    assert cart.is_empty()

def test_checkout_multiple_items():
    user = User(name="Mike", wallet=50.0)
    cart = ShoppingCart()
    product1 = Product(name="Apple", price=15.0, units=1)
    product2 = Product(name="Orange", price=20.0, units=1)
    cart.add_item(product1)
    cart.add_item(product2)
    checkout(user, cart)
    assert user.wallet == 15.0
    assert cart.is_empty()

def test_checkout_with_zero_wallet_balance():
    user = User(name="Alex", wallet=50.0)
    cart = ShoppingCart()
    product = Product(name="Milk", price=50.0, units=1)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 0.0
    assert cart.is_empty()

def test_checkout_with_high_quantity():
    user = User(name="Chris", wallet=100.0)
    cart = ShoppingCart()
    product = Product(name="Cereal", price=25.0, units=4)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 0.0
    assert cart.is_empty()

def test_checkout_large_wallet():
    user = User(name="Eve", wallet=1000.0)
    cart = ShoppingCart()
    product = Product(name="Laptop", price=999.99, units=1)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 0.01
    assert cart.is_empty()

def test_checkout_multiple_units_of_same_item():
    user = User(name="Sara", wallet=500.0)
    cart = ShoppingCart()
    product = Product(name="Book", price=100.0, units=5)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 0.0
    assert cart.is_empty()

def test_checkout_when_cart_is_already_empty():
    user = User(name="David", wallet=200.0)
    cart = ShoppingCart()
    checkout(user, cart)
    assert user.wallet == 200.0
    assert cart.is_empty()

def test_checkout_wallet_precision():
    user = User(name="Leo", wallet=20.75)
    cart = ShoppingCart()
    product = Product(name="Chocolate", price=20.75, units=1)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 0.0
    assert cart.is_empty()

def test_checkout_with_discounted_items():
    user = User(name="Grace", wallet=100.0)
    cart = ShoppingCart()
    product = Product(name="Shoes", price=90.0, units=1)
    product.price *= 0.9  # Applying a discount
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 10.0
    assert cart.is_empty()

def test_checkout_insufficient_wallet_balance():
    user = User(name="Anna", wallet=5.0)
    cart = ShoppingCart()
    product = Product(name="Juice", price=10.0, units=1)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 5.0
    assert not cart.is_empty()

def test_checkout_empty_cart():
    user = User(name="Mark", wallet=50.0)
    cart = ShoppingCart()
    checkout(user, cart)
    assert user.wallet == 50.0
    assert cart.is_empty()

def test_checkout_with_negative_wallet_balance():
    user = User(name="Bella", wallet=-10.0)
    cart = ShoppingCart()
    product = Product(name="Tea", price=10.0, units=1)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == -10.0
    assert not cart.is_empty()

def test_checkout_with_invalid_product_units():
    user = User(name="Tom", wallet=100.0)
    cart = ShoppingCart()
    product = Product(name="Soap", price=10.0, units=-5)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 100.0
    assert not cart.is_empty()
