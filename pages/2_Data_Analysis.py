import streamlit as st
from datetime import datetime
import random
from streamlit_autorefresh import st_autorefresh

# === Layout and Modules ===
from utils.layout import (
    set_background,
    render_sidebar,
    render_sidebar_chatbot,
    render_clock,
    render_title_bar
)
from backend.data_loader_cleaner import DataLoaderCleaner
from backend.feature_engineering import FeatureEngineering
from backend.eda_analysis import FlightDataAnalysis, UnivariateAnalyzer

# === PAGE CONFIG ===
st.set_page_config(page_title="Data Analysis", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }
        .welcome-text {
            font-size: 1.3rem;
            font-weight: 500;
         color: black;}
    </style>
""", unsafe_allow_html=True)


# === DARK MODE & TOKEN INIT ===
query_params = st.query_params
dark_mode_param = query_params.get("dark", "0") == "1"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = dark_mode_param
if "token" not in st.session_state:
    st.session_state.token = random.randint(1000, 999999)

# === DASHBOARD TITLE (CENTERED) ===
render_title_bar()

# === CLOCK + DARK MODE TOGGLE ===
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

# === BACKGROUND VIDEO ===
light_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978357/bg_light_q3ifwd.mp4"
dark_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978356/bg_dark_kffpsn.mp4"
video_url = f"{dark_video if st.session_state.dark_mode else light_video}?v={st.session_state.token}"
set_background(video_url)

# === SIDEBAR ===
render_sidebar()
render_sidebar_chatbot()
# === Load Data ===
@st.cache_data
def get_analysis_data():
    loader = DataLoaderCleaner()
    raw = loader.load_data("data/Airline_Delay_Cause.csv")
    clean = loader.clean_data(raw)
    fe = FeatureEngineering().transform(clean)
    return raw, clean, fe

raw_df, clean_df, fe_df = get_analysis_data()
eda_fe = FlightDataAnalysis(fe_df)
uni = UnivariateAnalyzer(fe_df)

# === SECTION 1: UNIVARIATE ANALYSIS ===
# === SECTION 1: UNIVARIATE ANALYSIS ===
# === SECTION 1: UNIVARIATE ANALYSIS (Aligned Descriptions & Insights) ===
with st.container():
    st.subheader("Univariate Analysis")

    # Row 1: Descriptions
    desc1, desc2 = st.columns(2)
    with desc1:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);"">
            <b>Yearly Flight Arrivals</b><br>
            Displays the total number of flight arrivals per year. This visualization helps identify long-term trends,
            disruptions, and recovery patterns in air traffic volume over time.
        </div>
        """, unsafe_allow_html=True)

    with desc2:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);"">
            <b>Airline Share</b><br>
            This pie chart presents the share of each airline carrier in the dataset.
            To improve readability, only the top 10 carriers are shown individually; the remaining ones are grouped as “Other”.
        </div>
        """, unsafe_allow_html=True)

    # Row 2: Plots
    plot1, plot2 = st.columns(2)
    with plot1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(uni.plot_yearly_arrivals())

    with plot2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(uni.plot_pie("carrier"))

    # Row 3: Insights
    insight1, insight2 = st.columns(2)
    with insight1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85);
        padding: 1rem; border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> The airline industry experienced strong growth from 2013–2019, followed by a sharp collapse in 2020 due to COVID-19. While 2021–2022 saw recovery in demand, the 2023 drop signals ongoing operational and economic volatility, emphasizing the need for resilient forecasting and agile capacity planning.
        </div>
        """, unsafe_allow_html=True)

    with insight2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85);
        padding: 1rem; border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Flight activity is highly concentrated among a few dominant carriers — with OO, DL, and MQ leading. This imbalance skews overall delay trends toward the operational behaviors of these major airlines. However, the 26% of flights grouped under “Other” highlight the need for granular, carrier-specific analysis when assessing delay risk or crafting optimization strategies.
        </div>
        """, unsafe_allow_html=True)

    # Bottom spacing after full block
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# === SECTION 2: TIME TRENDS (CLEAN & ALIGNED) ===
with st.container():
    st.subheader("Time Trends (Yearly)")

    # Row 1: Descriptions
    desc1, desc2 = st.columns(2)
    with desc1:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Delay Ratio Over Time</b><br>
        This plot tracks the proportion of delayed flights (15+ mins) to total flights on a yearly basis. 
        It highlights how operational performance changes over time, independent of traffic volume.
        </div>""", unsafe_allow_html=True)

    with desc2:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Cancellation Rate Over Time</b><br>
        This chart shows the yearly trend in cancellations as a percentage of total scheduled flights. 
        It captures seasonal impacts, crisis periods, and airline-level operational challenges.
        </div>""", unsafe_allow_html=True)

    # Row 2: Plots
    plot1, plot2 = st.columns(2)
    with plot1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.plot_delay_ratio_yearly())

    with plot2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.plot_cancellation_rate_yearly())

    # Row 3: Insights
    insight1, insight2 = st.columns(2)
    with insight1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Delay ratios rebounded post-2020, surpassing pre-pandemic levels by 2023 — 
        indicating that operational bottlenecks, staffing shortages, or demand surges may now outweigh past systemic controls. 
        Even with fewer flights than 2019, punctuality has deteriorated — signaling deeper structural inefficiencies.
        </div>
        """, unsafe_allow_html=True)

    with insight2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Excluding the 2020 crisis spike, cancellation rates have remained consistently low,
        demonstrating strong airline control over schedule execution. This contrasts with rising delays,
        suggesting airlines prioritize operating flights — even late — over canceling them.
        </div>
        """, unsafe_allow_html=True)

# Row 4: Diversion Description (full-width)
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
<b>Diversion Rate Over Time</b><br>
This lineplot represents the percentage of flights diverted from their intended destination each year. 
It is a measure of airspace or airport instability and last-minute routing changes.
</div>
""", unsafe_allow_html=True)

