import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Reynolds Consumer Products - Centralized Business Dashboard")

# -----------------------------
# Generate Dummy Data
# -----------------------------
np.random.seed(42)

dates = pd.date_range(start="2024-01-01", periods=180)

regions = ["North", "South", "East", "West"]
products = ["Aluminum Foil", "Hefty Trash Bags", "Wax Paper", "Food Containers"]

data = pd.DataFrame({
    "Date": np.random.choice(dates, 1000),
    "Region": np.random.choice(regions, 1000),
    "Product": np.random.choice(products, 1000),
    "Inventory": np.random.randint(500, 5000, 1000),
    "Orders_Placed": np.random.randint(50, 500, 1000),
    "Orders_Fulfilled": np.random.randint(40, 450, 1000),
    "Forecast_Demand": np.random.randint(60, 550, 1000),
    "Revenue": np.random.randint(5000, 50000, 1000),
    "Cost": np.random.randint(3000, 40000, 1000),
    "Promotion_Spend": np.random.randint(500, 5000, 1000)
})

data["Profit"] = data["Revenue"] - data["Cost"]
data["Fulfillment_Rate"] = data["Orders_Fulfilled"] / data["Orders_Placed"]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect("Select Region", regions, default=regions)
selected_product = st.sidebar.multiselect("Select Product", products, default=products)

filtered_data = data[
    (data["Region"].isin(selected_region)) &
    (data["Product"].isin(selected_product))
]

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${filtered_data['Revenue'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_data['Profit'].sum():,.0f}")
col3.metric("Avg Fulfillment Rate", f"{filtered_data['Fulfillment_Rate'].mean():.2%}")
col4.metric("Total Promotion Spend", f"${filtered_data['Promotion_Spend'].sum():,.0f}")

st.markdown("---")

# -----------------------------
# Drill Down Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Inventory", "Order Details", "Financials", "Promotions"]
)

# -----------------------------
# Inventory Tab
# -----------------------------
with tab1:
    st.subheader("Inventory Analysis")
    inv_summary = filtered_data.groupby("Product")["Inventory"].sum().reset_index()
    fig = px.bar(inv_summary, x="Product", y="Inventory", color="Product")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Order Details Tab
# -----------------------------
with tab2:
    st.subheader("Order Analysis")

    order_summary = filtered_data.groupby("Date")[[
        "Orders_Placed", "Orders_Fulfilled", "Forecast_Demand"
    ]].sum().reset_index()

    fig = px.line(order_summary, x="Date", y=[
        "Orders_Placed", "Orders_Fulfilled", "Forecast_Demand"
    ])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Drill Down by Region")
    region_summary = filtered_data.groupby("Region")[[
        "Orders_Placed", "Orders_Fulfilled"
    ]].sum().reset_index()

    fig2 = px.bar(region_summary, x="Region",
                  y=["Orders_Placed", "Orders_Fulfilled"],
                  barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Financials Tab
# -----------------------------
with tab3:
    st.subheader("Financial Performance")

    fin_summary = filtered_data.groupby("Region")[[
        "Revenue", "Cost", "Profit"
    ]].sum().reset_index()

    fig = px.bar(fin_summary, x="Region",
                 y=["Revenue", "Cost", "Profit"],
                 barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Promotions Tab
# -----------------------------
with tab4:
    st.subheader("Promotion Effectiveness")

    promo_summary = filtered_data.groupby("Product")[[
        "Promotion_Spend", "Revenue"
    ]].sum().reset_index()

    fig = px.scatter(promo_summary,
                     x="Promotion_Spend",
                     y="Revenue",
                     size="Revenue",
                     color="Product")
    st.plotly_chart(fig, use_container_width=True)
