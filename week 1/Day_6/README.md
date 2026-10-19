# Day 6 - SQL Relationships, Joins, and Analytics

Day 6 is a practical PostgreSQL lesson about connecting related tables and
answering business questions with SQL. The main practice file is
[`analytics_queries.sql`](./analytics_queries.sql).

By the end of this lesson, you should be able to:

- create tables with primary keys and foreign keys;
- insert and inspect related data;
- model one-to-one, one-to-many, and many-to-many relationships;
- use `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `CROSS JOIN`;
- filter, sort, group, and count joined data;
- understand how a junction table connects two entities; and
- translate a question into a SQL query and verify its result.

> **Database used:** PostgreSQL. The script uses `SERIAL`, `NUMERIC`, and
> PostgreSQL-style constraints. It is not a drop-in SQLite script.

## Contents

1. [How to run the lesson](#how-to-run-the-lesson)
2. [What is implemented](#what-is-implemented)
3. [Part 1: students, marks, and profiles](#part-1-students-marks-and-profiles)
4. [Part 2: products and orders](#part-2-products-and-orders)
5. [Part 3: many-to-many student enrolment](#part-3-many-to-many-student-enrolment)
6. [Expected outputs](#expected-outputs)
7. [Exercises to try](#exercises-to-try)
8. [Important notes about the current SQL file](#important-notes-about-the-current-sql-file)
9. [Quick revision](#quick-revision)

## How to run the lesson

### 1. Start PostgreSQL

Create a practice database if you do not already have one:

```bash
createdb day6_sql
psql -d day6_sql
```

Inside `psql`, confirm the connection:

```sql
\conninfo
```

### 2. Run the script in sections

The SQL file is a learning notebook rather than a single repeatable migration.
For the clearest results, copy and run one logical section at a time:

```bash
psql -d day6_sql -f "week 1/Day_6/analytics_queries.sql"
```

If you are running it for the first time, read
[the notes about execution order and known limitations](#important-notes-about-the-current-sql-file)
first. To inspect the created tables:

```sql
\dt
\d students
\d marks
\d products
\d orders
\d student_courses
```

To make a clean practice database between attempts:

```sql
DROP TABLE IF EXISTS student_courses, courses, student, orders,
    student_profiles, marks, students, products CASCADE;
```

## What is implemented

| Section | Tables | Main ideas |
| --- | --- | --- |
| Students and marks | `students`, `marks` | One-to-many relationship and joins |
| Student profiles | `student_profiles` | One-to-one relationship |
| Product ordering | `products`, `orders` | Foreign keys, product/order analysis |
| Course enrolment | `student`, `courses`, `student_courses` | Many-to-many relationship |

The script also demonstrates `SELECT *`, aliases, `WHERE`, `DISTINCT`,
`ORDER BY`, `COUNT`, `SUM`, `GROUP BY`, and `HAVING`.

## Part 1: students, marks, and profiles

### Students and marks

The first model stores a student once in `students` and stores each subject
mark as a separate row in `marks`:

```text
students (1) ───────────< marks
```

Important columns:

| Table | Column | Role |
| --- | --- | --- |
| `students` | `student_id` | Primary key |
| `students` | `name` | Required student name |
| `marks` | `mark_id` | Primary key |
| `marks` | `student_id` | Foreign key to `students` |
| `marks` | `subject`, `marks` | Subject result |

The seed data represents three students:

| `student_id` | `name` |
| ---: | --- |
| 1 | Anuj biswas |
| 2 | Akash yas |
| 3 | Rohan Gupta |

There are three marks for each student:

| Student | English | math | science |
| --- | ---: | ---: | ---: |
| Anuj biswas | 85 | 89 | 92 |
| Akash yas | 80 | 89 | 78 |
| Rohan Gupta | 72 | 70 | 74 |

### One-to-one student profiles

`student_profiles.student_id` is both a primary key and a foreign key. This
means one student can have at most one profile row:

```text
students (1) ─────────── (0..1) student_profiles
```

The profile data is:

| `student_id` | `address` | `age` | `phone` |
| ---: | --- | ---: | --- |
| 1 | Delhi,India | 22 | 9757645678 |
| 2 | Mumbai,India | 34 | 738293847 |
| 3 | Banglaore,India | 23 | 819293322 |

The profile join:

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

Expected output:

```text
 student_id |    name     |   address    | age |    phone
