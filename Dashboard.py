import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set page layout to wide
st.set_page_config(page_title="E-Commerce Complete Dashboard", layout="wide")
st.title("🛍️ E-Commerce Sales Performance Dashboard")
st.markdown("Created by **Vernon Chinkuli**")

# Load Cleaned Data
@st.cache_data
def load_data():
    # Reads your new lightweight file directly from your repository folder
    df = pd.read_csv('Cleaned_Online_Retail_Small.csv')
    
    # Structure columns accurately for metrics and charts
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    
    return df

# Run the function to generate the main dataframe
df = load_data()

# --- SIDEBAR FILTER ---
st.sidebar.header("Filter Options")
selected_country = st.sidebar.selectbox("Select a Country", options=["All"] + list(df['Country'].unique()))

# Apply filter based on user selection
if selected_country != "All":
    df_filtered = df[df['Country'] == selected_country]
else:
    df_filtered = df

# --- KEY METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Revenue", f"${df_filtered['Revenue'].sum():,.2f}")
with col2:
    st.metric("Total Items Sold", f"{df_filtered['Quantity'].sum():,}")
with col3:
    st.metric("Unique Transactions", f"{df_filtered['InvoiceNo'].nunique():,}")

st.markdown("---")

# --- ROW 1: TWO COLUMNS ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("🌍 Top 5 Revenue-Generating Countries")
    top_countries = df_filtered.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(5)
    fig1, ax1 = plt.subplots(figsize=(6, 3.5))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="viridis", ax=ax1)
    ax1.set_xlabel("Total Revenue ($)")
    st.pyplot(fig1)

with row1_col2:
    st.subheader("📦 Top 10 Best Selling Products")
    top_products = df_filtered.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
    fig2, ax2 = plt.subplots(figsize=(6, 3.5))
    sns.barplot(x=top_products.values, y=top_products.index, palette="magma", ax=ax2)
    ax2.set_xlabel("Total Quantity Sold")
    st.pyplot(fig2)

st.markdown("---")

# --- ROW 2: TWO COLUMNS ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("📈 Monthly Sales Revenue Trend")
    monthly_sales = df_filtered.groupby('YearMonth')['Revenue'].sum().reset_index()
    monthly_sales['YearMonth'] = monthly_sales['YearMonth'].astype(str)
    fig3, ax3 = plt.subplots(figsize=(6, 3.5))
    ax3.plot(monthly_sales['YearMonth'], monthly_sales['Revenue'], marker='o', color='crimson', linewidth=2)
    plt.xticks(rotation=45)
    st.pyplot(fig3)

with row2_col2:
    st.subheader("💰 Product Unit Price Distribution")
    fig4, ax4 = plt.subplots(figsize=(6, 3.5))
    sns.histplot(df_filtered[df_filtered['UnitPrice'] < 20]['UnitPrice'], bins=30, color="skyblue", kde=True, ax=ax4)
    ax4.set_xlabel("Unit Price ($)")
    st.pyplot(fig4)

st.markdown("---")

# --- ROW 3: FULL WIDTH ---
st.subheader("🛒 Customer Purchasing Behavior: Distribution of Quantities Ordered")
fig5, ax5 = plt.subplots(figsize=(12, 2.5))
sns.boxplot(x=df_filtered[df_filtered['Quantity'] < 50]['Quantity'], color="lightgreen", ax=ax5)
ax5.set_xlabel("Quantity Ordered per Line Item")
st.pyplot(fig5)
