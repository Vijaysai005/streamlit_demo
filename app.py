import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(layout="wide")

# ----------------------------------------------------
# STYLE
# ----------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0A1F44;
}
[data-testid="stSidebar"] * {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# MOCK ENTERPRISE DATA
# ----------------------------------------------------
np.random.seed(42)

products = ["Reynolds Wrap 200sqft", "Hefty Trash Bags 30ct",
            "Reynolds Plastic Wrap", "Hefty Food Containers"]

retailers = ["Walmart", "Target", "Kroger"]
regions = ["North", "South", "East", "West"]

dates = pd.date_range("2024-01-01", periods=180)

data = pd.DataFrame({
    "Date": np.random.choice(dates, 2000),
    "Retailer": np.random.choice(retailers, 2000),
    "Region": np.random.choice(regions, 2000),
    "Product": np.random.choice(products, 2000),
    "Revenue": np.random.randint(5000, 50000, 2000),
    "COGS": np.random.randint(3000, 30000, 2000),
    "Trade Spend": np.random.randint(500, 5000, 2000),
    "Volume": np.random.randint(1000, 10000, 2000)
})

data["Gross Margin %"] = ((data["Revenue"] - data["COGS"]) / data["Revenue"]) * 100

# ----------------------------------------------------
# GLOBAL FILTERS (Apply Everywhere)
# ----------------------------------------------------
st.sidebar.title("Reynolds CPG Toolkit")

# ----------------------------------------------------
# MODULE NAVIGATION
# ----------------------------------------------------
module = st.sidebar.radio("Navigation", [
    "Data Management Portal",
    "Power BI Dashboard",
    "TPO Simulator",
    "Gen AI NL Assistant"
])


st.sidebar.markdown("## Global Filters")

selected_retailer = st.sidebar.multiselect(
    "Retailer", retailers, default=[retailers[0]]
)

selected_region = st.sidebar.multiselect(
    "Region", regions, default=[regions[0]]
)

selected_product = st.sidebar.multiselect(
    "Product", products, default=[products[0]]
)

date_range = st.sidebar.date_input(
    "Date Range",
    [data["Date"].min(), data["Date"].max()]
)

# Apply Filters
filtered_data = data[
    (data["Retailer"].isin(selected_retailer)) &
    (data["Region"].isin(selected_region)) &
    (data["Product"].isin(selected_product)) &
    (data["Date"] >= pd.to_datetime(date_range[0])) &
    (data["Date"] <= pd.to_datetime(date_range[1]))
]


# ====================================================
# MODULE 1: DATA MANAGEMENT
# ====================================================
if module == "Data Management Portal":

    st.title("Data Management Portal")

    st.subheader("SKU Mapping Engine")

    sku_map = pd.DataFrame({
        "Retailer SKU": ["WM123", "TG456", "KR789"],
        "Retailer": ["Walmart", "Target", "Kroger"],
        "SAP Material": ["SAP001", "SAP002", ""],
        "Status": ["Mapped", "Mapped", "Unmapped"]
    })

    st.dataframe(sku_map, use_container_width=True)

    st.subheader("Data Quality Scorecard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Data Freshness", "97%")
    col2.metric("Accuracy", "99%")
    col3.metric("Completeness", "91%")

# ====================================================
# MODULE 2: POWER BI DASHBOARD
# ====================================================
elif module == "Power BI Dashboard":

    st.title("Enterprise Analytics")

    page = st.tabs([
        "Enterprise KPI Scorecard",
        "Shipment to Shelf",
        "SKU & Customer Profitability"
    ])

    # PAGE 1
    with page[0]:

        total_revenue = filtered_data["Revenue"].sum()
        avg_margin = filtered_data["Gross Margin %"].mean()
        total_volume = filtered_data["Volume"].sum()
        total_trade = filtered_data["Trade Spend"].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Revenue", f"${total_revenue:,.0f}")
        col2.metric("Gross Margin %", f"{avg_margin:.1f}%")
        col3.metric("Volume", f"{total_volume:,.0f}")
        col4.metric("Trade Spend", f"${total_trade:,.0f}")

        trend = filtered_data.groupby("Date")["Revenue"].sum().reset_index()
        fig = px.line(trend, x="Date", y="Revenue", title="Revenue Trend")
        st.plotly_chart(fig, use_container_width=True)

    # PAGE 2
    with page[1]:

        ship_vs_pos = filtered_data.groupby("Date").agg({
            "Revenue": "sum",
            "Volume": "sum"
        }).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ship_vs_pos["Date"],
                                 y=ship_vs_pos["Revenue"],
                                 name="Shipments"))
        fig.add_trace(go.Scatter(x=ship_vs_pos["Date"],
                                 y=ship_vs_pos["Volume"],
                                 name="POS Consumption"))
        st.plotly_chart(fig, use_container_width=True)

        heatmap_data = filtered_data.pivot_table(
            values="Volume",
            index="Retailer",
            columns="Product",
            aggfunc="sum"
        )

        st.dataframe(
            heatmap_data.style.background_gradient(cmap="Blues"),
            use_container_width=True
        )

    # PAGE 3
    with page[2]:

        st.subheader("SKU & Customer Profitability")
    
        if filtered_data.empty:
            st.warning("No data available for selected filters.")
        else:
    
            # ------------------------------------------------
            # AGGREGATED PROFIT DATA
            # ------------------------------------------------
            profit_summary = filtered_data.groupby("Product").agg({
                "Revenue": "sum",
                "COGS": "sum",
                "Trade Spend": "sum",
                "Volume": "sum",
                "Gross Margin %": "mean"
            }).reset_index()
    
            # ------------------------------------------------
            # 1️⃣ MARGIN WATERFALL
            # ------------------------------------------------
            st.markdown("### Margin Waterfall")
    
            total_revenue = filtered_data["Revenue"].sum()
            total_cogs = filtered_data["COGS"].sum()
            total_trade = filtered_data["Trade Spend"].sum()
            net_margin = total_revenue - total_cogs - total_trade
    
            waterfall = go.Figure(go.Waterfall(
                measure=["absolute", "relative", "relative", "total"],
                x=["Gross Revenue", "COGS", "Trade Spend", "Net Margin"],
                y=[total_revenue, -total_cogs, -total_trade, net_margin],
                connector={"line": {"color": "gray"}},
            ))
    
            waterfall.update_layout(title="Revenue to Net Margin Breakdown")
    
            st.plotly_chart(waterfall, use_container_width=True)
    
            # ------------------------------------------------
            # 2️⃣ DRIVERS & DRAGGERS
            # ------------------------------------------------
            st.markdown("### Drivers & Draggers")
    
            fig = px.scatter(
                profit_summary,
                x="Volume",
                y="Gross Margin %",
                size="Revenue",
                color="Gross Margin %",
                text="Product",
                title="Sales Volume vs Gross Margin %",
                color_continuous_scale="RdYlGn"
            )
    
            fig.update_traces(textposition="top center")
    
            st.plotly_chart(fig, use_container_width=True)
    
            st.caption("""
            • Top Right = High Volume + High Margin (Profit Drivers)  
            • Bottom Right = High Volume + Low Margin (Margin Draggers)  
            """)
    
            # ------------------------------------------------
            # 3️⃣ TRADE ROI CALCULATOR
            # ------------------------------------------------
            st.markdown("### Trade ROI Calculator")
    
            trade_summary = filtered_data.groupby(
                ["Retailer", "Product"]
            ).agg({
                "Trade Spend": "sum",
                "Revenue": "sum"
            }).reset_index()
    
            # Simulate Incremental Lift
            trade_summary["Incremental Lift"] = trade_summary["Revenue"] * 0.15
    
            trade_summary["ROI"] = (
                trade_summary["Incremental Lift"] /
                trade_summary["Trade Spend"]
            ).round(2)
    
            st.dataframe(trade_summary.sort_values("ROI", ascending=False),
                         use_container_width=True)
    
            # Highlight risk
            low_roi = trade_summary[trade_summary["ROI"] < 1]
    
            if not low_roi.empty:
                st.warning("⚠ Trade events below 1.0 ROI detected — review spend efficiency.")
            else:
                st.success("All trade events generating positive ROI.")
