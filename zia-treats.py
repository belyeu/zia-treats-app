import streamlit as st
import time

# --- High-Fidelity Styling ---
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        /* Sticky Header */
        .main-header {
            position: fixed;
            top: 0;
            width: 100%;
            background: white;
            z-index: 1000;
            border-bottom: 1px solid #f0f0f0;
            padding: 10px 0;
            text-align: center;
        }
        
        /* Crumbl-Style Cookie Card */
        .cookie-card {
            background: #fff;
            border-radius: 24px;
            padding: 20px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            text-align: center;
            border: 1px solid #f1f1f1;
        }
        
        /* The Pink Button */
        .stButton>button {
            background-color: #FFD1DC !important;
            color: #333 !important;
            border: none !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 0.6rem 2rem;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #F8B1C3 !important;
            transform: translateY(-2px);
        }

        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background-color: #fdf2f4;
        }
        </style>
    """, unsafe_allow_html=True)

# --- App Logic & State ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'box_size' not in st.session_state: st.session_state.box_size = 0
if 'selection' not in st.session_state: st.session_state.selection = []

DATA = {
    "boxes": {
        "Single": {"qty": 1, "price": 4.50},
        "4-Pack": {"qty": 4, "price": 15.50},
        "6-Pack": {"qty": 6, "price": 22.25},
        "12-Pack": {"qty": 12, "price": 38.50}
    },
    "flavors": [
        {"name": "Milk Chocolate Chip", "tags": "WARM", "cals": "140-720 cal", "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400"},
        {"name": "Pink Velvet", "tags": "CHILLED", "cals": "160-800 cal", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400"},
        {"name": "Brownie Sundae", "tags": "WARM", "cals": "180-920 cal", "img": "https://images.unsplash.com/photo-1590080876251-130a74c692dd?w=400"},
        {"name": "Lemon Glaze", "tags": "WARM", "cals": "130-650 cal", "img": "https://images.unsplash.com/photo-1506459225024-1428097a7e18?w=400"}
    ]
}

local_css()

# --- Navigation ---
with st.sidebar:
    st.title("ZIA")
    if st.button("🏠 Home"): st.session_state.view = 'home'
    if st.button("🛍️ Order Now"): st.session_state.view = 'box_select'
    if st.button("👤 Loyalty Rewards"): st.session_state.view = 'auth'

# --- Views ---
if st.session_state.view == 'home':
    st.markdown("<h1 style='text-align:center;'>This Week's Lineup</h1>", unsafe_allow_html=True)
    cols = st.columns(len(DATA["flavors"]))
    for i, flavor in enumerate(DATA["flavors"]):
        with cols[i]:
            st.image(flavor["img"])
            st.markdown(f"**{flavor['name']}**")
    if st.button("START ORDER"):
        st.session_state.view = 'box_select'
        st.rerun()

elif st.session_state.view == 'box_select':
    st.markdown("<h1 style='text-align:center;'>Choose Your Box</h1>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (name, details) in enumerate(DATA["boxes"].items()):
        with cols[i]:
            st.markdown(f"""<div class="cookie-card"><h3>{name}</h3><p>${details['price']:.2f}</p></div>""", unsafe_allow_html=True)
            if st.button(f"SELECT {name.split('-')[0]}", key=name):
                st.session_state.box_size = details['qty']
                st.session_state.current_box_name = name
                st.session_state.view = 'flavor_select'
                st.rerun()

elif st.session_state.view == 'flavor_select':
    remaining = st.session_state.box_size - len(st.session_state.selection)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"## Fill Your {st.session_state.current_box_name}")
        st.caption(f"Select {remaining} more cookies")
        f_cols = st.columns(2)
        for i, f in enumerate(DATA["flavors"]):
            with f_cols[i % 2]:
                st.markdown(f"""<div class="cookie-card"><img src="{f['img']}" width="100%"><br><b>{f['name']}</b><br><small>{f['tags']} • {f['cals']}</small></div>""", unsafe_allow_html=True)
                if st.button(f"Add {f['name']}", disabled=remaining <= 0, key=f"btn_{i}"):
                    st.session_state.selection.append(f['name'])
                    st.rerun()

    with col2:
        st.markdown("### Your Box")
        for item in st.session_state.selection:
            st.markdown(f"✅ {item}")
        if remaining == 0:
            if st.button("CHECKOUT"):
                st.balloons()
                st.success("Redirecting to payment...")
