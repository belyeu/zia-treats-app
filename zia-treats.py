import streamlit as st

# --- Page Config & Styling ---
st.set_page_config(page_title="Zia Sweet Treats | Lubbock", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .box-option {
        border: 2px solid #EEE;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        background-color: #FFF;
        cursor: pointer;
    }
    .selected-box { border: 2px solid #FFD1DC; background-color: #FDF2F4; }
    .stButton>button {
        background-color: #FFD1DC;
        border-radius: 50px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'step' not in st.session_state: st.session_state.step = 'box_selection'
if 'selected_box' not in st.session_state: st.session_state.selected_box = None
if 'box_contents' not in st.session_state: st.session_state.box_contents = []

# Box Sizes (Crumbl Style)
boxes = {
    "Single": {"size": 1, "price": 4.50},
    "4-Pack": {"size": 4, "price": 15.50},
    "6-Pack": {"size": 6, "price": 22.25},
    "12-Pack (Party)": {"size": 12, "price": 38.50}
}

# Weekly Flavors
flavors = {
    "Milk Chocolate Chip": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=300",
    "Pink Velvet": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300",
    "Salted Caramel": "https://images.unsplash.com/photo-1590080876251-130a74c692dd?w=300"
}

# --- Step 1: Box Selection ---
if st.session_state.step == 'box_selection':
    st.markdown("<h2 style='text-align: center;'>PICK YOUR BOX SIZE</h2>", unsafe_allow_html=True)
    cols = st.columns(len(boxes))
    
    for i, (name, info) in enumerate(boxes.items()):
        with cols[i]:
            st.markdown(f"### {name}")
            st.write(f"${info['price']:.2f}")
            if st.button(f"CHOOSE {name}", key=name):
                st.session_state.selected_box = name
                st.session_state.step = 'flavor_selection'
                st.rerun()

# --- Step 2: Flavor Selection ---
elif st.session_state.step == 'flavor_selection':
    box_size = boxes[st.session_state.selected_box]['size']
    remaining = box_size - len(st.session_state.box_contents)
    
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.header(f"Fill your {st.session_state.selected_box}")
        st.write(f"Remaining: **{remaining} spots**")
        
        f_cols = st.columns(3)
        for i, (flavor, img) in enumerate(flavors.items()):
            with f_cols[i % 3]:
                st.image(img, use_container_width=True)
                if st.button(f"Add {flavor}", disabled=remaining <= 0):
                    st.session_state.box_contents.append(flavor)
                    st.rerun()

    with col_r:
        st.markdown("### Your Selection")
        for item in st.session_state.box_contents:
            st.write(f"✅ {item}")
        
        if remaining == 0:
            if st.button("PROCEED TO CHECKOUT"):
                st.success("Redirecting to payment...")
        
        if st.button("Change Box Size", type="secondary"):
            st.session_state.step = 'box_selection'
            st.session_state.box_contents = []
            st.rerun()
