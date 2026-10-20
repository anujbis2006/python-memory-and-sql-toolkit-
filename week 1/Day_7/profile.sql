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

-- COMMON TABLE EXPRESSIONS (CTEs) WITH THE WITH CLAUSE
-- A CTE gives a temporary result a name so that the main query is easier to
-- read. The CTE exists only for this one SQL statement.

-- BASIC CTE
-- First create high_score_profiles, then query it like a temporary table.
WITH high_score_profiles AS (
    SELECT
        profile_id,
        full_name,
        score
    FROM profiles
    WHERE score >= 80
)
SELECT *
FROM high_score_profiles
ORDER BY score DESC;

-- CTE WITH AN ALIAS
-- The CTE name can be given a short alias in the main query.
WITH active_profiles AS (
    SELECT profile_id, full_name, city, score
    FROM profiles
    WHERE account_status = 'active'
)
SELECT
    ap.full_name,
    ap.city,
    ap.score
FROM active_profiles AS ap
ORDER BY ap.score DESC;

-- CTE WITH AGGREGATION
-- Build one summary first, then filter the summary outside the CTE.
WITH status_summary AS (
    SELECT
        account_status,
        COUNT(*) AS profile_count,
        ROUND(AVG(score), 2) AS average_score
    FROM profiles
    GROUP BY account_status
)
SELECT
    account_status,
    profile_count,
    average_score
FROM status_summary
WHERE average_score >= 60
ORDER BY average_score DESC;

-- MULTIPLE CTEs
-- Separate steps can be named and then used by a later CTE or the final query.
WITH scored_profiles AS (
    SELECT
        profile_id,
        full_name,
        account_status,
        score,
        CASE
            WHEN score >= 80 THEN 'Excellent'
            WHEN score >= 60 THEN 'Good'
            WHEN score >= 40 THEN 'Needs improvement'
            ELSE 'Poor'
        END AS performance
    FROM profiles
),
excellent_profiles AS (
    SELECT *
    FROM scored_profiles
    WHERE performance = 'Excellent'
)
SELECT
    full_name,
    score,
    performance
FROM excellent_profiles
ORDER BY score DESC;

-- CTE COMPARED WITH A SUBQUERY
-- The following CTE is easier to read than placing the average query inside
-- the WHERE clause, but both produce the same result.
WITH overall_score AS (
    SELECT AVG(score) AS average_score
    FROM profiles
)
SELECT
    p.full_name,
    p.score
FROM profiles AS p
CROSS JOIN overall_score AS os
WHERE p.score > os.average_score
ORDER BY p.score DESC;

-- CTE FOR UPDATE
-- PostgreSQL also allows a CTE to provide rows for an UPDATE. This example
-- is intentionally commented out so the revision script does not change data.
-- WITH low_scores AS (
--     SELECT profile_id
--     FROM profiles
--     WHERE score < 40
-- )
-- UPDATE profiles
-- SET account_status = 'pending'
-- WHERE profile_id IN (SELECT profile_id FROM low_scores);

-- RECURSIVE CTE
-- A recursive CTE can repeatedly refer to itself. This small example
-- generates the numbers 1 through 5 without needing a numbers table.
WITH RECURSIVE numbers AS (
    SELECT 1 AS number
    UNION ALL
    SELECT number + 1
    FROM numbers
    WHERE number < 5
)
SELECT number
FROM numbers
ORDER BY number;

-- Original CTE practice query (kept exactly as written).
with cte_avgmarks as 
(
    select branch , avg(markobtained) as 'avg marks '
    from allstudents
    group by branch
)
select studeint_id , firstname,lastname,a.branch,marksobtained,
from allstudent a
inner join cte_avgmarks c
on a.branch = c.branch
and a.marksobtained > c.[avg.marks]

-- WINDOW FUNCTIONS
-- A window function calculates across related rows while keeping each
-- original row in the result. Unlike GROUP BY, it does not merge rows.
--
-- Main types:
-- 1. Ranking: ROW_NUMBER, RANK, DENSE_RANK, and NTILE assign positions or
--    buckets.
-- 2. Aggregate: SUM, AVG, COUNT, MIN, and MAX summarize the window while
--    keeping every row.
-- 3. Navigation/value: LAG, LEAD, FIRST_VALUE, LAST_VALUE, and NTH_VALUE
--    read values from another row or position in the window.
-- 4. Distribution: PERCENT_RANK and CUME_DIST show relative position.
--
-- PARTITION BY and the window frame are not types. They control which rows
-- each function can see and how the calculation is performed.

-- Basic ROW_NUMBER: give every profile a unique position by score.
SELECT
    full_name,
    score,
    ROW_NUMBER() OVER (ORDER BY score DESC) AS score_position
FROM profiles
ORDER BY score_position;

