# SQL Learning Guide

This guide uses **PostgreSQL** syntax. It covers:

1. Creating a products table
2. Inserting sample data
3. Basic `SELECT` queries
4. Filtering, grouping, sorting, and aggregate functions
5. One-to-one, one-to-many, and many-to-many relationships
6. Joins, views, and stored procedures

> **Important:** Commands such as `SERIAL`, `BOOLEAN`, `NOW()`, and
> `LANGUAGE plpgsql` are PostgreSQL-specific. They will not run unchanged in
> SQLite.

---

## 1. Products Table

### 1.1 Create the table

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sku_code CHAR(8) UNIQUE NOT NULL,
    price NUMERIC(10, 2) CHECK (price > 0),
    stock_quantity INT DEFAULT 0 CHECK (stock_quantity >= 0),
    is_available BOOLEAN DEFAULT TRUE,
    category TEXT NOT NULL,
    added_on DATE DEFAULT CURRENT_DATE,
    last_updated TIMESTAMP DEFAULT NOW()
);
```

### What the important constraints mean

| Constraint | Meaning |
| --- | --- |
| `PRIMARY KEY` | Uniquely identifies each row |
| `NOT NULL` | The column must contain a value |
| `UNIQUE` | Duplicate values are not allowed |
| `DEFAULT` | Provides a value when one is not supplied |
| `CHECK` | Rejects values that do not satisfy a condition |

### 1.2 Insert sample data

```sql
INSERT INTO products (
    name,
    sku_code,
    price,
    stock_quantity,
    is_available,
    category
)
VALUES
    ('Wireless Mouse', 'WM123456', 699.99, 50, TRUE, 'Electronics'),
    ('Bluetooth Speaker', 'BS234567', 1499.00, 30, TRUE, 'Electronics'),
    ('Laptop Stand', 'LS345678', 799.50, 20, TRUE, 'Accessories'),
    ('USB-C Hub', 'UC456789', 1299.99, 15, TRUE, 'Accessories'),
    ('Notebook', 'NB567890', 99.99, 100, TRUE, 'Stationery'),
    ('Pen Set', 'PS678901', 199.00, 200, TRUE, 'Stationery'),
    ('Coffee Mug', 'CM789012', 299.00, 75, TRUE, 'Home & Kitchen'),
    ('LED Desk Lamp', 'DL890123', 899.00, 40, TRUE, 'Home & Kitchen'),
    ('Yoga Mat', 'YM901234', 499.00, 25, TRUE, 'Fitness'),
    ('Water Bottle', 'WB012345', 349.00, 60, TRUE, 'Fitness');
```

---

## 2. Basic Queries

### Q1. Show the name and price of every product

```sql
SELECT name, price
FROM products;
```

### Q2. Show all electronics products

```sql
SELECT *
FROM products
WHERE category = 'Electronics';
```

### Q3. Show unique categories

`DISTINCT` removes duplicate values.

```sql
SELECT DISTINCT category
FROM products;
```

### Q4. Rename columns in the result

```sql
SELECT
    name AS item_name,
    price AS item_price
FROM products;
```

### Q5. Sort products from cheapest to most expensive

```sql
SELECT *
FROM products
ORDER BY price ASC;
```

Use `DESC` for descending order:

```sql
SELECT *
FROM products
ORDER BY price DESC;
```

### Q6. Show only the first three products

```sql
SELECT *
FROM products
LIMIT 3;
```

### Q7. Filter using multiple conditions

```sql
SELECT name, stock_quantity
FROM products
WHERE is_available = TRUE
  AND stock_quantity > 50
  AND price <> 299.00;
```

`<>` means "not equal to". PostgreSQL also accepts `!=`.

### Q8. Filter using a list of values

```sql
SELECT name, category, price
FROM products
WHERE category IN ('Home & Kitchen', 'Fitness');
```

---

## 3. Grouping and Aggregate Functions

Aggregate functions calculate a result from multiple rows:

| Function | Purpose |
| --- | --- |
| `COUNT()` | Counts rows |
| `SUM()` | Adds values |
| `AVG()` | Calculates an average |
| `MIN()` | Finds the smallest value |
| `MAX()` | Finds the largest value |

### Q1. Count products in each category

```sql
SELECT
    category,
    COUNT(*) AS product_count
