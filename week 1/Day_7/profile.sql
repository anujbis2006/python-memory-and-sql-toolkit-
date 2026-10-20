-- Day 7: CASE expressions in PostgreSQL
-- Run this file with:
-- psql -d day7_sql -f "week 1/Day_7/profile.sql"

DROP TABLE IF EXISTS profiles;

CREATE TABLE profiles (
    profile_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    age INT NOT NULL CHECK (age > 0),
    account_status VARCHAR(20) NOT NULL,
    score INT NOT NULL CHECK (score BETWEEN 0 AND 100)
);

INSERT INTO profiles (
    full_name,
    city,
    age,
    account_status,
    score
)
VALUES
    ('Anuj Biswas', 'Delhi', 22, 'active', 92),
    ('Akash Yas', 'Mumbai', 34, 'inactive', 68),
    ('Rohan Gupta', 'Bangalore', 17, 'active', 81),
    ('Simran Kaur', 'Pune', 45, 'pending', 55),
    ('Meera Shah', 'Kolkata', 29, 'active', 39);

-- Check the source data.
SELECT *
FROM profiles
ORDER BY profile_id;

-- SIMPLE CASE EXPRESSION
-- Simple CASE compares one expression with several possible values.
-- Here, account_status is compared with 'active', 'inactive', and 'pending'.
SELECT
    profile_id,
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

-- SEARCHED (CONDITIONAL) CASE EXPRESSION
-- Searched CASE checks conditions from top to bottom.
-- The first condition that is true supplies the result.
SELECT
    profile_id,
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

-- A second searched CASE can classify a numeric score.
SELECT
    profile_id,
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

-- CASE can also be used in ORDER BY to put active profiles first.
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


-- SUBQUERIES
-- A subquery is a query inside another query. The inner query runs first and
-- supplies a value, a list of values, rows, or an existence check.

-- SINGLE-ROW (SCALAR) SUBQUERY
-- The subquery returns one value: the average score (67.00).
-- The main query finds profiles scoring above that value.
SELECT
    full_name,
    score
FROM profiles
WHERE score > (
    SELECT AVG(score)
    FROM profiles
)
ORDER BY score DESC;

-- A scalar subquery can also be used in the SELECT list.
SELECT
    full_name,
    score,
    (SELECT ROUND(AVG(score), 2) FROM profiles) AS overall_average,
    ROUND(score - (SELECT AVG(score) FROM profiles), 2) AS difference_from_average
FROM profiles
ORDER BY profile_id;

-- MULTIPLE-ROW SUBQUERY WITH IN
-- The inner query returns several statuses. IN matches any value in that list.
SELECT
    full_name,
    account_status,
    score
FROM profiles
WHERE account_status IN (
    SELECT account_status
    FROM profiles
    WHERE score >= 80
)
ORDER BY profile_id;

-- MULTIPLE-ROW SUBQUERY WITH ANY
-- ANY means the comparison must be true for at least one value returned
-- by the subquery. This finds scores greater than at least one adult score.
SELECT
    full_name,
    score
FROM profiles
WHERE score > ANY (
    SELECT score
    FROM profiles
    WHERE age >= 18
)
ORDER BY score DESC;

-- MULTIPLE-ROW SUBQUERY WITH ALL
-- ALL means the comparison must be true for every value returned by the
-- subquery. This finds scores greater than every minor's score.
SELECT
    full_name,
    score
FROM profiles
WHERE score > ALL (
    SELECT score
    FROM profiles
    WHERE age < 18
)
ORDER BY score DESC;

-- CORRELATED SUBQUERY
-- The inner query refers to the current outer row (p.account_status).
-- It calculates the average score for that profile's own status.
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

-- EXISTS
-- EXISTS returns TRUE when the inner query finds at least one row.
-- This returns profiles that have another profile with the same status and
-- a higher score.
SELECT
    p.full_name,
    p.account_status,
    p.score
FROM profiles AS p
WHERE EXISTS (
    SELECT 1
    FROM profiles AS other
    WHERE other.account_status = p.account_status
      AND other.score > p.score
)
ORDER BY p.score DESC;

-- NOT EXISTS
-- This returns the highest-scoring profile in each account-status group.
SELECT
    p.full_name,
    p.account_status,
    p.score
FROM profiles AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM profiles AS other
    WHERE other.account_status = p.account_status
      AND other.score > p.score
)
ORDER BY p.account_status, p.score DESC;

-- SUBQUERY IN FROM (DERIVED TABLE)
-- A subquery in FROM creates a temporary result that needs an alias.
-- The outer query filters the grouped status summary.
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