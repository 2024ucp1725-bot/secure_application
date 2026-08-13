import sqlite3
import os
import html

DB_NAME = "ecommerce.db"

# -----------------------------
# Database setup
# -----------------------------
def setup_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            product_name TEXT,
            quantity INTEGER,
            total REAL
        )
    """)

    products = [
        (1, "Laptop", 55000),
        (2, "Headphones", 2500),
        (3, "Keyboard", 1500),
        (4, "Mouse", 800)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO products VALUES (?, ?, ?)",
        products
    )

    connection.commit()
    connection.close()


# -----------------------------
# 1. Product Browsing
# -----------------------------
def browse_products():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print("\n------ PRODUCTS ------")

    for product in products:
        print(
            f"ID: {product[0]} | "
            f"Name: {product[1]} | "
            f"Price: ₹{product[2]}"
        )

    connection.close()


# -----------------------------
# 2. Shopping Cart
# -----------------------------
def shopping_cart():
    cart = []

    while True:
        product_id = input(
            "\nEnter product ID to add to cart (0 to finish): "
        )

        if product_id == "0":
            break

        try:
            product_id = int(product_id)

            connection = sqlite3.connect(DB_NAME)
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            )

            product = cursor.fetchone()
            connection.close()

            if product:
                cart.append(product)
                print(f"{product[1]} added to cart.")
            else:
                print("Product not found.")

        except ValueError:
            print("Please enter a valid product ID.")

    return cart


# -----------------------------
# 3. Checkout
# -----------------------------
def checkout(cart):
    if not cart:
        print("\nCart is empty.")
        return

    username = input("Enter username: ")

    total = 0

    print("\n------ CHECKOUT ------")

    for product in cart:
        print(f"{product[1]} - ₹{product[2]}")
        total += product[2]

    print(f"Total amount: ₹{total}")

    confirm = input("Confirm order? (yes/no): ")

    if confirm.lower() == "yes":

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        for product in cart:
            cursor.execute(
                "INSERT INTO orders "
                "(username, product_name, quantity, total) "
                "VALUES (?, ?, ?, ?)",
                (username, product[1], 1, product[2])
            )

        connection.commit()
        connection.close()

        print("Order placed successfully.")


# -----------------------------
# 4. Order History
# -----------------------------
def order_history():
    username = input("Enter username: ")

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # INTENTIONALLY VULNERABLE:
    # SQL Injection
    query = (
        "SELECT * FROM orders WHERE username = '"
        + username
        + "'"
    )

    cursor.execute(query)
    orders = cursor.fetchall()

    print("\n------ ORDER HISTORY ------")

    for order in orders:
        print(order)

    connection.close()


# -----------------------------
# 5. Product Review
# -----------------------------
def product_review():
    username = input("Enter your name: ")
    review = input("Enter product review: ")

    # INTENTIONALLY VULNERABLE:
    # XSS-style unsafe HTML generation
    review_page = (
        "<html><body>"
        "<h2>Product Review</h2>"
        "<p>User: " + username + "</p>"
        "<p>Review: " + review + "</p>"
        "</body></html>"
    )

    print("\nGenerated review page:")
    print(review_page)


# -----------------------------
# 6. File Upload
# -----------------------------
def upload_file():
    filename = input("Enter file path to upload: ")

    # INTENTIONALLY VULNERABLE:
    # Unsafe file upload / path handling
    upload_directory = "uploads"

    os.makedirs(upload_directory, exist_ok=True)

    destination = os.path.join(
        upload_directory,
        os.path.basename(filename)
    )

    try:
        with open(filename, "rb") as source:
            with open(destination, "wb") as target:
                target.write(source.read())

        print("File uploaded successfully.")

    except Exception as error:
        print("Upload failed:", error)


# -----------------------------
# Main Menu
# -----------------------------
def main():
    setup_database()

    while True:

        print("\n================================")
        print("       E-COMMERCE SYSTEM")
        print("================================")
        print("1. Browse Products")
        print("2. Shopping Cart")
        print("3. Checkout")
        print("4. Order History")
        print("5. Product Review")
        print("6. File Upload")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            browse_products()

        elif choice == "2":
            cart = shopping_cart()
            checkout(cart)

        elif choice == "3":
            print("Please use option 2 to create a cart and checkout.")

        elif choice == "4":
            order_history()

        elif choice == "5":
            product_review()

        elif choice == "6":
            upload_file()

        elif choice == "7":
            print("Thank you for using E-Commerce System.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
