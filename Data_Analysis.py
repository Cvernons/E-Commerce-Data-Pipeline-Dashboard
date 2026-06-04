import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("==================================================")
# Load our newly cleaned dataset
df = pd.read_csv('Cleaned_Online_Retail.csv')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create a Total Revenue column for financial analyses
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# ------------------------------------------------
# TASK 3: GENERATE SUMMARY STATISTICS
# ------------------------------------------------
print("--- TASK 3: NUMERICAL SUMMARY STATISTICS ---")
print(df[['Quantity', 'UnitPrice', 'Revenue']].describe())
print("==================================================\n")


# ------------------------------------------------
# TASK 3 & 4: EXPLORATORY DATA ANALYSIS & VISUALIZATIONS
# ------------------------------------------------
print("--- Generating Exploratory Analysis & Visualizations ---")

# Set a clean layout style for graphs
sns.set_theme(style="whitegrid")

# Analysis 1: Top 5 Highest Revenue-Generating Countries
plt.figure(figsize=(10, 5))
top_countries = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(5)
sns.barplot(x=top_countries.values, y=top_countries.index, palette="viridis")
plt.title("Top 5 Highest Revenue-Generating Countries")
plt.xlabel("Total Revenue ($)")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig('1_top_revenue_countries.png')
plt.close()
print("-> Chart 1 Saved: 1_top_revenue_countries.png")

# Analysis 2: Top 10 Best-Selling Products (By Quantity sold)
plt.figure(figsize=(10, 5))
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top_products.values, y=top_products.index, palette="magma")
plt.title("Top 10 Best-Selling Products by Quantity")
plt.xlabel("Total Quantity Sold")
plt.ylabel("Product Description")
plt.tight_layout()
plt.savefig('2_top_selling_products.png')
plt.close()
print("-> Chart 2 Saved: 2_top_selling_products.png")

# Analysis 3: Distribution of Order Unit Prices (Histogram to view common item pricing)
plt.figure(figsize=(10, 5))
# Filtering out extreme outliers (> $20) just so the visual distribution is clear and highly readable
sns.histplot(df[df['UnitPrice'] < 20]['UnitPrice'], bins=30, kde=True, color="skyblue")
plt.title("Distribution of Product Unit Prices (Items < $20)")
plt.xlabel("Unit Price ($)")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.savefig('3_unit_price_distribution.png')
plt.close()
print("-> Chart 3 Saved: 3_unit_price_distribution.png")

# Analysis 4: Monthly Sales Trends (Time-Series Analysis)
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
monthly_sales = df.groupby('YearMonth')['Revenue'].sum().reset_index()
monthly_sales['YearMonth'] = monthly_sales['YearMonth'].astype(str)

plt.figure(figsize=(12, 5))
plt.plot(monthly_sales['YearMonth'], monthly_sales['Revenue'], marker='o', color='crimson', linewidth=2)
plt.title("Monthly Sales Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('4_monthly_sales_trend.png')
plt.close()
print("-> Chart 4 Saved: 4_monthly_sales_trend.png")

# Analysis 5: Customer Purchasing Behavior (Quantity per transaction line item)
plt.figure(figsize=(8, 4))
sns.boxplot(x=df[df['Quantity'] < 50]['Quantity'], color="lightgreen")
plt.title("Customer Purchasing Behavior: Distribution of Quantities Ordered per Item")
plt.xlabel("Quantity Ordered in a Single Line Item")
plt.tight_layout()
plt.savefig('5_quantity_purchasing_behavior.png')
plt.close()
print("-> Chart 5 Saved: 5_quantity_purchasing_behavior.png")

print("\n==================================================")
print("SUCCESS: Summary statistics calculated and all 5 charts saved!")
print("==================================================")