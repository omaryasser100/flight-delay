import streamlit as st
from datetime import datetime
import random
from streamlit_autorefresh import st_autorefresh
from utils.layout import (
    set_background,
    render_title_bar,
    render_sidebar,
    render_clock,
    render_sidebar_chatbot
)

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Business Insights", layout="wide", initial_sidebar_state="expanded")

# ========== DARK MODE & TOKEN INIT ==========
query_params = st.query_params
dark_mode_param = query_params.get("dark", "0") == "1"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = dark_mode_param

if "token" not in st.session_state:
    st.session_state.token = random.randint(1000, 999999)

# ========== BACKGROUND VIDEO ==========
light_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978357/bg_light_q3ifwd.mp4"
dark_video = "https://res.cloudinary.com/dlyswnhz4/video/upload/v1748978356/bg_dark_kffpsn.mp4"
selected_video = dark_video if st.session_state.dark_mode else light_video
video_url = f"{selected_video}?v={st.session_state.token}"
set_background(video_url)

# ========== TITLE BAR ==========
render_title_bar()

# ========== GREETING + DARK MODE TOGGLE ==========
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

# ========== SIDEBAR ==========
render_sidebar()
render_sidebar_chatbot()

# ========== EXECUTIVE SUMMARY ==========
st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.85);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.15rem;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    ">
    This section presents final business insights derived from comprehensive analysis of U.S. flight delay data. The goal is to translate complex data patterns into actionable recommendations for airlines, airports, and policymakers.
    </div>
""", unsafe_allow_html=True)

# ========== STRATEGIC INSIGHTS ==========
insights = [
    ("1. Fragile Recovery Demands Smarter Forecasting", 
     "Flight volumes declined again in 2023 despite earlier post-COVID recovery, highlighting a fragile demand environment. Airlines and airports should implement dynamic forecasting systems that account for macroeconomic signals, weather disruptions, and health indicators to avoid resource misalignment and revenue shortfalls."
    ),
    
    ("2. Persistent Delays Signal Operational Saturation", 
     "Delay rates have exceeded pre-pandemic levels, pointing to systemic strain across airside and ground operations. Stakeholders should upgrade queue management, implement real-time gate flow analytics, and enhance coordination between carriers and ATC to absorb volume spikes and reduce inefficiencies."
    ),
    
    ("3. Seasonal Delay Patterns Require Targeted Planning", 
     "Summer delays are often tied to crew and turnaround issues, while winter disruptions are driven by severe weather. Response protocols must be customized per season—flexible staffing in summer and early rerouting in winter—rather than applying generic disruption plans."
    ),
    
    ("4. Airline-Controlled Issues Dominate Delay Causes", 
     "Most delays originate from controllable airline operations such as late aircraft readiness, inefficient turnaround, and crew scheduling conflicts. Prioritizing predictive maintenance, real-time dispatching, and improved SOP adherence can significantly reduce these delays."
    ),
    
    ("5. Carrier Performance Disparities Reveal Optimization Gaps", 
     "Some airlines consistently underperform in delay rates compared to peers. Industry-wide benchmarking, performance transparency, and cross-carrier learning can raise operational standards and reduce variance across the network."
    ),
    
    ("6. Peak Season Breakdowns Point to Fragile Schedules", 
     "Carriers experiencing operational decline during peak travel periods may be lacking resilience mechanisms. Stress-testing summer schedules and integrating buffers—such as standby crew and aircraft—can improve system stability during demand surges."
    ),
    
    ("7. Airport Efficiency Is Not Solely Volume Dependent", 
     "Airports with similar traffic profiles show varying delay outcomes. High-performing hubs optimize gate allocation, ground routing, and terminal flow. Underperforming airports should prioritize localized bottleneck analysis and surface logistics upgrades."
    ),
    
    ("8. Delay Drivers Are Location-Specific", 
     "Airports experience distinct dominant causes—ranging from airspace congestion to seasonal weather or carrier operations. Localized mitigation strategies tailored to each airport’s disruption profile are more effective than universal solutions."
    ),
    
    ("9. Low Traffic Doesn’t Guarantee Low Risk", 
     "Despite lower traffic, winter remains the most disrupted season, while fall often performs best. Adopting fall-season practices such as proactive crew assignment and flexible slot planning may improve resilience in high-risk months."
    ),
    
    ("10. Risk Stratification Enables Proactive Scheduling", 
     "A large portion of flights fall into medium or high delay-risk segments. Integrating delay risk scores into scheduling workflows allows operators to reroute, reschedule, or preemptively adjust high-risk flights to minimize network-wide impact."
    )
]

for title, body in insights:
    st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.65);
            border-left: 5px solid #2a9d8f;
            padding: 1rem 1.5rem;
            margin-bottom: 1.2rem;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        ">
        <h4 style="margin-top:0;">{title}</h4>
        <p style="font-size: 0.95rem; line-height: 1.6;">{body}</p>
        </div>
    """, unsafe_allow_html=True)

# ========== CONCLUSION BOX ==========
st.markdown("""
    <div style="
        background: #264653;
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 10px;
        font-size: 1.05rem;
        font-weight: 500;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        margin-top: 2rem;
    ">
    <b>Conclusion:</b><br><br>
    The flight delay dashboard not only reveals systemic bottlenecks but also points to clear, actionable improvements in forecasting, planning, and operations. By acting on these insights, airlines, airports, and regulators can improve on-time performance, reduce resource waste, and boost resilience across the national airspace system.
    </div>
""", unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("""
<hr style="margin-top: 3rem; border: none; border-top: 1px solid rgba(255,255,255,0.3);">
<div style='
    text-align: center;
    padding: 1rem 0;
    color: white;
    font-size: 0.9rem;
    text-shadow: 0 0 3px rgba(0,0,0,0.5);
'>
Flight Delay Dashboard v1.0 — Built by Omar Yasser
</div>
""", unsafe_allow_html=True)
