import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# --- Page Configuration ---
st.set_page_config(page_title="Zia Sweet Treats", page_icon="🍪", layout="wide")

# Custom CSS for a more "pleasing" aesthetic
st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    .stButton>button { width: 100%; border-radius: 20px; border: 1px solid #ff4b4b; background-color: white; color: #ff4b4b; }
    .stButton>button:hover { background-color: #ff4b4b; color: white; }
    .cookie-card { border: 1px solid #eee; padding: 15px; border-radius: 15px; background-color: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'user' not in st.session_state:
    st.session_state.user = {"name": "", "contact": "", "logged_in": False}

# Shared Inventory (Mock database)
inventory = {
    "Chocolate Chip": {"price": 2.50, "stock": 50, "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400"},
    "Oatmeal Raisin": {"price": 2.00, "stock": 30, "img": "https://images.unsplash.com/photo-1590080876251-130a74c692dd?w=400"},
    "Sugar Cookie":   {"price": 1.75, "stock": 40, "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400"},
    "Peanut Butter":  {"price": 2.25, "stock": 25, "img": "https://images.unsplash.com/photo-1506459225024-1428097a7e18?w=400"}
}

# --- Main UI ---
st.title("🍭 Zia Sweet Treats")
st.write("---")

# 1. Better Customer Login Layout
if not st.session_state.user["logged_in"]:
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("Welcome! Please Sign In")
            name = st.text_input("Name")
            contact = st.text_input("Phone or Email")
            if st.button("Start Shopping"):
                if name:
                    st.session_state.user = {"name": name, "contact": contact, "logged_in": True}
                    st.rerun()
                else:
                    st.error("Please enter your name.")
    st.stop() # Prevents showing the store until login

# 2. Main Store Layout
col_menu, col_cart = st.columns([3, 1], gap="large")

with col_menu:
    st.markdown(f"### Hello, {st.session_state.user['name']}! 🍪")
    st.write("Pick your favorite treats below:")
    
    # Grid Layout for Cookies
    m_col1, m_col2 = st.columns(2)
    for i, (item, details) in enumerate(inventory.items()):
        target_col = m_col1 if i % 2 == 0 else m_col2
        with target_col:
            st.markdown(f'<div class="cookie-card">', unsafe_allow_html=True)
            st.image(details['img'], use_container_width=True)
            st.write(f"**{item}**")
            st.write(f"${details['price']:.2f} | Stock: {details['stock']}")
            if st.button(f"Add to Box", key=item):
                st.session_state.cart[item] = st.session_state.cart.get(item, 0) + 1
                st.toast(f"Added {item}!")
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("") # Spacer

with col_cart:
    st.markdown("### 🛒 Your Box")
    if not st.session_state.cart:
        st.write("Your box is empty.")
    else:
        total = 0
        for item, qty in st.session_state.cart.items():
            subtotal = inventory[item]['price'] * qty
            total += subtotal
            st.write(f"{qty}x {item} (${subtotal:.2f})")
        
        st.write("---")
        st.write(f"**Grand Total: ${total:.2f}**")
        
        if st.button("Clear Box"):
            st.session_state.cart = {}
            st.rerun()
            
        if st.button("Checkout & PDF"):
            st.balloons()
            st.success("Order Placed!")
            # Add PDF generation logic here as needed
            st.session_state.cart = {}

# Sidebar: Sign out / Manager
with st.sidebar:
    st.write(f"Logged in as: **{st.session_state.user['name']}**")
    if st.button("Sign Out"):
        st.session_state.user = {"name": "", "contact": "", "logged_in": False}
        st.session_state.cart = {}
        st.rerun()
