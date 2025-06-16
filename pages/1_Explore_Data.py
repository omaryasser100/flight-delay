import streamlit as st
from datetime import datetime
import random
from utils.layout import (
    set_background,
    render_title_bar,
    render_sidebar,
    render_clock,
    render_sidebar_chatbot
)
from backend.data_loader_cleaner import DataLoaderCleaner
from backend.feature_engineering import FeatureEngineering
from backend.visual_explorer import VisualExplorer

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Explore Data", layout="wide", initial_sidebar_state="expanded")

# ========== 🌐 LOAD GLOBAL FONTS ==========
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }
        .welcome-text {
            font-size: 1.2rem;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# ========== DARK MODE & TOKEN INIT ==========
query_params = st.query_params
dark_mode_param = query_params.get("dark", "0") == "1"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = dark_mode_param

if "token" not in st.session_state:
    st.session_state.token = random.randint(1000, 999999)

# ========== TITLE ==========
render_title_bar()

# ========== CLOCK + DARK MODE TOGGLE ==========
col1, col2 = st.columns([6, 1])

with col1:
    now = datetime.now()
    greeting = "Good morning" if now.hour < 12 else "Good afternoon" if now.hour < 18 else "Good evening"
    st.markdown(f"<div class='welcome-text'>{greeting}, <b>User</b>!</div>", unsafe_allow_html=True)
    render_clock()

with col2:
    toggle_key = f"dark_toggle_{st.session_state.token}"
    new_mode = st.toggle("🌙", value=st.session_state.dark_mode, key=toggle_key)

    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.session_state.token = random.randint(1000, 999999)
        st.query_params["dark"] = "1" if new_mode else "0"
        st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)  # 🔁 Force refresh

# ========== BACKGROUND VIDEO ==========
light_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978357/bg_light_q3ifwd.mp4"
dark_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978356/bg_dark_kffpsn.mp4"
selected_video = dark_video if st.session_state.dark_mode else light_video
video_url = f"{selected_video}?v={st.session_state.token}"
set_background(video_url)

# ========== SIDEBAR ==========
render_sidebar()
render_sidebar_chatbot()

# ========== DATA LOADING ==========
@st.cache_data
def get_data_stages():
    cleaner = DataLoaderCleaner()
    raw = cleaner.load_data("data/Airline_Delay_Cause.csv")
    clean = cleaner.clean_data(raw)
    fe = FeatureEngineering().transform(clean)
    return raw, clean, fe

raw_df, clean_df, fe_df = get_data_stages()
stage = st.radio("Select Data Stage", ["Raw", "Cleaned", "Feature Engineered"], horizontal=True)
df = {"Raw": raw_df, "Cleaned": clean_df, "Feature Engineered": fe_df}[stage]
explorer = VisualExplorer(df)

# ========== DATA VIEW ==========
st.markdown("### Data Viewer")
cols = st.multiselect("Choose Columns to View", options=df.columns.tolist(), default=df.columns.tolist())
num_rows = st.slider("Number of Rows", 5, 100, 20)
st.dataframe(explorer.view_columns(cols, num_rows), use_container_width=True)

# ========== ROW VIEW ==========
with st.expander("View Row by Index"):
    row_index = st.number_input("Enter Row Index", min_value=0, max_value=len(df) - 1, value=0)
    st.dataframe(explorer.view_row_by_index(row_index))

# ========== VISUAL EXPLORATION ==========
st.markdown("### Visual Exploration")
viz_type = st.radio("Select Plot Type", ["Univariate", "Bivariate", "Correlation Heatmap"], horizontal=True)

if viz_type == "Univariate":
    uni_col = st.selectbox("Select Column", options=df.select_dtypes(include='number').columns)
    uni_kind = st.selectbox("Plot Type", ["hist", "box", "violin"], index=0)
    st.pyplot(explorer.univariate_plot(uni_col, kind=uni_kind))

elif viz_type == "Bivariate":
    x_col = st.selectbox("X Axis", options=df.select_dtypes(include='number').columns)
    y_col = st.selectbox("Y Axis", options=[col for col in df.select_dtypes(include='number').columns if col != x_col])
    bi_kind = st.selectbox("Plot Type", ["scatter", "line", "box", "bar"], index=0)
    st.pyplot(explorer.bivariate_plot(x_col, y_col, kind=bi_kind))

elif viz_type == "Correlation Heatmap":
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    default_heatmap_cols = [numeric_cols[0]] if numeric_cols else []
    heat_cols = st.multiselect("Select Columns", options=numeric_cols, default=default_heatmap_cols)
    st.pyplot(explorer.correlation_heatmap(heat_cols))

# ========== KPI METRICS ==========
st.markdown("### Key Metrics")
metric_col = st.selectbox("Select Numeric Column", options=df.select_dtypes(include='number').columns)
k1, k2, k3 = st.columns(3)
k1.metric("Max", f"{df[metric_col].max():,.2f}")
k2.metric("Mean", f"{df[metric_col].mean():,.2f}")
k3.metric("Min", f"{df[metric_col].min():,.2f}")

# ========== CATEGORICAL INSIGHTS ==========
st.markdown("### Categorical Insights")
cat_col = st.selectbox("Select Categorical Column", options=df.select_dtypes(include='object').columns)

most_common = df[cat_col].value_counts().idxmax()
most_common_count = df[cat_col].value_counts().max()
unique_count = df[cat_col].nunique()

c1, c2, c3 = st.columns(3)
c1.metric("Unique Values", f"{unique_count}")
c2.metric("Most Frequent", most_common)
c3.metric("Count", f"{most_common_count:,}")

# ========== FOOTER ==========
st.markdown("""
<hr style="margin-top: 3rem; border: none; border-top: 1px solid #ccc;">
<div style='text-align: center; padding: 1rem 0; color: #666; font-size: 0.9rem; font-family: Roboto, sans-serif;'>
Explore Page — Part of the Flight Delay Dashboard by <b>Omar Yasser</b>
</div>
""", unsafe_allow_html=True)
