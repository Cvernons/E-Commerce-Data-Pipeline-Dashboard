import pandas as pd

print("==================================================")
print("   E-COMMERCE DATA CLEANING & UNDERSTANDING       ")
print("==================================================\n")

# ------------------------------------------------
# TASK 1: DATASET UNDERSTANDING
# ------------------------------------------------
# Loading with correct text encoding for retail transaction files
df = pd.read_csv('OnlineRetail.csv', encoding='ISO-8859-1')

print("--- TASK 1: DATASET STRUCTURE ---")
rows, cols = df.shape
print(f"Number of Rows: {rows}")
print(f"Number of Columns: {cols}")

print("\n--- DATA TYPES ---")
print(df.dtypes)

# Identify feature types automatically
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = df.select_dtypes(include=['object']).columns.tolist()
print(f"\nNumerical Features: {numerical_features}")
print(f"Categorical Features: {categorical_features}")
print(f"Possible Unique Identifier: 'InvoiceNo' (Transaction level) or 'CustomerID' (User level)")

print("\n--- FIRST 3 ROWS OF RAW DATA ---")
print(df.head(3))


# ------------------------------------------------
# TASK 2: DATA CLEANING
# ------------------------------------------------
print("\n==================================================")
print("--- TASK 2: STARTING CLEANING PROCESS ---")
print("==================================================")

# 1. Track Missing Values
missing_before = df.isnull().sum()
print("\n[1] Missing Values Found Per Column:")
print(missing_before[missing_before > 0])

# Action: Drop rows where CustomerID is missing
df_clean = df.dropna(subset=['CustomerID']).copy()

# 2. Track & Remove Duplicate Records
duplicates_found = df_clean.duplicated().sum()
df_clean.drop_duplicates(inplace=True)

# 3. Standardization
# Convert InvoiceDate string to actual datetime format
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
# Clean text spaces and force uppercase for product descriptions
df_clean['Description'] = df_clean['Description'].str.strip().str.upper()
df_clean['Country'] = df_clean['Country'].str.strip()

# 4. Data Validation & Outlier Handling
# Filter for > 0 to establish a clean baseline of completed sales transactions.
invalid_quantity = (df_clean['Quantity'] <= 0).sum()
invalid_price = (df_clean['UnitPrice'] <= 0).sum()

df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]


# ------------------------------------------------
# CLEANING SUMMARY TABLE
# ------------------------------------------------
print("\n--- CLEANING SUMMARY LOG ---")
summary_data = {
    "Issue Found": [
        "Missing Customer IDs", 
        "Duplicate Rows", 
        "Invalid/Negative Quantities", 
        "Zero/Negative Unit Prices", 
        "Inconsistent Date/Text Format"
    ],
    "Action Taken": [
        f"Removed {missing_before['CustomerID']} rows with missing IDs",
        f"Removed {duplicates_found} duplicate records",
        f"Filtered out {invalid_quantity} transaction lines",
        f"Filtered out {invalid_price} bad price lines",
        "Converted to datetime; Applied uppercase & stripped text spaces"
    ],
    "Justification": [
        "Primary key required for customer behavioral metrics",
        "Prevents artificial inflation of revenue and sales volume",
        "Cancellations distort standard purchasing trends",
        "Corrects pricing anomalies and accounting artifacts",
        "Ensures precise time-series indexing and uniform groupings"
    ]
}

summary_table = pd.DataFrame(summary_data)
print(summary_table.to_string(index=False))

# Save the final cleaned output to a new CSV file
df_clean.to_csv('Cleaned_Online_Retail.csv', index=False)
print("\n==================================================")
print("SUCCESS: 'Cleaned_Online_Retail.csv' has been generated!")
print("==================================================")