# Row 5: Diversion Plot (full-width)
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.pyplot(eda_fe.plot_diversion_rate_yearly())

# Row 6: Diversion Insight (still full-width)
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
<i>Insight:</i> Diversions are infrequent but have risen post-pandemic, peaking in 2023. 
This trend signals growing instability in airport or airspace operations — likely linked to increased weather volatility, 
route congestion, or limited infrastructure flexibility during recovery. Continuous monitoring is essential, 
as diversions carry high passenger disruption costs despite low frequency.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
# === SECTION 3: DELAY CAUSE ANALYSIS ===
with st.container():
    st.subheader("Delay Cause Analysis")

    # Row 1: Descriptions
    desc1, desc2 = st.columns(2)
    with desc1:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Average Delay % by Cause</b><br>
        This plot shows the average percentage of total delay attributed to each delay category. 
        It highlights which factors contribute most consistently across the dataset.
        </div>""", unsafe_allow_html=True)

    with desc2:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Delay Causes (Peak Season)</b><br>
        This pie chart illustrates the distribution of delay causes during peak traffic months. 
        It captures how delay factors shift during the most operationally intense periods.
        </div>""", unsafe_allow_html=True)

    # Row 2: Plots
    plot1, plot2 = st.columns(2)
    with plot1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.plot_avg_delay_pct_by_cause())

    with plot2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.plot_delay_causes_proportion_peak())

    # Row 3: Insights
    insight1, insight2 = st.columns(2)
    with insight1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Carrier-related issues and late aircraft delays are the top contributors to total delay time,
        together accounting for over 70%. These represent systemic and recurring inefficiencies within airline operations — such as tight schedules, crew/resource delays, or maintenance issues — and outweigh external causes like weather or air traffic control. Prioritizing internal process optimization can yield the highest impact on overall delay reduction.
        </div>
        """, unsafe_allow_html=True)

    with insight2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> During peak traffic months, late aircraft delays surge to over 40%, becoming the dominant disruption source. Carrier delays remain high as well, highlighting operational strain during holidays and summer travel. This suggests that airlines face major scalability issues in high-demand periods, and should invest in buffer strategies, flexible scheduling, and turnaround optimization to reduce cascading delays.
        </div>
        """, unsafe_allow_html=True)

    # Row 4: Full-width description for third chart
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
    border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
    <b>Dominant Delay Cause (per flight)</b><br>
    This bar chart reveals the most common primary cause of delay at the flight level. 
    Each flight is assigned its top contributing delay factor.
    </div>
    """, unsafe_allow_html=True)

    # Plot and Insight (full-width)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.pyplot(eda_fe.plot_dominant_delay_causes_count())

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
    border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
    <i>Insight:</i> Most delayed flights are primarily caused by carrier-related and late aircraft delays — not external disruptions. This highlights deep-rooted internal inefficiencies like tight scheduling, crew availability, or inadequate turnaround buffers. These internal delays often create a ripple effect that propagates across the network, especially during high-frequency schedules. Tackling these leading causes offers the most direct path to performance improvement.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)


# Note: Column col4 remains empty to keep layout balanced.
# === SECTION 4: SEASONAL DELAY PATTERNS ===
with st.container():
    st.subheader("Seasonal Delay Patterns")

    # Row 1: Descriptions
    desc1, desc2 = st.columns(2)
    with desc1:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Average Delay per Flight by Season</b><br>
        This bar chart displays the average delay time per flight for each season. 
        It highlights how travel efficiency changes with seasonal patterns.
        </div>""", unsafe_allow_html=True)

    with desc2:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Total Flights per Season</b><br>
        This chart shows the total number of flights operated in each season. 
        It provides context for comparing seasonal delay rates with traffic volume.
        </div>""", unsafe_allow_html=True)

    # Row 2: Plots
    plot1, plot2 = st.columns(2)
    with plot1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.plot_avg_delay_per_flight_seasonal())

    with plot2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.plot_flights_per_season())

    # Row 3: Insights
    insight1, insight2 = st.columns(2)
    with insight1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Summer shows the highest average delay per flight, reflecting the operational strain of peak demand and tighter schedules. Winter delays are also elevated, likely due to weather-related challenges. In contrast, fall emerges as the most efficient season — offering a key opportunity for performance benchmarking.
        </div>
        """, unsafe_allow_html=True)

    with insight2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Summer leads in total flight volume, but winter’s lower traffic doesn’t guarantee fewer delays — suggesting that volume isn’t the sole disruption driver. Seasonal inefficiencies likely stem from a mix of demand surges and environmental factors, reinforcing the need for season-specific operational strategies.
        </div>
        """, unsafe_allow_html=True)

    # Row 4: Additional seasonal insights
    plot3, plot4 = st.columns(2)
    with plot3:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.plot_delay_causes_seasonal_distribution())

    with plot4:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.plot_disruption_rate_by_season())

    # Row 5: Final insights
    insight3, insight4 = st.columns(2)
    with insight3:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Summer brings a sharp rise in carrier and late aircraft delays, reflecting operational overload. Weather becomes the dominant disruptor in winter, while spring and summer see heavier NAS-related delays — suggesting seasonal congestion patterns in airspace and infrastructure.
        </div>
        """, unsafe_allow_html=True)

    with insight4:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Winter suffers the highest proportion of disrupted flights despite lower traffic, indicating reduced reliability due to weather and seasonal volatility. Fall stands out as the most stable season — an operational benchmark for reliability and planning.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# === SECTION 5: CARRIER BEHAVIOR ===
