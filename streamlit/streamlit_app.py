import streamlit as st
import pandas as pd
import pydeck as pdk
from snowflake.snowpark.context import get_active_session


# =========================================================
# Caption: Page Configuration
# =========================================================

st.set_page_config(
    page_title="AtmoSync Cold Chain Control Tower",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# Caption: Custom Dashboard Styling
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0b1220;
        color: #f8fafc;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .main-subtitle {
        font-size: 16px;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 28px;
        margin-bottom: 15px;
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(
            145deg,
            #111c30,
            #16233a
        );
        border: 1px solid #263752;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    }

    .kpi-label {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #f8fafc;
        font-size: 30px;
        font-weight: 800;
    }

    .kpi-danger {
        color: #ff5c67;
    }

    .kpi-success {
        color: #39d98a;
    }

    .kpi-warning {
        color: #fbbf24;
    }

    .kpi-info {
        color: #38bdf8;
    }

    /* Map container */
    .map-title {
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 30px;
    }

    /* Small information cards */
    .info-card {
        background-color: #111c30;
        border: 1px solid #263752;
        border-radius: 12px;
        padding: 16px;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #263752;
        border-radius: 10px;
    }

    /* Divider */
    hr {
        border-color: #263752;
    }
    /* GPS shipment metric visibility */
[data-testid="stMetric"] {
    background-color: #111c30;
    border: 1px solid #263752;
    border-radius: 12px;
    padding: 14px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# Caption: Snowflake Session
# =========================================================

session = get_active_session()


# =========================================================
# Caption: Dashboard Header
# =========================================================

st.markdown(
    '<div class="main-title">🌡️ AtmoSync Cold Chain Control Tower</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Real-time shipment health • Spoilage risk • Financial exposure • GPS tracking • Rerouting decisions'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# Caption: Load KPI Data
# =========================================================

kpi_df = session.sql("""
    SELECT
        COUNT(*) AS TOTAL_SHIPMENTS,
        COUNT_IF(SPOILAGE_RISK = 'HIGH') AS HIGH_RISK_SHIPMENTS,
        COUNT_IF(SPOILAGE_RISK = 'LOW') AS LOW_RISK_SHIPMENTS,
        SUM(AT_RISK_QUANTITY) AS TOTAL_AT_RISK_QUANTITY,
        SUM(POTENTIAL_FINANCIAL_IMPACT) AS TOTAL_POTENTIAL_EXPOSURE
    FROM ATMOSYNC.ANALYTICS.DASHBOARD_MASTER
""").to_pandas()


# =========================================================
# Caption: KPI Cards
# =========================================================

if not kpi_df.empty:

    total_shipments = int(kpi_df.iloc[0]["TOTAL_SHIPMENTS"])
    high_risk = int(kpi_df.iloc[0]["HIGH_RISK_SHIPMENTS"])
    low_risk = int(kpi_df.iloc[0]["LOW_RISK_SHIPMENTS"])
    at_risk_quantity = int(kpi_df.iloc[0]["TOTAL_AT_RISK_QUANTITY"])
    potential_exposure = int(kpi_df.iloc[0]["TOTAL_POTENTIAL_EXPOSURE"])

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">TOTAL SHIPMENTS</div>
                <div class="kpi-value kpi-info">{total_shipments:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">HIGH RISK</div>
                <div class="kpi-value kpi-danger">{high_risk:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">LOW RISK</div>
                <div class="kpi-value kpi-success">{low_risk:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">AT-RISK QUANTITY</div>
                <div class="kpi-value kpi-warning">{at_risk_quantity:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">POTENTIAL EXPOSURE</div>
                <div class="kpi-value kpi-danger">₹{potential_exposure:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()


# =========================================================
# Caption: Risk Distribution
# =========================================================

st.markdown(
    '<div class="section-title">🚨 Shipment Risk Overview</div>',
    unsafe_allow_html=True
)

risk_df = session.sql("""
    SELECT
        SPOILAGE_RISK,
        COUNT(*) AS SHIPMENT_COUNT
    FROM ATMOSYNC.ANALYTICS.DASHBOARD_MASTER
    GROUP BY SPOILAGE_RISK
    ORDER BY
        CASE
            WHEN SPOILAGE_RISK = 'HIGH' THEN 1
            WHEN SPOILAGE_RISK = 'MEDIUM' THEN 2
            ELSE 3
        END
""").to_pandas()


risk_col1, risk_col2 = st.columns([1.4, 1])


with risk_col1:

    if not risk_df.empty:

        risk_chart = risk_df.set_index("SPOILAGE_RISK")

        st.bar_chart(
            risk_chart["SHIPMENT_COUNT"],
            height=320
        )


with risk_col2:

    st.dataframe(
        risk_df,
        width="stretch",
        hide_index=True,
        height=320
    )


st.divider()


# =========================================================
# Caption: Financial Exposure by Vaccine
# =========================================================

st.markdown(
    '<div class="section-title">💰 Financial Exposure by Vaccine</div>',
    unsafe_allow_html=True
)

vaccine_df = session.sql("""
    SELECT
        VACCINE_TYPE,
        SUM(AT_RISK_QUANTITY) AS AT_RISK_QUANTITY,
        SUM(POTENTIAL_FINANCIAL_IMPACT) AS POTENTIAL_FINANCIAL_EXPOSURE
    FROM ATMOSYNC.ANALYTICS.DASHBOARD_MASTER
    GROUP BY VACCINE_TYPE
    ORDER BY POTENTIAL_FINANCIAL_EXPOSURE DESC
""").to_pandas()


vaccine_col1, vaccine_col2 = st.columns([1.2, 1])


with vaccine_col1:

    if not vaccine_df.empty:

        chart_df = vaccine_df.set_index("VACCINE_TYPE")

        st.bar_chart(
            chart_df["POTENTIAL_FINANCIAL_EXPOSURE"],
            height=350
        )


with vaccine_col2:

    st.dataframe(
        vaccine_df,
        width="stretch",
        hide_index=True,
        height=350
    )


st.divider()


# =========================================================
# Caption: Rerouting Analysis
# =========================================================

st.markdown(
    '<div class="section-title">🚚 Rerouting Priorities</div>',
    unsafe_allow_html=True
)

reroute_df = session.sql("""
    SELECT
        DESTINATION,
        COUNT(*) AS REROUTE_SHIPMENTS
    FROM ATMOSYNC.ANALYTICS.DASHBOARD_MASTER
    WHERE REROUTING_RECOMMENDATION =
          'REROUTE SHIPMENT TO REDUCE SPOILAGE RISK'
    GROUP BY DESTINATION
    ORDER BY REROUTE_SHIPMENTS DESC
""").to_pandas()


reroute_col1, reroute_col2 = st.columns([1.3, 1])


with reroute_col1:

    if not reroute_df.empty:

        st.bar_chart(
            reroute_df.set_index("DESTINATION")["REROUTE_SHIPMENTS"],
            height=350
        )


with reroute_col2:

    st.dataframe(
        reroute_df,
        width="stretch",
        hide_index=True,
        height=350
    )


st.divider()


# =========================================================
# Caption: Real GPS Shipment Tracking
# =========================================================

st.markdown(
    '<div class="section-title">🗺️ GPS Shipment Tracking</div>',
    unsafe_allow_html=True
)

st.caption(
    "Select one shipment to inspect its actual recorded GPS movement."
)


# =========================================================
# Caption: Load GPS Data
# =========================================================

gps_df = session.sql("""
    SELECT
        I.SHIPMENT_ID,
        I.TIMESTAMP,
        I.LATITUDE::FLOAT AS LATITUDE,
        I.LONGITUDE::FLOAT AS LONGITUDE,
        I.TEMPERATURE::FLOAT AS TEMPERATURE,
        I.HUMIDITY::FLOAT AS HUMIDITY,
        I.VIBRATION::FLOAT AS VIBRATION,
        D.SPOILAGE_RISK,
        D.SOURCE,
        D.DESTINATION
    FROM ATMOSYNC.STAGING.IOT_KAFKA_CLEAN I
    JOIN ATMOSYNC.ANALYTICS.DASHBOARD_MASTER D
        ON I.SHIPMENT_ID = REPLACE(D.SHIPMENT_ID, '"', '')
    ORDER BY I.SHIPMENT_ID, I.TIMESTAMP
""").to_pandas()


# =========================================================
# Caption: Clean GPS Data
# =========================================================

if not gps_df.empty:

    gps_df["SHIPMENT_ID"] = (
        gps_df["SHIPMENT_ID"]
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    gps_df["SOURCE"] = (
        gps_df["SOURCE"]
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    gps_df["DESTINATION"] = (
        gps_df["DESTINATION"]
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.strip()
    )


# =========================================================
# Caption: Shipment Selector
# =========================================================

if not gps_df.empty:

    shipment_options = sorted(
        gps_df["SHIPMENT_ID"].dropna().unique().tolist()
    )

    selected_shipment = st.selectbox(
        "Select Shipment",
        shipment_options,
        index=0
    )

    selected_gps = gps_df[
        gps_df["SHIPMENT_ID"] == selected_shipment
    ].copy()

    selected_gps = selected_gps.sort_values("TIMESTAMP")


    # =====================================================
    # Caption: Shipment Route Information
    # =====================================================

    shipment_info = selected_gps.iloc[0]

    info1, info2, info3, info4 = st.columns(4)

    with info1:
        st.metric(
            "Route",
            f"{shipment_info['SOURCE']} → {shipment_info['DESTINATION']}"
        )

    with info2:
        st.metric(
            "GPS Readings",
            f"{len(selected_gps):,}"
        )

    with info3:
        st.metric(
            "Risk",
            str(shipment_info["SPOILAGE_RISK"])
        )

    with info4:
        st.metric(
            "Latest Temperature",
            f"{float(selected_gps.iloc[-1]['TEMPERATURE']):.1f} °C"
        )


    # =====================================================
    # Caption: Build Actual GPS Path
    # =====================================================

    gps_path = [
        [float(lon), float(lat)]
        for lon, lat in zip(
            selected_gps["LONGITUDE"],
            selected_gps["LATITUDE"]
        )
    ]


    # =====================================================
    # Caption: Start and Latest GPS Positions
    # =====================================================

    start_point = selected_gps.iloc[0]
    latest_point = selected_gps.iloc[-1]


    start_df = pd.DataFrame([{
        "LATITUDE": float(start_point["LATITUDE"]),
        "LONGITUDE": float(start_point["LONGITUDE"]),
        "LABEL": "START"
    }])


    latest_df = pd.DataFrame([{
        "LATITUDE": float(latest_point["LATITUDE"]),
        "LONGITUDE": float(latest_point["LONGITUDE"]),
        "LABEL": "LATEST"
    }])


    # =====================================================
    # Caption: GPS Route Layer
    # =====================================================

    gps_route_layer = pdk.Layer(
        "PathLayer",
        data=[{"PATH": gps_path}],
        get_path="PATH",
        get_color=[38, 166, 255, 240],
        width_min_pixels=5,
        pickable=True
    )


    # =====================================================
    # Caption: GPS Reading Points
    # =====================================================

    gps_points_layer = pdk.Layer(
        "ScatterplotLayer",
        data=selected_gps,
        get_position="[LONGITUDE, LATITUDE]",
        get_radius=1800,
        get_fill_color=[56, 189, 248, 150],
        pickable=True,
        auto_highlight=True
    )


    # =====================================================
    # Caption: Start Marker
    # =====================================================

    start_layer = pdk.Layer(
        "ScatterplotLayer",
        data=start_df,
        get_position="[LONGITUDE, LATITUDE]",
        get_radius=7000,
        get_fill_color=[34, 197, 94, 255],
        pickable=True
    )


    # =====================================================
    # Caption: Latest Marker
    # =====================================================

    latest_layer = pdk.Layer(
        "ScatterplotLayer",
        data=latest_df,
        get_position="[LONGITUDE, LATITUDE]",
        get_radius=8500,
        get_fill_color=[239, 68, 68, 255],
        pickable=True
    )


    # =====================================================
    # Caption: GPS Map
    # =====================================================

    map_center_lat = float(selected_gps["LATITUDE"].mean())
    map_center_lon = float(selected_gps["LONGITUDE"].mean())


    st.pydeck_chart(
        pdk.Deck(
            map_style="dark",

            initial_view_state=pdk.ViewState(
                latitude=map_center_lat,
                longitude=map_center_lon,
                zoom=7,
                pitch=0,
                bearing=0
            ),

            layers=[
                gps_route_layer,
                gps_points_layer,
                start_layer,
                latest_layer
            ],

            tooltip={
                "html": """
                    <div>
                        <b>Shipment:</b> {SHIPMENT_ID}<br/>
                        <b>Time:</b> {TIMESTAMP}<br/>
                        <b>Temperature:</b> {TEMPERATURE} °C<br/>
                        <b>Humidity:</b> {HUMIDITY}%<br/>
                        <b>Vibration:</b> {VIBRATION}<br/>
                        <b>Risk:</b> {SPOILAGE_RISK}
                    </div>
                """,

                "style": {
                    "backgroundColor": "#111827",
                    "color": "white"
                }
            }
        ),
        height=650
    )


    st.caption(
        "🟢 Start position   •   🔴 Latest position   •   "
        "🔵 Recorded GPS movement"
    )


st.divider()


# =========================================================
# Caption: High Risk Shipment Details
# =========================================================

st.markdown(
    '<div class="section-title">🔴 High-Risk Shipments Requiring Attention</div>',
    unsafe_allow_html=True
)


high_risk_df = session.sql("""
    SELECT
        SHIPMENT_ID,
        CONTAINER_ID,
        VACCINE_TYPE,
        SOURCE,
        DESTINATION,
        SPOILAGE_RISK,
        OUT_OF_RANGE_PERCENT,
        AT_RISK_QUANTITY,
        POTENTIAL_FINANCIAL_IMPACT,
        RECOMMENDED_ACTION,
        REROUTING_RECOMMENDATION
    FROM ATMOSYNC.ANALYTICS.DASHBOARD_MASTER
    WHERE SPOILAGE_RISK = 'HIGH'
    ORDER BY
        POTENTIAL_FINANCIAL_IMPACT DESC,
        OUT_OF_RANGE_PERCENT DESC
""").to_pandas()


if not high_risk_df.empty:

    st.dataframe(
        high_risk_df,
        width="stretch",
        hide_index=True,
        height=450
    )


# =========================================================
# Caption: Business Insight
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">💡 Management Insight</div>',
    unsafe_allow_html=True
)

if not kpi_df.empty:

    high_risk_percentage = (
        high_risk / total_shipments * 100
        if total_shipments > 0
        else 0
    )

    st.info(
        f"""
        **{high_risk} of {total_shipments} shipments ({high_risk_percentage:.1f}%)**
        are currently classified as high risk.

        These shipments represent approximately
        **{at_risk_quantity:,} units** of potentially affected inventory
        and **₹{potential_exposure:,} of estimated financial exposure**
        under the project's assumed valuation model.

        Recommended operational focus: **prioritize high-risk shipments
        for immediate review and potential rerouting.**
        """
    )


# =========================================================
# Caption: Dashboard Footer
# =========================================================

st.caption(
    "AtmoSync • Real-Time Cold Chain Logistics & Spoilage Analytics"
)