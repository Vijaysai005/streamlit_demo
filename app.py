import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reynolds CPG Analytics Toolkit", layout="wide")

# --- CUSTOM CSS FOR HIGH-FIDELITY UI ---
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #F8F9FA; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0E1629;
        min-width: 280px !important;
    }
    
    /* Left-aligned Sidebar Buttons with Active State */
    .stButton > button {
        width: 100%;
        background-color: transparent;
        color: #AEB9C8;
        border: none;
        text-align: left;
        padding: 12px 20px;
        font-size: 16px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #1E293B;
        color: #FFFFFF;
        border: none;
    }
    .stButton > button:focus, .stButton > button:active {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: none;
    }

    /* Professional Headers */
    h1, h2, h3 { color: #1E293B; font-family: 'Inter', sans-serif; }
    
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'Data Management'

def set_page(page_name):
    st.session_state.page = page_name

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>Reynolds</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; margin-top:0;'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🗄️  Data Management"): set_page('Data Management')
    if st.button("📊  Unified Business Intelligence"): set_page('UBI')
    if st.button("📈  TPO Simulator"): set_page('TPO')
    if st.button("✨  Gen AI Assistant"): set_page('AI')
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 Reynolds Consumer Products")

# --- GAUGE COMPONENT FUNCTION ---
def draw_gauge(label, value, color="#2563EB"):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': label, 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E2E8F0",
            'steps': [
                {'range': [0, 70], 'color': '#FEE2E2'},
                {'range': [70, 90], 'color': '#FEF3C7'},
                {'range': [90, 100], 'color': '#DCFCE7'}],
        }
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig

# --- MODULE 1: DATA MANAGEMENT ---
if st.session_state.page == 'Data Management':
    st.title("Data Management Portal")
    
    st.subheader("Data Quality Scorecard")
    g1, g2, g3, g4 = st.columns(4)
    with g1: st.plotly_chart(draw_gauge("Nielsen POS", 98, "#10B981"), use_container_width=True)
    with g2: st.plotly_chart(draw_gauge("Internal Shipments", 100, "#10B981"), use_container_width=True)
    with g3: st.plotly_chart(draw_gauge("Trade Planner", 85, "#F59E0B"), use_container_width=True)
    with g4: st.plotly_chart(draw_gauge("IRI Data", 92, "#10B981"), use_container_width=True)
    
    st.markdown("---")
    st.subheader("SKU Mapping Engine")
    col_f1, col_f2 = st.columns([2, 1])
    search = col_f1.text_input("🔍 Search by SKU, description, or retailer...", placeholder="e.g. WMT-RF-200")
    status_filter = col_f2.selectbox("Status", ["All", "Mapped", "Unmapped"])
    
    mapping_df = pd.DataFrame({
        "Retailer": ["Walmart", "Target", "Kroger", "CVS", "Walmart", "Kroger"],
        "Retailer SKU": ["WMT-RF-200-01", "TGT-TB-30-50", "KRG-PW-100", "CVS-AF-75", "WMT-P-50", "KRG-F-12"],
        "Product Description": ["Reynolds Wrap Aluminum Foil 200sqft", "Hefty Ultra Strong 30Gal", "Reynolds Plastic Wrap 100sqft", "Reynolds Foil 75sqft", "Reynolds Parchment 50sqft", "Reynolds Foil 12sqft"],
        "SAP Material #": ["1000234567", "1000987654", "1000556677", "1000334455", "1000112233", "Pending"],
        "Status": ["Mapped", "Mapped", "Unmapped", "Mapped", "Mapped", "Unmapped"]
    })
    st.dataframe(mapping_df, use_container_width=True, hide_index=True)

