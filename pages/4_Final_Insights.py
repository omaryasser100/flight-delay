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
insights =insights = [
    ("1. Demand is Still Unstable — Plan Smarter", 
     "Flight traffic dropped again in 2023, showing that recovery is still uncertain. Airlines and airports should use smarter forecasting tools that track things like the economy, weather, and health events to avoid wasting resources or losing revenue."
    ),
    
    ("2. High Delays Show Systems Are Overloaded", 
     "Delays are now worse than before the pandemic. This suggests that airport operations are under pressure. To fix this, improve how passengers and planes move through the airport and improve coordination between airlines and air traffic control."
    ),
    
    ("3. Delay Patterns Change with the Seasons", 
     "Summer delays are often due to staff shortages and slow turnarounds. Winter delays are usually caused by weather. Each season needs a different plan: add more flexible staff in summer and focus on faster rerouting in winter."
    ),
    
    ("4. Most Delays Come from the Airlines Themselves", 
     "Many delays happen because of things airlines can control — like late planes, poor scheduling, or slow processes. Fixing this means better maintenance, faster communication, and sticking to better internal procedures."
    ),
    
    ("5. Some Airlines Perform Much Worse Than Others", 
     "Not all airlines handle delays equally. To close the gap, the industry should compare performance, be transparent, and share best practices to help all carriers improve."
    ),
    
    ("6. Busy Seasons Expose Weaknesses", 
     "Some airlines struggle more during peak travel times. These problems can be reduced by testing schedules ahead of time and adding backup crews and planes during busy periods."
    ),
    
    ("7. Airport Efficiency Isn’t Only About Size", 
     "Airports with similar traffic levels often show very different delay records. The best ones manage gates, ground traffic, and passenger flow better. Others should study their specific issues and improve those areas first."
    ),
    
    ("8. Delay Causes Vary by Airport", 
     "Different airports face different problems — some deal with traffic congestion, others with bad weather. The best solutions are local ones that match each airport’s specific delay patterns."
    ),
    
    ("9. Less Traffic Doesn’t Always Mean Fewer Delays", 
     "Winter has fewer flights but still the most delays. Fall usually performs best. Using strategies that work well in fall, like smart crew planning and flexible scheduling, could help improve winter performance too."
    ),
    
    ("10. Knowing Risk Helps Plan Better Flights", 
     "Many flights fall into medium or high delay-risk categories. Using delay risk scores when scheduling flights helps avoid problems by adjusting or rescheduling high-risk flights ahead of time."
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
