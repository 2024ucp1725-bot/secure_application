import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

# 1. SQL Injection vulnerability
def search_product():
    username = request.args.get("username", "")
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    return cursor.fetchall()


# 2. Cross-Site Scripting (XSS)
@app.route("/review")
def product_review():
    review = request.args.get("review", "")
    return "<html><body>Product Review: " + review + "</body></html>"


# 3. File Upload vulnerability
@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    filename = uploaded_file.filename

    upload_path = os.path.join("uploads", filename)
    uploaded_file.save(upload_path)

    return "File uploaded successfully."


@app.route("/")
def home():
    return "E-Commerce Website"


if __name__ == "__main__":
    app.run(debug=True)
