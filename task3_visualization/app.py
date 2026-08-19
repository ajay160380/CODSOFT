import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure Page
st.set_page_config(page_title="Task 3: Visualization", layout="wide", page_icon="📈")

# --- Custom CSS for 100000X Better UI ---
st.markdown("""
    <style>
    /* Gradient Text for Main Title */
    .premium-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px !important;
        padding-bottom: 10px;
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
        border: 1px solid rgba(255, 107, 107, 0.2);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 107, 107, 0.6);
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
        color: #FF8E53;
        margin: 0;
    }
    
    /* Insight Cards */
    .insight-box {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10B981;
        padding: 15px;
        border-radius: 4px;
        margin-top: 10px;
        color: #E2E8F0;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="premium-title">📈 Executive Data Visualization Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Interactive insights and analytics derived from the cleaned Superstore dataset.</p>', unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    # Load the cleaned dataset
    df = pd.read_csv('../data/processed/superstore_cleaned.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ Error: Cleaned data file not found. Ensure Task 1 was completed properly.")
    st.stop()

# --- KPIs ---
total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
total_orders = df['order_id'].nunique()

col1, col2, col3 = st.columns(3)
col1.markdown(f'<div class="kpi-card"><p class="kpi-title">Total Sales Revenue</p><p class="kpi-value">${total_sales:,.0f}</p></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="kpi-card"><p class="kpi-title">Total Profit</p><p class="kpi-value">${total_profit:,.0f}</p></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="kpi-card"><p class="kpi-title">Total Unique Orders</p><p class="kpi-value">{total_orders:,}</p></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Visualizations ---
st.markdown("### 📊 Business Performance Metrics")
tab1, tab2, tab3 = st.tabs(["📌 Categories & Regions", "📈 Time Series Trends", "🔬 Distributions & Correlations"])

# Custom Colors
custom_colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#1A535C', '#F7FFF7']

with tab1:
    colA, colB = st.columns(2)
    
    with colA:
        # 1. Bar Chart (Sales by Category)
        st.markdown("#### 🛒 Sales by Category")
        cat_sales = df.groupby('category')['sales'].sum().reset_index().sort_values('sales', ascending=False)
        fig_bar = px.bar(cat_sales, x='category', y='sales', 
                         color='category', color_discrete_sequence=custom_colors,
                         text_auto='.2s', template='plotly_dark')
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Insight:</b> Technology and Furniture lead in overall sales volume, suggesting these are the core revenue drivers.</div>', unsafe_allow_html=True)

    with colB:
        # 2. Pie Chart (Sales by Region)
        st.markdown("#### 🌍 Sales Distribution by Region")
        reg_sales = df.groupby('region')['sales'].sum().reset_index()
        fig_pie = px.pie(reg_sales, values='sales', names='region', hole=0.4, 
                         color_discrete_sequence=custom_colors, template='plotly_dark')
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Insight:</b> The West and East regions account for the vast majority of our total sales nationwide.</div>', unsafe_allow_html=True)


with tab2:
    # 3. Line Chart (Sales Trend over time)
    st.markdown("#### 📅 Monthly Sales Trend")
    # Resample by month
    monthly_sales = df.set_index('order_date').resample('ME')['sales'].sum().reset_index()
    fig_line = px.line(monthly_sales, x='order_date', y='sales', markers=True, 
                       line_shape='spline', template='plotly_dark')
    fig_line.update_traces(line_color='#4ECDC4', line_width=3, marker=dict(size=8, color='#FF6B6B'))
    fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('<div class="insight-box"><b>Insight:</b> Sales show strong seasonality, generally peaking around the end of the year (Q4) due to holiday shopping.</div>', unsafe_allow_html=True)


with tab3:
    colC, colD = st.columns(2)
    
    with colC:
        # 4. Histogram (Distribution of Sales)
        st.markdown("#### 📉 Distribution of Order Values")
        # Filter outliers for better visualization
        filtered_sales = df[df['sales'] < 1000]
        fig_hist = px.histogram(filtered_sales, x='sales', nbins=50, 
                                color_discrete_sequence=['#FFE66D'], template='plotly_dark')
        fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Insight:</b> The vast majority of orders are small-ticket items under $100.</div>', unsafe_allow_html=True)
        
    with colD:
        # 5. Scatter Plot (Sales vs Profit)
        st.markdown("#### 🎯 Sales vs Profit Correlation")
        fig_scatter = px.scatter(df, x='sales', y='profit', color='category', 
                                 size='quantity', hover_name='sub_category',
                                 color_discrete_sequence=custom_colors, template='plotly_dark')
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Insight:</b> While higher sales generally lead to higher profits, Furniture (specifically Tables) often results in a negative profit margin despite high sales volume.</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748B;'>Task 3 Completed — CodSoft Data Analytics Internship</div>", unsafe_allow_html=True)
