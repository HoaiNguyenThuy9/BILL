import streamlit as st
import pandas as pd

# Cấu hình trang sang trọng
st.set_page_config(page_title="Nhà hàng Cao cấp", layout="wide", page_icon="🍽️")

# CSS để giao diện đẹp hơn
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {width: 100%; border-radius: 5px; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

st.title("🍽️ Signature Restaurant Menu")
st.markdown("---")

# Thực đơn
menu = {
    "Đồ ăn": {"Pizza Hải Sản": 150000, "Bít tết Bò Mỹ": 250000, "Lẩu Thái hải sản": 350000, "Burger Gà": 65000},
    "Thức uống": {"Mojito chanh dây": 55000, "Nước ép cam": 40000, "Trà Đào Cam Sả": 35000, "Bia Heineken": 30000}
}

if 'cart' not in st.session_state: st.session_state.cart = {}

# Layout 3 cột chọn món
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    category = st.selectbox("Loại món:", list(menu.keys()))
with col2:
    item = st.selectbox("Tên món:", list(menu[category].keys()))
with col3:
    quantity = st.number_input("Số lượng:", min_value=1, value=1)
    if st.button("➕ Thêm vào đơn"):
        price = menu[category][item]
        if item in st.session_state.cart:
            st.session_state.cart[item]["Số lượng"] += quantity
            st.session_state.cart[item]["Thành tiền"] = st.session_state.cart[item]["Số lượng"] * price
        else:
            st.session_state.cart[item] = {"Giá": price, "Số lượng": quantity, "Thành tiền": price * quantity}
        st.rerun()

st.markdown("---")

# Giỏ hàng trong Sidebar để trông tinh tế hơn
with st.sidebar:
    st.header("🛒 Đơn hàng của bạn")
    if st.session_state.cart:
        for name, info in st.session_state.cart.items():
            st.write(f"**{name}**")
            col_a, col_b = st.columns([2, 1])
            col_a.write(f"{info['Số lượng']} x {info['Giá']:,}đ")
            if col_b.button("❌", key=name):
                del st.session_state.cart[name]
                st.rerun()
    else:
        st.info("Giỏ hàng trống.")

# Tính toán tổng tiền
if st.session_state.cart:
    df = pd.DataFrame.from_dict(st.session_state.cart, orient='index')
    tam_tinh = df["Thành tiền"].sum()
    giam_gia = (tam_tinh * 0.05) if tam_tinh > 1000000 else 0
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Tạm tính", f"{tam_tinh:,.0f} VNĐ")
    with col_res2:
        if giam_gia > 0:
            st.metric("Giảm giá (5%)", f"-{giam_gia:,.0f} VNĐ")
            st.success("Voucher VIP đã được áp dụng!")
            
    st.markdown("---")
    st.metric("TỔNG THANH TOÁN", f"{tam_tinh - giam_gia:,.0f} VNĐ")
    
    if st.button("💳 Thanh toán ngay"):
        st.balloons()
        st.success("Cảm ơn quý khách đã đặt món!")
        st.session_state.cart = {}
