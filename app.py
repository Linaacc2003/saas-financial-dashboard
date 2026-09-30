import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="SaaS Financial Dashboard", page_icon="📊", layout="wide")

# Title and description
st.title("📊 B2B SaaS Executive Financial Dashboard")
st.markdown("This interactive dashboard tracks key subscription metrics, revenue growth, and churn for executive decision-making.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('saas_data.csv')

df = load_data()

# Data preprocessing
df['Signup_Date'] = pd.to_datetime(df['Signup_Date'])
df['Month'] = df['Signup_Date'].dt.to_period('M').astype(str)

# Sidebar filters
st.sidebar.header("Dashboard Filters")
selected_tier = st.sidebar.multiselect(
    "Select Subscription Tier(s):",
    options=df['Subscription_Tier'].unique(),
    default=df['Subscription_Tier'].unique()
)

# Filter dataframe based on sidebar
filtered_df = df[df['Subscription_Tier'].isin(selected_tier)]

# --- TOP METRICS ROW ---
total_mrr = filtered_df[filtered_df['Status'] == 'Active']['Monthly_Fee'].sum()
active_users = len(filtered_df[filtered_df['Status'] == 'Active'])
total_churned = len(filtered_df[filtered_df['Status'] == 'Churned'])
churn_rate = (total_churned / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Monthly Recurring Revenue (MRR)", f"${total_mrr:,.2f}")
col2.metric("Active Customers", f"{active_users:,}")
col3.metric("Estimated Churn Rate", f"{churn_rate:.2f}%")

st.markdown("---")

# --- CHARTS SECTION ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 MRR Growth Over Time")
    mrr_trend = filtered_df[filtered_df['Status'] == 'Active'].groupby('Month')['Monthly_Fee'].sum().reset_index()
    fig_mrr = px.line(mrr_trend, x='Month', y='Monthly_Fee', markers=True, title="Monthly Revenue Trajectory")
    st.plotly_chart(fig_mrr, use_container_width=True)

with col_right:
    st.subheader("👥 Customer Distribution by Tier")
    tier_counts = filtered_df['Subscription_Tier'].value_counts().reset_index()
    tier_counts.columns = ['Tier', 'Count']
    fig_tier = px.bar(tier_counts, x='Tier', y='Count', color='Tier', title="Active vs Churned Signups by Tier")
    st.plotly_chart(fig_tier, use_container_width=True)

# Raw data preview
with st.expander("🔍 View Raw Underlying Data"):
    st.dataframe(filtered_df)