# ========================== IMPORTS ==========================
import streamlit as st
import pandas as pd
import joblib
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# UI elements from the layout module
from utils.layout import (
    set_background,
    render_title_bar,
    render_sidebar,
    render_clock,
    render_sidebar_chatbot
)

# ========================== PAGE CONFIG ==========================
st.set_page_config(page_title="Machine Learning", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            color: #000000 !important;
        }
        .welcome-text {
            font-size: 1.3rem;
            font-weight: 500;
            color: #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ========================== DARK MODE STATE ==========================
query_params = st.query_params
dark_mode_param = query_params.get("dark", "0") == "1"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = dark_mode_param
if "token" not in st.session_state:
    st.session_state.token = random.randint(1000, 999999)

# ========================== UI HEADER SECTION ==========================
render_title_bar()

col1, col2 = st.columns([6, 1])
now = datetime.now()
greeting = "Good morning" if now.hour < 12 else "Good afternoon" if now.hour < 18 else "Good evening"

with col1:
    st.markdown(f"<div class='welcome-text'>{greeting}, <b>User</b>!</div>", unsafe_allow_html=True)
    render_clock()

with col2:
    toggle_key = f"dark_toggle_{st.session_state.token}"
    new_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode, key=toggle_key)

    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.session_state.token = random.randint(1000, 999999)
        st.query_params["dark"] = "1" if new_mode else "0"
        st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

# ========================== BACKGROUND VIDEO ==========================
light_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978357/bg_light_q3ifwd.mp4"
dark_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978356/bg_dark_kffpsn.mp4"
video_url = f"{dark_video if st.session_state.dark_mode else light_video}?v={st.session_state.token}"
set_background(video_url)

# ========================== SIDEBAR RENDERING ==========================
render_sidebar()
render_sidebar_chatbot()

# ========================== INTRO TEXT ==========================
st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.8);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 500;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        color: #000000;
    ">
    This section contains machine learning models for classifying delay risk and estimating arrival delay.
    </div>
""", unsafe_allow_html=True)

# ========================== TABS: CLASSIFIER + REGRESSOR ==========================
tab1, tab2 = st.tabs(["Flight Delay Classifier", "Arrival Delay Regressor"])

# ============== FLIGHT DELAY CLASSIFIER TAB ==============
with tab1:
    st.subheader("Flight Delay Classifier")

    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 1.25rem 2rem;
        border-left: 5px solid #1f77b4;
        border-radius: 10px;
        font-size: 1.05rem;
        line-height: 1.6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-top: 1rem;
        color: #000000;
    ">
    This classifier predicts delay risk levels (Low, Moderate, High) and allows you to fine-tune decision thresholds based on your business goals. It uses historical flight data and advanced optimization.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Show Training Details"):
        st.markdown("""
**Preprocessing Summary**
- Cleaned data using custom pipelines (handling missing values, encoding, leakage removal)
- One-hot encoding for categorical variables
- Standard scaling for numeric variables
- Feature engineering included delay ratios and dominant causes

**Training Summary**
- XGBoost classifier (GPU acceleration enabled)
- Hyperparameter tuning with Optuna (100 trials, F1 macro optimization)
- Class imbalance handled via weighted loss and threshold optimization
- Final model: 70% train, 15% validation, 15% test
        """)

    from backend.Classifier_Pipeline import ClassifierPipeline

    @st.cache_resource
    def load_classifier_pipeline():
        return ClassifierPipeline()

    pipeline = load_classifier_pipeline()

    uploaded_file = st.file_uploader("Upload cleaned flight data", type=["csv"], key="classifier_upload")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.markdown("### Uploaded Data Preview")
            st.dataframe(df.head(min(100, len(df))), use_container_width=True)

            strategy = st.selectbox("Threshold Strategy", list(pipeline.thresholds_dict.keys()))
            pipeline.set_threshold_strategy(strategy)

            results = pipeline.run_pipeline(df, mode="test")
            st.success("Prediction Complete")

            label_map = {0: "Low", 1: "Moderate", 2: "High"}
            y_pred = results["y_pred"]
            y_true = results["y_true"]
            input_preview = results["X_input"]

            st.markdown("### Predicted Risk Labels")
            pred_df = pd.DataFrame({
                "Input Row Index": input_preview.index,
                "Predicted Risk Level": y_pred,
                "Risk Description": pd.Series(y_pred).map(label_map)
            })
            st.dataframe(pred_df, use_container_width=True)

            if st.checkbox("Show Evaluation"):
                from sklearn.metrics import classification_report
                labels = [0, 1, 2]
                report = classification_report(y_true, y_pred, output_dict=True, labels=labels, zero_division=0)
                report_df = pd.DataFrame(report).transpose().round(4)
                report_df = report_df.reindex([str(i) for i in labels] + ["accuracy", "macro avg", "weighted avg"])
                st.dataframe(report_df, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")

# ============== ARRIVAL DELAY REGRESSOR TAB ==============
with tab2:
    st.subheader("Arrival Delay Regressor")

    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 1.25rem 2rem;
        border-left: 5px solid #2ca02c;
        border-radius: 10px;
        font-size: 1.05rem;
        line-height: 1.6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-top: 1rem;
        color: #000000;
    ">
    This regressor estimates expected arrival delay (in minutes) using historical patterns and performance trends.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Show Training Details"):
        st.markdown("""
- Model: XGBoost Regressor  
- Objective: Minimize Mean Absolute Error (MAE)  
- Input: Cleaned data with engineered features (seasonality, performance, delay trends)  
- Output: Estimated delay in minutes
        """)

    from backend.RegressorPipeline import RegressorPipeline

    @st.cache_resource
    def load_regressor_pipeline():
        return RegressorPipeline()

    reg_pipeline = load_regressor_pipeline()

    uploaded_file_reg = st.file_uploader("Upload cleaned flight data", type=["csv"], key="regressor_upload")

    if uploaded_file_reg:
        try:
            df_reg = pd.read_csv(uploaded_file_reg)
            st.markdown("### Uploaded Data Preview")
            st.dataframe(df_reg.head(min(100, len(df_reg))), use_container_width=True)

            results_reg = reg_pipeline.run_pipeline(df_reg, mode="test")
            st.success("Prediction Complete")

            y_pred = results_reg["y_pred"]
            y_true = results_reg["y_true"]
            input_preview = results_reg["X_input"]

            st.markdown("### Predicted vs Actual Delays")
            result_df = pd.DataFrame({
                "Input Row Index": input_preview.index,
                "Actual Delay (min)": y_true,
                "Predicted Delay (min)": y_pred
            })
            st.dataframe(result_df, use_container_width=True)

            if st.checkbox("Show Evaluation Metrics"):
                metrics_df = pd.DataFrame({
                    "Metric": ["MAE", "MSE", "RMSE", "R² Score"],
                    "Value": [
                        round(results_reg["mae"], 2),
                        round(results_reg["mse"], 2),
                        round(results_reg["rmse"], 2),
                        round(results_reg["r2"], 4)
                    ]
                })
                st.dataframe(metrics_df, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
