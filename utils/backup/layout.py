import streamlit as st
from datetime import datetime

def set_background(video_url):
    st.markdown(f"""
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent !important;
            overflow-x: hidden;
            overflow-y: auto;
        }}

        .stApp {{
            background-color: transparent;
        }}

        #background-video-container {{
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            width: 100vw;
            z-index: -1;
            overflow: hidden;
        }}

        #background-video-container video {{
            object-fit: cover;
            width: 100vw;
            height: 100vh;
        }}

        header, footer {{
            background-color: rgba(0, 0, 0, 0) !important;
        }}

        section[data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(10px);
        }}

        section[data-testid="stSidebar"] * {{
            color: white !important;
            text-shadow: 0 0 3px rgba(0,0,0,0.6);
        }}
    </style>

    <div id="background-video-container">
        <video autoplay muted loop playsinline>
            <source src="{video_url}" type="video/mp4">
        </video>
    </div>
    """, unsafe_allow_html=True)




def render_title_bar():
    st.markdown("""
        <div class='title-in-bar'>Flight Delay Dashboard</div>
    """, unsafe_allow_html=True)

def render_clock():
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    st.markdown(
        f"<div class='welcome-text'>📅 {date_str} | 🕒 {time_str}</div>",
        unsafe_allow_html=True
    )

def render_sidebar():
    with st.sidebar:
        pass

def render_sidebar_chatbot():
    from backend.chatbot_module import get_flight_delay_answer

    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 Ask the Delay Assistant")

    query = st.sidebar.text_input("Ask me about flight delays:", key="chatbot_input")
    if query:
        with st.spinner("Thinking..."):
            response = get_flight_delay_answer(query)
        st.sidebar.markdown("#### ✈️ Answer")
        st.sidebar.write(response)
