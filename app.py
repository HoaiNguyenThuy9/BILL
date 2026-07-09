import streamlit as st
import pandas as pd

st.set_page_config(page_title="Order Nhà Hàng", layout="wide")

st.title("🍽️ Hệ thống Order Nhà Hàng")

# Thực đơn phong phú hơn
menu = {
    "Đồ ăn": {
        "Pizza Hải Sản": 150000, "Mì Ý Bò Bằm": 95000, "Burger Gà": 65000,
        "Salad Trộn": 50000, "Bít tết Bò Mỹ": 250000, "Sườn nướng BBQ": 180000,
        "Cánh gà chiên mắm": 75000, "Lẩu Thái hải sản": 350000
    },
    "Thức uống": {
        "Coca Cola": 20000, "Trà Đào Cam Sả": 35000, "Cà Phê Sữa": 25000,
        "Nước Suối": 10000, "Sinh tố Bơ": 45000, "Nước ép cam": 40000,
        "Mojito chanh dây": 55000, "Bia Heineken": 30000
    }
}

if 'order_list' not in st.session_state:
    st.session_state.order_list = []

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Chọn Món")
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

with col2:
    st.subheader("Giỏ hàng")
    if st.session_state.order_list:
        df = pd.DataFrame(st.session_state.order_list)
        st.table(df)
        
        tam_tinh = df["Thành tiền"].sum()
        giam_gia = 0
        
        # Tính voucher 5% cho hóa đơn > 1.000.000
        if tam_tinh > 1000000:
            giam_gia = tam_tinh * 0.05
            st.info(f"🎉 Chúc mừng! Bạn được giảm 5% vì hóa đơn trên 1.000.000 VNĐ.")
        
        tong_thanh_toan = tam_tinh - giam_gia
        
        st.write(f"**Tạm tính:** {tam_tinh:,.0f} VNĐ")
        if giam_gia > 0:
            st.write(f"**Giảm giá (5%):** -{giam_gia:,.0f} VNĐ")
        st.metric(label="Tổng thanh toán", value=f"{tong_thanh_toan:,.0f} VNĐ")
        
        if st.button("Xóa giỏ hàng"):
            st.session_state.order_list = []
            st.rerun()
    else:
        st.info("Giỏ hàng đang trống.")
