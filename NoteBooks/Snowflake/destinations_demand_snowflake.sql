-- ==================================================================
-- Destinations Demand — Snowflake Load & Validation Script
-- ==================================================================
-- Usage:
--   1. Update the file format / stage / COPY INTO section with your
--      actual stage name (internal @stage or external S3/Azure/GCS).
--   2. Run the LOAD section first, then the VALIDATION section.
-- ==================================================================

-- ------------------------------------------------------------------
-- 0. Context — set your working database/schema/warehouse
-- ------------------------------------------------------------------
USE WAREHOUSE YOUR_WAREHOUSE;
USE DATABASE YOUR_DATABASE;
USE SCHEMA YOUR_SCHEMA;

-- ------------------------------------------------------------------
-- 1. LOAD: Create target table
-- ------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DESTINATIONS_DEMAND_CLEANED (
    destination_id      VARCHAR(20)      NOT NULL,
    destination          VARCHAR(100),
    demand                VARCHAR(20),
    required_quantity    NUMBER(10,2),
    priority              VARCHAR(20)
);

-- ------------------------------------------------------------------
-- 2. LOAD: File format for the cleaned CSV export
-- ------------------------------------------------------------------
CREATE FILE FORMAT IF NOT EXISTS CSV_STANDARD_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE;

-- ------------------------------------------------------------------
-- 3. LOAD: Create a stage (internal example — swap for your S3/Azure/GCS stage)
-- ------------------------------------------------------------------
CREATE STAGE IF NOT EXISTS DESTINATIONS_DEMAND_STAGE
    FILE_FORMAT = CSV_STANDARD_FORMAT;

-- If using an internal stage, upload the file first via SnowSQL:
--   PUT file://data3_clean.csv @DESTINATIONS_DEMAND_STAGE;
--
-- If using external cloud storage instead, use something like:
-- CREATE STAGE IF NOT EXISTS DESTINATIONS_DEMAND_STAGE
--     URL = 's3://your-bucket/destinations_demand/'
--     CREDENTIALS = (AWS_KEY_ID = 'YOUR_KEY' AWS_SECRET_KEY = 'YOUR_SECRET')
--     FILE_FORMAT = CSV_STANDARD_FORMAT;

-- ------------------------------------------------------------------
-- 4. LOAD: Copy data from stage into the table
-- ------------------------------------------------------------------
COPY INTO DESTINATIONS_DEMAND_CLEANED (
    destination_id, destination, demand, required_quantity, priority
)
FROM @DESTINATIONS_DEMAND_STAGE/data3_clean.csv
FILE_FORMAT = (FORMAT_NAME = CSV_STANDARD_FORMAT)
ON_ERROR = 'CONTINUE';

-- Check how the load went
SELECT * FROM TABLE(VALIDATE(DESTINATIONS_DEMAND_CLEANED, JOB_ID => '_last'));

-- Quick row count sanity check
SELECT COUNT(*) AS total_rows_loaded FROM DESTINATIONS_DEMAND_CLEANED;


-- ==================================================================
-- 5. VALIDATION: Data quality checks on the loaded table
-- ==================================================================

-- 5.1 Row count and basic shape
SELECT COUNT(*) AS total_rows FROM DESTINATIONS_DEMAND_CLEANED;

-- 5.2 Missing values per column
SELECT
    SUM(CASE WHEN destination_id   IS NULL THEN 1 ELSE 0 END) AS null_destination_id,
    SUM(CASE WHEN destination      IS NULL THEN 1 ELSE 0 END) AS null_destination,
    SUM(CASE WHEN demand           IS NULL THEN 1 ELSE 0 END) AS null_demand,
    SUM(CASE WHEN required_quantity IS NULL THEN 1 ELSE 0 END) AS null_required_quantity,
    SUM(CASE WHEN priority         IS NULL THEN 1 ELSE 0 END) AS null_priority
FROM DESTINATIONS_DEMAND_CLEANED;

-- 5.3 Duplicate rows (exact duplicates across all columns)
SELECT destination_id, destination, demand, required_quantity, priority, COUNT(*) AS occurrences
FROM DESTINATIONS_DEMAND_CLEANED
GROUP BY destination_id, destination, demand, required_quantity, priority
HAVING COUNT(*) > 1;

-- 5.4 Duplicate destination_id values (should be unique)
SELECT destination_id, COUNT(*) AS occurrences
FROM DESTINATIONS_DEMAND_CLEANED
GROUP BY destination_id
HAVING COUNT(*) > 1;

-- 5.5 destination_id format check (expects pattern 'DESTxxxx')
SELECT destination_id
FROM DESTINATIONS_DEMAND_CLEANED
WHERE NOT REGEXP_LIKE(destination_id, '^DEST[0-9]{4}$');

-- 5.6 Categorical validity: demand
SELECT DISTINCT demand
FROM DESTINATIONS_DEMAND_CLEANED
WHERE demand NOT IN ('Very High', 'High', 'Medium', 'Low', 'Very Low')
   OR demand IS NULL;

-- 5.7 Categorical validity: priority
SELECT DISTINCT priority
FROM DESTINATIONS_DEMAND_CLEANED
WHERE priority NOT IN ('Critical', 'High', 'Medium', 'Low')
   OR priority IS NULL;

-- 5.8 Numeric sanity: required_quantity should be non-negative
SELECT *
FROM DESTINATIONS_DEMAND_CLEANED
WHERE required_quantity < 0;

-- 5.9 Numeric outliers: values far outside the typical range (basic IQR-style check)
WITH stats AS (
    SELECT
        APPROX_PERCENTILE(required_quantity, 0.25) AS q1,
        APPROX_PERCENTILE(required_quantity, 0.75) AS q3
    FROM DESTINATIONS_DEMAND_CLEANED
)
SELECT d.*
FROM DESTINATIONS_DEMAND_CLEANED d, stats s
WHERE d.required_quantity < (s.q1 - 1.5 * (s.q3 - s.q1))
   OR d.required_quantity > (s.q3 + 1.5 * (s.q3 - s.q1));

-- 5.10 Overall validation summary (single-row pass/fail rollup)
SELECT
    (SELECT COUNT(*) FROM DESTINATIONS_DEMAND_CLEANED)                                   AS total_rows,
    (SELECT COUNT(*) FROM DESTINATIONS_DEMAND_CLEANED WHERE destination_id IS NULL
        OR required_quantity IS NULL)                                                    AS rows_with_nulls,
    (SELECT COUNT(*) FROM (
        SELECT destination_id FROM DESTINATIONS_DEMAND_CLEANED
        GROUP BY destination_id HAVING COUNT(*) > 1
    ))                                                                                    AS duplicate_id_count,
    (SELECT COUNT(*) FROM DESTINATIONS_DEMAND_CLEANED WHERE required_quantity < 0)        AS negative_quantity_count,
    (SELECT COUNT(*) FROM DESTINATIONS_DEMAND_CLEANED
        WHERE NOT REGEXP_LIKE(destination_id, '^DEST[0-9]{4}$'))                          AS bad_id_format_count;