FROM products
GROUP BY category;
```

### Q2. Show categories with more than one product

`HAVING` filters groups after `GROUP BY`.

```sql
SELECT
    category,
    COUNT(*) AS product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 1;
```

### Q3. Find the average price of selected categories

```sql
SELECT
    category,
    AVG(price) AS average_price
FROM products
WHERE category IN ('Home & Kitchen', 'Fitness')
GROUP BY category;
```

### Q4. Find the most expensive product price in each category

```sql
SELECT
    category,
    MAX(price) AS highest_price
FROM products
GROUP BY category;
```

### Q5. Find the cheapest product in the entire table

```sql
SELECT name, price
FROM products
WHERE price = (
    SELECT MIN(price)
    FROM products
);
```

### Q6. Display categories in uppercase, sorted descending

```sql
SELECT DISTINCT
    UPPER(category) AS category_upper
FROM products
ORDER BY category_upper DESC;
```

---

## 4. One-to-One Relationship: Students and Profiles

In a one-to-one relationship, one student has at most one profile.
The profile's `student_id` is both its primary key and a foreign key.

### 4.1 Create the tables

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE student_profiles (
    student_id INT PRIMARY KEY,
    address TEXT,
    age INT,
    phone VARCHAR(15),
    CONSTRAINT fk_student_profile
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
);
```

### 4.2 Insert data

```sql
INSERT INTO students (name)
VALUES
    ('Akarsh Vyas'),
    ('Simran Mehta'),
    ('Rohan Gupta');

INSERT INTO student_profiles (student_id, address, age, phone)
VALUES
    (1, 'Delhi, India', 22, '9999999999'),
    (2, 'Mumbai, India', 21, '8888888888'),
    (3, 'Bangalore, India', 23, '7777777777');
```

### 4.3 Join students with their profiles

```sql
SELECT
    s.student_id,
    s.name,
    sp.address,
    sp.age,
    sp.phone
FROM students AS s
JOIN student_profiles AS sp
    ON s.student_id = sp.student_id;
```

---

## 5. One-to-Many Relationship: Students and Marks

In a one-to-many relationship, one student can have many marks records.

### 5.1 Create the tables and insert data

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    subject VARCHAR(50) NOT NULL,
    marks INT CHECK (marks BETWEEN 0 AND 100),
    CONSTRAINT fk_marks_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
);

INSERT INTO students (name)
VALUES
    ('Akarsh Vyas'),
    ('Simran Mehta'),
    ('Rohan Gupta');

INSERT INTO marks (student_id, subject, marks)
VALUES
    (1, 'English', 85),
    (1, 'Math', 89),
    (1, 'Science', 92),
    (2, 'English', 80),
    (2, 'Math', 75),
    (2, 'Science', 78),
    (3, 'English', 72),
    (3, 'Math', 70),
    (3, 'Science', 74);
```

### 5.2 Display every student's marks

```sql
SELECT
    s.name,
    m.subject,
    m.marks
FROM students AS s
JOIN marks AS m
    ON s.student_id = m.student_id
ORDER BY s.student_id, m.subject;
```

---

## 6. One-to-Many Relationship: Products and Orders

One product can appear in many orders. The `orders.product_id` foreign key
connects each order to a product.

### 6.1 Create the tables

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(10, 2) CHECK (price > 0),
    stock_quantity INT CHECK (stock_quantity >= 0),
    is_available BOOLEAN DEFAULT TRUE,
    added_on DATE DEFAULT CURRENT_DATE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT CHECK (quantity > 0),
    order_date DATE DEFAULT CURRENT_DATE,
    customer_name VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50),
    CONSTRAINT fk_order_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);
```

### 6.2 Useful order queries

#### Q1. Show each order with the product name and price

```sql
SELECT
    o.order_id,
    o.customer_name,
    p.product_name,
    p.price
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id;
```

#### Q2. Show every product, including products with no orders

`LEFT JOIN` keeps all rows from the left table.

```sql
SELECT
    p.product_name,
    o.order_id
FROM products AS p
LEFT JOIN orders AS o
    ON p.product_id = o.product_id;
```

#### Q3. Show orders for electronics products

