import streamlit as st
from datetime import datetime
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === Custom Modules ===
from utils.layout import (
    set_background,
    render_sidebar,
    render_clock,
    render_sidebar_chatbot,
    render_title_bar
)
from backend.eda_analysis import FlightDataAnalysis

# ===================== ⚙️ PAGE CONFIGURATION =====================
st.set_page_config(
    page_title="Flight Delay Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== 🧠 INIT SESSION STATE =====================
query_params = st.query_params
dark_mode_param = query_params.get("dark", "0") == "1"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = dark_mode_param

if "token" not in st.session_state:
    st.session_state.token = random.randint(1000, 999999)

# ===================== 🎞️ BACKGROUND VIDEO =====================
light_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978357/bg_light_q3ifwd.mp4"
dark_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978356/bg_dark_kffpsn.mp4"
selected_video = dark_video if st.session_state.dark_mode else light_video
video_url = f"{selected_video}?v={st.session_state.token}"
set_background(video_url)

# =====================  DASHBOARD TITLE CENTERED =====================
render_title_bar()

# ===================== 👋 GREETING AND THEME TOGGLE =====================
col1, col2 = st.columns([6, 1])
now = datetime.now()
greeting = "Good morning" if now.hour < 12 else "Good afternoon" if now.hour < 18 else "Good evening"

with col1:
    st.markdown(f"<div class='welcome-text'>{greeting}, <b>User</b>!</div>", unsafe_allow_html=True)
    render_clock()

with col2:
    toggle_key = f"dark_toggle_{st.session_state.token}"
    new_mode = st.toggle("🌙", value=st.session_state.dark_mode, key=toggle_key)

    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.session_state.token = random.randint(1000, 999999)
        st.query_params["dark"] = "1" if new_mode else "0"
        st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

# ===================== 📚 SIDEBAR =====================
render_sidebar()
render_sidebar_chatbot()

# ===================== 📄 PROJECT SUMMARY BOX =====================
st.markdown(
    '''
    <div style="
        background: rgba(255,255,255,0.9);
        border-left: 5px solid #1f77b4;
        padding: 1.2rem 2rem;
        border-radius: 10px;
        font-size: 1.05rem;
        line-height: 1.6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-top: 1rem;
    ">
    <b>Project Summary:</b><br>
    This interactive dashboard provides a comprehensive analysis of monthly flight performance across U.S. airports and airlines.
    It is designed to reveal operational trends, analyze causes of delay, and support data-driven decision-making.<br><br>
    <b>Key features include:</b><br>
    - In-depth analysis of flight volume, delay frequencies, cancellations, and diversion rates<br>
    - Breakdown of delay causes including carrier issues, weather disruptions, NAS inefficiencies, security incidents, and late-arriving aircraft<br><br>
    <b>Machine Learning Integration:</b><br>
    - A regression model to predict arrival delays<br>
    - A classification model to identify flights at risk of significant delays<br><br>
    Users can also perform custom data exploration through a modular visualization engine.<br>
    The dashboard concludes with a Business Insights section offering strategic recommendations.<br><br>
    An experimental chatbot assistant is also included to support natural language interaction with the data.
    </div>
    ''', unsafe_allow_html=True
)

# ===================== 🔢 KPI CARDS =====================
def render_kpi(title, value, color="#0066cc"):
    st.markdown(f'''
    <div style="
        margin: 0.5rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.15);
        border-left: 5px solid {color};
    ">
        <div style="font-size: 15px; color: #333;">{title}</div>
        <div style="font-size: 24px; font-weight: 700; color: #111;">{value}</div>
    </div>
    ''', unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)
with k1:
    render_kpi("Total Flights", "45,120", color="#1f77b4")
with k2:
    render_kpi("Average Delay", "12.5 mins", color="#ff7f0e")
with k3:
    render_kpi("Cancelled Flights", "3.2%", color="#d62728")

# ===================== 📊 DATA LOADING + ANALYSIS =====================
df = pd.read_csv("data/Airline_Delay_Cause.csv")
eda = FlightDataAnalysis(df)

st.markdown("### Statistical Summary")
st.dataframe(eda.summary_statistics(), use_container_width=True)

missing_df = eda.missing_values_report()
if not missing_df.empty:
    st.markdown("### Missing Values Report")
    st.dataframe(missing_df, use_container_width=True)
else:
    st.info("No missing values in the dataset.")

st.markdown("### Correlation Matrix")
st.pyplot(eda.correlation_matrix())

# ===================== ⚓ FOOTER (REUSABLE) =====================
st.markdown(
    '''
    <hr style="margin-top: 3rem; border: none; border-top: 1px solid #ccc;">
    <div style='text-align: center; padding: 1rem 0; color: #666; font-size: 0.9rem;'>
    Built with by <b>Omar Yasser</b> — Flight Delay Dashboard v1.0
    </div>
    ''',
    unsafe_allow_html=True
)
