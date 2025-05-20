import csv
import os
import re
from utils import input_int
from db_config import get_db_connection

class Customer:
    def __init__(self):
        self.conn = get_db_connection()

    def generate_customer_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(customer_id) FROM Customers")
            result = cursor.fetchone()
            if result[0] is None:
                return 1
            #max_id = result[0] 
            next_id = result[0]+1
            #return f"C{next_id:05}"
            return next_id
        except Exception as e:
            print(f"Error generating customer ID: {e}")
            return None
        
    
    def is_valid_name(self, name):
        if isinstance(name, str) and name.strip() != "":
            if re.search(r'\d', name): 
                return False
            return True
        return False
    
    def is_valid_phone(self, phone):
        phone = phone.strip()
        if phone.startswith('+91 ') and len(phone) == 14 and phone[4:].isdigit():
            return True
        return False
    
    def format_phone(self, phone):
        if phone.startswith("+91"):
            return phone
        else:
            return "+91" + phone

    def add_customer(self, name, phone):

        if not self.is_valid_name(name):
            print("Name must be a non-empty string.")
            return
        if not self.is_valid_phone(phone):
            print("Phone number must be a valid 10-digit number.")
            return
        
        phone = self.format_phone(phone)
        try:
            customer_id = self.generate_customer_id()
            if customer_id is None:
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Customers (customer_id, name, phone) VALUES (?, ?, ?)",
                           (customer_id, name, phone))
            self.conn.commit()
            print(f"Customer with ID {customer_id} added successfully.")
        except Exception as e:
            if '23000' in str(e):  # SQL Server duplicate key error code
                print(f"Error adding customer: Customer ID {customer_id} already exists.")
            else:
                print(f"Error adding customer: {e}")
    

    def view_customers(self, page=1, page_size=10):
        try:
            cursor = self.conn.cursor()
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM customers ORDER BY customer_id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY", (offset, page_size))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No products on this page.")
        except Exception as e:
            print(f"Error viewing products: {e}")

    def update_customer(self, customer_id, name=None, phone=None):
        try:
            cursor = self.conn.cursor()
            # Fetch current data
            cursor.execute("SELECT name, phone FROM Customers WHERE customer_id=?", (customer_id,))
            result = cursor.fetchone()
            if not result:
                print("Customer not found.")
                return
            
            current_name, current_phone = result
            new_name = name if name else current_name
            new_phone = phone if phone else current_phone

            if phone and not self.is_valid_phone(phone):
                print("Error: Phone number must be a valid 10-digit number.")
                return

            if phone:
                new_phone = self.format_phone(new_phone)

            cursor.execute("""
                UPDATE Customers
                SET name = ?, phone = ?
                WHERE customer_id = ?
            """, (new_name, new_phone, customer_id))
            self.conn.commit()
            print("Customer updated.")
        except Exception as e:
            print(f"Error updating customer: {e}")

    def delete_customer(self, customer_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Customers WHERE customer_id=?", (customer_id,))
            self.conn.commit()
            print("Customer deleted.")
        except Exception as e:
            print(f"Error deleting customer: {e}")

    def search_customer(self, keyword):
        try:
            cursor = self.conn.cursor()
            search_term = f"%{keyword}%"
            cursor.execute("""
                SELECT * FROM Customers
                WHERE customer_id LIKE ? OR name LIKE ? OR phone LIKE ?
            """, (search_term, search_term, search_term))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("No customers found.")
        except Exception as e:
            print(f"Error searching customer: {e}")

    def export_customers_csv(self):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\store\data"

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Customers")
            rows = cursor.fetchall()

            file_path = os.path.join(data_folder, "customers.csv")

            with open(file_path, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([column[0] for column in cursor.description])  # headers
                writer.writerows(rows)
            print(f"Customers exported to {file_path}.")
        except Exception as e:
            print(f"Error exporting customers CSV: {e}")

    def import_customers_csv(self, filename):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\store\data"

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            file_path = os.path.join(data_folder, filename)

            cursor = self.conn.cursor()
            with open(file_path, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customer_id = row['customer_id']
                    name = row['name']
                    phone = row['phone']

                    if not self.is_valid_phone(phone):
                        print(f"Invalid phone number format for {name}. Skipping row.")
                        continue
                    cursor.execute("SELECT COUNT(*) FROM Customers WHERE customer_id = ?", (customer_id,))
                    if cursor.fetchone()[0] > 0:
                        print(f"Customer ID {customer_id} already exists. Skipping.")
                        continue

                    cursor.execute("""
                        INSERT INTO Customers (customer_id, name, phone)
                        VALUES (?, ?, ?)
                    """, (customer_id, name, phone))

            self.conn.commit()
            print(f"Customers imported from {file_path}.")
        except Exception as e:
            print(f"Error importing customers from CSV: {e}")

    
