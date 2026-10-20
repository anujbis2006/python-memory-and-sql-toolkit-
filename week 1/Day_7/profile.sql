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