# ====================================================
# MODULE 3: TPO SIMULATOR
# ====================================================
elif module == "TPO Simulator":

    st.title("Trade Promotion Simulator")

    col1, col2 = st.columns([1,2])

    with col1:
        retailer = st.selectbox("Retailer", selected_retailer)
        product = st.selectbox("Product", selected_product)
        discount = st.selectbox("Discount Type", ["TPR", "BOGO", "Feature"])
        duration = st.slider("Duration (Weeks)", 1, 8, 4)

    with col2:
        baseline = filtered_data[
            (filtered_data["Retailer"] == retailer) &
            (filtered_data["Product"] == product)
        ]

        base_rev = baseline["Revenue"].sum()
        simulated_rev = base_rev * (1 + 0.25)

        comparison = pd.DataFrame({
            "Baseline Revenue": [base_rev],
            "Simulated Revenue (+25%)": [simulated_rev]
        })

        st.dataframe(comparison)

# ====================================================
# MODULE 4: GEN AI ASSISTANT
# ====================================================
elif module == "Gen AI NL Assistant":

    st.title("Enterprise AI Assistant")

    user_query = st.text_input("Ask a question")

    if user_query:
        result = filtered_data.groupby("Product")["Gross Margin %"].mean().sort_values().head(3)
        st.write("Top Margin Draggers:")
        st.dataframe(result.reset_index())

    st.subheader("Automated Insights")
    st.info("Foil margins declining in South region.")
    st.warning("High trade spend at Walmart impacting ROI.")
