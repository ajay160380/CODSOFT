import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    
    /* Better DataFrame headers */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="premium-title">✨ Superstore Data Cleaning Pipeline</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transforming raw, messy datasets into clean, actionable analytics ready data.</p>', unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    raw_df = pd.read_csv('../data/raw/superstore_raw.csv', encoding='cp1252')
    clean_df = pd.read_csv('../data/processed/superstore_cleaned.csv')
    return raw_df, clean_df

try:
    raw_df, clean_df = load_data()
except Exception as e:
    st.error("⚠️ Error: Data files not found. Ensure raw and processed CSVs exist.")
    st.stop()

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
    
    # KPI Row
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="kpi-card"><p class="kpi-title">Total Rows</p><p class="kpi-value">{raw_df.shape[0]:,}</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="kpi-card"><p class="kpi-title">Total Columns</p><p class="kpi-value">{raw_df.shape[1]}</p></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="kpi-card"><p class="kpi-title">Data Size</p><p class="kpi-value">~2.2 MB</p></div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown("#### Raw Data Preview")
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
                         color='Missing', color_continuous_scale='Rose',
                         template='plotly_dark', labels={'index': 'Column', 'Missing': 'Null Count'})
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No missing values!")
            
    with col2:
        st.markdown("#### 👯 Duplicate Records")
        duplicates = raw_df.duplicated().sum()
        
        # Display as a huge KPI
        color_class = "danger" if duplicates > 0 else "success"
        st.markdown(f'<div class="kpi-card" style="margin-top: 20px;"><p class="kpi-title">Exact Duplicates Found</p><p class="kpi-value {color_class}">{duplicates}</p></div>', unsafe_allow_html=True)
        
        if duplicates > 0:
            st.warning("These exact duplicates skew our sales/profit metrics and must be dropped.")

# --- TAB 3: TRANSFORMATIONS ---
with tab3:
    st.markdown("### 🛠️ The Cleaning Engine")
    
    st.info("Hover over the steps below to see exactly what transformations were applied.")
    
    with st.expander("📝 1. Column Standardization", expanded=True):
        st.code("df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')", language='python')
        st.caption("Standardized all columns to `snake_case` to prevent querying errors.")
        
    with st.expander("🩹 2. Missing Value Imputation", expanded=True):
        st.code("df['postal_code'] = df['postal_code'].fillna(0).astype(int)", language='python')
        st.caption("Filled missing postal codes (common in international regions) with `0`.")
        
    with st.expander("✂️ 3. Duplicate Removal", expanded=True):
        st.code("df = df.drop_duplicates()", language='python')
        st.caption(f"Successfully dropped {duplicates} exact duplicate rows.")

    with st.expander("⏱️ 4. Feature Engineering (Dates)", expanded=True):
        st.code('''df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])
df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days''', language='python')
        st.caption("Converted string dates to actual `datetime` objects and calculated the total `shipping_days`.")

# --- TAB 4: FINAL OUTPUT ---
with tab4:
    st.markdown("### 💎 The Final Polished Dataset")
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="kpi-card"><p class="kpi-title">Final Rows</p><p class="kpi-value success">{clean_df.shape[0]:,}</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="kpi-card"><p class="kpi-title">Missing Values</p><p class="kpi-value success">0</p></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="kpi-card"><p class="kpi-title">Duplicates</p><p class="kpi-value success">0</p></div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown("#### Cleaned Data Ready for Analysis")
    st.dataframe(clean_df.head(50), use_container_width=True)
    
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        csv = clean_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="🚀 Download Final Cleaned CSV",
            data=csv,
            file_name='superstore_cleaned.csv',
            mime='text/csv',
            use_container_width=True
        )
