import csv
import os
from utils import input_int
from db_config import get_db_connection

class Product:
    def __init__(self):
        self.conn = get_db_connection()

    
    def is_product_exists(self, product_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Products WHERE Product_id = ?", (product_id,))
            result = cursor.fetchone()[0]
            return result > 0 
        except Exception as e:
            print(f"Error checking product existence: {e}")
            return False

    def generate_product_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Products")
            count = cursor.fetchone()[0] + 1
            return count
        except Exception as e:
            print(f"Error generating product ID: {e}")
            return None

    def add_product(self, name, category, price, quantity):
        try:
            product_id = self.generate_product_id()
            if product_id is None:
                return
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Products (Product_id, Name, category, price, quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, name, category, price, quantity))
            self.conn.commit()
            print("Product added successfully.")
        except Exception as e:
            print(f"Error adding product: {e}")

    def view_products(self, page=1, page_size=10):
        try:
            cursor = self.conn.cursor()
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM Products ORDER BY product_id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY", (offset, page_size))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No products on this page.")
        except Exception as e:
            print(f"Error viewing products: {e}")

    def update_product(self, product_id, quantity):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Products SET quantity=? WHERE product_id=?", (quantity, product_id))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating product: {e}")

    def delete_product(self, product_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Products WHERE product_id=?", (product_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting product: {e}")

    def search_product(self, keyword):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM Products
                WHERE Name LIKE ? OR category LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("No matching products found.")
        except Exception as e:
            print(f"Error searching product: {e}")

    def export_products_csv(self):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\store\data"

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Products")
            rows = cursor.fetchall()

            file_path = os.path.join(data_folder, "products.csv")

            with open(file_path, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([column[0] for column in cursor.description])
                writer.writerows(rows)
            print(f"Products exported to {file_path}.")
        except Exception as e:
            print(f"Error exporting products CSV: {e}")

    def import_products_csv(self, filename):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\store\data"

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            file_path = os.path.join(data_folder, filename)

            cursor = self.conn.cursor()
            with open(file_path, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cursor.execute("""
                        INSERT INTO Products (product_id, Name, category, quantity, price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (row['product_id'], row['Name'], row['category'], int(row['quantity']), float(row['price'])))
            self.conn.commit()
            print(f"Products imported from {file_path}.")
        except Exception as e:
            print(f"Error importing products from CSV: {e}")

    def update_product_details(self, product_id, name=None, category=None, price=None, quantity=None):
        try:
            cursor = self.conn.cursor()
            update_fields = []
            update_values = []

            if name:
                update_fields.append("Name = ?")
                update_values.append(name)
            if category:
                update_fields.append("Category = ?")
                update_values.append(category)
            if price is not None:  
                update_fields.append("price = ?")
                update_values.append(price)
            if quantity is not None: 
                update_fields.append("Quantity = ?")
                update_values.append(quantity)

            if not update_fields:
                print("No fields to update.")
                return
            
            query = f"UPDATE Products SET {', '.join(update_fields)} WHERE Product_id = ?"
            update_values.append(product_id)

            cursor.execute(query, tuple(update_values)) 
            self.conn.commit()
            print("Product updated successfully.")
        except Exception as e:
            print(f"Error updating product: {e}")
