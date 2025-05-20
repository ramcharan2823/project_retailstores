from products import Product
from customers import Customer
from sales import Sale
from utils import input_int, input_float, confirm

def product_menu():
    product = Product()
    while True:
        print("\n--- Product Menu ---")
        print("1. Add product")
        print("2. View products")
        print("3. Update product stock")
        print("4. Delete product")
        print("5. Search product")
        print("6. Export products to CSV")
        print("7. Import products from CSV")
        print("0. Back to main menu")

        try:
            choice = input_int("Choose an option: ", 0, 7)

            if choice == 1:
                name = input("Product name: ")
                category = input("Category: ")
                stock = input_int("Stock quantity: ", 0)
                price = input_float("Price: ", 0)
                product.add_product(name, category, stock, price)

            elif choice == 2:
                page = 1
                while True:
                    product.view_products(page=page)
                    nav = input("N-next page, P-previous page, Q-quit: ").lower()
                    if nav == 'n':
                        page += 1
                    elif nav == 'p' and page > 1:
                        page -= 1
                    elif nav == 'q':
                        break
                    else:
                        print("Invalid option.")

            elif choice == 3:
                pid = input("Product ID to update stock: ")

                if not product.is_product_exists(pid):
                    print(f"Error: Product with ID {pid} does not exist.")
                    continue
                while True:
                    print("\nSelect the field to update:")
                    print("1. Name")
                    print("2. Category")
                    print("3. Price")
                    print("4. Quantity")
                    print("0. Done")

                    field_choice = input_int("Your choice: ", 0, 4)

                    if field_choice == 0:
                        break
                    elif field_choice == 1:
                        name = input("New name: ")
                        product.update_product_details(pid, name=name)
                    elif field_choice == 2:
                        category = input("New category: ")
                        product.update_product_details(pid, category=category)
                    elif field_choice == 3:
                        price = input_float("New price: ", 0)
                        product.update_product_details(pid, price=price)
                    elif field_choice == 4:
                        quantity = input_int("New quantity: ", 0)
                        product.update_product_details(pid, quantity=quantity)

                
                print("Product details updated.")
                #break

            elif choice == 4:
                pid = input("Product ID to delete: ")
                if not product.is_product_exists(pid):
                    print(f"Error: Product with ID {pid} does not exist.")
                    continue
                if confirm("Are you sure you want to delete this product? (y/n): "):
                    product.delete_product(pid)
                    print("Product deleted.")

            elif choice == 5:
                keyword = input("Enter search keyword: ")
                product.search_product(keyword)

            elif choice == 6:
                product.export_products_csv()

            elif choice == 7:
                filename = input("Enter CSV filename to import: ")
                product.import_products_csv(filename)

            elif choice == 0:
                break

        except Exception as e:
            print(f"Error: {e}")

def customer_menu():
    customer = Customer()
    while True:
        print("\n--- Customer Menu ---")
        print("1. Add customer")
        print("2. View customers")
        print("3. Update customer")
        print("4. Delete customer")
        print("5. Search customer")
        print("6. export customers to csv")
        print("7. import customers from csv")
        print("0. Back to main menu")

        try:
            choice = input_int("Choose an option: ", 0, 7)

            if choice == 1:
                name = input("Customer name: ")
                phone = input("Phone: ")
                customer.add_customer(name, phone)

            elif choice == 2:
                page = 1
                while True:
                    customer.view_customers(page=page)
                    nav = input("N-next page, P-previous page, Q-quit: ").lower()
                    if nav == 'n':
                        page += 1
                    elif nav == 'p' and page > 1:
                        page -= 1
                    elif nav == 'q':
                        break
                    else:
                        print("Invalid option.")
                

            elif choice == 3:
                cid = input("Customer ID to update: ")
                cursor = customer.conn.cursor()
                cursor.execute("SELECT 1 FROM Customers WHERE customer_id=?", (cid,))
                if cursor.fetchone() is None:
                    print("Customer ID does not exist.")
                else:
                    name = input("New name (leave blank to keep unchanged): ")
                    phone = input("New phone (leave blank to keep unchanged): ")
                    customer.update_customer(cid, name, phone)

            elif choice == 4:
                cid = input("Customer ID to delete: ")
                cursor = customer.conn.cursor()
                cursor.execute("SELECT 1 FROM Customers WHERE customer_id=?", (cid,))
                if cursor.fetchone() is None:
                    print("Customer ID does not exist.")
                else:
                    if confirm("Are you sure you want to delete this customer? (y/n): "):
                        customer.delete_customer(cid)
                print("Customer deleted.")

            elif choice == 5:
                keyword = input("Enter search keyword: ")
                customer.search_customer(keyword)

            elif choice == 6:
                customer.export_customers_csv()

            elif choice == 7:
                filename = input("Enter CSV filename to import: ")
                customer.import_customers_csv(filename)

            elif choice == 0:
                break

        except Exception as e:
            print(f"Error: {e}")

def sale_menu():
    sale = Sale()
    while True:
        print("\n--- Sales Menu ---")
        print("1. Record a sale")
        print("2. View sales")
        print("3. Search sales")
        print("4. export sales to csv")
        print("5. Alert: Low stock products")
        print("6. View daily sales summary")
        print("7. View monthly sales summary")
        print("0. Back to main menu")

        try:
            choice = input_int("Choose an option: ", 0, 7)

            if choice == 1:
                customer_id = input("Customer ID: ")
                product_id = input("Product ID: ")
                quantity = input_int("Quantity: ", 1)
                sale.record_sale(customer_id, product_id, quantity)

            elif choice == 2:
                sale.view_sales()

            elif choice == 3:
                keyword = input("Enter search keyword (customer name/product ID): ")
                sale.search_sales(keyword)

            elif choice == 4:
                sale.export_sales_csv()

            elif choice == 5:
                sale.alert_low_quantity()

            elif choice == 6:
                sale.daily_summary()

            elif choice == 7:
                sale.monthly_summary()

            elif choice == 0:
                break

        except Exception as e:
            print(f"Error: {e}")

def main():
    while True:
        print("\n=== Inventory Management CLI ===")
        print("1. Manage Products")
        print("2. Manage Customers")
        print("3. Manage Sales")
        print("0. Exit")

        try:
            choice = input_int("Choose an option: ", 0, 3)

            if choice == 1:
                product_menu()
            elif choice == 2:
                customer_menu()
            elif choice == 3:
                sale_menu()
            elif choice == 0:
                print("Goodbye!")
                break

        except Exception as e:
            print(f"Main Menu Error: {e}")

if __name__ == "__main__":
    main()
