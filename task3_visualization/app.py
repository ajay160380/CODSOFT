import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure Page - MUST BE FIRST
st.set_page_config(page_title="Executive Analytics", layout="wide", page_icon="⚡")

# --- ULTRA PREMIUM CSS ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Animated Gradient Title */
    .ultra-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(270deg, #FF6B6B, #4ECDC4, #FFE66D, #FF6B6B);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: gradient-shift 10s ease infinite;
        margin-bottom: 0px !important;
        padding-bottom: 5px;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .ultra-subtitle {
        text-align: center;
        color: #94A3B8;
        font-size: 1.2rem;
        margin-bottom: 30px;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* Next-Gen Glassmorphism KPI Cards */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .ultra-kpi {
        flex: 1;
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        border-left: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .ultra-kpi::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
        transform: skewX(-20deg);
        transition: 0.5s;
    }
    
    .ultra-kpi:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(78, 205, 196, 0.2);
        border-color: rgba(78, 205, 196, 0.5);
    }
    
    .ultra-kpi:hover::before {
        left: 200%;
    }
    
    .kpi-title {
        font-size: 1rem;
        color: #CBD5E1;
        margin-bottom: 5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
        text-shadow: 0 0 20px rgba(255,255,255,0.3);
    }
    .accent-sales { color: #4ECDC4; text-shadow: 0 0 20px rgba(78,205,196,0.4); }
    .accent-profit { color: #FFE66D; text-shadow: 0 0 20px rgba(255,230,109,0.4); }
    .accent-orders { color: #FF6B6B; text-shadow: 0 0 20px rgba(255,107,107,0.4); }

    /* Customizing Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #94A3B8;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(78, 205, 196, 0.1) !important;
        color: #4ECDC4 !important;
        border: 1px solid rgba(78, 205, 196, 0.3) !important;
        border-bottom: none !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="ultra-title">⚡ Nexus Analytics Engine</h1>', unsafe_allow_html=True)
st.markdown('<p class="ultra-subtitle">Real-time interactive intelligence powered by Python.</p>', unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('../data/processed/superstore_cleaned.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ Error: Cleaned data file not found.")
    st.stop()

# --- INTERACTIVE SIDEBAR FILTERS ---
st.sidebar.markdown("### 🎛️ Control Panel")
st.sidebar.markdown("Filter the dashboard dynamically.")

# Filters
all_regions = ["All"] + list(df['region'].unique())
selected_region = st.sidebar.selectbox("🌍 Select Region", all_regions)

all_categories = ["All"] + list(df['category'].unique())
selected_category = st.sidebar.selectbox("🛒 Select Category", all_categories)

# Apply Filters
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df['region'] == selected_region]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# Prevent empty data crash
if filtered_df.empty:
    st.warning("No data available for these filters. Please adjust your selection.")
    st.stop()

# --- KPIs ---
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
total_orders = filtered_df['order_id'].nunique()

st.markdown(f"""
<div class="kpi-container">
    <div class="ultra-kpi"><p class="kpi-title">Revenue Generated</p><p class="kpi-value accent-sales">${total_sales:,.0f}</p></div>
    <div class="ultra-kpi"><p class="kpi-title">Net Profit</p><p class="kpi-value accent-profit">${total_profit:,.0f}</p></div>
    <div class="ultra-kpi"><p class="kpi-title">Total Orders</p><p class="kpi-value accent-orders">{total_orders:,}</p></div>
</div>
""", unsafe_allow_html=True)

# --- THEME FOR CHARTS ---
# Custom Plotly Theme to match the dark glass UI
chart_layout = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#94A3B8', family="Outfit"),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
)
custom_colors = ['#4ECDC4', '#FF6B6B', '#FFE66D', '#A06CD5', '#F7FFF7']

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Market Overview", "📈 Temporal Trends", "🎯 Deep Analytics"])

with tab1:
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("<h4 style='text-align: center; color: #E2E8F0;'>Top Selling Sub-Categories</h4>", unsafe_allow_html=True)
        sub_sales = filtered_df.groupby('sub_category')['sales'].sum().reset_index().nlargest(10, 'sales')
        fig_bar = px.bar(sub_sales, x='sales', y='sub_category', orientation='h', 
                         color='sales', color_continuous_scale='Tealgrn')
        fig_bar.update_layout(**chart_layout, coloraxis_showscale=False)
        fig_bar.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_bar, use_container_width=True)

    with colB:
        st.markdown("<h4 style='text-align: center; color: #E2E8F0;'>Profit Share by Segment</h4>", unsafe_allow_html=True)
        seg_profit = filtered_df.groupby('segment')['profit'].sum().reset_index()
        # Filter out negative segments for pie chart clarity if needed, or use absolute values
        seg_profit['profit'] = seg_profit['profit'].apply(lambda x: max(x, 0))
        fig_pie = px.pie(seg_profit, values='profit', names='segment', hole=0.5, 
                         color_discrete_sequence=custom_colors)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=2)))
        fig_pie.update_layout(**chart_layout, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.markdown("<h4 style='text-align: center; color: #E2E8F0;'>Revenue vs Profit Trajectory</h4>", unsafe_allow_html=True)
    monthly_trend = filtered_df.set_index('order_date').resample('ME')[['sales', 'profit']].sum().reset_index()
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=monthly_trend['order_date'], y=monthly_trend['sales'], mode='lines+markers',
                                  name='Sales', line=dict(color='#4ECDC4', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(78, 205, 196, 0.1)'))
    fig_line.add_trace(go.Scatter(x=monthly_trend['order_date'], y=monthly_trend['profit'], mode='lines+markers',
                                  name='Profit', line=dict(color='#FF6B6B', width=3, shape='spline')))
    
    fig_line.update_layout(**chart_layout, hovermode='x unified', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_line, use_container_width=True)

with tab3:
    colC, colD = st.columns(2)
    
    with colC:
        st.markdown("<h4 style='text-align: center; color: #E2E8F0;'>Sales Distribution Density</h4>", unsafe_allow_html=True)
        # Filter outliers for clean histogram
        hist_data = filtered_df[filtered_df['sales'] < 800]
        fig_hist = px.histogram(hist_data, x='sales', nbins=40, color_discrete_sequence=['#FFE66D'], marginal="box")
        fig_hist.update_layout(**chart_layout)
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with colD:
        st.markdown("<h4 style='text-align: center; color: #E2E8F0;'>Profitability Matrix (Sales vs Profit)</h4>", unsafe_allow_html=True)
        fig_scatter = px.scatter(filtered_df, x='sales', y='profit', color='region', 
                                 size='quantity', hover_data=['product_name'],
                                 color_discrete_sequence=custom_colors)
        # Add a zero profit line
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="#FF6B6B", annotation_text="Break Even", annotation_position="bottom right")
        fig_scatter.update_layout(**chart_layout)
        st.plotly_chart(fig_scatter, use_container_width=True)