-------------+-------------+--------------+-----+------------
           1 | Anuj biswas | Delhi,India  |  22 | 9757645678
           2 | Akash yas   | Mumbai,India |  34 | 738293847
           3 | Rohan Gupta | Banglaore,India | 23 | 819293322
```

### Join demonstrations

The script demonstrates these join behaviors:

- **Inner join:** only rows with a matching student and mark.
- **Left join:** every student from the left table, including students with
  no marks.
- **Right join:** every mark from the right table, including marks whose
  student is not present (the foreign key normally prevents that case).
- **Cross join:** every possible student/mark combination. This can produce
  many rows and is different from a full outer join.

The query for Akash's marks returns:

```text
   name    | subject | marks
-----------+---------+-------
 Akash yas | English |    80
 Akash yas | math    |    89
 Akash yas | science |    78
```

## Part 2: products and orders

The second model connects each order to one product:

```text
products (1) ───────────< orders
```

### Product table

`products` contains 20 seeded products from these categories:

- Electronics
- Accessories
- Stationery
- Home & Kitchen
- Fitness

Each product has an ID, name, category, price, stock quantity, availability,
and date added. `product_id` is the primary key.

### Orders table

`orders` contains 20 seeded orders. Each order stores:

- `order_id`;
- `product_id`, a foreign key to `products`;
- `order_date`;
- `customer_name`; and
- `payment_method`.

The foreign key uses `ON DELETE CASCADE`, so deleting a product also deletes
orders that reference it. Use this behavior carefully in a real application.

### Implemented order-analysis queries

#### Show each order with product information

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

Example output:

```text
 order_id | customer_name |   product_name   |  price
----------+---------------+------------------+---------
        1 | Rohan         | Fitness Band     | 1451.69
        2 | Anjali        | Power Bank       | 831.88
        3 | Rohan         | Wireless Mouse   | 1611.53
```

The complete result contains one row per order (20 rows).

#### Show every product, including products with no order

```sql
SELECT
    p.product_id,
    p.product_name,
    o.order_id
FROM products AS p
LEFT JOIN orders AS o
    ON p.product_id = o.product_id
ORDER BY p.product_id;
```

This is a `LEFT JOIN`: a product with no matching order remains in the result
and its `order_id` is `NULL`.

#### Show only Electronics orders

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

Expected order IDs:

```text
2, 3, 10, 17
```

#### Sort orders by product price

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

The first three rows are:

| `order_id` | `product_name` | `price` |
| ---: | --- | ---: |
| 5 | Notebook | 1987.74 |
| 11 | Notebook | 1987.74 |
| 3 | Wireless Mouse | 1611.53 |

#### Count orders per product

```sql
SELECT
    p.product_name,
    COUNT(o.order_id) AS total_orders
FROM products AS p
LEFT JOIN orders AS o
    ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name
ORDER BY p.product_id;
```

The `LEFT JOIN` is important: it also reports products whose count is zero.

## Part 3: many-to-many student enrolment

A student can take many courses, and a course can have many students. A
junction table is required:

```text
student (1) ─────< student_courses >───── (1) courses
```

The composite primary key `(student_id, course_id)` prevents the same student
from being enrolled in the same course twice.

Seed enrolments:

| Student | Course |
| --- | --- |
| AKASH | SQL |
| ANUJ | python |
| ANUJ | Power BI |
| ROHAN | SQL |

### List every student and course

```sql
SELECT
    s.student_name,
    c.course_name
