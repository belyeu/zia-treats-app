import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime

# --- Page Config & Theme ---
st.set_page_config(page_title="Zia Sweet Treats | Lubbock", page_icon="🍪", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #333333; font-family: 'Helvetica Neue', sans-serif; text-transform: uppercase; letter-spacing: 2px; text-align: center; }
    .box-card { border: 2px solid #F0F0F0; border-radius: 20px; padding: 25px; text-align: center; background-color: #FAFAFA; transition: 0.3s; }
    .box-card:hover { border-color: #FFD1DC; background-color: #FDF2F4; }
    .stButton>button { background-color: #FFD1DC; color: #333333; border-radius: 50px; border: none; padding: 12px 20px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #F8B1C3; color: white; }
    [data-testid="stSidebar"] { background-color: #FDF2F4; border-left: 1px solid #FFD1DC; }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'step' not in st.session_state: st.session_state.step = 'login'
if 'user' not in st.session_state: st.session_state.user = {"name": "", "contact": ""}
if 'selected_box' not in st.session_state: st.session_state.selected_box = None
if 'box_contents' not in st.session_state: st.session_state.box_contents = []

DATA_FILE = 'zia_orders.csv'

# --- Data Definitions ---
boxes = {
    "Single": {"size": 1, "price": 4.50},
    "4-Pack": {"size": 4, "price": 15.50},
    "6-Pack": {"size": 6, "price": 22.25},
    "12-Pack (Party)": {"size": 12, "price": 38.50}
}

flavors = {
    "Milk Chocolate Chip": {"img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400"},
    "Classic Sugar": {"img": "https://images.unsplash.com/photo-1506459225024-1428097a7e18?w=400"},
    "Red Velvet": {"img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400"},
    "Salted Caramel": {"img": "https://images.unsplash.com/photo-1590080876251-130a74c692dd?w=400"}
}

# --- Helper Functions ---
def save_order(note):
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Customer", "Contact", "Box", "Contents", "Total", "Note"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            st.session_state.user['name'],
            st.session_state.user['contact'],
            st.session_state.selected_box,
            ", ".join(st.session_state.box_contents),
            boxes[st.session_state.selected_box]['price'],
            note
        ])

# --- Main App Logic ---
st.markdown("<h1>Zia Sweet Treats</h1>", unsafe_allow_html=True)

# 1. Login Step
if st.session_state.step == 'login':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Welcome to our Weekly Lineup")
        name = st.text_input("Name")
        contact = st.text_input("Phone Number")
        if st.button("Start Order"):
            if name and contact:
                st.session_state.user = {"name": name, "contact": contact}
                st.session_state.step = 'box_selection'
                st.rerun()
            else:
                st.warning("Please fill in your details.")

# 2. Box Selection Step
elif st.session_state.step == 'box_selection':
    st.markdown("## Step 1: Pick Your Box")
    cols = st.columns(len(boxes))
    for i, (name, info) in enumerate(boxes.items()):
        with cols[i]:
            st.markdown(f'<div class="box-card"><h3>{name}</h3><p>${info["price"]:.2f}</p></div>', unsafe_allow_html=True)
            if st.button(f"SELECT {name}", key=name):
                st.session_state.selected_box = name
                st.session_state.step = 'flavor_selection'
                st.rerun()

# 3. Flavor Selection Step
elif st.session_state.step == 'flavor_selection':
    size = boxes[st.session_state.selected_box]['size']
    remaining = size - len(st.session_state.box_contents)
    
    col_l, col_r = st.columns([2, 1], gap="large")
    
    with col_l:
        st.header(f"Fill Your {st.session_state.selected_box}")
        st.write(f"Spots left: **{remaining}**")
        f_cols = st.columns(2)
        for i, (name, d) in enumerate(flavors.items()):
            with f_cols[i % 2]:
                st.image(d['img'], use_container_width=True)
                if st.button(f"ADD {name.upper()}", key=name, disabled=remaining <= 0):
                    st.session_state.box_contents.append(name)
                    st.rerun()

    with col_r:
        st.markdown("### 📦 YOUR PINK BOX")
        for i, cookie in enumerate(st.session_state.box_contents):
            st.write(f"**{i+1}.** {cookie}")
        
        st.divider()
        note = st.text_area("Gift Note / Special Instructions")
        
        if remaining == 0:
            if st.button("FINALIZE ORDER"):
                save_order(note)
                st.balloons()
                st.session_state.step = 'complete'
                st.rerun()
        
        if st.button("Restart Order", type="secondary"):
            st.session_state.step = 'box_selection'
            st.session_state.box_contents = []
            st.rerun()

# 4. Completion Step
elif st.session_state.step == 'complete':
    st.success(f"Thank you, {st.session_state.user['name']}! Your order has been sent to the kitchen.")
    st.write("Pick up your fresh cookies at our Lubbock location.")
    if st.button("Place New Order"):
        st.session_state.step = 'box_selection'
        st.session_state.box_contents = []
        st.rerun()

# --- Sidebar: Admin/Manager ---
with st.sidebar:
    if st.checkbox("Admin Dashboard"):
        pw = st.text_input("Manager Password", type="password")
        if pw == "zia2025":
            st.subheader("Active Orders")
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
                st.dataframe(df)
                st.download_button("Export CSV", df.to_csv(index=False), "orders.csv")
