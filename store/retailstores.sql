create database retailstores

use retailstores

create schema Tables;
go

create table products(
	product_id INT PRIMARY KEY,
	Name VARCHAR(100) NOT NULL,
	category VARCHAR(100) NOT NULL,
	price DECIMAL (10,2) NOT NULL,
	quantity INT NOT NULL
)

create table customers(
	customer_id INT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	phone VARCHAR(15) NOT NULL
)

create table sales(
	sale_id INT IDENTITY(1,1) PRIMARY KEY ,
	customer_id INT NOT NULL,
	product_id INT NOT NULL,
	quantity INT NOT NULL,
	sale_date DATE NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE ON UPDATE CASCADE
	)

--products
DECLARE @counter INT = 1;

-- Insert 400 products with sample data
WHILE @counter <= 400
BEGIN
    INSERT INTO products (product_id, Name, category, price, quantity)
    VALUES (
        @counter,  -- Product ID
        'Product ' + CAST(@counter AS VARCHAR(5)),  -- Product Name (Product 1, Product 2, ...)
        'Category ' + CAST((@counter % 10) + 1 AS VARCHAR(2)),  -- Category from Category 1 to Category 10
        CAST((RAND() * 100) AS DECIMAL(10,2)),  -- Random Price between 0 and 100
        FLOOR(RAND() * 100 + 1)  -- Random Quantity between 1 and 100
    );

    SET @counter = @counter + 1;
END



---for inserting customer records randomly
DECLARE @counter INT = 1;

WHILE @counter <= 400
BEGIN
    INSERT INTO Customers (customer_id, Name, Phone)
    VALUES (
        @counter, 
        'Customer ' + CAST(@counter AS VARCHAR(5)),  -- Generating a sample name (Customer 1, Customer 2, ...)
        -- Generate a random 10-digit number between 7000000000 and 9999999999
        '+91 ' + CAST((ABS(CHECKSUM(NEWID())) % 1000000000 + 7000000000) AS VARCHAR(10)) -- Start with 7 and generate 9 digits
    );

    SET @counter = @counter + 1;
END

---sales
DECLARE @counter INT = 1;

-- Insert 400 sales records with sample data
WHILE @counter <= 400
BEGIN
    INSERT INTO sales (customer_id, product_id, quantity, sale_date)
    VALUES (
        (ABS(CHECKSUM(NEWID())) % 400 + 1),  -- Random customer_id between 1 and 400
        (ABS(CHECKSUM(NEWID())) % 400 + 1),  -- Random product_id between 1 and 400
        FLOOR(RAND() * 10 + 1),  -- Random quantity between 1 and 10
        GETDATE()  -- Current date for sale_date
    );

    SET @counter = @counter + 1;
END


ALTER TABLE products
ALTER COLUMN product_id NVARCHAR(10);


select * from products
where name = 'ram'
select * from customers
select * from sales


drop table products

drop table customers

truncate table customers

truncate table products

truncate table sales

drop table sales





