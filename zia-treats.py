import streamlit as st
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Zia Sweet Treats | Lubbock", page_icon="🍪", layout="wide")

# --- Custom Crumbl-Inspired CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #333333; font-family: 'Helvetica Neue', sans-serif; text-transform: uppercase; letter-spacing: 2px; text-align: center; }
    
    /* Box Selection Cards */
    .box-card {
        border: 2px solid #F0F0F0;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        background-color: #FAFAFA;
        transition: 0.3s;
    }
    .box-card:hover { border-color: #FFD1DC; background-color: #FDF2F4; }
    
    /* Buttons */
    .stButton>button {
        background-color: #FFD1DC; /* Signature Pink */
        color: #333333;
        border-radius: 50px;
        border: none;
        padding: 12px 20px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover { background-color: #F8B1C3; color: white; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #FDF2F4; border-left: 1px solid #FFD1DC; }
    </style>
    """, unsafe_allow_html=True)

# --- App State ---
if 'step' not in st.session_state: st.session_state.step = 'box_selection'
if 'selected_box' not in st.session_state: st.session_state.selected_box = None
if 'box_contents' not in st.session_state: st.session_state.box_contents = []

# --- Data Definitions ---
boxes = {
    "Single": {"size": 1, "price": 4.50},
    "4-Pack": {"size": 4, "price": 15.50},
    "6-Pack": {"size": 6, "price": 22.25},
    "12-Pack (Party)": {"size": 12, "price": 38.50}
}

flavors = {
    "Milk Chocolate Chip": {"desc": "The classic, thick and gooey.", "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400"},
    "Classic Sugar": {"desc": "Chilled with almond frosting.", "img": "https://images.unsplash.com/photo-1506459225024-1428097a7e18?w=400"},
    "Red Velvet": {"desc": "Cake-like with cream cheese swirl.", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400"},
    "Salted Caramel": {"desc": "Sweet & salty perfection.", "img": "https://images.unsplash.com/photo-1590080876251-130a74c692dd?w=400"}
}

# --- UI Header ---
st.markdown("<h1>Zia Sweet Treats</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>FRESHLY BAKED • LUBBOCK, TX</p>", unsafe_allow_html=True)
st.write("---")

# --- Logic: Step 1 (Pick Box) ---
if st.session_state.step == 'box_selection':
    st.markdown("## 1. SELECT YOUR BOX")
    cols = st.columns(len(boxes))
    
    for i, (name, info) in enumerate(boxes.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="box-card">
                    <h3 style="font-size: 1.1em;">{name}</h3>
                    <p style="font-size: 1.3em; font-weight: bold;">${info['price']:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"SELECT {name}", key=f"btn_{name}"):
                st.session_state.selected_box = name
                st.session_state.step = 'flavor_selection'
                st.rerun()

# --- Logic: Step 2 (Fill Box) ---
elif st.session_state.step == 'flavor_selection':
    box_size = boxes[st.session_state.selected_box]['size']
    remaining = box_size - len(st.session_state.box_contents)
    
    col_l, col_r = st.columns([2.5, 1], gap="large")
    
    with col_l:
        st.markdown(f"## 2. FILL YOUR {st.session_state.selected_box}")
        st.write(f"Spots remaining: **{remaining}**")
        
        f_cols = st.columns(2)
        for i, (name, d) in enumerate(flavors.items()):
            with f_cols[i % 2]:
                st.markdown(f"""
                    <div style="background:#f9f9f9; padding:15px; border-radius:15px; margin-bottom:10px; text-align:center;">
                        <img src="{d['img']}" style="width:100%; border-radius:10px;">
                        <h4 style="margin-top:10px;">{name}</h4>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"ADD {name.upper()}", key=f"add_{name}", disabled=remaining <= 0):
                    st.session_state.box_contents.append(name)
                    st.rerun()

    # --- Live Sidebar: The Pink Box ---
    with col_r:
        st.markdown("### 📦 YOUR PINK BOX")
        if not st.session_state.box_contents:
            st.info("Your box is empty. Add flavors to start!")
        else:
            for i, cookie in enumerate(st.session_state.box_contents):
                st.write(f"**{i+1}.** {cookie}")
            
            st.divider()
            st.write(f"**Total: ${boxes[st.session_state.selected_box]['price']:.2f}**")
            
            # Gifting Feature
            is_gift = st.checkbox("Is this a gift? 🎁")
            if is_gift:
                st.text_area("Add a digital gift note:", placeholder="Happy Birthday! Enjoy the cookies...")
            
            if remaining == 0:
                if st.button("PROCEED TO CHECKOUT"):
                    st.balloons()
                    st.success("Redirecting to payment portal...")
            
            if st.button("Change Box Size", type="secondary"):
                st.session_state.step = 'box_selection'
                st.session_state.box_contents = []
                st.rerun()

# --- Footer ---
st.markdown("<br><br><p style='text-align: center; color: #AAA; font-size: 0.8em;'>© 2025 ZIA SWEET TREATS LUBBOCK</p>", unsafe_allow_html=True)
