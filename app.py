import streamlit as st
import pandas as pd

st.set_page_config(page_title="Order Nhà Hàng", layout="wide")

st.title("🍽️ Ứng dụng Order Đồ ăn & Thức uống")

# Danh sách thực đơn mẫu
menu = {
    "Đồ ăn": {
        "Pizza Hải Sản": 150000,
        "Mì Ý Bò Bằm": 95000,
        "Burger Gà": 65000,
        "Salad Trộn": 50000
    },
    "Thức uống": {
        "Coca Cola": 20000,
        "Trà Đào": 35000,
        "Cà Phê Sữa": 25000,
        "Nước Suối": 10000
    }
}

# Khởi tạo giỏ hàng (session state)
if 'order_list' not in st.session_state:
    st.session_state.order_list = []

# Giao diện chọn món
col1, col2 = st.columns(2)

with col1:
    st.subheader("Menu")
    category = st.selectbox("Chọn loại:", list(menu.keys()))
    item = st.selectbox("Chọn món:", list(menu[category].keys()))
    quantity = st.number_input("Số lượng:", min_value=1, value=1)
    
    if st.button("Thêm vào giỏ"):
        price = menu[category][item]
        st.session_state.order_list.append({
            "Tên món": item,
            "Đơn giá": price,
            "Số lượng": quantity,
            "Thành tiền": price * quantity
        })
        st.success(f"Đã thêm {item} vào giỏ!")

# Hiển thị giỏ hàng
with col2:
    st.subheader("Giỏ hàng của bạn")
    if st.session_state.order_list:
        df = pd.DataFrame(st.session_state.order_list)
        st.table(df)
        
        tong_bill = df["Thành tiền"].sum()
        st.metric(label="Tổng hóa đơn (VNĐ)", value=f"{tong_bill:,.0f}")
        
        if st.button("Xóa giỏ hàng"):
            st.session_state.order_list = []
            st.rerun()
    else:
        st.info("Giỏ hàng đang trống.")

# Xuất hóa đơn
if st.session_state.order_list:
    csv = pd.DataFrame(st.session_state.order_list).to_csv(index=False).encode('utf-8')
    st.download_button("Tải hóa đơn (CSV)", csv, "hoa_don.csv", "text/csv")
