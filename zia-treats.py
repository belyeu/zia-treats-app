import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Zia Sweet Treats", page_icon="🍪", layout="wide")

# --- Crumbl-Inspired Custom CSS ---
st.markdown("""
    <style>
    /* Main background and fonts */
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #333333; font-family: 'Helvetica Neue', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Cookie Card Styling */
    .cookie-container {
        border-radius: 20px;
        padding: 20px;
        background-color: #F9F9F9;
        text-align: center;
        transition: transform 0.3s;
        margin-bottom: 20px;
    }
    .cookie-container:hover { transform: scale(1.02); }
    
    /* Signature Pink Button */
    .stButton>button {
        background-color: #FFD1DC; /* Crumbl Pink */
        color: #333333;
        border-radius: 50px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #F8B1C3;
        color: white;
    }
    
    /* Cart Sidebar */
    [data-testid="stSidebar"] { background-color: #FDF2F4; }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Inventory with Large Close-up Images
inventory = {
    "The Classic Choco": {"price": 4.50, "desc": "Our award-winning milk chocolate chip.", "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600"},
    "Pink Velvet": {"price": 4.50, "desc": "A cakey velvet cookie topped with cream cheese frosting.", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600"},
    "Midnight Oreo": {"price": 4.50, "desc": "Dark chocolate cookie with white chocolate chunks.", "img": "https://images.unsplash.com/photo-1590080876251-130a74c692dd?w=600"},
    "Iced Sugar": {"price": 4.00, "desc": "Perfectly chilled sugar cookie with almond frosting.", "img": "https://images.unsplash.com/photo-1506459225024-1428097a7e18?w=600"}
}

# --- Layout ---
# Logo / Header
st.markdown("<h1 style='text-align: center;'>Zia Sweet Treats</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #999;'>TASTE THE WEEKLY LINEUP</p>", unsafe_allow_html=True)
st.write("---")

# Menu Grid
col1, col2 = st.columns(2, gap="large")

for i, (item, details) in enumerate(inventory.items()):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
            <div class="cookie-container">
                <img src="{details['img']}" style="width:100%; border-radius:15px; margin-bottom:15px;">
                <h3>{item}</h3>
                <p style="color: #666; font-style: italic;">{details['desc']}</p>
                <p style="font-weight: bold; font-size: 1.2em;">${details['price']:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"ADD TO BOX", key=item):
            st.session_state.cart[item] = st.session_state.cart.get(item, 0) + 1
            st.toast(f"Added {item} to your box! 🎀")

# --- Sticky Sidebar Cart ---
with st.sidebar:
    st.markdown("## YOUR PINK BOX")
    if not st.session_state.cart:
        st.write("Your box is empty! Add some treats to get started.")
    else:
        total = 0
        for item, qty in st.session_state.cart.items():
            sub = inventory[item]['price'] * qty
            total += sub
            st.write(f"**{qty}x** {item} — ${sub:.2f}")
        
        st.divider()
        st.write(f"### Total: ${total:.2f}")
        
        if st.button("CHECKOUT"):
            st.balloons()
            st.success("Order Placed! Your cookies are being baked fresh.")
            st.session_state.cart = {}
            
        if st.button("EMPTY BOX", type="secondary"):
            st.session_state.cart = {}
            st.rerun()

    st.markdown("---")
    st.markdown("📍 Zia Sweet Treats | Fresh Weekly")