# --- MODULE 2: UNIFIED BUSINESS INTELLIGENCE ---
elif st.session_state.page == 'UBI':
    st.title("Unified Business Intelligence")
    ubi_tabs = st.tabs(["Enterprise KPI Scorecard", "Shipment to Shelf", "SKU & Customer Profitability"])
    
    with ubi_tabs[0]:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Market Share", "23.4%", "1.2%", help="Target: 22.5%")
        k2.metric("Velocity", "4.2", "-0.3", help="Target: 4.5")
        k3.metric("Gross Margin", "34.8%", "2.1%", help="Target: 33.0%")
        k4.metric("Trade ROI", "2.8x", "0.4x", help="Target: 2.5x")
        
        st.subheader("Market Share Tracker (12 Month)")
        st.line_chart(np.random.randn(12, 3) + [24, 19, 16])

    with ubi_tabs[1]:
        st.subheader("Inventory Health Matrix (Days of Supply)")
        dos_data = pd.DataFrame({
            "Retailer": ["Walmart", "Target", "Kroger", "CVS"],
            "Aluminum Foil": [18, 25, 12, 8],
            "Trash Bags": [22, 19, 16, 11],
            "Plastic Wrap": [15, 21, 14, 9]
        })
        st.table(dos_data.style.background_gradient(cmap='RdYlGn', subset=["Aluminum Foil", "Trash Bags", "Plastic Wrap"]))
        st.error("🚨 **OOS Risk Alert**: Reynolds Wrap 200sqft at CVS (8 Days Supply) - Critical Risk Level")

    with ubi_tabs[2]:
        st.subheader("Margin Waterfall")
        # Simplified representation of the waterfall logic
        st.image("https://upload.wikimedia.org", width=700) # Placeholder
        st.caption("Waterfall details: Gross Sales -> COGS -> Trade Spend -> Net Margin")

# --- MODULE 3: TPO SIMULATOR ---
elif st.session_state.page == 'TPO':
    st.title("TPO Simulator")
    sim_col1, sim_col2 = st.columns([1, 2])
    
    with sim_col1:
        st.info("Promo Parameters")
        st.selectbox("Retailer", ["Walmart", "Target", "Kroger"])
        st.selectbox("Product", ["Reynolds Wrap 200sqft", "Hefty Ultra Strong 30Gal"])
        st.selectbox("Discount Type", ["% Off", "BOGO", "TPR"])
        st.number_input("Discount Amount (%)", value=20)
        st.number_input("Duration (weeks)", value=2)
        st.button("Run Simulation", type="primary", use_container_width=True)

    with sim_col2:
        st.subheader("Scenario Comparison")
        comp_df = pd.DataFrame({
            "Metric": ["Volume", "Revenue ($)", "Margin ($)", "ROI"],
            "Baseline": ["42,000", "$168k", "$58.8k", "0.0x"],
            "Scenario 1 (Moderate)": ["56,700 (+35%)", "$208k", "$45k", "1.6x"],
            "Scenario 2 (Aggressive)": ["65,100 (+55%)", "$229k", "$38k", "0.9x"]
        })
        st.table(comp_df)
        st.success("✅ **Recommendation**: Scenario 1 offers the best balance of volume lift and ROI at 1.6x.")

# --- MODULE 4: GEN AI ASSISTANT ---
elif st.session_state.page == 'AI':
    st.title("Gen AI NL Assistant")
    ai_left, ai_right = st.columns([2, 1])
    
    with ai_left:
        st.chat_message("assistant").write("Hello! I'm your CPG Analytics Assistant. Ask me anything about Reynolds market performance or trade effectiveness.")
        st.text_input("Ask a question about your CPG data...", placeholder="e.g., Show me top 5 margin draggers at Walmart last month")
        st.caption("Quick questions: Top margin draggers | Market share trends | Best promo ROI")

    with ai_right:
        st.markdown("### Automated Insights")
        st.warning("**Commodity Cost Alert**\nAluminum costs rose 3%, impacting foil margins. Expected Q2 impact: -$1.2M")
        st.info("**Retailer Insight**\nWalmart promo ROI exceeded expectations by 0.4x last period.")
