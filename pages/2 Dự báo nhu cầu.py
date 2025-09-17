import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import re
from io import StringIO
import fnmatch  # Thêm để match pattern dễ hơn

st.set_page_config(page_title="Weekly Forecast Demo", layout="wide")

st.title("DỰ BÁO NHU CẦU PHỤ TÙNG")

# Path đến folder chứa các file SARIMA - sử dụng đường dẫn tương đối từ app
SARIMA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SARIMA ')  # Adjust nếu cần

# Data mẫu hardcode (chỉ dùng SARIMA cho hiện tại)
data_sample_text = """
Ma sp	Method	Week	Actual	Predicted	Error	RMSE	MAE	MAPE
28113I7100	SARIMA	317	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	318	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	319	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	320	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	321	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	322	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	323	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	324	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	325	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	326	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	327	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	328	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	329	39,15748031	39,15748031	0	0	0	0
28113I7100	SARIMA	330	39,15748031	39,15748031	0	0	0	0
"""

# Convert text to df sample
df_sample = pd.read_csv(StringIO(data_sample_text), sep='\t')
df_sample['Actual'] = df_sample['Actual'].str.replace(',', '.').astype(float)
df_sample['Predicted'] = df_sample['Predicted'].str.replace(',', '.').astype(float)
df_sample['Error'] = df_sample['Error'].astype(float)
df_sample['RMSE'] = df_sample['RMSE'].astype(float)
df_sample['MAE'] = df_sample['MAE'].astype(float)
df_sample['MAPE'] = df_sample['MAPE'].astype(float)

# Danh sách mô hình (dự đoán mở rộng cho tương lai)
models = ['SARIMA', 'Neural Network', 'XGBoost', 'LSTM']

# Chọn mô hình
selected_model = st.selectbox("Chọn mô hình:", models, index=0)