```sql
SELECT
    o.order_id,
    p.product_name,
    p.category
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
WHERE p.category = 'Electronics';
```

#### Q4. Sort orders by product price, highest first

```sql
SELECT
    o.order_id,
    p.product_name,
    p.price
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
ORDER BY p.price DESC;
```

#### Q5. Count orders for each product

```sql
SELECT
    p.product_name,
    COUNT(o.order_id) AS total_orders
FROM products AS p
LEFT JOIN orders AS o
    ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name;
```

#### Q6. Calculate total revenue for each product

Revenue = `quantity × price`.

```sql
SELECT
    p.product_name,
    SUM(o.quantity * p.price) AS total_revenue
FROM products AS p
JOIN orders AS o
    ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name;
```

#### Q7. Show products with revenue greater than ₹2,000

```sql
SELECT
    p.product_name,
    SUM(o.quantity * p.price) AS total_revenue
FROM products AS p
JOIN orders AS o
    ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name
HAVING SUM(o.quantity * p.price) > 2000;
```

#### Q8. Find unique customers who ordered fitness products

```sql
SELECT DISTINCT o.customer_name
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
WHERE p.category = 'Fitness';
```

---

## 7. Many-to-Many Relationship: Students and Courses

In a many-to-many relationship:

- One student can take many courses.
- One course can have many students.
- `student_courses` is the junction table.

### 7.1 Create the tables

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL
);

CREATE TABLE student_courses (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

### 7.2 Insert sample mapping data

```sql
INSERT INTO student_courses (student_id, course_id)
VALUES
    (1, 101),
    (1, 102),
    (2, 101),
    (2, 103),
    (3, 102);
```

### 7.3 Show student and course names

```sql
SELECT
    s.student_name,
    c.course_name
FROM student_courses AS sc
JOIN students AS s
    ON sc.student_id = s.student_id
JOIN courses AS c
    ON sc.course_id = c.course_id;
```

### 7.4 List all courses taken by Simran

```sql
SELECT c.course_name
FROM student_courses AS sc
JOIN students AS s
    ON sc.student_id = s.student_id
JOIN courses AS c
    ON sc.course_id = c.course_id
WHERE s.student_name = 'Simran';
```

---

## 8. Views

A view is a saved query. It behaves like a virtual table and does not usually
store a separate copy of the data.

### 8.1 Available fitness products

```sql
CREATE VIEW available_fitness_products AS
SELECT
    product_id,
    name,
    price,
    stock_quantity
FROM products
WHERE category = 'Fitness'
  AND is_available = TRUE;
```

Use the view:

```sql
SELECT *
FROM available_fitness_products;
```

### 8.2 Low-stock products

```sql
CREATE VIEW low_stock_products AS
SELECT
    name,
    category,
    stock_quantity
FROM products
WHERE stock_quantity < 30;
```

---

## 9. Stored Procedure

Stored procedures contain reusable database logic. The following procedure
adds a product and prints a success message.

```sql
CREATE OR REPLACE PROCEDURE add_product(
    p_name VARCHAR,
    p_sku CHAR(8),
    p_price NUMERIC,
    p_qty INT,
    p_category TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO products (
        name,
        sku_code,
        price,
        stock_quantity,
        category
    )
    VALUES (
        p_name,
        p_sku,
        p_price,
        p_qty,
        p_category
    );

    RAISE NOTICE 'Product added successfully!';
END;
$$;
```

Call the procedure:

```sql
CALL add_product(
    'Mechanical Keyboard',
    'MK345678',
    2499.00,
    10,
    'Electronics'
);
```

---

## 10. Quick Revision

| Keyword | Use |
| --- | --- |
| `SELECT` | Read data |
| `WHERE` | Filter rows |
| `DISTINCT` | Remove duplicates |
| `ORDER BY` | Sort results |
| `GROUP BY` | Create groups |
| `HAVING` | Filter groups |
| `JOIN` | Combine related tables |
| `LEFT JOIN` | Keep every row from the left table |
| `INSERT` | Add data |
| `CREATE VIEW` | Save a query as a virtual table |
| `FOREIGN KEY` | Connect tables |

### Query execution order

SQL is generally processed in this logical order:

```text
FROM / JOIN
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT
```
