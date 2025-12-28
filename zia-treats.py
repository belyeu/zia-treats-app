import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Configuration & Styling ---
st.set_page_config(page_title="Zia Sweet Treats | Lubbock", layout="wide", page_icon="🍪")

# Crumbl-Inspired CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #333333; font-family: 'Helvetica Neue', sans-serif; text-transform: uppercase; letter-spacing: 2px; text-align: center; }
    .box-card { border: 2px solid #F0F0F0; border-radius: 20px; padding: 25px; text-align: center; background-color: #FAFAFA; transition: 0.3s; cursor: pointer; }
    .box-card:hover { border-color: #FFD1DC; background-color: #FDF2F4; }
    .stButton>button { background-color: #FFD1DC; color: #333333; border-radius: 50px; border: none; padding: 12px 20px; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #F8B1C3; color: white; }
    .cookie-img { width: 100%; border-radius: 15px; margin-bottom: 10px; }
    [data-testid="stSidebar"] { background-color: #FDF2F4; border-left: 1px solid #FFD1DC; }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'order_step' not in st.session_state: st.session_state.order_step = 'box'
if 'selected_box' not in st.session_state: st.session_state.selected_box = None
if 'box_items' not in st.session_state: st.session_state.box_items = []

# --- Menu Data ---
box_types = {
    "Single": {"size": 1, "price": 4.50, "save": "0%"},
    "4-Pack": {"size": 4, "price": 15.50, "save": "12%"},
    "6-Pack": {"size": 6, "price": 22.25, "save": "16%"},
    "12-Pack": {"size": 12, "price": 38.50, "save": "28%"}
}

weekly_flavors = {
    "Milk Chocolate Chip": {"desc": "Thick, soft, and packed with milk chocolate chips.", "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400", "cals": 730},
    "Pink Velvet Cake": {"desc": "A velvety cookie topped with cream cheese frosting.", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400", "cals": 810},
    "Salted Caramel Brownie": {"desc": "Fudgy chocolate brownie topped with gooey caramel.", "img": "https://images.unsplash.com/photo-1590080876251-130a74c692dd?w=400", "cals": 850},
    "Lemon Poppy Seed": {"desc": "Zesty lemon cookie with a tangy filling.", "img": "https://images.unsplash.com/photo-1506459225024-1428097a7e18?w=400", "cals": 680}
}

# --- Header ---
st.markdown("<h1>Zia Sweet Treats</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>FRESHLY BAKED • LUBBOCK, TX</p>", unsafe_allow_html=True)

# --- Step 1: Box Selection (Functional Replica) ---
if st.session_state.order_step == 'box':
    st.markdown("## 1. Choose Your Box")
    cols = st.columns(len(box_types))
    for name, details in box_types.items():
        with cols[list(box_types.keys()).index(name)]:
            st.markdown(f"""
                <div class="box-card">
                    <h3 style="font-size: 1em;">{name}</h3>
                    <p style="font-size: 1.2em; font-weight: bold;">${details['price']:.2f}</p>
                    <p style="color: #ff4b4b; font-size: 0.8em;">Save {details['save']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"SELECT", key=name):
                st.session_state.selected_box = name
                st.session_state.order_step = 'flavor'
                st.rerun()

# --- Step 2: Flavor Selection (Functional Replica) ---
elif st.session_state.order_step == 'flavor':
    box_size = box_types[st.session_state.selected_box]['size']
    remaining = box_size - len(st.session_state.box_items)
    
    col_l, col_r = st.columns([2.5, 1], gap="large")
    
    with col_l:
        st.markdown(f"## 2. Fill Your {st.session_state.selected_box}")
        st.write(f"Spots remaining: **{remaining}**")
        
        f_cols = st.columns(2)
        for i, (name, d) in enumerate(weekly_flavors.items()):
            with f_cols[i % 2]:
                st.markdown(f"""
                    <div style="background:#fcfcfc; padding:20px; border-radius:20px; border: 1px solid #eee; margin-bottom:15px;">
                        <img src="{d['img']}" class="cookie-img">
                        <h4 style="margin: 5px 0;">{name}</h4>
                        <p style="font-size: 0.8em; color: #666;">{d['desc']}</p>
                        <p style="font-weight: bold; color: #333;">{d['cals']} CAL</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"ADD {name.upper()}", key=f"add_{name}", disabled=remaining <= 0):
                    st.session_state.box_items.append(name)
                    st.rerun()

    # Sticky Sidebar / Selection Column
    with col_r:
        st.markdown("### 📦 Your Selection")
        if not st.session_state.box_items:
            st.info("Your box is empty! Add some cookies.")
        else:
            for idx, item in enumerate(st.session_state.box_items):
                st.write(f"**{idx+1}.** {item}")
            
            st.divider()
            st.write(f"**Box Total: ${box_types[st.session_state.selected_box]['price']:.2f}**")
            
            # Gifting Feature (Replicating Crumbl's checkout option)
            st.checkbox("Is this a gift? 🎀")
            
            if remaining == 0:
                if st.button("PROCEED TO CHECKOUT"):
                    st.balloons()
                    st.success("Redirecting to secure checkout...")
            
            if st.button("Change Box Size", type="secondary"):
                st.session_state.order_step = 'box'
                st.session_state.box_items = []
                st.rerun()
