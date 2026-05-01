from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("products.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, price REAL NOT NULL,
            category TEXT, stock INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO products (id,name,price,category,stock) VALUES
        (1,'Laptop',999.99,'Electronics',10),
        (2,'Smartphone',499.99,'Electronics',25),
        (3,'Book',19.99,'Education',100),
        (4,'Headphones',149.99,'Electronics',30),
        (5,'Desk Chair',299.99,'Furniture',15)
    """)
    conn.commit()
    return conn

@app.route("/products")
def get_products():
    category = request.args.get("category")
    db = get_db()
    rows = db.execute(
        "SELECT * FROM products WHERE category = ?" if category else "SELECT * FROM products",
        (category,) if category else ()
    ).fetchall()
    return jsonify([{"id":r[0],"name":r[1],"price":r[2],"category":r[3],"stock":r[4]} for r in rows])

@app.route("/products/<int:pid>")
def get_product(pid):
    db = get_db()
    row = db.execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
    if not row:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"id":row[0],"name":row[1],"price":row[2],"category":row[3],"stock":row[4]})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "product-service"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
