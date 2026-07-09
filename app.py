import streamlit as st
import pandas as pd

st.set_page_config(page_title="Order Nhà Hàng", layout="wide")

st.title("🍽️ Hệ thống Order Nhà Hàng Cao Cấp")

# Thực đơn mở rộng
menu = {
    "Khai vị": {
        "Súp nấm truffle": 85000, "Salad Caesar": 95000, "Gỏi cuốn tôm thịt": 60000, "Khoai tây chiên": 45000
    },
    "Món chính": {
        "Pizza Hải Sản": 150000, "Mì Ý Bò Bằm": 95000, "Bít tết Bò Mỹ": 250000, 
        "Sườn nướng BBQ": 180000, "Lẩu Thái hải sản": 350000, "Cá hồi áp chảo": 280000,
        "Gà nướng thảo mộc": 160000, "Cơm chiên dương châu": 85000
    },
    "Tráng miệng": {
        "Bánh Tiramisu": 65000, "Panna Cotta": 55000, "Trái cây dầm": 40000, "Kem Gelato": 35000
    },
    "Thức uống": {
        "Coca Cola": 20000, "Trà Đào Cam Sả": 35000, "Cà Phê Sữa": 25000,
        "Nước Suối": 10000, "Sinh tố Bơ": 45000, "Nước ép cam": 40000,
        "Mojito chanh dây": 55000, "Bia Heineken": 30000, "Rượu vang đỏ": 120000
    }
}

# Quản lý giỏ hàng
if 'order_dict' not in st.session_state:
    st.session_state.order_dict = {}

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📝 Chọn Món")
    category = st.selectbox("Chọn danh mục:", list(menu.keys()))
    item = st.selectbox("Chọn món:", list(menu[category].keys()))
    quantity = st.number_input("Số lượng:", min_value=1, step=1, value=1)
    
    if st.button("➕ Thêm vào giỏ"):
        price = menu[category][item]
        if item in st.session_state.order_dict:
            st.session_state.order_dict[item]["Số lượng"] += quantity
            st.session_state.order_dict[item]["Thành tiền"] = (
                st.session_state.order_dict[item]["Số lượng"] * price
            )
        else:
            st.session_state.order_dict[item] = {
                "Tên món": item,
                "Đơn giá": price,
                "Số lượng": quantity,
                "Thành tiền": price * quantity
            }
        st.success(f"Đã thêm {item} vào giỏ!")

with col2:
    st.subheader("🛒 Giỏ hàng của bạn")
    if st.session_state.order_dict:
        df = pd.DataFrame.from_dict(st.session_state.order_dict, orient='index')
        st.table(df[["Tên món", "Đơn giá", "Số lượng", "Thành tiền"]])
        
        tam_tinh = df["Thành tiền"].sum()
        giam_gia = (tam_tinh * 0.05) if tam_tinh > 1000000 else 0
        
        if giam_gia > 0:
            st.info(f"🎉 Chúc mừng! Bạn được giảm 5% vì hóa đơn trên 1.000.000 VNĐ.")
        
        tong_thanh_toan = tam_tinh - giam_gia
        
        st.write(f"**Tạm tính:** {tam_tinh:,.0f} VNĐ")
        if giam_gia > 0:
            st.write(f"**Giảm giá (5%):** -{giam_gia:,.0f} VNĐ")
        st.metric(label="Tổng thanh toán", value=f"{tong_thanh_toan:,.0f} VNĐ")
        
        if st.button("❌ Xóa giỏ hàng"):
            st.session_state.order_dict = {}
            st.rerun()
    else:
        st.info("Giỏ hàng đang trống.")
