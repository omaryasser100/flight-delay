import streamlit as st
from datetime import datetime
from backend.chatbot_backend import query_huggingface_api  # ✅ Import chatbot logic


# ===================== 🔧 Background Video Setup =====================
def set_background(video_url):
    """Set a full-screen looping video as the app's background."""
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

        /* === Sidebar Styling === */
        section[data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(10px);
        }}

        section[data-testid="stSidebar"] * {{
            color: white !important;
            text-shadow: 0 0 3px rgba(0,0,0,0.6);
        }}

        /* === Sidebar Hover Animation for Navigation === */
        section[data-testid="stSidebar"] ul li a {{
            position: relative;
            font-weight: bold;
            color: white !important;
            text-shadow: 0 0 3px rgba(0,0,0,0.5);
            transition: all 0.3s ease;
            padding: 8px 16px;
            border-radius: 8px;
        }}

        section[data-testid="stSidebar"] ul li a:hover {{
            background-color: rgba(255,255,255,0.15);
            transform: scale(1.04) translateX(5px);
            text-shadow: 0 0 6px #00ffff;
        }}
    </style>

    <div id="background-video-container">
        <video autoplay muted loop playsinline>
            <source src="{video_url}" type="video/mp4">
        </video>
    </div>
    """, unsafe_allow_html=True)


# ===================== 🧭 Title in Transparent Top Bar =====================
def render_title_bar():
    """Render the main title embedded in the top transparent bar."""
    st.markdown("""
        <div class='title-in-bar' style="
            width: 100%;
            text-align: center;
            font-size: 2rem;
            font-weight: 800;
            padding: 1rem 0;
            color: white;
            text-shadow: 0 0 4px rgba(0,0,0,0.6);
        ">
            Flight Delay Dashboard
        </div>
    """, unsafe_allow_html=True)



# ===================== 🕒 Dynamic Clock Display =====================
def render_clock():
    """Display a live date and time (hourly granularity)."""
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")

    st.markdown(f"""
        <div class='welcome-text' style="
            font-size: 1rem;
            font-weight: 500;
            color: #eee;
            padding-bottom: 0.5rem;
            text-shadow: 0 0 3px rgba(0,0,0,0.4);
        ">
            📅 {date_str} | 🕒 {time_str}
        </div>
    """, unsafe_allow_html=True)


# ===================== 📚 Sidebar Layout Placeholder =====================
def render_sidebar():
    """Empty placeholder for future sidebar elements."""
    with st.sidebar:
        pass


# ===================== 🤖 Chatbot Frontend UI =====================
def render_sidebar_chatbot():
    """Render chatbot input and visual box inside the sidebar."""
    with st.sidebar:
        st.markdown("---")

        # Info box about the chatbot
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.07);
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 0 6px rgba(0,0,0,0.2);
            text-align: center;
            margin-top: 1rem;
        ">
            <h4 style="color: white; margin-bottom: 0.5rem;">💬 Delay Assistant</h4>
            <p style="font-size: 0.9rem; color: #ddd;">
                Ask me anything about flight delays.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Chat input box
        query = st.text_input("Type your question here...", key="chatbot_input")

        # Show response if query is submitted
        if query:
            st.markdown("####  Answer")
            with st.spinner(" Thinking..."):
                response = query_huggingface_api(query)
                st.write(response)
