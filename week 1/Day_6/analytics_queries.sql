create table students (
student_id serial primary key,
name varchar (100) not null
);

create table marks(
mark_id SERIAL PRIMARY KEY,
student_id INT,
subject VARCHAR(50),
marks INT,
FOREIGN KEY (student_id) REFERENCES students (student_id)
);

insert into marks (student_id,subject , marks )
values
(1, 'English',85),
(1,'math',89),
(1,'science',92),

(2, 'English',80),
(2,'math',89),
(2,'science',78),

(3, 'English',72),
(3,'math',70),
(3,'science',74);

select * from students;
select * from marks;

insert into students (name)
values ('Anuj biswas'),
		('Akash yas'),
		('Rohan Gupta');

create table student_profiles (
student_id INT primary key,
address TEXT,
age INT,
phone varchar(15)

);


insert into student_profiles(student_id , address,age,phone)
Values (1,'Delhi,India',22,'9757645678'),
		(2,'Mumbai,India',34,'738293847'),
		(3,'Banglaore,India',23,'819293322');

Alter table student_profiles
add constraint fk_student_id
foreign key (student_id) 
references students(student_id);


Select * from students;
Select * from student_profiles;



select 
	s.student_id,
	s.name,
	sp.address,
	sp.age,
	sp.phone
From students s
join student_profiles sp
on s.student_id = sp.student_id;

-- Joins - joins are used to combine worws from two or more tables,
-- based on related column, usually a primary key in one table and 
-- a foreign key in another .
-- inner joins
select * from students s 
join marks m on s.student_id  = m.student_id;

-- left joins 
-- return all rows from left tabel , even if theres no match in the righ table 
select s.name , m.subject,m.marks from students s 
left join marks m on s.student_id  = m.student_id
where name  = 'Akash yas';

-- right joins
-- returns all rows from the right table , even is there;s no mathc in the left table 
select s.name , m.subject,m.marks from students s 
right join marks m on s.student_id  = m.student_id
where name  = 'Akash yas';

-- full joins
-- returns all rows from both tables, fills null for missing matches
select s.name , m.subject,m.marks from students s 
cross join marks m ;






-- Question
-- 1. Show each students name along with their subject and marks,
select s.name , m.subject,m.marks from students s 
join marks m on s.student_id  = m.student_id
where name  = 'Akash yas';



Create table products (
	product_id INT PRIMARY KEY,
	product_name VARCHAR(100),
	category TEXT,
	price numeric(10,2),
	stock_quantity INT,
	is_available BOOLEAN,
	added_on DATE

);

CREATE TABLE orders(
	order_id INT PRIMARY KEY,
	product_id INT,
	order_date DATE,
	Customer_name VARCHAR(50),
	payment_method VARCHAR(50),
	CONSTRAINT fk_product
		FOREIGN KEY (product_id)
		REFERENCES products(product_id)
		ON DELETE CASCADE
);

