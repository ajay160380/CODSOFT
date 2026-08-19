import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Task 1: Data Cleaning", layout="wide", page_icon="🧹")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        color: #2e6c80;
        text-align: center;
        font-weight: bold;
    }
    .sub-title {
        font-size: 24px;
        color: #1f4e5b;
        margin-top: 20px;
        border-bottom: 2px solid #2e6c80;
        padding-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Task 1: Data Cleaning & Preprocessing</div>', unsafe_allow_html=True)
st.write("Welcome to the Data Analytics Dashboard! This application showcases the step-by-step data cleaning process for the Sample Superstore dataset.")

@st.cache_data
def load_raw_data():
    return pd.read_csv('data/raw/superstore_raw.csv', encoding='cp1252')

@st.cache_data
def load_cleaned_data():
    return pd.read_csv('data/processed/superstore_cleaned.csv')

# Load Data
try:
    raw_df = load_raw_data()
    clean_df = load_cleaned_data()
except Exception as e:
    st.error(f"Error loading data: {e}. Make sure the dataset exists in the data directory.")
    st.stop()

# --- Section 1: Import & Inspect ---
st.markdown('<div class="sub-title">1. Import & Inspect Raw Data</div>', unsafe_allow_html=True)
st.write(f"**Original Dataset Shape:** {raw_df.shape[0]} rows and {raw_df.shape[1]} columns.")
st.dataframe(raw_df.head(), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.write("**Raw Data Types:**")
    st.dataframe(raw_df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column', 0: 'Type'}))
with col2:
    st.write("**Statistical Summary:**")
    st.dataframe(raw_df.describe())

# --- Section 2: Identify Issues ---
st.markdown('<div class="sub-title">2. Identify Issues</div>', unsafe_allow_html=True)

# Missing Values
missing_data = raw_df.isnull().sum()
missing_percent = (missing_data / len(raw_df)) * 100
missing_df = pd.DataFrame({'Missing Values': missing_data, 'Percentage (%)': missing_percent})
missing_df = missing_df[missing_df['Missing Values'] > 0]

st.write("**Missing Values Found:**")
if not missing_df.empty:
    st.dataframe(missing_df)
    
    # Plot missing values
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=missing_df.index, y=missing_df['Percentage (%)'], ax=ax, palette='viridis')
    ax.set_title("Percentage of Missing Values")
    ax.set_ylabel("Percentage (%)")
    st.pyplot(fig)
else:
    st.success("No missing values found!")

# Duplicates
duplicates = raw_df.duplicated().sum()
st.write(f"**Duplicate Rows Found:** {duplicates}")
if duplicates > 0:
    st.dataframe(raw_df[raw_df.duplicated(keep=False)].head())

# --- Section 3 & 4: Cleaning & Validation ---
st.markdown('<div class="sub-title">3. Clean & Validate</div>', unsafe_allow_html=True)

st.write("""
### Actions Performed:
1. **Standardized Columns:** Converted to `snake_case`.
2. **Missing Values:** Imputed placeholder `0` for missing `postal_code`.
3. **Duplicates Removed:** Dropped exact row duplicates.
4. **Text Cleaning:** Stripped whitespaces and fixed casing for categorical features.
5. **Date Parsing:** Converted `order_date` and `ship_date` to `datetime` objects.
6. **Feature Engineering:** Added `shipping_days` (Difference between ship date and order date).
""")

st.write(f"**Cleaned Dataset Shape:** {clean_df.shape[0]} rows and {clean_df.shape[1]} columns.")
st.dataframe(clean_df.head(), use_container_width=True)

st.write("**Final Cleaned Data Types:**")
st.dataframe(clean_df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column', 0: 'Type'}).T)

# Validation Proof
col3, col4 = st.columns(2)
with col3:
    st.info(f"Remaining Missing Values: {clean_df.isnull().sum().sum()}")
with col4:
    st.info(f"Remaining Duplicates: {clean_df.duplicated().sum()}")

# --- Section 5: Save & Download ---
st.markdown('<div class="sub-title">4. Export</div>', unsafe_allow_html=True)
st.success("Cleaned dataset has been successfully processed and saved to `data/processed/superstore_cleaned.csv`.")

# Provide a download button for the video presentation
csv = clean_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Cleaned Dataset CSV",
    data=csv,
    file_name='superstore_cleaned.csv',
    mime='text/csv',
)
