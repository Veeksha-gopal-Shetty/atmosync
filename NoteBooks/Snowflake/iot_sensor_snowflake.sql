-- ============================================================
-- AtmoSync - IoT Sensor Data | Snowflake Ingestion & Validation
-- ============================================================


-- ============================================================
-- 1. USE RAW SCHEMA
-- ============================================================

USE SCHEMA ATMOSYNC.RAW;


-- ============================================================
-- 2. RAW IoT SENSOR READINGS TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS ATMOSYNC.RAW.IOT_SENSOR_READINGS (
    READING_ID VARCHAR,
    SHIPMENT_ID VARCHAR,
    CONTAINER_ID VARCHAR,
    TIMESTAMP TIMESTAMP_NTZ,
    TEMPERATURE FLOAT,
    HUMIDITY FLOAT,
    VIBRATION FLOAT,
    LATITUDE FLOAT,
    LONGITUDE FLOAT
);


-- ============================================================
-- 3. CSV FILE FORMAT
-- ============================================================

CREATE FILE FORMAT IF NOT EXISTS ATMOSYNC.RAW.CSV_FORMAT
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
TRIM_SPACE = TRUE
EMPTY_FIELD_AS_NULL = TRUE;


-- ============================================================
-- 4. RAW INGESTION STAGE
-- ============================================================

CREATE STAGE IF NOT EXISTS ATMOSYNC.RAW.INGEST_STAGE;


-- ============================================================
-- 5. RAW DATA VALIDATION
-- ============================================================

-- Preview RAW data
SELECT *
FROM ATMOSYNC.RAW.IOT_SENSOR_READINGS
LIMIT 10;


-- Check total RAW rows
SELECT COUNT(*) AS TOTAL_ROWS
FROM ATMOSYNC.RAW.IOT_SENSOR_READINGS;


-- Check NULL values
SELECT
    COUNT_IF(READING_ID IS NULL) AS NULL_READING_ID,
    COUNT_IF(SHIPMENT_ID IS NULL) AS NULL_SHIPMENT_ID,
    COUNT_IF(CONTAINER_ID IS NULL) AS NULL_CONTAINER_ID,
    COUNT_IF(TIMESTAMP IS NULL) AS NULL_TIMESTAMP,
    COUNT_IF(TEMPERATURE IS NULL) AS NULL_TEMPERATURE,
    COUNT_IF(HUMIDITY IS NULL) AS NULL_HUMIDITY,
    COUNT_IF(VIBRATION IS NULL) AS NULL_VIBRATION,
    COUNT_IF(LATITUDE IS NULL) AS NULL_LATITUDE,
    COUNT_IF(LONGITUDE IS NULL) AS NULL_LONGITUDE
FROM ATMOSYNC.RAW.IOT_SENSOR_READINGS;


-- Check duplicate Reading IDs
SELECT
    READING_ID,
    COUNT(*) AS CNT
FROM ATMOSYNC.RAW.IOT_SENSOR_READINGS
GROUP BY READING_ID
HAVING COUNT(*) > 1
ORDER BY CNT DESC;


-- Check sensor and GPS ranges
SELECT
    MIN(TEMPERATURE) AS MIN_TEMPERATURE,
    MAX(TEMPERATURE) AS MAX_TEMPERATURE,
    MIN(HUMIDITY) AS MIN_HUMIDITY,
    MAX(HUMIDITY) AS MAX_HUMIDITY,
    MIN(VIBRATION) AS MIN_VIBRATION,
    MAX(VIBRATION) AS MAX_VIBRATION,
    MIN(LATITUDE) AS MIN_LATITUDE,
    MAX(LATITUDE) AS MAX_LATITUDE,
    MIN(LONGITUDE) AS MIN_LONGITUDE,
    MAX(LONGITUDE) AS MAX_LONGITUDE
FROM ATMOSYNC.RAW.IOT_SENSOR_READINGS;


-- Check invalid values
SELECT
    COUNT_IF(TEMPERATURE < 0 OR TEMPERATURE > 30) AS INVALID_TEMPERATURE,
    COUNT_IF(HUMIDITY < 0 OR HUMIDITY > 100) AS INVALID_HUMIDITY,
    COUNT_IF(VIBRATION < 0) AS INVALID_VIBRATION,
    COUNT_IF(LATITUDE < -90 OR LATITUDE > 90) AS INVALID_LATITUDE,
    COUNT_IF(LONGITUDE < -180 OR LONGITUDE > 180) AS INVALID_LONGITUDE