INSERT INTO products
(product_id, product_name, category, price, stock_quantity, is_available, added_on)
VALUES
(101, 'Wireless Mouse', 'Electronics', 1611.53, 79, FALSE, '2025-04-29'),
(102, 'Bluetooth Speaker', 'Electronics', 135.14, 23, TRUE, '2025-06-04'),
(103, 'Laptop Stand', 'Accessories', 1020.92, 161, FALSE, '2025-07-09'),
(104, 'USB-C Hub', 'Accessories', 408.39, 164, FALSE, '2025-05-12'),
(105, 'Notebook', 'Stationery', 1987.74, 116, TRUE, '2025-07-01'),
(106, 'Pen Set', 'Stationery', 1048.10, 150, TRUE, '2025-06-29'),
(107, 'Coffee Mug', 'Home & Kitchen', 1063.53, 76, FALSE, '2025-04-15'),
(108, 'LED Desk Lamp', 'Home & Kitchen', 239.10, 93, FALSE, '2025-05-23'),
(109, 'Yoga Mat', 'Fitness', 1514.86, 162, TRUE, '2025-05-05'),
(110, 'Water Bottle', 'Fitness', 420.99, 191, TRUE, '2025-05-09'),
(111, 'Smartphone', 'Electronics', 361.20, 200, FALSE, '2025-04-18'),
(112, 'Headphones', 'Electronics', 154.84, 178, TRUE, '2025-05-18'),
(113, 'Gaming Keyboard', 'Accessories', 103.24, 100, FALSE, '2025-04-19'),
(114, 'Monitor', 'Electronics', 305.20, 123, FALSE, '2025-05-20'),
(115, 'HDMI Cable', 'Accessories', 552.97, 105, TRUE, '2025-06-17'),
(116, 'Power Bank', 'Electronics', 831.88, 13, FALSE, '2025-07-01'),
(117, 'Backpack', 'Accessories', 1517.11, 64, TRUE, '2025-05-08'),
(118, 'Webcam', 'Electronics', 1428.30, 76, FALSE, '2025-06-11'),
(119, 'Desk Organizer', 'Home & Kitchen', 404.69, 136, FALSE, '2025-06-14'),
(120, 'Fitness Band', 'Fitness', 1451.69, 171, FALSE, '2025-05-06')
ON CONFLICT (product_id) DO NOTHING;



INSERT INTO orders
(order_id, product_id, order_date, customer_name, payment_method)
VALUES
(1, 120, '2025-06-26', 'Rohan', 'Cash on Delivery'),
(2, 116, '2025-06-21', 'Anjali', 'Cash on Delivery'),
(3, 101, '2025-06-23', 'Rohan', 'Credit Card'),
(4, 115, '2025-06-16', 'Akarsh', 'Credit Card'),
(5, 105, '2025-06-24', 'Simran', 'Credit Card'),
(6, 110, '2025-06-20', 'Simran', 'Credit Card'),
(7, 113, '2025-07-06', 'Anjali', 'Credit Card'),
(8, 106, '2025-06-30', 'Rohan', 'Credit Card'),
(9, 107, '2025-06-27', 'Anjali', 'Cash on Delivery'),
(10, 112, '2025-06-15', 'Meera', 'Cash on Delivery'),
(11, 105, '2025-07-07', 'Meera', 'Net Banking'),
(12, 110, '2025-06-13', 'Anjali', 'UPI'),
(13, 106, '2025-07-10', 'Simran', 'Credit Card'),
(14, 104, '2025-06-16', 'Akarsh', 'Net Banking'),
(15, 106, '2025-07-11', 'Anjali', 'Cash on Delivery'),
(16, 119, '2025-06-18', 'Akarsh', 'Cash on Delivery'),
(17, 111, '2025-07-05', 'Akarsh', 'Cash on Delivery'),
(18, 107, '2025-07-10', 'Anjali', 'Credit Card'),
(19, 119, '2025-06-27', 'Meera', 'Cash on Delivery'),
(20, 109, '2025-07-08', 'Akarsh', 'Credit Card')
ON CONFLICT (order_id) DO NOTHING;

select * from products
select * from orders


-- EXERCISE 
-- 1 Show each order long with the product name price.
select * from orders o inner join products p
on o.product_id = p.product_id;

select o.order_id , o.customer_name, p.product_name, p.price 
from orders o inner join products p
on o.product_id = p.product_id;

-- 2 show all products even if they were never ordered.

select o.order_id , p.product_name
from products p left join orders o
on o.product_id = p.product_id;

-- 3 show orders for only 'Electronics cateogory'.
select o.order_id, p.product_name,p.category
from orders o
join products p on o.product_id = p.product_id
where p.category = 'Electronics';

-- 4 list all orders sorted by product price (high to low)
select o.order_id, p.product_name , p.price
from orders o
join products p on o.product_id = p.product_id
ORDER by p.price DESC;

