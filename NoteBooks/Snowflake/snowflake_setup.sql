-- ============================================================
-- AtmoSync - Snowflake Database Setup
-- ============================================================


-- ============================================================
-- 1. DATABASE
-- ============================================================

CREATE DATABASE IF NOT EXISTS ATMOSYNC;


-- ============================================================
-- 2. SCHEMAS
-- ============================================================

CREATE SCHEMA IF NOT EXISTS ATMOSYNC.RAW;
CREATE SCHEMA IF NOT EXISTS ATMOSYNC.STAGING;
CREATE SCHEMA IF NOT EXISTS ATMOSYNC.ANALYTICS;


-- ============================================================
-- 3. DATA WAREHOUSE
-- ============================================================

CREATE WAREHOUSE IF NOT EXISTS ATMOSYNC_WH
WITH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;


-- ============================================================
-- 4. RAW DATA INGESTION STAGE
-- ============================================================

CREATE STAGE IF NOT EXISTS ATMOSYNC.RAW.INGEST_STAGE;


-- ============================================================
-- 5. CSV FILE FORMAT
-- ============================================================

CREATE FILE FORMAT IF NOT EXISTS ATMOSYNC.RAW.CSV_FORMAT
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
TRIM_SPACE = TRUE
EMPTY_FIELD_AS_NULL = TRUE;


-- ============================================================
-- 6. CLEAN DATA STAGE - IoT
-- ============================================================

CREATE STAGE IF NOT EXISTS ATMOSYNC.STAGING.IOT_CLEAN_STAGE;


-- ============================================================
-- 7. RAW IoT SENSOR READINGS TABLE
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
-- 8. CLEAN IoT SENSOR READINGS TABLE
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
-- END OF ATMOSYNC SNOWFLAKE SETUP
-- ============================================================

-- NOTE:
-- Data-loading commands are intentionally not included here.
-- Raw and cleaned files are loaded separately into their
-- corresponding stages/tables.
