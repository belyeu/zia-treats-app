import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Config & Styling ---
st.set_page_config(page_title="Zia Sweet Treats", page_icon="🍪", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    /* Crumbl Pink accents */
    [data-testid="stSidebar"] { background-color: #FDF2F4; border-right: 1px solid #FFD1DC; }
    .stButton>button { background-color: #FFD1DC; border-radius: 50px; font-weight: bold; width: 100%; border: none; }
    .stButton>button:hover { background-color: #F8B1C3; color: white; }
    h1 { color: #333333; text-transform: uppercase; letter-spacing: 2px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'page' not in st.session_state: st.session_state.page = 'Home'
if 'user' not in st.session_state: st.session_state.user = {"name": "", "logged_in": False}
if 'box_items' not in st.session_state: st.session_state.box_items = []

# --- Sidebar Menu ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=200", caption="Zia Sweet Treats")
    st.title("Menu")
    
    # Navigation Buttons
    if st.button("🏠 Home"): st.session_state.page = 'Home'
    if st.button("🍪 Order Now"): st.session_state.page = 'Order'
    if st.button("👤 Sign In"): st.session_state.page = 'Sign In'
    
    st.divider()
    if st.session_state.user["logged_in"]:
        st.write(f"Logged in as: **{st.session_state.user['name']}**")
        if st.button("Logout"):
            st.session_state.user = {"name": "", "logged_in": False}
            st.rerun()

# --- Page Logic ---

# HOME PAGE
if st.session_state.page == 'Home':
    st.markdown("<h1>Zia Sweet Treats</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1000", use_container_width=True)
    st.markdown("### This Week's Flavors")
    st.write("Taste the rotating menu that Lubbock is talking about!")
    if st.button("START YOUR ORDER"):
        st.session_state.page = 'Order'
        st.rerun()

# SIGN IN PAGE
elif st.session_state.page == 'Sign In':
    st.markdown("<h1>Sign In</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            name = st.text_input("First Name")
            phone = st.text_input("Phone Number")
            if st.button("Access My Rewards"):
                st.session_state.user = {"name": name, "logged_in": True}
                st.session_state.page = 'Home'
                st.rerun()

# ORDER PAGE (Box-First Flow)
elif st.session_state.page == 'Order':
    st.markdown("<h1>Select Your Box</h1>", unsafe_allow_html=True)
    
    # Reusing our Box-First Logic
    boxes = {"Single": 4.50, "4-Pack": 15.50, "6-Pack": 22.25, "12-Pack": 38.50}
    cols = st.columns(len(boxes))
    
    for i, (name, price) in enumerate(boxes.items()):
        with cols[i]:
            st.markdown(f"""
                <div style="text-align:center; border:1px solid #eee; padding:20px; border-radius:15px;">
                    <h4>{name}</h4>
                    <p>${price:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"SELECT {name}", key=name):
                st.success(f"{name} selected! Next: Pick your flavors.")
                # Logic for flavor selection would follow here
