import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# ----------------------------------------------------
# THEME STYLING (Reynolds Enterprise Aesthetic)
# ----------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0A1F44;
}
[data-testid="stSidebar"] * {
    color: white;
}
.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# MOCK DATA
# ----------------------------------------------------
np.random.seed(42)

products = ["Reynolds Wrap 200sqft", "Hefty Trash Bags 30ct", 
            "Reynolds Plastic Wrap", "Hefty Food Containers"]

retailers = ["Walmart", "Target", "Kroger"]
business_units = ["Cooking & Baking", "Waste & Storage"]

dates = pd.date_range(end=datetime.today(), periods=12, freq="M")

sales_data = pd.DataFrame({
    "Month": np.tile(dates, 3),
    "Brand": np.repeat(["Reynolds", "Competitor", "Private Label"], 12),
    "Market Share": np.random.uniform(20, 40, 36)
})

shipment_data = pd.DataFrame({
    "Month": dates,
    "Shipments": np.random.randint(5000, 9000, 12),
    "POS": np.random.randint(4500, 8500, 12)
})

profit_data = pd.DataFrame({
    "SKU": products,
    "Sales Volume": np.random.randint(10000, 50000, 4),
    "Gross Margin %": np.random.uniform(15, 45, 4)
})

# ----------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------
st.sidebar.title("Reynolds CPG Toolkit")
module = st.sidebar.radio("Navigation", [
    "Data Management Portal",
    "Power BI Dashboard",
    "TPO Simulator",
    "Gen AI NL Assistant"
])

# ----------------------------------------------------
# MODULE 1: DATA MANAGEMENT PORTAL
# ----------------------------------------------------
if module == "Data Management Portal":
    st.title("Data Management Portal")

    st.subheader("SKU Mapping Engine")

    sku_map = pd.DataFrame({
        "Retailer SKU Code": ["WM123", "TG456", "KR789"],
        "Retailer Description": ["Foil 200sqft", "Trash Bags 30ct", "Plastic Wrap"],
        "SAP Material Number": ["SAP001", "SAP002", ""],
        "Status": ["Mapped", "Mapped", "Unmapped"]
    })

    st.dataframe(sku_map, use_container_width=True)

    st.subheader("Data Quality Scorecard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Nielsen POS", "98%", "▲ 1%", delta_color="normal")
    col2.metric("Internal Shipments", "100%", "Stable")
    col3.metric("Trade Planner", "85%", "▼ 3%", delta_color="inverse")

# ----------------------------------------------------
# MODULE 2: POWER BI DASHBOARD
# ----------------------------------------------------
elif module == "Power BI Dashboard":
    st.title("Enterprise Analytics Dashboard")

    page = st.tabs([
        "Enterprise KPI Scorecard",
        "Shipment to Shelf",
        "SKU & Customer Profitability"
    ])

    # ------------------------------------------------
    # PAGE 1: KPI SCORECARD
    # ------------------------------------------------
    with page[0]:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Market Share", "32.4%", "+1.2% vs Target")
        col2.metric("Velocity", "8.3 Units/Store/Wk", "+0.4")
        col3.metric("Gross Margin", "28.5%", "-0.8%")
        col4.metric("Trade ROI", "2.8x", "+0.3")

        st.subheader("Market Share Tracker")

        fig = px.line(sales_data, x="Month", y="Market Share", color="Brand")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Brand & BU Scorecard")
        bu_table = pd.DataFrame({
            "Business Unit": business_units,
            "Revenue ($M)": [220, 180],
            "Margin %": [32, 25]
        })
        st.dataframe(bu_table, use_container_width=True)

    # ------------------------------------------------
    # PAGE 2: SHIPMENT TO SHELF
    # ------------------------------------------------
    with page[1]:
        st.subheader("Internal Shipments vs POS")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=shipment_data["Month"], y=shipment_data["Shipments"], name="Shipments"))
        fig.add_trace(go.Scatter(x=shipment_data["Month"], y=shipment_data["POS"], name="POS Consumption"))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Inventory Health Matrix")

        dos = pd.DataFrame(
            np.random.randint(10, 60, (3, 4)),
            index=retailers,
            columns=products
        )
        st.dataframe(dos.style.background_gradient(cmap="Blues"), use_container_width=True)

        st.subheader("OOS Risk Radar")
        st.warning("High OOS Risk: Reynolds Wrap 200sqft at Kroger (Velocity Spike + Low Inventory)")

    # ------------------------------------------------
    # PAGE 3: PROFITABILITY
    # ------------------------------------------------
    with page[2]:
        st.subheader("Drivers & Draggers")

        fig = px.scatter(profit_data,
                         x="Sales Volume",
                         y="Gross Margin %",
                         text="SKU",
                         size="Sales Volume",
                         color="Gross Margin %")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Margin Waterfall")

        waterfall = go.Figure(go.Waterfall(
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=["Gross Revenue", "COGS", "Trade Spend", "Allowances", "Net Margin"],
            y=[100, -40, -20, -10, 0]
        ))
        st.plotly_chart(waterfall, use_container_width=True)

        st.subheader("Trade ROI Calculator")
        roi_table = pd.DataFrame({
            "Retailer": retailers,
            "Spend ($)": [50000, 40000, 35000],
            "Incremental Lift ($)": [150000, 90000, 80000],
            "ROI": [3.0, 2.25, 2.28]
        })
        st.dataframe(roi_table, use_container_width=True)

# ----------------------------------------------------
# MODULE 3: TPO SIMULATOR
# ----------------------------------------------------
elif module == "TPO Simulator":
    st.title("Trade Promotion Optimization Simulator")

    col1, col2 = st.columns([1,2])

    with col1:
        retailer = st.selectbox("Select Retailer", retailers)
        product = st.selectbox("Select Product", products)
        discount = st.selectbox("Discount Type", ["TPR", "BOGO", "Feature"])
        duration = st.slider("Duration (Weeks)", 1, 8, 4)

    with col2:
        baseline = {"Volume": 10000, "Revenue": 120000, "Spend": 0, "ROI": 1.0}
        scenario1 = {"Volume": 15000, "Revenue": 180000, "Spend": 40000, "ROI": 2.5}
        scenario2 = {"Volume": 17000, "Revenue": 200000, "Spend": 60000, "ROI": 2.2}

        comparison = pd.DataFrame([baseline, scenario1, scenario2],
                                  index=["Baseline", "Scenario A", "Scenario B"])
        st.dataframe(comparison, use_container_width=True)

# ----------------------------------------------------
# MODULE 4: GEN AI ASSISTANT
# ----------------------------------------------------
elif module == "Gen AI NL Assistant":
    st.title("Enterprise AI Business Assistant")

    col1, col2 = st.columns([2,1])

    with col1:
        user_input = st.text_input("Ask a business question...")
        if user_input:
            st.success("Top 5 Margin Dragging SKUs at Kroger Last Month:")
            sample = profit_data.sort_values("Gross Margin %").head(2)
            st.dataframe(sample)

    with col2:
        st.subheader("Automated Insights Feed")
        st.info("Aluminum commodity costs rose 3%, impacting foil margins.")
        st.info("Velocity at Target increased 5% post feature promotion.")
        st.warning("OOS risk rising at Walmart for Trash Bags.")
