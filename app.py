import streamlit as st
import pandas as pd

st.set_page_config(page_title="Order Nhà Hàng", layout="wide")

st.title("🍽️ Hệ thống Order Nhà Hàng Cao Cấp")

# Thực đơn với hình ảnh
menu = {
    "Khai vị": {
        "Súp nấm truffle": {"price": 85000, "image": "https://source.unsplash.com/featured/?mushroom-soup"},
        "Salad Caesar": {"price": 95000, "image": "https://source.unsplash.com/featured/?caesar-salad"},
        "Gỏi cuốn tôm thịt": {"price": 60000, "image": "https://source.unsplash.com/featured/?spring-rolls"},
        "Khoai tây chiên": {"price": 45000, "image": "https://source.unsplash.com/featured/?french-fries"}
    },
    "Món chính": {
        "Pizza Hải Sản": {"price": 150000, "image": "https://source.unsplash.com/featured/?seafood-pizza"},
        "Mì Ý Bò Bằm": {"price": 95000, "image": "https://source.unsplash.com/featured/?spaghetti-bolognese"},
        "Bít tết Bò Mỹ": {"price": 250000, "image": "https://source.unsplash.com/featured/?steak"},
        "Sườn nướng BBQ": {"price": 180000, "image": "https://source.unsplash.com/featured/?bbq-ribs"},
        "Lẩu Thái hải sản": {"price": 350000, "image": "https://source.unsplash.com/featured/?thai-soup"},
        "Cá hồi áp chảo": {"price": 280000, "image": "https://source.unsplash.com/featured/?salmon"},
        "Gà nướng thảo mộc": {"price": 160000, "image": "https://source.unsplash.com/featured/?roast-chicken"},
        "Cơm chiên dương châu": {"price": 85000, "image": "https://source.unsplash.com/featured/?fried-rice"}
    },
    "Tráng miệng": {
        "Bánh Tiramisu": {"price": 65000, "image": "https://source.unsplash.com/featured/?tiramisu"},
        "Panna Cotta": {"price": 55000, "image": "https://source.unsplash.com/featured/?panna-cotta"},
        "Trái cây dầm": {"price": 40000, "image": "https://source.unsplash.com/featured/?fruit-salad"},
        "Kem Gelato": {"price": 35000, "image": "https://source.unsplash.com/featured/?gelato"}
    },
    "Thức uống": {
        "Coca Cola": {"price": 20000, "image": "https://source.unsplash.com/featured/?coca-cola"},
        "Trà Đào Cam Sả": {"price": 35000, "image": "https://source.unsplash.com/featured/?iced-tea"},
        "Cà Phê Sữa": {"price": 25000, "image": "https://source.unsplash.com/featured/?vietnamese-coffee"},
        "Nước Suối": {"price": 10000, "image": "https://source.unsplash.com/featured/?mineral-water"},
        "Sinh tố Bơ": {"price": 45000, "image": "https://source.unsplash.com/featured/?avocado-smoothie"},
        "Nước ép cam": {"price": 40000, "image": "https://source.unsplash.com/featured/?orange-juice"},
        "Mojito chanh dây": {"price": 55000, "image": "https://source.unsplash.com/featured/?mojito"},
        "Bia Heineken": {"price": 30000, "image": "https://source.unsplash.com/featured/?beer"},
"Rượu vang đỏ": {"price": 120000, "image": "https://source.unsplash.com/featured/?red-wine"}
    }
}

# Quản lý giỏ hàng
if 'order_dict' not in st.session_state:
    st.session_state.order_dict = {}

col1, col2 = st.columns([1.2, 1.8])

with col1:
    st.subheader("📝 Chọn Món")
    category = st.selectbox("Chọn danh mục:", list(menu.keys()))
    
    st.subheader(f"🍽️ {category}")
    items = menu[category]
    
    cols = st.columns(2)
    for idx, (item_name, item_data) in enumerate(items.items()):
        with cols[idx % 2]:
            st.image(item_data["image"], width=250, use_column_width=True)
            st.write(f"**{item_name}**")
            st.write(f"💰 {item_data['price']:,.0f} VNĐ")
            
            qty = st.number_input(f"Số lượng", min_value=0, step=1, value=0, key=f"qty_{category}_{item_name}")
            
            if st.button(f"➕ Thêm {item_name}", key=f"add_{category}_{item_name}"):
                if qty > 0:
                    price = item_data["price"]
                    if item_name in st.session_state.order_dict:
                        st.session_state.order_dict[item_name]["Số lượng"] += qty
                        st.session_state.order_dict[item_name]["Thành tiền"] = (
                            st.session_state.order_dict[item_name]["Số lượng"] * price
                        )
                    else:
                        st.session_state.order_dict[item_name] = {
                            "Tên món": item_name,
                            "Đơn giá": price,
                            "Số lượng": qty,
                            "Thành tiền": price * qty
                        }
                    st.success(f"Đã thêm {qty} {item_name} vào giỏ!")
                    st.rerun()
                else:
                    st.warning("Vui lòng chọn số lượng > 0")

with col2:
    st.subheader("🛒 Giỏ hàng của bạn")
    if st.session_state.order_dict:
        df = pd.DataFrame.from_dict(st.session_state.order_dict, orient='index')
        st.dataframe(df[["Tên món", "Đơn giá", "Số lượng", "Thành tiền"]], use_container_width=True)
        
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

if st.button("💳 Thanh toán"):
if st.session_state.order_dict:
        st.success("Cảm ơn bạn đã đặt hàng! Hóa đơn đã được ghi nhận.")
        st.balloons()
    else:
        st.warning("Giỏ hàng trống!")