-- RANK leaves gaps when two rows have the same value.
-- DENSE_RANK does not leave gaps after a tie.
SELECT
    full_name,
    score,
    RANK() OVER (ORDER BY score DESC) AS score_rank,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_score_rank
FROM profiles
ORDER BY score DESC;

-- NTILE divides ordered rows into numbered buckets.
SELECT
    full_name,
    score,
    NTILE(4) OVER (ORDER BY score DESC) AS score_quartile
FROM profiles
ORDER BY score DESC;

-- PARTITION BY restarts the calculation for each account status.
SELECT
    full_name,
    account_status,
    score,
    ROW_NUMBER() OVER (
        PARTITION BY account_status
        ORDER BY score DESC
    ) AS status_position
FROM profiles
ORDER BY account_status, status_position;

-- A windowed aggregate shows the status average without removing rows.
SELECT
    full_name,
    account_status,
    score,
    ROUND(
        AVG(score) OVER (PARTITION BY account_status),
        2
    ) AS status_average
FROM profiles
ORDER BY account_status, score DESC;

-- Compare every score with its status average.
SELECT
    full_name,
    account_status,
    score,
    ROUND(
        score - AVG(score) OVER (PARTITION BY account_status),
        2
    ) AS difference_from_status_average
FROM profiles
ORDER BY account_status, score DESC;

-- Running total and running average ordered by score.
SELECT
    full_name,
    score,
    SUM(score) OVER (
        ORDER BY score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    ROUND(
        AVG(score) OVER (
            ORDER BY score DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_average
FROM profiles
ORDER BY score DESC;

-- A window frame chooses the rows used for the current calculation.
-- General form:
-- function_name(value) OVER (
--     ORDER BY sort_column
--     ROWS BETWEEN frame_start AND frame_end
-- )
--
-- Frame boundaries:
-- UNBOUNDED PRECEDING = start at the first row in the ordered window.
-- N PRECEDING          = include up to N rows before the current row.
-- CURRENT ROW          = the row currently being calculated.
-- N FOLLOWING          = include up to N rows after the current row.
-- UNBOUNDED FOLLOWING  = end at the last row in the ordered window.
--
-- The full frame includes every row for every calculation.
SELECT
    full_name,
    score,
    LAST_VALUE(score) OVER (
        ORDER BY score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_score
FROM profiles
ORDER BY score DESC;

-- The current row and the next two rows.
SELECT
    full_name,
    score,
    SUM(score) OVER (
        ORDER BY score DESC
        ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING
    ) AS current_and_next_two_total
FROM profiles
ORDER BY score DESC;

-- LAG reads the previous row and LEAD reads the next row.
SELECT
    full_name,
    score,
    LAG(score) OVER (ORDER BY score DESC) AS previous_score,
    LEAD(score) OVER (ORDER BY score DESC) AS next_score
FROM profiles
ORDER BY score DESC;

-- Find the highest-scoring profile in every status.
-- Calculate the window result in a CTE before filtering it.
WITH ranked_profiles AS (
    SELECT
        full_name,
        account_status,
        score,
        ROW_NUMBER() OVER (
            PARTITION BY account_status
            ORDER BY score DESC
        ) AS status_position
    FROM profiles
)
SELECT
    full_name,
    account_status,
    score
FROM ranked_profiles
WHERE status_position = 1
ORDER BY account_status;

-- MOVING AVERAGE
-- The frame includes the previous row, current row, and next row.
-- At the first and last rows, only available rows are used.
SELECT
    full_name,
    score,
    ROUND(
        AVG(score) OVER (
            ORDER BY score DESC
            ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
        ),
        2
    ) AS moving_average
FROM profiles
ORDER BY score DESC;

-- LAG AND LEAD WITH DEFAULT VALUES
-- If there is no previous or next row, return 0 instead of NULL.
SELECT
    full_name,
    score,
    LAG(score, 1, 0) OVER (ORDER BY score DESC) AS previous_score,
    LEAD(score, 1, 0) OVER (ORDER BY score DESC) AS next_score
FROM profiles
ORDER BY score DESC;

-- FIRST_VALUE and LAST_VALUE read values from positions in the window.
-- The explicit frame lets LAST_VALUE see the final row, not only the
-- current row.
SELECT
    full_name,
    score,
    FIRST_VALUE(score) OVER (
        ORDER BY score DESC
    ) AS highest_score,
    LAST_VALUE(score) OVER (
        ORDER BY score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_score
FROM profiles
ORDER BY score DESC;

-- Distribution functions show relative and cumulative position.
SELECT
    full_name,
    score,
    ROUND(PERCENT_RANK() OVER (ORDER BY score DESC)::numeric, 2)
        AS percent_rank,
    ROUND(CUME_DIST() OVER (ORDER BY score DESC)::numeric, 2)
        AS cumulative_distribution
FROM profiles
ORDER BY score DESC;