# 📦 Inventory Management System Documentation
# 📚 Overview
The Inventory Management System is a Python-based application designed to manage different types of products in an inventory. It leverages Object-Oriented Programming (OOP) principles to provide a robust, scalable, and reusable solution for handling stock operations, sales, and data persistence. The system supports three product types: Electronics , Grocery , and Clothing , each with unique attributes and behaviors.

Perfect for learning advanced OOP concepts and applying them to real-world use cases!

# 🚀 Features

Product Types :

Electronics : Includes warranty years and brand.

Grocery : Includes expiry date and expiration status.

Clothing : Includes size and material.

Inventory Operations :

Add, remove, restock, and sell products.

Search products by name or type.

List all products in the inventory.

Calculate total inventory value.

Data Persistence :

Save and load inventory data in JSON format.

Reconstruct subclasses properly when loading data.

Custom Exceptions :

Handle errors like duplicate product IDs, insufficient stock, and invalid product data.

CLI Menu :

Interactive menu for managing the inventory.
# 🔧 Code Explanation

# 1. Abstract Base Class: Product

Attributes :

_product_id: Unique identifier for the product.

_name: Name of the product.

_price: Price of the product.

_quantity_in_stock: Available stock quantity.

Methods :

restock(amount): Adds stock to the product.

sell(quantity): Reduces stock when selling.

get_total_value(): Calculates the total value of the product in stock.

__str__(): Returns a formatted string representation of the product.

# 2. Subclasses of Product

Electronics :

Additional Attributes: _warranty_years, _brand.

Overrides __str__() to include warranty and brand details.

Grocery :

Additional Attributes: _expiry_date.

Methods: is_expired() checks if the product has expired.

Overrides __str__() to include expiry date and status.

Clothing :

Additional Attributes: _size, _material.
Overrides __str__() to include size and material details.

# 3. Inventory Class

Attributes :

_products: A dictionary to store products with their IDs as keys.

Methods :

add_product(product): Adds a product to the inventory.

remove_product(product_id): Removes a product by ID.

search_by_name(name): Searches products by name.

search_by_type(product_type): Searches products by type (e.g., Electronics).

list_all_products(): Lists all products in the inventory.

sell_product(product_id, quantity): Sells a specified quantity of a product.

restock_product(product_id, quantity): Restocks a specified quantity of a product.

total_inventory_value(): Calculates the total value of all products in the inventory.

remove_expired_products(): Removes expired grocery items from the inventory.

# 4. Custom Exceptions

DuplicateProductIDError : Raised when adding a product with a duplicate ID.

InsufficientStockError : Raised when attempting to sell more than available stock.

InvalidProductDataError : Raised when loading invalid product data from a file.

# 5. CLI Menu

Provides an interactive interface for:

Adding, selling, and restocking products.

Searching and listing products.

Saving and loading inventory data.

Exiting the application.

# 📋 Requirements

To run this project, you need the following:

Python 3.8+

Required Python libraries:

json (built-in)

datetime (built-in)

No external libraries are required for core functionality.

# 🚀 How to Run

Clone the Repository :

bash

git clone repository

Run the App :

python app.py

Interact via CLI :

Use the menu options to add, sell, restock, search, and manage products.

# 🛠️ Usage Instructions

1. Add a Product

Choose "Add Product" from the menu.

Enter the product type (Electronics, Grocery, or Clothing), ID, name, price, and stock quantity.

For specific product types:

Electronics : Provide warranty years and brand.

Grocery : Provide expiry date (format: YYYY-MM-DD).

Clothing : Provide size and material.

2. Sell a Product

Choose "Sell Product" from the menu.

Enter the product ID and the quantity to sell.

The system will deduct the sold quantity from the stock.

3. Restock a Product

Choose "Restock Product" from the menu.

Enter the product ID and the quantity to restock.

The system will add the restocked quantity to the stock.

4. Search Products

Choose "Search by Name" or "List All Products" from the menu.

View detailed information about the products.

5. Save and Load Inventory

Choose "Save Inventory to File" to save the current inventory to a JSON file.

Choose "Load Inventory from File" to load inventory data from a JSON file.

6. Exit

Choose "Exit" to quit the application.

🌟 Future Enhancements

Database Integration :

Replace JSON persistence with a database (e.g., SQLite, PostgreSQL).

GUI Interface :

Build a graphical user interface using libraries like Tkinter or Streamlit.

Advanced Reporting :

Generate reports on sales, stock levels, and expired products.

User Authentication :

Add login functionality for different user roles (e.g., admin, staff).

# 📜 License

This project is licensed under the MIT License .

# 📧 Contact

For questions, feedback, or collaboration, feel free to reach out:

Email: asadhussainshad@gmail.com

GitHub: huzaifa-1100

# 🙏 Acknowledgments

Python's abc Module : For enabling abstract base classes.

JSON Module : For data persistence.

Datetime Module : For handling expiry dates.