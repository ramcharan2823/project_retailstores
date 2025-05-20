import os
from datetime import datetime

class Billing:
    @staticmethod
    def generate_invoice(customer_id, product_id, quantity, total, tax, grand_total):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\store\reports\invoices"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            filename = f"invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            file_path = os.path.join(data_folder, filename)
            with open(file_path, "w") as file:
                file.write(f"Invoice Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Customer ID: {customer_id}\n")
                file.write(f"Product ID: {product_id}\n")
                file.write(f"Quantity: {quantity}\n")
                file.write(f"Subtotal: {total}\n")
                file.write(f"Tax (5%): {tax}\n")
                file.write(f"Grand Total: {grand_total}\n")
            
            print(f"Invoice generated and saved to {file_path}.")
        except Exception as e:
            print(f"Error generating invoice: {e}")