-- 5. show number of orders placed for each product
select p.product_name , count(o.order_id) as total_orders
from products p
left join orders o on p.product_id = o.product_id
group by p.product_name 

-- 6. show total revenue earned per product.
select p.product_name , SUM(o.quantity * p.price ) as revenue
from products p
left join orders o on p.product_id = o.product_id
group by p.product_name ;

-- 7. show products where total order revenue > 2000
select p.product_name , SUM(o.quantity * p.price ) as revenue
from products p
left join orders o on p.product_id = o.product_id
group by p.product_name 
having SUM(o.quantity * p.price ) > 2000;

-- 8 show unique customers who ordered 'Fitness' products.
select distinct o.customer_name 
from orders o 
join products p on o.product_id = p.product_id
where p.category = 'Fintess';





-- Many -to - many relationship 
-- one row in table a can be linked to many rows in table b.
-- and one row in table b can be inked to many rows in table a .

create table student(
student_id INT primary key,
student_name VARCHAR(100)
);

-- SAMPLE DATA
INSERT INTO student (student_id, student_name) Values
(1,'AKASH'),
(2,'ANUJ'),
(3,'ROHAN');

select * from student

create table courses (
course_id INT PRIMARY KEY,
course_name VARCHAR(100)
);
-- sample DATA
INSERT INTO courses (course_id,course_name) VALUES
(101,'python'),
(102,'SQL'),
(103,'Power BI')

select * from courses;

-- now in many to  many relationship we have to create
-- the juntion table 
CREATE TABLE student_courses (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

INSERT INTO student_courses (student_id, course_id)
VALUES
    (1, 102),
    (2, 101),
    (2, 103),
    (3, 102);

-- 1. show list of students with courses they are enrolled in.

SELECT
    s.student_name,
    c.course_name
FROM student_courses sc
JOIN student s
    ON sc.student_id = s.student_id
JOIN courses c
    ON sc.course_id = c.course_id;


-- 2 Find all the courses takedn by the stduent names 'Anuj'
SELECT
    c.course_name
FROM student_courses sc
JOIN student s
    ON sc.student_id = s.student_id
JOIN courses c
    ON sc.course_id = c.course_id
where 
	s.student_name = 'ANUJ';

-- 1. Views — Virtual Table
-- A VIEW is a saved SQL query that you can use like a table. It generally doesn't store the query's result data itself; 
-- it fetches data from the underlying tables when you query it.

-- Suppose you have three tables: students, courses, and student_courses.

-- Normally, to see which student enrolled in which course, you would write a JOIN query every time.

SELECT
    s.student_name,
    c.course_name
FROM student_courses sc
JOIN student s
    ON sc.student_id = s.student_id
JOIN courses c
    ON sc.course_id = c.course_id;

-- Instead, you can save this query as a view.
CREATE VIEW student_course_view AS
SELECT
    s.student_name,
    c.course_name
FROM student_courses sc
JOIN student s
    ON sc.student_id = s.student_id
JOIN courses c
    ON sc.course_id = c.course_id;

SELECT * FROM student_course_view;


-- Stored Procedures — Saved SQL Operations
-- A stored procedure is a named block of SQL code that you can execute when you want to perform a task. It can accept parameters and contain multiple SQL statements, conditions, and loops.

-- For example, suppose you frequently want to find a student's enrolled courses using their student ID.

-- In PostgreSQL, you can create a procedure like this:

-- Why use Stored Procedures?

-- - Reuse database operations.
-- - Perform multiple operations in one call.
-- - Apply business rules and validation.
-- - Manage transactions and automate repetitive database tasks.

CREATE PROCEDURE add_student(
    p_id INT,
    p_name VARCHAR(100)
)
LANGUAGE SQL
AS $$
    INSERT INTO students (student_id, student_name)
    VALUES (p_id, p_name);
$$;

CALL add_student(10, 'Anuj');