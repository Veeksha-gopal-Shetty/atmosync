# 🌡️ AtmoSync --- Real-Time Cold Chain Logistics & Spoilage Analytics

## 📌 Project Overview

AtmoSync is a real-time cold chain logistics analytics solution designed
to monitor shipment conditions, identify spoilage risks, estimate
potential financial exposure, and support operational decisions such as
rerouting.

The system combines vaccine shipment information, IoT sensor readings,
route data, and destination demand data to provide an end-to-end view of
cold chain shipment health.

------------------------------------------------------------------------

## 🎯 Business Objective

The primary objective of AtmoSync is to help organizations:

-   Monitor environmental conditions inside shipment containers
-   Detect temperature-related shipment risks
-   Identify shipments with potential spoilage exposure
-   Estimate the financial value of at-risk inventory
-   Recommend operational actions
-   Identify shipments requiring potential rerouting
-   Track actual shipment GPS movement
-   Provide management with an analytical dashboard

------------------------------------------------------------------------

## 🔄 Business Process

The AtmoSync workflow follows an end-to-end cold chain analytics
process:

``` text
IoT Sensor Data
       ↓
Real-Time Data Ingestion
       ↓
Data Storage & Organization
       ↓
Container Health Analysis
       ↓
Spoilage Risk Detection
       ↓
Financial Impact Estimation
       ↓
Recommended Action
       ↓
Rerouting Recommendation
       ↓
Management Dashboard
```

------------------------------------------------------------------------

## 📊 Data Sources

AtmoSync uses four primary datasets to build the cold chain analytics
workflow.

### 1. Vaccine Shipments

Contains shipment-level information required to understand the vaccine
being transported and its safe temperature requirements.

Key fields include:

-   Shipment ID
-   Container ID
-   Vaccine Type
-   Batch ID
-   Quantity
-   Source
-   Destination
-   Departure Time
-   Expected Arrival
-   Minimum Temperature
-   Maximum Temperature

### 2. IoT Sensor Readings

Contains environmental and location data collected from shipment
containers.

Key fields include:

-   Reading ID
-   Shipment ID
-   Container ID
-   Timestamp
-   Temperature
-   Humidity
-   Vibration
-   Latitude
-   Longitude

### 3. Routes

Contains transportation route information used for shipment and
rerouting analysis.

Key fields include:

-   Route ID
-   Source
-   Destination
-   Distance
-   Estimated Travel Time

### 4. Destination Demand

Contains destination-level demand information used to understand
delivery requirements and priorities.

Key fields include:

-   Destination ID
-   Destination
-   Demand
-   Required Quantity
-   Priority

------------------------------------------------------------------------

## 🏗️ Data Architecture

The AtmoSync architecture follows a layered approach to process raw
operational data into decision-ready analytics.

``` text
                         AtmoSync
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
   Vaccine Data        IoT Sensor Data    Route Data
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                   Destination Demand
                            │
                            ↓
                       RAW Layer
                            ↓
                     STAGING Layer
                            ↓
                    ANALYTICS Layer
                            ↓
                  Decision Analytics
                            ↓
                  Management Dashboard
```

------------------------------------------------------------------------

## ❄️ Container Health Analysis

The system compares observed IoT temperature readings with the safe
temperature limits defined for each vaccine shipment.

A shipment is classified as:

-   **NORMAL** --- Sensor readings remain within the allowed temperature
    range.
-   **CRITICAL** --- Sensor readings exceed the defined safe temperature
    range.

### Container Health Results

  Health Status     Shipments
  --------------- -----------
  NORMAL                  445
  CRITICAL                 55
  **Total**           **500**

------------------------------------------------------------------------

## 🚨 Spoilage Risk Detection

Spoilage risk is calculated using the percentage of IoT temperature
readings that fall outside the permitted temperature range.

### Risk Classification

  Risk Level   Condition
  ------------ -------------------------------------
  LOW          0% out-of-range readings
  MEDIUM       Up to 10% out-of-range readings
  HIGH         More than 10% out-of-range readings

### Risk Results

  Risk Level     Shipments
  ------------ -----------
  LOW                  445
  MEDIUM                 0
  HIGH                  55
  **Total**        **500**

------------------------------------------------------------------------

