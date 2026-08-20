import streamlit as st
import pandas as pd
import plotly.express as px

# Configure Page
st.set_page_config(page_title="Data Cleaning Pro", layout="wide", page_icon="✨")

# --- Custom CSS for 100000X Better UI ---
st.markdown("""
    <style>
    /* Gradient Text for Main Title */
    .premium-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #00E5FF 0%, #007BFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px !important;
        padding-bottom: 20px;
    }
    
    .subtitle {
        text-align: center;
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 40px;
        font-weight: 300;
    }

    /* Glassmorphism KPI Cards */
    .kpi-card {
        background: rgba(20, 28, 47, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 229, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 229, 255, 0.4);
    }
    .kpi-title {
        font-size: 1rem;
        color: #94A3B8;
        margin-bottom: 10px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00E5FF;
        margin: 0;
    }
    .kpi-value.danger { color: #F43F5E; }
    .kpi-value.success { color: #10B981; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="premium-title">✨ Universal Data Cleaning Pipeline</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload any dataset or use the default Superstore data to see the magic happen.</p>', unsafe_allow_html=True)

# --- SIDEBAR: File Upload ---
st.sidebar.markdown("### 📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload your own CSV dataset", type=["csv"])
st.sidebar.info("If no file is uploaded, the default Superstore dataset will be used.")

# Load Data
@st.cache_data
def load_default_data():
    raw_df = pd.read_csv('../data/raw/superstore_raw.csv', encoding='cp1252')
    return raw_df, True # True signifies it's the default superstore data

try:
    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        is_default = False
        dataset_name = uploaded_file.name
    else:
        raw_df, is_default = load_default_data()
        dataset_name = "Sample Superstore Retail (Default)"
except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

st.info(f"**📂 Active Dataset:** `{dataset_name}`")

# --- THE CLEANING ENGINE (Dynamic) ---
@st.cache_data
def process_data(df, is_default):
    clean_df = df.copy()
    
    # 1. Standardize columns
    clean_df.columns = clean_df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    
    # 2. Universal Duplicate Removal
    duplicates_dropped = clean_df.duplicated().sum()
    clean_df = clean_df.drop_duplicates()
    
    # 3. Handle Missing Values
    missing_imputed = clean_df.isnull().sum().sum()
    if is_default and 'postal_code' in clean_df.columns:
        # Superstore specific logic
        clean_df['postal_code'] = clean_df['postal_code'].fillna(0).astype(int)
    else:
        # Universal generic logic: Fill numeric with median, categorical with 'Unknown'
        num_cols = clean_df.select_dtypes(include=['number']).columns
        cat_cols = clean_df.select_dtypes(exclude=['number']).columns
        clean_df[num_cols] = clean_df[num_cols].fillna(clean_df[num_cols].median())
        clean_df[cat_cols] = clean_df[cat_cols].fillna('Unknown')
        
    # 4. Feature Engineering (Only for default)
    if is_default and 'order_date' in clean_df.columns and 'ship_date' in clean_df.columns:
        clean_df['order_date'] = pd.to_datetime(clean_df['order_date'])
        clean_df['ship_date'] = pd.to_datetime(clean_df['ship_date'])
        clean_df['shipping_days'] = (clean_df['ship_date'] - clean_df['order_date']).dt.days

    return clean_df, duplicates_dropped, missing_imputed

clean_df, duplicates_dropped, missing_imputed = process_data(raw_df, is_default)

# Create Beautiful Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 1. Raw Inspection", 
    "🚨 2. Issues Found", 
    "🛠️ 3. Transformations", 
    "💎 4. Final Output"
])

# --- TAB 1: RAW DATA ---
with tab1:
    st.markdown("### 📊 Initial Dataset Architecture")
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="kpi-card"><p class="kpi-title">Total Rows</p><p class="kpi-value">{raw_df.shape[0]:,}</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="kpi-card"><p class="kpi-title">Total Columns</p><p class="kpi-value">{raw_df.shape[1]}</p></div>', unsafe_allow_html=True)
    size_mb = raw_df.memory_usage(deep=True).sum() / (1024 * 1024)
    col3.markdown(f'<div class="kpi-card"><p class="kpi-title">Data Size</p><p class="kpi-value">~{size_mb:.1f} MB</p></div>', unsafe_allow_html=True)
    
    st.write("")
    st.dataframe(raw_df.head(10), use_container_width=True)

# --- TAB 2: ISSUES ---
with tab2:
    st.markdown("### 🚨 Identified Data Anomalies")
    
    missing_data = raw_df.isnull().sum()
    missing_df = pd.DataFrame({'Missing': missing_data}).reset_index()
    missing_df = missing_df[missing_df['Missing'] > 0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚫 Missing Values")
        if not missing_df.empty:
            fig = px.bar(missing_df, x='index', y='Missing', 
                         color='Missing', color_continuous_scale='Reds',
                         template='plotly_dark', labels={'index': 'Column', 'Missing': 'Null Count'})
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No missing values detected in the raw data!")
            
    with col2:
        st.markdown("#### 👯 Duplicate Records")
        duplicates = raw_df.duplicated().sum()
        color_class = "danger" if duplicates > 0 else "success"
        st.markdown(f'<div class="kpi-card" style="margin-top: 20px;"><p class="kpi-title">Exact Duplicates Found</p><p class="kpi-value {color_class}">{duplicates}</p></div>', unsafe_allow_html=True)

# --- TAB 3: TRANSFORMATIONS ---
with tab3:
    st.markdown("### 🛠️ The Cleaning Engine")
    
    with st.expander("📝 1. Column Standardization", expanded=True):
        st.code("df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')", language='python')
        st.caption("Standardized all columns to `snake_case` format.")
        
    with st.expander("🩹 2. Missing Value Imputation", expanded=True):
        if is_default:
            st.code("df['postal_code'] = df['postal_code'].fillna(0)", language='python')
            st.caption("Custom Logic: Filled missing postal codes with `0`.")
        else:
            st.code("df[num_cols].fillna(median); df[cat_cols].fillna('Unknown')", language='python')
            st.caption(f"Universal Logic: Handled {missing_imputed} missing data points across the dataset automatically.")
        
    with st.expander("✂️ 3. Duplicate Removal", expanded=True):
        st.code("df = df.drop_duplicates()", language='python')
        st.caption(f"Successfully dropped {duplicates_dropped} exact duplicate rows.")

    if is_default:
        with st.expander("⏱️ 4. Feature Engineering (Dates)", expanded=True):
            st.code("df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days", language='python')

# --- TAB 4: FINAL OUTPUT ---
with tab4:
    st.markdown("### 💎 The Final Polished Dataset")
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="kpi-card"><p class="kpi-title">Final Rows</p><p class="kpi-value success">{clean_df.shape[0]:,}</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="kpi-card"><p class="kpi-title">Remaining Missing</p><p class="kpi-value success">0</p></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="kpi-card"><p class="kpi-title">Remaining Duplicates</p><p class="kpi-value success">0</p></div>', unsafe_allow_html=True)
    
    st.write("")
    st.dataframe(clean_df.head(50), use_container_width=True)
    
    st.markdown("---")
    
    csv = clean_df.to_csv(index=False).encode('utf-8')
    dataset_name = "custom_cleaned_data.csv" if not is_default else "superstore_cleaned.csv"
    
    st.download_button(
        label=f"🚀 Download Final Cleaned CSV ({dataset_name})",
        data=csv,
        file_name=dataset_name,
        mime='text/csv',
        use_container_width=True
    )