with st.container():
    st.subheader("Carrier Behavior")

    # Row 1: Descriptions
    desc1, desc2 = st.columns(2)
    with desc1:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Avg Delay Ratio per Carrier</b><br>
        This chart ranks airlines based on the average proportion of delayed flights. 
        It highlights overall reliability across the entire dataset.
        </div>""", unsafe_allow_html=True)

    with desc2:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Carrier Delay Ratio by Season</b><br>
        This seasonal breakdown compares how delay ratios shift for each airline throughout the year.
        </div>""", unsafe_allow_html=True)

    # Row 2: Plots
    plot1, plot2 = st.columns(2)
    with plot1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.avg_delay_ratio_per_carrier())

    with plot2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.delay_ratio_across_seasons())

    # Row 3: Insights
    insight1, insight2 = st.columns(2)
    with insight1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Airlines like Envoy Air and JetBlue exhibit the highest average delay ratios across the dataset, suggesting persistent reliability issues. In contrast, Southwest and Delta maintain strong operational performance, indicating effective delay mitigation strategies and better schedule management.
        </div>
        """, unsafe_allow_html=True)

    with insight2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Some airlines — such as JetBlue and Frontier — show sharp seasonal deterioration, especially in summer, pointing to scalability issues under pressure. Others, including Delta and Southwest, exhibit consistent year-round performance, indicating robust operational resilience.
        </div>
        """, unsafe_allow_html=True)

    # Row 4: Additional descriptions
    desc3, desc4 = st.columns(2)
    with desc3:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Top 10 Carriers: Delay Cause Breakdown</b><br>
        This chart decomposes total delay minutes for the top 10 airlines, categorized by delay type.
        </div>""", unsafe_allow_html=True)

    with desc4:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Delay Cause vs Disruption Rate</b><br>
        This scatterplot shows how different delay causes contribute to higher disruption rates across carriers.
        </div>""", unsafe_allow_html=True)

    # Row 5: Final plots
    plot3, plot4 = st.columns(2)
    with plot3:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.delay_cause_breakdown_top3_carriers())

    with plot4:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.delay_cause_vs_disruption_correlation())

    # Row 6: Final insights
    insight3, insight4 = st.columns(2)
    with insight3:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Most major airlines are primarily impacted by late aircraft and carrier-related delays, highlighting internal operational bottlenecks. However, some carriers also exhibit elevated NAS and weather-related delays, indicating varying levels of infrastructure exposure and airspace vulnerability.
        </div>
        """, unsafe_allow_html=True)

    with insight4:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Carrier and late aircraft delays are the strongest predictors of disruption at the airline level. Flights delayed for these reasons tend to result in broader network unreliability. By contrast, weather and security delays have less consistent correlation with high disruption — making internal airline processes the top target for reliability improvements.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
# === SECTION 6: AIRPORT INSIGHTS ===
with st.container():
    st.subheader("Airport Insights")

    # Row 1: Descriptions
    desc1, desc2 = st.columns(2)
    with desc1:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Avg Delay vs Delay Rate (Top Airports)</b><br>
        Compares delay intensity and frequency among the 10 busiest airports. 
        This highlights how different hubs handle traffic and disruptions.
        </div>""", unsafe_allow_html=True)

    with desc2:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
        <b>Delay Ratio vs Flight Volume</b><br>
        Visualizes the relationship between flight volume and average delay ratio across airports. 
        Helps assess whether higher traffic leads to worse performance.
        </div>""", unsafe_allow_html=True)

    # Row 2: Plots
    plot1, plot2 = st.columns(2)
    with plot1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.top_airports_delay_metrics())

    with plot2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.pyplot(eda_fe.delay_ratio_vs_flight_volume())

    # Row 3: Insights
    insight1, insight2 = st.columns(2)
    with insight1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> Some major hubs — such as Chicago and San Francisco — consistently experience both longer and more frequent delays, suggesting structural or environmental constraints. Others, like Atlanta and Dallas, handle comparable traffic with lower disruption levels — making them operational benchmarks worth studying.
        </div>
        """, unsafe_allow_html=True)

    with insight2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
        border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
        <i>Insight:</i> High traffic volume does not necessarily lead to worse delay performance. Many large airports operate with low delay ratios, indicating that efficiency is driven more by management practices, layout, and resource allocation than by raw traffic volume alone.
        </div>
        """, unsafe_allow_html=True)

    # Heatmap (full width)
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
    border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
    <b>Top Airports: Delay Cause Breakdown</b><br>
    Heatmap displaying the total number of delays by cause for the top 20 busiest airports. 
    Enables pinpointing operational weaknesses across major hubs.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.pyplot(eda_fe.airport_delay_cause_heatmap())

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
    border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
    <i>Insight:</i> This heatmap reveals clear delay type dominance across major U.S. airports, exposing location-specific vulnerabilities. For example, NAS delays plague Chicago and Newark, while carrier and late aircraft delays are the main bottlenecks at Atlanta and Dallas. These patterns enable targeted operational interventions — such as airspace coordination at ORD and turnaround efficiency improvements at ATL.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# === SECTION 7: RISK LEVELS ===
with st.container():
    st.subheader("Risk Level Distribution")

    # Description
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
    border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"">
    <b>Distribution of Delay Risk Levels</b><br>
    Breaks down the share of flights into low, medium, and high delay risk. 
    These levels help gauge how widespread and severe delay threats are across the dataset.
    </div>""", unsafe_allow_html=True)

    # Plot
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.pyplot(eda_fe.plot_delay_risk_level_distribution())

    # Insight
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="<div style="color: black; background: rgba(255,255,255,0.85); padding: 1rem;
    border-radius: 12px; min-height: 210px; max-height: 210px; overflow-y: auto;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 1rem; line-height: 1.6; font-family: 'Roboto', sans-serif;"">
    <i>Insight:</i> While most flights are low risk, nearly 40% fall into medium to high delay risk categories — signaling a non-negligible vulnerability across the network. These insights are valuable for proactive planning, such as prioritizing resource allocation, adjusting buffer times, and targeting high-risk routes or carriers for operational reviews.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)


# === FOOTER (Unified with other pages) ===
st.markdown("""
<hr style="margin-top: 3rem; border: none; border-top: 1px solid #ccc;">
<div style='text-align: center; padding: 1rem 0; color: #666; font-size: 0.9rem; font-family: 'Roboto', sans-serif;'>
Data Analysis Page — Part of the Flight Delay Dashboard by <b>Omar Yasser</b>
</div>
""", unsafe_allow_html=True)