FROM ATMOSYNC.RAW.IOT_SENSOR_READINGS;


-- ============================================================
-- 6. CLEANED IoT DATA STAGE
-- ============================================================

CREATE STAGE IF NOT EXISTS ATMOSYNC.STAGING.IOT_CLEAN_STAGE;


-- ============================================================
-- 7. CLEANED IoT SENSOR READINGS TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS ATMOSYNC.STAGING.IOT_CLEAN (
    READING_ID VARCHAR,
    SHIPMENT_ID VARCHAR,
    CONTAINER_ID VARCHAR,
    TIMESTAMP TIMESTAMP_NTZ,
    TEMPERATURE FLOAT,
    HUMIDITY FLOAT,
    VIBRATION FLOAT,
    LATITUDE FLOAT,
    LONGITUDE FLOAT
);


-- ============================================================
-- 8. PREVIEW CLEANED CSV
-- ============================================================

SELECT
    SPLIT($1, ',')[0]::VARCHAR AS READING_ID,
    SPLIT($1, ',')[1]::VARCHAR AS SHIPMENT_ID,
    SPLIT($1, ',')[2]::VARCHAR AS CONTAINER_ID,
    SPLIT($1, ',')[3]::TIMESTAMP AS TIMESTAMP,
    SPLIT($1, ',')[4]::FLOAT AS TEMPERATURE,
    SPLIT($1, ',')[5]::FLOAT AS HUMIDITY,
    SPLIT($1, ',')[6]::FLOAT AS VIBRATION,
    SPLIT($1, ',')[7]::FLOAT AS LATITUDE,
    SPLIT($1, ',')[8]::FLOAT AS LONGITUDE
FROM @ATMOSYNC.STAGING.IOT_CLEAN_STAGE/data2_clean.csv
(FILE_FORMAT => 'ATMOSYNC.RAW.CSV_FORMAT')
LIMIT 5;


-- ============================================================
-- 9. LOAD CLEANED IoT DATA
-- ============================================================

INSERT INTO ATMOSYNC.STAGING.IOT_CLEAN
SELECT
    SPLIT($1, ',')[0]::VARCHAR,
    SPLIT($1, ',')[1]::VARCHAR,
    SPLIT($1, ',')[2]::VARCHAR,
    SPLIT($1, ',')[3]::TIMESTAMP,
    SPLIT($1, ',')[4]::FLOAT,
    SPLIT($1, ',')[5]::FLOAT,
    SPLIT($1, ',')[6]::FLOAT,
    SPLIT($1, ',')[7]::FLOAT,
    SPLIT($1, ',')[8]::FLOAT
FROM @ATMOSYNC.STAGING.IOT_CLEAN_STAGE/data2_clean.csv
(FILE_FORMAT => 'ATMOSYNC.RAW.CSV_FORMAT');


-- ============================================================
-- 10. CLEANED DATA VALIDATION
-- ============================================================

-- Preview cleaned data
SELECT *
FROM ATMOSYNC.STAGING.IOT_CLEAN
LIMIT 10;


-- Check cleaned row count
SELECT COUNT(*) AS TOTAL_ROWS
FROM ATMOSYNC.STAGING.IOT_CLEAN;


-- Final quality check
SELECT
    COUNT(*) AS TOTAL_ROWS,
    COUNT(DISTINCT READING_ID) AS UNIQUE_READING_IDS,
    COUNT_IF(READING_ID IS NULL) AS NULL_READING_ID,
    COUNT_IF(TEMPERATURE IS NULL) AS NULL_TEMPERATURE,
    COUNT_IF(HUMIDITY IS NULL) AS NULL_HUMIDITY,
    COUNT_IF(VIBRATION IS NULL) AS NULL_VIBRATION
FROM ATMOSYNC.STAGING.IOT_CLEAN;


-- ============================================================
-- END OF IoT SENSOR DATA INGESTION & VALIDATION
-- ============================================================
