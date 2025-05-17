from abc import ABC, abstractmethod
import json
from datetime import datetime

# Custom Exceptions
class InventoryError(Exception):
    pass


class DuplicateProductIDError(InventoryError):
    def __str__(self):
        return "A product with this ID already exists in the inventory."


class InsufficientStockError(InventoryError):
    def __init__(self, product_id, requested, available):
        self.product_id = product_id
        self.requested = requested
        self.available = available

    def __str__(self):
        return f"Insufficient stock for product {self.product_id}. Requested: {self.requested}, Available: {self.available}"


class InvalidProductDataError(InventoryError):
    def __str__(self):
        return "Invalid product data encountered while loading from file."


# Abstract Base Class: Product
class Product(ABC):
    def __init__(self, product_id, name, price, quantity_in_stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock

    @abstractmethod
    def restock(self, amount):
        pass

    @abstractmethod
    def sell(self, quantity):
        pass

    def get_total_value(self):
        return self._price * self._quantity_in_stock

    @abstractmethod
    def __str__(self):
        pass


# Subclasses of Product
class Electronics(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, warranty_years, brand):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._warranty_years = warranty_years
        self._brand = brand

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise InsufficientStockError(self._product_id, quantity, self._quantity_in_stock)
        self._quantity_in_stock -= quantity

    def __str__(self):
        return (f"[Electronics] ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}, "
                f"Stock: {self._quantity_in_stock}, Brand: {self._brand}, Warranty: {self._warranty_years} years")


class Grocery(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, expiry_date):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise InsufficientStockError(self._product_id, quantity, self._quantity_in_stock)
        self._quantity_in_stock -= quantity

    def is_expired(self):
        return datetime.now().date() > self._expiry_date

    def __str__(self):
        status = "Expired" if self.is_expired() else "Not Expired"
        return (f"[Grocery] ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}, "
                f"Stock: {self._quantity_in_stock}, Expiry Date: {self._expiry_date}, Status: {status}")


class Clothing(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, size, material):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._size = size
        self._material = material

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise InsufficientStockError(self._product_id, quantity, self._quantity_in_stock)
        self._quantity_in_stock -= quantity

    def __str__(self):
        return (f"[Clothing] ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}, "
                f"Stock: {self._quantity_in_stock}, Size: {self._size}, Material: {self._material}")


# Inventory Class
class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product._product_id in self._products:
            raise DuplicateProductIDError()
        self._products[product._product_id] = product

    def remove_product(self, product_id):
        if product_id not in self._products:
            raise ValueError(f"Product with ID {product_id} not found.")
        del self._products[product_id]

    def search_by_name(self, name):
        return [p for p in self._products.values() if name.lower() in p._name.lower()]

    def search_by_type(self, product_type):
        return [p for p in self._products.values() if isinstance(p, product_type)]

    def list_all_products(self):
        return list(self._products.values())

    def sell_product(self, product_id, quantity):
        if product_id not in self._products:
            raise ValueError(f"Product with ID {product_id} not found.")
        self._products[product_id].sell(quantity)

    def restock_product(self, product_id, quantity):
        if product_id not in self._products:
            raise ValueError(f"Product with ID {product_id} not found.")
        self._products[product_id].restock(quantity)

    def total_inventory_value(self):
        return sum(p.get_total_value() for p in self._products.values())

    def remove_expired_products(self):
        expired = []
        for product in self._products.values():
            if isinstance(product, Grocery) and product.is_expired():
                expired.append(product._product_id)
        for pid in expired:
            self.remove_product(pid)
        return expired

    # Save and Load Inventory
    def save_to_file(self, filename):
        data = []
        for product in self._products.values():
            if isinstance(product, Electronics):
                product_data = {
                    "type": "Electronics",
                    "product_id": product._product_id,
                    "name": product._name,
                    "price": product._price,
                    "quantity_in_stock": product._quantity_in_stock,
                    "warranty_years": product._warranty_years,
                    "brand": product._brand
                }
            elif isinstance(product, Grocery):
                product_data = {
                    "type": "Grocery",
                    "product_id": product._product_id,
                    "name": product._name,
                    "price": product._price,
                    "quantity_in_stock": product._quantity_in_stock,
                    "expiry_date": product._expiry_date.strftime("%Y-%m-%d")
                }
            elif isinstance(product, Clothing):
                product_data = {
                    "type": "Clothing",
                    "product_id": product._product_id,
                    "name": product._name,
                    "price": product._price,
                    "quantity_in_stock": product._quantity_in_stock,
                    "size": product._size,
                    "material": product._material
                }
            data.append(product_data)

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            for item in data:
                if item["type"] == "Electronics":
                    product = Electronics(
                        product_id=item["product_id"],
                        name=item["name"],
                        price=item["price"],
                        quantity_in_stock=item["quantity_in_stock"],
                        warranty_years=item["warranty_years"],
                        brand=item["brand"]
                    )
                elif item["type"] == "Grocery":
                    product = Grocery(
                        product_id=item["product_id"],
                        name=item["name"],
                        price=item["price"],
                        quantity_in_stock=item["quantity_in_stock"],
                        expiry_date=item["expiry_date"]
                    )
                elif item["type"] == "Clothing":
                    product = Clothing(
                        product_id=item["product_id"],
                        name=item["name"],
                        price=item["price"],
                        quantity_in_stock=item["quantity_in_stock"],
                        size=item["size"],
                        material=item["material"]
                    )
                else:
                    raise InvalidProductDataError()
                self.add_product(product)
        except Exception as e:
            raise InvalidProductDataError() from e


# CLI Menu
def main():
    inventory = Inventory()

    while True:
        print("\n=== Inventory Management System ===")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. Restock Product")
        print("4. Search by Name")
        print("5. List All Products")
        print("6. Remove Expired Products")
        print("7. Save Inventory to File")
        print("8. Load Inventory from File")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_type = input("Enter product type (Electronics/Grocery/Clothing): ")
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter stock quantity: "))

            if product_type.lower() == "electronics":
                warranty_years = int(input("Enter warranty years: "))
                brand = input("Enter brand: ")
                product = Electronics(product_id, name, price, quantity, warranty_years, brand)
            elif product_type.lower() == "grocery":
                expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
                product = Grocery(product_id, name, price, quantity, expiry_date)
            elif product_type.lower() == "clothing":
                size = input("Enter size: ")
                material = input("Enter material: ")
                product = Clothing(product_id, name, price, quantity, size, material)
            else:
                print("Invalid product type.")
                continue

            try:
                inventory.add_product(product)
                print("Product added successfully.")
            except DuplicateProductIDError as e:
                print(e)

        elif choice == "2":
            product_id = input("Enter product ID: ")
            quantity = int(input("Enter quantity to sell: "))
            try:
                inventory.sell_product(product_id, quantity)
                print(f"Sold {quantity} units of product {product_id}.")
            except ValueError as e:
                print(e)
            except InsufficientStockError as e:
                print(e)

        elif choice == "3":
            product_id = input("Enter product ID: ")
            quantity = int(input("Enter quantity to restock: "))
            try:
                inventory.restock_product(product_id, quantity)
                print(f"Restocked {quantity} units of product {product_id}.")
            except ValueError as e:
                print(e)

        elif choice == "4":
            name = input("Enter product name to search: ")
            results = inventory.search_by_name(name)
            if results:
                for product in results:
                    print(product)
            else:
                print("No products found.")

        elif choice == "5":
            products = inventory.list_all_products()
            for product in products:
                print(product)

        elif choice == "6":
            removed = inventory.remove_expired_products()
            if removed:
                print(f"Removed expired products: {removed}")
            else:
                print("No expired products found.")

        elif choice == "7":
            filename = input("Enter filename to save inventory: ")
            inventory.save_to_file(filename)
            print("Inventory saved successfully.")

        elif choice == "8":
            filename = input("Enter filename to load inventory: ")
            try:
                inventory.load_from_file(filename)
                print("Inventory loaded successfully.")
            except InvalidProductDataError as e:
                print(e)

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()