FROM student_courses AS sc
JOIN student AS s
    ON sc.student_id = s.student_id
JOIN courses AS c
    ON sc.course_id = c.course_id
ORDER BY s.student_id, c.course_id;
```

Expected output:

```text
 student_name | course_name
--------------+-------------
 AKASH        | SQL
 ANUJ         | python
 ANUJ         | Power BI
 ROHAN        | SQL
```

### Find Anuj's courses

```sql
SELECT c.course_name
FROM student_courses AS sc
JOIN student AS s
    ON sc.student_id = s.student_id
JOIN courses AS c
    ON sc.course_id = c.course_id
WHERE s.student_name = 'ANUJ'
ORDER BY c.course_id;
```

Expected output:

```text
 course_name
-------------
 python
 Power BI
```

## Expected outputs

Use these checkpoints to confirm that each section is working:

| Check | Expected result |
| --- | --- |
| Student count | 3 |
| Marks count | 9 |
| Profiles count | 3 |
| Product count | 20 |
| Order count | 20 |
| Electronics order IDs | 2, 3, 10, 17 |
| Enrolment count | 4 |
| ANUJ's courses | python, Power BI |

The exact display alignment can differ between terminals, but the values and
row counts should match.

## Exercises to try

1. Calculate the average mark for every student.
2. Find the student with the highest science mark.
3. Show students who have an average mark greater than 80.
4. Count orders for each payment method.
5. Find the most expensive product that was ordered.
6. List customers who ordered an Electronics product.
7. Show products that have never been ordered.
8. Count how many students are enrolled in each course.
9. Add a new course and enrol two students in it.
10. Try inserting a duplicate `(student_id, course_id)` pair and explain the
    primary-key error.

Example solution for exercise 1:

```sql
SELECT
    s.name,
    ROUND(AVG(m.marks), 2) AS average_mark
FROM students AS s
JOIN marks AS m
    ON s.student_id = m.student_id
GROUP BY s.student_id, s.name
ORDER BY average_mark DESC;
```

Expected averages:

| Student | Average |
| --- | ---: |
| Anuj biswas | 88.67 |
| Akash yas | 82.33 |
| Rohan Gupta | 72.00 |

## Important notes about the current SQL file

The source file is intentionally a practice notebook, but it should be read
with these details in mind:

1. The `marks` seed insert appears before the `students` seed insert. Because
   `marks.student_id` references `students.student_id`, create and populate
   `students` first, then insert marks.
2. The product/order revenue examples use `o.quantity`, but the current
   `orders` table does not define a `quantity` column. Those revenue queries
   will fail until `quantity` is added or revenue is calculated as
   `COUNT(o.order_id) * p.price`.
3. The query labelled “full join” is currently a `CROSS JOIN`. A true full
   outer join would use `FULL OUTER JOIN ... ON ...`.
4. The query that filters the Fitness category contains the spelling
   `'Fintess'`; it should be `'Fitness'` to return rows.
5. `question.sql` is currently empty. The exercises in this README are
   provided as the Day 6 practice questions until that file is populated.
6. Table names such as `student` and `students` are different tables. This is
   intentional in the script, but using consistent plural names would make a
   production schema easier to maintain.

These notes explain why running the complete file in one pass may not produce
every result shown above. They do not change the learning goals of the
examples.

## Quick revision

- A **primary key** identifies a row uniquely.
- A **foreign key** links a row to another table.
- A **one-to-many** relationship stores one parent row and many child rows.
- A **one-to-one** relationship uses a unique child key for each parent.
- A **many-to-many** relationship needs a junction table.
- `INNER JOIN` keeps matches only.
- `LEFT JOIN` keeps every row from the left table.
- `RIGHT JOIN` keeps every row from the right table.
- `CROSS JOIN` creates every combination of rows.
- `GROUP BY` creates groups for aggregate calculations.
- `HAVING` filters grouped results.

