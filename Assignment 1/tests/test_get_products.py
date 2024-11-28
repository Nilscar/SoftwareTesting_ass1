import pytest
from unittest.mock import mock_open, patch


class Product:
    def __init__(self, name, price, units):
        self.name = name
        self.price = float(price)
        self.units = int(units)

def get_products(file_name):
    products = []
    with open(file_name, 'r') as file:
        for line in file:
            # Skip header line
            if line.startswith("Product"):
                continue
            name, price, units = line.strip().split(',')
            products.append(Product(name, price, units))
    return products

# Test Case 1: Basic Valid Input
@pytest.mark.parametrize("csv_data, expected_count, expected_name, expected_price, expected_units", [
    ("Product,Price,Units\nApple,2,10\nBanana,1,5", 2, "Apple", 2.0, 10)
])
def test_basic_valid_input(csv_data, expected_count, expected_name, expected_price, expected_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/products.csv")
        assert len(products) == expected_count
        assert products[0].name == expected_name
        assert products[0].price == expected_price
        assert products[0].units == expected_units

# Test Case 2: Valid CSV with Different Product Types
@pytest.mark.parametrize("csv_data, expected_name, expected_price, expected_units", [
    ("Product,Price,Units\nApple,2,10\nLaptop,1000,5", "Laptop", 1000.0, 5)
])
def test_valid_csv_with_different_types(csv_data, expected_name, expected_price, expected_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/products.csv")
        assert len(products) == 2
        assert products[1].name == expected_name
        assert products[1].price == expected_price
        assert products[1].units == expected_units

# Test Case 3: Valid CSV with Correct Price and Units Data
@pytest.mark.parametrize("csv_data, expected_price, expected_units", [
    ("Product,Price,Units\nApple,2.99,10\nBanana,1.49,15", 2.99, 10)
])
def test_valid_csv_price_and_units_data(csv_data, expected_price, expected_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/products.csv")
        assert products[0].price == expected_price
        assert products[0].units == expected_units

# Test Case 4: CSV with Single Product
@pytest.mark.parametrize("csv_data, expected_count, expected_name, expected_price, expected_units", [
    ("Product,Price,Units\nApple,2,10", 1, "Apple", 2.0, 10)
])
def test_single_product(csv_data, expected_count, expected_name, expected_price, expected_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/single_product.csv")
        assert len(products) == expected_count
        assert products[0].name == expected_name
        assert products[0].price == expected_price
        assert products[0].units == expected_units

# Test Case 5: CSV with Multiple Products, Some with Zero Units
@pytest.mark.parametrize("csv_data, first_units, second_units", [
    ("Product,Price,Units\nApple,2,0\nBanana,1,5", 0, 5)
])
def test_csv_with_zero_units(csv_data, first_units, second_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/zero_units.csv")
        assert products[0].units == first_units
        assert products[1].units == second_units

# Test Case 6: CSV with Large Numbers
@pytest.mark.parametrize("csv_data, expected_price, expected_units", [
    ("Product,Price,Units\nLaptop,1000,1000", 1000.0, 1000)
])
def test_csv_with_large_numbers(csv_data, expected_price, expected_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/large_numbers.csv")
        assert products[0].price == expected_price
        assert products[0].units == expected_units

# Test Case 7: Valid CSV File with Multiple Lines and Same Product Names
@pytest.mark.parametrize("csv_data, expected_count, expected_name, expected_units", [
    ("Product,Price,Units\nApple,2,10\nApple,2,5", 2, "Apple", 5)
])
def test_duplicates(csv_data, expected_count, expected_name, expected_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/duplicates.csv")
        assert len(products) == expected_count
        assert products[1].name == expected_name
        assert products[1].units == expected_units

# Test Case 8: CSV with Products Having Decimal Prices
@pytest.mark.parametrize("csv_data, expected_price, expected_units", [
    ("Product,Price,Units\nApple,2.99,10\nBanana,1.49,15", 2.99, 10)
])
def test_decimal_prices(csv_data, expected_price, expected_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/decimal_prices.csv")
        assert products[0].price == expected_price
        assert products[1].price == 1.49

# Test Case 9: Valid CSV with All Units Equal to Zero
@pytest.mark.parametrize("csv_data, expected_units", [
    ("Product,Price,Units\nApple,2.0,0\nBanana,1.0,0", 0)
])
def test_zero_units(csv_data, expected_units):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/zero_units.csv")
        assert products[0].units == expected_units
        assert products[1].units == expected_units

# Test Case 10: CSV with Maximum Length (Large Data Set)
@pytest.mark.parametrize("csv_data", [
    "Product,Price,Units\n" + "Product,1,1\n" * 1000
])
def test_large_data(csv_data):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        products = get_products("files/large_data.csv")
        assert len(products) == 1000


# Invalid Test Case 1: Invalid File Path
def test_invalid_file_path():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            get_products("files/non_existent_file.csv")

# Invalid Test Case 2: Invalid CSV Format (Missing Columns)
def test_invalid_csv_format():
    with patch("builtins.open", mock_open(read_data="Product,Price\nApple,2\nBanana,1")):
        with pytest.raises(KeyError):
            get_products("files/invalid_format.csv")

# Invalid Test Case 3: Invalid Price Format (Non-Numeric Price)
def test_invalid_price_format():
    with patch("builtins.open", mock_open(read_data="Product,Price,Units\nApple,abc,10")):
        with pytest.raises(ValueError):
            get_products("files/invalid_price.csv")

# Invalid Test Case 4: Invalid Units Format (Non-Numeric Units)
def test_invalid_units_format():
    with patch("builtins.open", mock_open(read_data="Product,Price,Units\nApple,2,abc")):
        with pytest.raises(ValueError):
            get_products("files/invalid_units.csv")