# Load và xử lý dữ liệu chỉ khi chọn SARIMA
if selected_model == 'SARIMA':
    # Load danh sách mã từ các file trong folder SARIMA
    codes = []
    if os.path.exists(SARIMA_FOLDER):
        all_files = [f for f in os.listdir(SARIMA_FOLDER) if f.endswith('.xlsx') and f.startswith('Forecast_')]
        
        for f in all_files:
            match = re.search(r"Forecast_(\w+)_Tuan_", f)
            if match:
                codes.append(match.group(1))
        codes = list(set(codes))  # Remove duplicates if any
        if not codes:
            codes = ["28113I7100"]  # Fallback
    else:
        st.warning(f"Không tìm thấy folder {SARIMA_FOLDER} tại đường dẫn {SARIMA_FOLDER}. Kiểm tra vị trí folder SARIMA so với app.py.")
        codes = ["28113I7100"]  # Fallback nếu folder không tồn tại

    # Lấy danh sách mã từ session nếu có (từ page trước)
    session_codes = [p['code'] for p in st.session_state.user_products] if 'user_products' in st.session_state else []
    if session_codes:
        # Lọc codes chỉ lấy những mã thuộc user
        available_codes = [c for c in codes if c in session_codes]
        if not available_codes:
            st.warning("Không có mã nào trong folder thuộc quản trị của bạn.")
            available_codes = codes[:1]  # Show first as example
    else:
        available_codes = codes

    # Chọn mã sản phẩm
    selected_code = st.selectbox("Chọn mã sản phẩm:", available_codes, index=0)

    # Load file tương ứng với mã đã chọn
    df = None
    parsed_code = selected_code
    file_pattern = f"Forecast_{selected_code}_Tuan_*.xlsx"
    found_file = None
    matching_files = []
    if os.path.exists(SARIMA_FOLDER):
        all_files = [f for f in os.listdir(SARIMA_FOLDER) if f.endswith('.xlsx')]
        # Sử dụng fnmatch để match pattern tốt hơn
        matching_files = fnmatch.filter(all_files, file_pattern)
        
        if matching_files:
            # Lấy file mới nhất dựa trên tên (giả định date ở cuối, ví dụ 20250914_0054.xlsx)
            def extract_date(filename):
                match_date = re.search(r"_(\d{8})_", filename)
                if match_date:
                    return int(match_date.group(1))
                return 0
            
            found_file = max(matching_files, key=extract_date)
            file_path = os.path.join(SARIMA_FOLDER, found_file)
            try:
                df = pd.read_excel(file_path)
                # Lọc chỉ giữ các hàng có Method là SARIMA
                if 'Method' in df.columns:
                    df = df[df['Method'] == 'SARIMA'].reset_index(drop=True)
                # Xử lý dấu phẩy nếu cần
                if 'Actual' in df.columns and df['Actual'].dtype == 'object':
                    df['Actual'] = df['Actual'].str.replace(',', '.').astype(float)
                if 'Predicted' in df.columns and df['Predicted'].dtype == 'object':
                    df['Predicted'] = df['Predicted'].str.replace(',', '.').astype(float)
                if 'Error' in df.columns:
                    df['Error'] = pd.to_numeric(df['Error'], errors='coerce')
                if 'RMSE' in df.columns:
                    df['RMSE'] = pd.to_numeric(df['RMSE'], errors='coerce')
                if 'MAE' in df.columns:
                    df['MAE'] = pd.to_numeric(df['MAE'], errors='coerce')
                if 'MAPE' in df.columns:
                    df['MAPE'] = pd.to_numeric(df['MAPE'], errors='coerce')
            except Exception as e:
                st.error(f"Lỗi khi load file {file_path}: {e}")
                st.info("Chi tiết lỗi để debug: " + str(e))
                df = df_sample
        else:
            # Fallback: tìm file chứa mã mà không cần pattern chính xác
            fallback_files = [f for f in all_files if f"Forecast_{selected_code}_" in f]
            st.info(f"Không tìm thấy file khớp pattern, thử fallback: {fallback_files}")
            if fallback_files:
                found_file = fallback_files[0]  # Lấy file đầu tiên
                file_path = os.path.join(SARIMA_FOLDER, found_file)
                try:
                    df = pd.read_excel(file_path)
                    # Lọc chỉ giữ các hàng có Method là SARIMA
                    if 'Method' in df.columns:
                        df = df[df['Method'] == 'SARIMA'].reset_index(drop=True)
                    # Xử lý tương tự
                    if 'Actual' in df.columns and df['Actual'].dtype == 'object':
                        df['Actual'] = df['Actual'].str.replace(',', '.').astype(float)
                    if 'Predicted' in df.columns and df['Predicted'].dtype == 'object':
                        df['Predicted'] = df['Predicted'].str.replace(',', '.').astype(float)
                    st.success(f"Đã load fallback file: {found_file} và lọc Method SARIMA")
                except Exception as e:
                    st.error(f"Lỗi load fallback: {e}")
                    df = df_sample
            else:
                st.warning(f"Không tìm thấy file cho mã {selected_code}, sử dụng data mẫu.")
                df = df_sample
    else:
        st.warning(f"Folder {SARIMA_FOLDER} không tồn tại.")
        df = df_sample

    if df is None or df.empty:
        df = df_sample
        st.info("Sử dụng data mẫu.")

    if not df.empty:
        # Thống kê mô tả từ sai số có sẵn
        if 'Error' in df.columns and 'RMSE' in df.columns and 'MAE' in df.columns and 'MAPE' in df.columns:
            stats = df[['Error', 'RMSE', 'MAE', 'MAPE']].describe()
            st.subheader("Thống Kê Mô Tả Sai Số")
            st.dataframe(stats.style.format('{:.4f}'))
        
        # Hiển thị table
        st.subheader("Data Chi Tiết")
        numeric_cols = ['Actual', 'Predicted', 'Error', 'RMSE', 'MAE', 'MAPE']
        format_dict = {col: '{:.2f}' for col in numeric_cols if col in df.columns}
        st.dataframe(df.style.format(format_dict))

        # Trực quan biểu đồ
        st.subheader("Biểu Đồ Trực Quan")
        
        # Biểu đồ 1: Actual vs Predicted
        if 'Week' in df.columns and 'Actual' in df.columns and 'Predicted' in df.columns:
            fig1 = px.line(df, x='Week', y=['Actual', 'Predicted'], 
                           title=f"Actual vs Predicted cho Mã {parsed_code}",
                           labels={'value': 'Giá Trị', 'variable': 'Loại'})
            fig1.update_layout(hovermode='x unified')
            st.plotly_chart(fig1, use_container_width=True)
            
            # Biểu đồ 2: Error
            if 'Error' in df.columns:
                fig2 = px.line(df, x='Week', y='Error', 
                               title=f"Sai Số (Error) theo Tuần cho Mã {parsed_code}",
                               markers=True)
                fig2.update_traces(line_color='red')
                fig2.update_layout(hovermode='x unified')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Cột Error không có trong data, không thể vẽ biểu đồ sai số.")
        else:
            st.warning("Không đủ cột để vẽ biểu đồ (cần Week, Actual, Predicted).")
        
        # Lưu vào session
        st.session_state.forecast_result = df
        st.session_state.selected_code = parsed_code
        st.success("Trực quan hoàn tất! Kết quả lưu để xuất ở Page 3.")
    else:
        st.error("Data rỗng.")
else:
    st.info(f"Chọn mô hình {selected_model}, nhưng hiện chỉ hỗ trợ SARIMA. Các mô hình khác (Neural Network, XGBoost, LSTM) sẽ được phát triển sau.")

# Footer
st.markdown("---")
st.info("Code này cho phép chọn mô hình và sử dụng các file trong folder SARIMA cho SARIMA, thống kê mô tả sai số từ data có sẵn.")