## 💰 Financial Impact Estimation

The vaccine shipment dataset does not contain a direct monetary value
per unit.

For project demonstration purposes, an assumed value of **₹500 per
vaccine unit** is used to estimate potential financial exposure for
high-risk shipments.

### Calculation

``` text
Potential Financial Impact
=
At-Risk Quantity × Assumed Value Per Unit
```

Current analysis:

-   **At-Risk Quantity:** 239,000 units
-   **Assumed Value Per Unit:** ₹500
-   **Estimated Potential Financial Exposure:** ₹119,500,000

> **Note:** This represents estimated exposure under the project's
> assumption and is not actual company financial loss.

------------------------------------------------------------------------

## 🚚 Recommended Action

The system generates an operational recommendation based on spoilage
risk.

``` text
HIGH RISK
    ↓
IMMEDIATE ACTION / REROUTE

MEDIUM RISK
    ↓
MONITOR CLOSELY

LOW RISK
    ↓
CONTINUE SHIPMENT
```

### Recommended Action Results

  Recommended Action             Shipments
  ---------------------------- -----------
  CONTINUE SHIPMENT                    445
  MONITOR CLOSELY                        0
  IMMEDIATE ACTION / REROUTE            55
  **Total**                        **500**

------------------------------------------------------------------------

## 🗺️ Rerouting Recommendation

High-risk shipments are identified for potential rerouting to reduce
spoilage exposure.

``` text
High Spoilage Risk
       ↓
Identify Shipment
       ↓
Check Route
       ↓
Evaluate Destination
       ↓
Rerouting Recommendation
```

### Rerouting Results

  Recommendation                               Shipments
  ------------------------------------------ -----------
  NO REROUTING REQUIRED                              445
  REROUTE SHIPMENT TO REDUCE SPOILAGE RISK            55
  **Total**                                      **500**

------------------------------------------------------------------------

## 📡 Real-Time IoT & Kafka Integration

IoT sensor readings are streamed through Apache Kafka for real-time
ingestion.

``` text
IoT Sensor Data
       ↓
Kafka Producer
       ↓
Kafka Topic
       ↓
Snowflake Kafka Connector
       ↓
Snowflake RAW Layer
       ↓
STAGING
       ↓
ANALYTICS
```

The Kafka integration enables sensor readings to move into Snowflake for
downstream analytics.

### Kafka Integration Results

-   IoT sensor readings processed: **50,000**
-   Clean Kafka topic: `iot-sensor-readings-clean`
-   Snowflake RAW ingestion: **50,000 records**
-   Snowflake staging records: **50,000 records**
-   Shipment-level IoT analytics: **500 shipments**

------------------------------------------------------------------------

## ❄️ Snowflake Architecture

The Snowflake database is organized into three primary layers.

``` text
ATMOSYNC
│
├── RAW
│   ├── Vaccine Shipments
│   ├── IoT Sensor Readings
│   ├── Routes
│   └── Destination Demand
│
├── STAGING
│   ├── Cleaned Vaccine Shipments
│   ├── Cleaned IoT Data
│   ├── Cleaned Routes
│   └── Cleaned Destination Demand
│
└── ANALYTICS
    ├── Shipment Analytics
    ├── IoT Analytics
    ├── Container Health Analytics
    ├── Spoilage Risk Analytics
    ├── Financial Impact Analytics
    └── Decision Analytics
```

------------------------------------------------------------------------

## 📈 Key Analytics

The project generates analytics for:

-   Shipment health
-   Temperature compliance
-   Spoilage risk
-   At-risk inventory
-   Potential financial exposure
-   Recommended operational action
-   Rerouting recommendations
-   GPS shipment movement
-   Destination-level rerouting priorities

------------------------------------------------------------------------

## 🗺️ GPS Shipment Tracking

The dashboard provides actual GPS-based shipment tracking using latitude
and longitude readings collected from IoT sensors.

For a selected shipment, the dashboard displays:

-   Starting GPS position
-   Recorded GPS movement
-   Latest GPS position
-   Temperature
-   Humidity
-   Vibration
-   Shipment risk
-   Source and destination

The GPS visualization allows users to inspect the recorded movement path
of individual shipments.

------------------------------------------------------------------------

## 📊 Management Dashboard

