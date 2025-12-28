import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# --- Configuration & State ---
st.set_page_config(page_title="Cookie Delight Manager", layout="wide")

if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        "Chocolate Chip": {"price": 2.50, "stock": 50},
        "Oatmeal Raisin": {"price": 2.00, "stock": 30},
        "Sugar Cookie":   {"price": 1.75, "stock": 40},
        "Peanut Butter":  {"price": 2.25, "stock": 25},
        "Snickerdoodle":  {"price": 2.00, "stock": 35}
    }

DATA_FILE = 'store_data_v5.csv'

# --- Helper Functions ---
def load_data():
    customers = {}
    history = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Type'] == 'Customer':
                    customers[row['Name']] = row['Details']
                else:
                    history.append(row)
    return customers, history

def save_order(name, contact, items, total):
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Type", "Name", "Date", "Details", "Total"])
        # Ensure customer is saved
        writer.writerow(["Customer", name, "", contact, ""])
        # Save order
        writer.writerow(["Order", name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), items, total])

def generate_pdf(name, items, total):
    filename = f"receipt_{name}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "COOKIE DELIGHT STORE RECEIPT")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Customer: {name}")
    c.drawString(100, 715, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(100, 700, 500, 700)
    
    y = 680
    for item, qty in items.items():
        c.drawString(100, y, f"{qty}x {item}")
        y -= 20
    
    c.line(100, y, 500, y)
    c.drawString(100, y-20, f"TOTAL: ${total:.2f}")
    c.save()
    return filename

# --- UI Layout ---
st.title("🍪 Cookie Delight Manager Pro")

customers, history = load_data()

# Sidebar: Customer Info
st.sidebar.header("Customer Login")
customer_name = st.sidebar.text_input("Customer Name")
contact_info = st.sidebar.text_input("Contact Info")

if customer_name in customers:
    st.sidebar.success(f"Welcome back, {customer_name}!")
    contact_info = customers[customer_name]

# Main Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Menu")
    menu_cols = st.columns(2)
    for i, (cookie, info) in enumerate(st.session_state.inventory.items()):
        with menu_cols[i % 2]:
            st.info(f"**{cookie}**\n\nPrice: ${info['price']:.2f} | Stock: {info['stock']}")
            if st.button(f"Add {cookie}", key=cookie, disabled=info['stock'] <= 0):
                st.session_state.cart[cookie] = st.session_state.cart.get(cookie, 0) + 1
                st.session_state.inventory[cookie]['stock'] -= 1
                st.rerun()

with col2:
    st.subheader("Shopping Cart")
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        total = 0
        for item, qty in list(st.session_state.cart.items()):
            price = st.session_state.inventory[item]['price'] * qty
            total += price
            st.write(f"{qty}x {item} - ${price:.2f}")
        
        st.divider()
        st.write(f"### Total: ${total:.2f}")
        
        if st.button("Clear Cart"):
            for item, qty in st.session_state.cart.items():
                st.session_state.inventory[item]['stock'] += qty
            st.session_state.cart = {}
            st.rerun()

        if st.button("Complete Order"):
            if not customer_name:
                st.error("Please enter a customer name!")
            else:
                items_str = ", ".join([f"{q}x {i}" for i, q in st.session_state.cart.items()])
                save_order(customer_name, contact_info, items_str, total)
                pdf_path = generate_pdf(customer_name, st.session_state.cart, total)
                
                with open(pdf_path, "rb") as f:
                    st.download_button("Download Receipt PDF", f, file_name=pdf_path)
                
                st.session_state.cart = {}
                st.success("Order Processed!")

# Dashboard Section
st.divider()
if st.checkbox("Show Manager Dashboard (Password Required)"):
    pw = st.text_input("Password", type="password")
    if pw == "admin":
        st.subheader("Sales Analytics")
        df = pd.DataFrame(history)
        if not df.empty:
            df['Total'] = pd.to_numeric(df['Total'])
            st.metric("Total Revenue", f"${df['Total'].sum():.2f}")
            st.dataframe(df)
        else:
            st.write("No sales data yet.")