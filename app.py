import streamlit as st
import pandas as pd
from PIL import Image
import base64

# Page config
st.set_page_config(
    page_title="Weekly Forecast Demo", 
    layout="wide",
    page_icon="📊"
)

# Custom CSS để styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Tạo file style.css nếu chưa có, hoặc dùng CSS trực tiếp
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .company-info {
        flex-grow: 1;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)



# Hàm để load và hiển thị logo
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Header section với logo
col1, col2 = st.columns([1, 3])

with col1:
    try:
        logo = Image.open("logotmu.png")
        # Căn giữa bằng HTML
        st.markdown(
            f'<div style="display: flex; justify-content: center;">'
            f'<img src="data:image/png;base64,{get_base64_of_bin_file("logotmu.png")}" width="120">'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown("<p style='text-align: center; font-weight: bold;'>Khoa Toán Kinh tế</p>", 
                   unsafe_allow_html=True)
    except:
        st.markdown("""
        <div style='text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;'>
            <h2 style='font-size: 2.5em; margin: 0;'>📊</h2>
            <p style='font-weight: bold; margin: 5px 0 0 0;'>Khoa Toán Kinh tế</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="main-header">
        <h1 style='margin: 0; font-size: 2.5em;'>DỰ BÁO NHU CẦU</h1>
        <p style='margin: 5px 0 0 0; font-size: 1.2em;'>Hệ thống dự báo nhu cầu sản phẩm TST</p>
    </div>
    """, unsafe_allow_html=True)

# Thông tin công ty và metrics
st.markdown("---")

# Tạo 3 cột cho các metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📦 1,234</h3>
        <p>Sản phẩm tồn kho</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>📦 200,000</h3>
        <p>Số lượng xuất kho</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>📈 >90%</h3>
        <p>Độ chính xác</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3>⏰ 24/7</h3>
        <p>Hệ thống hoạt động</p>
    </div>
    """, unsafe_allow_html=True)

# Navigation section
st.markdown("---")
st.markdown("### Chức năng chính")

tab1, tab2, tab3 = st.tabs(["📦 Quản lý mã sản phẩm","📊 Dự báo nhu cầu", "📈 Xuất báo cáo"])

with tab1:
    st.info("Chức năng dự báo nhu cầu sản phẩm theo tuần")
    if st.button("Mở trang quản lý mã sản phẩm", key="forecast_btn"):
        st.switch_page("pages/1 Quản lý mã sản phẩm.py")

with tab2:
    st.info("Quản lý danh mục sản phẩm và mã hàng")
    if st.button("Mở trang dự báo nhu cầu", key="manage_btn"):
        st.switch_page("pages/2 Dự báo nhu cầu.py")

with tab3:
    st.info("Xem báo cáo và thông kê")
    if st.button("Mở trang báo cáo và thống kê", key="report_btn"):
        st.switch_page("pages/3 Xuất file báo cáo.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>© 2025 Khoa Toán Kinh tế - Hệ thống Dự báo nhu cầu phụ tùng</p>
    <p>📧 Email: contact@tkt.com | 📞 Hotline: 1900 1234</p>
</div>
""", unsafe_allow_html=True)

# Sidebar information
with st.sidebar:
    st.markdown("### ℹ️ Thông tin hệ thống")
    st.markdown("""
    - **Phiên bản:** 1.0.0
    - **Cập nhật:** 12/09/2025
    """)
    

    
    st.markdown("### 🔔 Thông báo gần đây")
    st.success("✅ Cập nhật dữ liệu thành công")
    st.warning("⚠️ Bảo trì hệ thống: 02:00-04:00")