The AtmoSync dashboard provides a centralized view of cold chain
operations.

### Dashboard Includes

-   Total shipments
-   High-risk shipments
-   Low-risk shipments
-   At-risk quantity
-   Potential financial exposure
-   Shipment risk overview
-   Financial exposure by vaccine
-   Rerouting priorities
-   Actual GPS shipment tracking
-   High-risk shipment details
-   Management insights

------------------------------------------------------------------------

## 📌 Project Results

  Metric                         Result
  ------------------------------ ---------------
  Total Shipments                500
  High-Risk Shipments            55
  Low-Risk Shipments             445
  At-Risk Quantity               239,000 units
  Estimated Financial Exposure   ₹119,500,000
  IoT Sensor Readings            50,000
  GPS Tracking                   Available

> **Note:** Financial exposure is calculated using the project's assumed
> value of ₹500 per vaccine unit.

------------------------------------------------------------------------

## 🛠️ Technologies Used

-   Python
-   Pandas
-   Streamlit
-   PyDeck
-   SQL
-   Snowflake
-   Apache Kafka
-   Git
-   GitHub
-   VS Code

------------------------------------------------------------------------

## 📁 Project Structure

``` text
AtmoSync/
│
├── Data/
│   └── Snowflake/
│
├── NoteBooks/
│   └── Snowflake/
│       ├── AtmoSync_Analytics.sql
│       ├── destinations_demand_snowflake.sql
│       ├── iot_sensor_snowflake.sql
│       ├── kafka_iot_analytics.sql
│       ├── route_data_snowflake.sql
│       ├── snowflake_setup.sql
│       └── validate_vaccine_shipment.sql
│
├── kafka/
│   └── producer/
│       ├── iot_producer.py
│       └── iot_producer_clean.py
│
├── streamlit/
│   └── streamlit_app.py
│
└── README.md
```

------------------------------------------------------------------------

## 👥 Team Responsibilities

  -----------------------------------------------------------------------
  Team Member                         Responsibility
  ----------------------------------- -----------------------------------
  Team Lead                           Project coordination, Snowflake
                                      integration, IoT analytics and
                                      dashboard

  VEEKSHA2817                         Route dataset

  ADHITHYA03                          Destination Demand dataset

  ANGELROSE123                        Vaccine Shipment dataset
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🔍 Data Validation

The project includes validation checks for:

-   Row counts
-   Duplicate records
-   Null values
-   Unique IDs
-   Data types
-   Temperature ranges
-   Route information
-   Shipment-to-IoT relationships
-   Shipment-to-route relationships
-   Shipment-to-demand relationships

### Final Validation

  Validation Metric                    Result
  ---------------------------- --------------
  Total Shipments                         500
  Unique Shipments                        500
  High-Risk Shipments                      55
  Immediate Action Shipments               55
  Rerouting Shipments                      55
  Total At-Risk Quantity              239,000
  Total Potential Exposure       ₹119,500,000

------------------------------------------------------------------------

## 🎯 Business Value

AtmoSync converts raw cold chain sensor data into actionable operational
insights.

``` text
Raw Sensor Data
       ↓
Data Processing
       ↓
Risk Detection
       ↓
Financial Exposure
       ↓
Operational Decision
       ↓
Rerouting
```

The solution provides visibility into shipment conditions and helps
identify shipments that require operational attention.

------------------------------------------------------------------------

## 🚀 Future Enhancements

Possible future enhancements include:

-   Machine learning-based spoilage prediction
-   Live streaming dashboard updates
-   Automated alerts for critical shipments
-   Dynamic rerouting using real-time route conditions
-   Actual vaccine pricing integration
-   ETA prediction
-   Weather condition integration
-   Automated notification systems
-   Advanced anomaly detection

------------------------------------------------------------------------

## 🏁 Conclusion

AtmoSync demonstrates an end-to-end cold chain analytics workflow that
combines shipment data, IoT sensor readings, route information, and
destination demand.

The solution transforms operational data into:

**Container Health → Spoilage Risk → Financial Impact → Recommended
Action → Rerouting Decision → Management Dashboard**

The project provides a foundation for improving cold chain visibility,
identifying potential spoilage exposure, and supporting data-driven
logistics decisions.
