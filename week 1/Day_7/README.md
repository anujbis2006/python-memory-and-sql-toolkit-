# Day 7 - SQL `CASE` Expressions

Day 7 introduces SQL `CASE` expressions. A `CASE` expression is SQL's
if/else-style tool: it checks a value or condition and returns a label or
calculated result.

The examples are in [`profile.sql`](./profile.sql) and use PostgreSQL syntax.

## Contents

1. [How to run the file](#how-to-run-the-file)
2. [Sample data](#sample-data)
3. [Simple CASE expression](#simple-case-expression)
4. [Searched CASE expression](#searched-case-expression)
5. [CASE in ORDER BY](#case-in-order-by)
6. [Subqueries](#subqueries)
7. [Expected outputs](#expected-outputs)
8. [Simple versus searched CASE](#simple-versus-searched-case)
9. [Practice questions](#practice-questions)

## How to run the file

Create a PostgreSQL database and execute the script:

```bash
createdb day7_sql
psql -d day7_sql -f "week 1/Day_7/profile.sql"
```

The file begins with `DROP TABLE IF EXISTS profiles`, so it can be rerun
while practising. That statement deletes the previous practice table and its
data; do not use it against a table containing important data.

To open an interactive PostgreSQL prompt instead:

```bash
psql -d day7_sql
```

Then run:

```sql
\i 'week 1/Day_7/profile.sql'
```

## Sample data

The script creates a `profiles` table with:

| Column | Meaning |
| --- | --- |
| `profile_id` | Automatically generated primary key |
| `full_name` | Profile owner's name |
| `city` | Profile city |
| `age` | Age, greater than zero |
| `account_status` | `active`, `inactive`, or `pending` |
| `score` | Number from 0 to 100 |

The five sample rows are:

| ID | Name | City | Age | Status | Score |
| ---: | --- | --- | ---: | --- | ---: |
| 1 | Anuj Biswas | Delhi | 22 | active | 92 |
| 2 | Akash Yas | Mumbai | 34 | inactive | 68 |
| 3 | Rohan Gupta | Bangalore | 17 | active | 81 |
| 4 | Simran Kaur | Pune | 45 | pending | 55 |
| 5 | Meera Shah | Kolkata | 29 | active | 39 |

## Simple CASE expression

A **simple `CASE`** compares one expression with several possible values:

```sql
CASE expression
    WHEN value_1 THEN result_1
    WHEN value_2 THEN result_2
    ELSE default_result
END
```

In this lesson, the expression is `account_status`:

```sql
SELECT
    full_name,
    account_status,
    CASE account_status
        WHEN 'active' THEN 'Account is active'
        WHEN 'inactive' THEN 'Account is inactive'
        WHEN 'pending' THEN 'Account is waiting for review'
        ELSE 'Unknown account status'
    END AS status_message
FROM profiles
ORDER BY profile_id;
```

The query compares `account_status` with exact values. It does not use
greater-than or less-than conditions.

Expected output:

| Name | Status | `status_message` |
| --- | --- | --- |
| Anuj Biswas | active | Account is active |
| Akash Yas | inactive | Account is inactive |
| Rohan Gupta | active | Account is active |
| Simran Kaur | pending | Account is waiting for review |
| Meera Shah | active | Account is active |

`ELSE` is the fallback. If `ELSE` is omitted and no `WHEN` matches, PostgreSQL
returns `NULL`.

## Searched CASE expression

A **searched `CASE`**, also called a conditional `CASE`, checks complete
Boolean conditions:

```sql
CASE
    WHEN condition_1 THEN result_1
    WHEN condition_2 THEN result_2
    ELSE default_result
END
```

### Classify profiles by age

```sql
SELECT
    full_name,
    age,
    CASE
        WHEN age < 18 THEN 'Minor'
        WHEN age BETWEEN 18 AND 30 THEN 'Young adult'
        WHEN age BETWEEN 31 AND 60 THEN 'Adult'
        ELSE 'Senior'
    END AS age_group
FROM profiles
ORDER BY profile_id;
```

Expected output:

| Name | Age | `age_group` |
| --- | ---: | --- |
| Anuj Biswas | 22 | Young adult |
| Akash Yas | 34 | Adult |
| Rohan Gupta | 17 | Minor |
| Simran Kaur | 45 | Adult |
| Meera Shah | 29 | Young adult |

### Classify profiles by score

Conditions are evaluated from top to bottom, and the first true condition
wins:

```sql
SELECT
    full_name,
    score,
    CASE
        WHEN score >= 80 THEN 'Excellent'
        WHEN score >= 60 THEN 'Good'
        WHEN score >= 40 THEN 'Needs improvement'
        ELSE 'Poor'
    END AS performance
FROM profiles
ORDER BY score DESC;
```

Expected output:

| Name | Score | `performance` |
| --- | ---: | --- |
| Anuj Biswas | 92 | Excellent |
| Rohan Gupta | 81 | Excellent |
| Akash Yas | 68 | Good |
| Simran Kaur | 55 | Needs improvement |
| Meera Shah | 39 | Poor |

The order of conditions matters. For example, if `score >= 60` appeared
before `score >= 80`, a score of 92 would be labelled `Good` and would never
reach the `Excellent` condition.

## CASE in ORDER BY

`CASE` is not limited to the `SELECT` list. This query sorts active profiles
first, pending profiles second, and inactive profiles last:

```sql
SELECT
    full_name,
    account_status,
    score
FROM profiles
ORDER BY
    CASE
        WHEN account_status = 'active' THEN 1
        WHEN account_status = 'pending' THEN 2
        ELSE 3
    END,
    full_name;
```

Expected order:

```text
Anuj Biswas   | active
Meera Shah    | active
Rohan Gupta   | active
Simran Kaur   | pending
Akash Yas     | inactive
```

The numbers are only sorting priorities; they are not returned unless they
are included in the `SELECT` list.

## Subqueries

A **subquery** is a query nested inside another SQL query. The inner query
runs as part of the outer query and can return:

- one value;
- a list of values;
- a set of rows; or
- a true/false existence result.

The examples below use the same `profiles` table created in
[`profile.sql`](./profile.sql).

### 1. Single-row (scalar) subquery

A scalar subquery returns exactly one value. This example calculates the
overall average score and finds profiles above it:

```sql
SELECT full_name, score
FROM profiles
WHERE score > (
    SELECT AVG(score)
    FROM profiles
)
ORDER BY score DESC;
```

The inner query returns `67.00`. Expected output:

| Name | Score |
| --- | ---: |
| Anuj Biswas | 92 |
| Rohan Gupta | 81 |
| Akash Yas | 68 |

If a scalar subquery returns more than one row, PostgreSQL raises an error.
Use `IN`, `ANY`, or `ALL` when multiple values are expected.

### 2. Scalar subquery in `SELECT`

A scalar subquery can also calculate a value displayed beside every row:

```sql
SELECT
    full_name,
    score,
    (SELECT ROUND(AVG(score), 2) FROM profiles) AS overall_average,
    ROUND(score - (SELECT AVG(score) FROM profiles), 2)
        AS difference_from_average
FROM profiles
ORDER BY profile_id;
```

Every row shows the same `overall_average` of `67.00`. The differences are:

| Name | Score | Difference |
| --- | ---: | ---: |
| Anuj Biswas | 92 | 25.00 |
| Akash Yas | 68 | 1.00 |
| Rohan Gupta | 81 | 14.00 |
| Simran Kaur | 55 | -12.00 |
| Meera Shah | 39 | -28.00 |

### 3. Multiple-row subquery with `IN`

This inner query returns a list of statuses. `IN` keeps rows matching any
value in that list:

```sql
SELECT full_name, account_status, score
FROM profiles
WHERE account_status IN (
    SELECT account_status
    FROM profiles
    WHERE score >= 80
)
ORDER BY profile_id;
```

Profiles with a score of at least 80 have status `active`, so the output is
Anuj Biswas, Rohan Gupta, and Meera Shah.

### 4. Multiple-row subquery with `ANY`

`ANY` means that the comparison must be true for at least one value returned
by the subquery:

```sql
SELECT full_name, score
FROM profiles
WHERE score > ANY (
    SELECT score
    FROM profiles
    WHERE age >= 18
)
ORDER BY score DESC;
```

The adult scores are 92, 68, 55, and 39. A score greater than at least one
of those values is returned:

| Name | Score |
| --- | ---: |
| Anuj Biswas | 92 |
| Rohan Gupta | 81 |
| Akash Yas | 68 |
| Simran Kaur | 55 |

`ANY` is similar to “at least one match”. `SOME` is a PostgreSQL synonym for
`ANY`.

### 5. Multiple-row subquery with `ALL`

`ALL` means that the comparison must be true for every value returned:

```sql
SELECT full_name, score
FROM profiles
WHERE score > ALL (
    SELECT score
    FROM profiles
    WHERE age < 18
)
ORDER BY score DESC;
```

The only minor has a score of 81, so the output is Anuj Biswas with 92.
`ALL` is useful for questions such as “greater than every value”.

### 6. Correlated subquery

A correlated subquery refers to a value from the current outer row. This
query compares each profile with the average score for that profile's own
status:

```sql
SELECT
    p.full_name,
    p.account_status,
    p.score
FROM profiles AS p
WHERE p.score > (
    SELECT AVG(p2.score)
    FROM profiles AS p2
    WHERE p2.account_status = p.account_status
)
ORDER BY p.score DESC;
```

Expected output:

| Name | Status | Score |
| --- | --- | ---: |
| Anuj Biswas | active | 92 |
| Rohan Gupta | active | 81 |

The inner query is evaluated using the current outer row's
`p.account_status`.

### 7. `EXISTS` correlated subquery

`EXISTS` returns true as soon as the inner query finds at least one row. This
query finds profiles that have another profile with the same status and a
higher score:

```sql
SELECT p.full_name, p.account_status, p.score
FROM profiles AS p
WHERE EXISTS (
    SELECT 1
    FROM profiles AS other
    WHERE other.account_status = p.account_status
      AND other.score > p.score
)
ORDER BY p.score DESC;
```

Expected output:

| Name | Status | Score |
| --- | --- | ---: |
| Rohan Gupta | active | 81 |
| Meera Shah | active | 39 |

The selected value `1` is not important; `EXISTS` only checks whether a row
exists.

### 8. `NOT EXISTS` correlated subquery

Negating `EXISTS` finds rows for which no matching row exists. This query
finds the highest-scoring profile in each status group:

```sql
SELECT p.full_name, p.account_status, p.score
FROM profiles AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM profiles AS other
    WHERE other.account_status = p.account_status
      AND other.score > p.score
)
ORDER BY p.account_status, p.score DESC;
```

Expected output:

| Name | Status | Score |
| --- | --- | ---: |
| Anuj Biswas | active | 92 |
| Akash Yas | inactive | 68 |
| Simran Kaur | pending | 55 |

### 9. Subquery in `FROM` (derived table)

A subquery in the `FROM` clause creates a temporary result. It must have an
alias:

```sql
SELECT
    status_summary.account_status,
    status_summary.average_score
FROM (
    SELECT
        account_status,
        ROUND(AVG(score), 2) AS average_score
    FROM profiles
    GROUP BY account_status
) AS status_summary
WHERE status_summary.average_score >= 60
ORDER BY status_summary.average_score DESC;
```

Expected output:

| Status | Average score |
| --- | ---: |
| active | 70.67 |
| inactive | 68.00 |

### Where subqueries can be used

Subqueries can appear in several parts of a statement:

| Location | Example in this lesson |
| --- | --- |
| `WHERE` | Scalar, `IN`, `ANY`, `ALL`, and correlated filters |
| `SELECT` | Overall average beside every profile |
| `FROM` | Derived status summary table |
| `EXISTS` | Checking for a related row |

Prefer a join when it expresses the relationship more clearly, and use
`EXISTS` when you only need to know whether a matching row is present.

## Expected outputs

When the complete file runs successfully, these checkpoints should match:

| Check | Expected result |
| --- | --- |
| Number of profiles | 5 |
| Active profiles | 3 |
| Minor profiles | 1 |
| Excellent scores | 2 |
| First profile in status-priority order | Anuj Biswas |
| Overall average score | 67.00 |
| Profiles above overall average | 3 |
| Highest profile per status | 3 |

Terminal spacing may differ, but the values and row order should match.

## Simple versus searched CASE

| Feature | Simple `CASE` | Searched/conditional `CASE` |
| --- | --- | --- |
| Syntax | `CASE expression WHEN value` | `CASE WHEN condition` |
| Compares | One expression to exact values | Any Boolean condition |
| Good for | Status or category labels | Ranges, thresholds, and rules |
| Example | `CASE account_status` | `CASE WHEN score >= 80` |

### Quick rule

- Use **simple `CASE`** when one column is being matched against known values.
- Use **searched `CASE`** when you need operators such as `>`, `<`, `BETWEEN`,
  `IN`, or multiple columns.

## Practice questions

1. Add a `country` column and label Indian profiles as `Domestic` and all
   others as `International`.
2. Write a searched `CASE` that labels scores below 40 as `Fail` and scores
   of 40 or above as `Pass`.
3. Add a `CASE` expression that labels ages 18 and above as `Eligible` and
   younger profiles as `Not eligible`.
4. Rewrite the status query without an `ELSE`, then test it with an unknown
   status.
5. Count how many profiles belong to each performance label using a subquery
   or a repeated `CASE` expression.
6. Find profiles whose score is below the overall average using a scalar
   subquery.
7. Find the lowest-scoring profile in each status using `NOT EXISTS`.
8. Rewrite the correlated average-score query using a join and `GROUP BY`.
9. Use `IN` to find profiles whose city belongs to a city containing a
   profile younger than 25.
