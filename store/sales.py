import csv
import os
from billing import Billing
from decimal import Decimal
from datetime import datetime
from utils import input_int
from db_config import get_db_connection


class Sale:
    def __init__(self):
        self.conn = get_db_connection()

    def create_sale(self, customer_id, product_id, quantity):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT Price, quantity FROM Products WHERE Product_id=?", (product_id,))
            result = cursor.fetchone()
            if not result:
                print("Product not found.")
                return
            price, available_quantity = result

            price = Decimal(price)

            if quantity > available_quantity:
                print("Insufficient quantity.")
                return

            total = price * Decimal(quantity)
            tax = round(total * Decimal(0.05), 2)
            grand_total = total + tax

            cursor.execute("""
                INSERT INTO Sales (Customer_id, Product_id, quantity, sale_date)
                VALUES (?, ?, ?, ?)
            """, (customer_id, product_id, quantity, datetime.now()))

            cursor.execute("UPDATE products SET quantity = quantity - ? WHERE Product_id=?", (quantity, product_id))

            self.conn.commit()
            print(f"Sale recorded. Total with tax: {grand_total}")

            Billing.generate_invoice(customer_id, product_id, quantity, total, tax, grand_total)
        except Exception as e:
            print(f"Error creating sale: {e}")


    def daily_summary(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT CONVERT(date, sales.sale_date) AS SaleDate, SUM(products.price * sales.quantity) AS TotalSales
                FROM Sales
                JOIN Products ON sales.Product_id = products.Product_id
                GROUP BY CONVERT(date, sales.sale_date)
                ORDER BY CONVERT(date, sales.sale_date) DESC
            """)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"Date: {row[0]}, Total Sales: {row[1]:.2f}")
            else:
                print("No sales records found for the selected period.")

        except Exception as e:
            print(f"Error fetching daily summary: {e}")

    
    def monthly_summary(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT YEAR(sale_date) AS SaleYear, MONTH(sale_date) AS SaleMonth, SUM(products.price * sales.quantity) AS TotalSales
                FROM Sales
                JOIN Products ON sales.product_id = products.product_id
                GROUP BY YEAR(sale_date), MONTH(sale_date)
                ORDER BY SaleYear DESC, SaleMonth DESC
            """)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"Year: {row[0]}, Month: {row[1]}, Total Sales: {row[2]:.2f}")
            else:
                print("No sales records found for the selected period.")

        except Exception as e:
            print(f"Error fetching monthly summary: {e}")


    def export_sales_csv(self):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\store\data"

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Sales")
            rows = cursor.fetchall()

            file_path = os.path.join(data_folder, "sales.csv")

            with open(file_path, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([column[0] for column in cursor.description])
                writer.writerows(rows)
            print(f"Sales exported to {file_path}.")
        except Exception as e:
            print(f"Error exporting sales CSV: {e}")

    def alert_low_quantity(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM products WHERE quantity < 5")
            for row in cursor.fetchall():
                print(f"Low quantity alert: {row}")
        except Exception as e:
            print(f"Error checking low quantity: {e}")

    def view_sales(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Sales")
            sales = cursor.fetchall()
            if sales:
                for sale in sales:
                    print(sale)  
            else:
                print("No sales records found.")
        except Exception as e:
            print(f"Error viewing sales: {e}")

    def search_sales(self, keyword):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM Sales 
                WHERE Customer_id LIKE ? OR Product_id LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)  
            else:
                print("No matching sales found.")
        except Exception as e:
            print(f"Error searching sales: {e}")

    def record_sale(self, customer_id, product_id, quantity):
        self.create_sale(customer_id, product_id, quantity)
