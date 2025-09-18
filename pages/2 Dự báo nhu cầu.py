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

# Danh sách 40 mã sản phẩm cố định
product_codes = [
    "971334F200", "82220B4000", "31110I7050", "31114I6000", "56351H6001FFF",
    "4141249670", "96611S1600", "95430B45004X", "98351B1000", "253301P000",
    "25231I7420", "81640S1000", "263304A001", "581641H000", "86514I7000",
    "28113I7100", "263502M000", "92401I6100", "93571BW2004X", "2630035505",
    "93410B4050", "28113N9000", "97133N9100", "56351C7001FFF", "55367S1CA1",
    "98361B1000", "96611N9000", "281134F000", "58302P2A30", "83220B4000",
    "86513I7000", "97133I7000", "58302S1A30", "58101D3A11", "72800N9250",
    "462202N500", "93571I62504X", "55530C5001", "581122P000", "527512B100QQH"
]

# Định nghĩa folder cho từng mô hình (XGBoost không dùng folder riêng)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
folders = {
    'SARIMA': os.path.join(BASE_DIR, 'SARIMA '),
    'LSTM': os.path.join(BASE_DIR, 'LSTM'),
    'XGBoost': BASE_DIR  # Sử dụng thư mục gốc cho file XGBoost
}

# Data mẫu cho SARIMA
data_sample_sarima = """
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
df_sample_sarima = pd.read_csv(StringIO(data_sample_sarima), sep='\t')
df_sample_sarima['Actual'] = df_sample_sarima['Actual'].str.replace(',', '.').astype(float)
df_sample_sarima['Predicted'] = df_sample_sarima['Predicted'].str.replace(',', '.').astype(float)
df_sample_sarima['Error'] = df_sample_sarima['Error'].astype(float)
df_sample_sarima['RMSE'] = df_sample_sarima['RMSE'].astype(float)
df_sample_sarima['MAE'] = df_sample_sarima['MAE'].astype(float)
df_sample_sarima['MAPE'] = df_sample_sarima['MAPE'].astype(float)

# Data mẫu cho XGBoost (dựa trên file bạn cung cấp)
data_sample_xgboost = """
Week	Actual	Predicted	Ma sp	Method	Error	RMSE	MAE	MAPE
1	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
2	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
3	1	1,17885077	82220B4000	XGBOOST	-0,17885077	0,17885077	0,17885077	17,885077
4	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
5	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
6	5	4,982263088	82220B4000	XGBOOST	0,017736912	0,017736912	0,017736912	0,354738235
7	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
8	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
9	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
10	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
11	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
12	1	1,126290441	82220B4000	XGBOOST	-0,126290441	0,126290441	0,126290441	12,62904406
13	3	3,604568481	82220B4000	XGBOOST	-0,604568481	0,604568481	0,604568481	20,15228271
14	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
15	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
16	3	2,839565992	82220B4000	XGBOOST	0,160434008	0,160434008	0,160434008	5,347800255
17	2	1,303004742	82220B4000	XGBOOST	0,696995258	0,696995258	0,696995258	34,84976292
18	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
19	3	2,839565992	82220B4000	XGBOOST	0,160434008	0,160434008	0,160434008	5,347800255
20	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
21	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
22	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
23	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
24	7	6,028737068	82220B4000	XGBOOST	0,971262932	0,971262932	0,971262932	13,87518474
25	1	0,305795819	82220B4000	XGBOOST	0,694204181	0,694204181	0,694204181	69,42041814
26	1	0,303442568	82220B4000	XGBOOST	0,696557432	0,696557432	0,696557432	69,65574324
27	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
28	0	0,185431346	82220B4000	XGBOOST	-0,185431346	0,185431346	0,185431346	
"""
df_sample_xgboost = pd.read_csv(StringIO(data_sample_xgboost), sep='\t')
df_sample_xgboost['Week'] = df_sample_xgboost['Week'].astype(int)  # Giữ Week là số nguyên
for col in ['Actual', 'Predicted', 'Error', 'RMSE', 'MAE', 'MAPE']:
    if col in df_sample_xgboost.columns and pd.api.types.is_string_dtype(df_sample_xgboost[col]):
        df_sample_xgboost[col] = df_sample_xgboost[col].str.replace(',', '.').astype(float)
    elif col in df_sample_xgboost.columns:
        df_sample_xgboost[col] = pd.to_numeric(df_sample_xgboost[col], errors='coerce')

# Data mẫu cho LSTM (giả định cấu trúc tương tự SARIMA)
df_sample_lstm = df_sample_sarima.copy()
df_sample_lstm['Method'] = 'LSTM'

# Danh sách mô hình
models = ['SARIMA', 'LSTM', 'XGBoost']

# Chọn mô hình
selected_model = st.selectbox("Chọn mô hình:", models, index=0)

# Chọn mã sản phẩm từ list cố định
selected_code = st.selectbox("Chọn mã sản phẩm:", product_codes, index=0)

# Hàm load data chung cho tất cả mô hình
def load_model_data(model_name, code, folder, sample_df):
    df = None
    if model_name in ['SARIMA', 'LSTM']:
        file_pattern = f"Forecast_{code}_Tuan_*.xlsx"
        found_file = None
        matching_files = []
        
        if os.path.exists(folder):
            all_files = [f for f in os.listdir(folder) if f.endswith('.xlsx')]
            matching_files = fnmatch.filter(all_files, file_pattern)
            
            if matching_files:
                def extract_date(filename):
                    match_date = re.search(r"_(\d{8})_", filename)
                    return int(match_date.group(1)) if match_date else 0
                found_file = max(matching_files, key=extract_date)
                file_path = os.path.join(folder, found_file)
                try:
                    df = pd.read_excel(file_path)
                    if 'Method' in df.columns:
                        df = df[df['Method'] == model_name].reset_index(drop=True)
                    numeric_cols = ['Actual', 'Predicted', 'Error', 'RMSE', 'MAE', 'MAPE']
                    for col in numeric_cols:
                        if col in df.columns and pd.api.types.is_string_dtype(df[col]):
                            df[col] = df[col].str.replace(',', '.').astype(float)
                        elif col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    st.error(f"Lỗi khi load file {file_path}: {e}")
                    return sample_df
            else:
                st.warning(f"Không tìm thấy file cho mã {code} trong folder {folder}.")
                return sample_df
        else:
            st.warning(f"Folder {folder} không tồn tại.")
            return sample_df
    elif model_name == 'XGBoost':
        file_path = os.path.join(folder, 'ket_qua_du_bao_xgboost.xlsx')
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path)
                if 'Ma sp' not in df.columns:
                    st.error(f"File {file_path} không chứa cột 'Ma sp'.")
                    return sample_df
                df['Week'] = df['Week'].astype(int)  # Giữ Week là số nguyên
                for col in ['Actual', 'Predicted', 'Error', 'RMSE', 'MAE', 'MAPE']:
                    if col in df.columns and pd.api.types.is_string_dtype(df[col]):
                        df[col] = df[col].str.replace(',', '.').astype(float)
                    elif col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                # Lọc theo mã sản phẩm
                df = df[df['Ma sp'] == code].reset_index(drop=True)
                if df.empty:
                    st.warning(f"Không tìm thấy dữ liệu cho mã {code} trong file {file_path}.")
                    return sample_df
            except Exception as e:
                st.error(f"Lỗi khi load file XGBoost {file_path}: {e}")
                return sample_df
        else:
            st.warning(f"Không tìm thấy file ket_qua_du_bao_xgboost.xlsx trong thư mục {folder}.")
            return sample_df
    
    return df if df is not None and not df.empty else sample_df

# Load data dựa trên mô hình được chọn
sample_df = df_sample_sarima if selected_model == 'SARIMA' else df_sample_lstm if selected_model == 'LSTM' else df_sample_xgboost
df = load_model_data(selected_model, selected_code, folders[selected_model], sample_df)

if not df.empty:
    # Thống kê mô tả từ sai số
    if selected_model in ['SARIMA', 'LSTM'] and all(col in df.columns for col in ['Error', 'RMSE', 'MAE', 'MAPE']):
        stats = df[['Error', 'RMSE', 'MAE', 'MAPE']].describe()
        st.subheader("Thống Kê Mô Tả Sai Số")
        st.dataframe(stats.style.format('{:.4f}'))
    elif selected_model == 'XGBoost' and all(col in df.columns for col in ['Error', 'RMSE', 'MAE', 'MAPE']):
        stats = df[['Error', 'RMSE', 'MAE', 'MAPE']].describe()
        st.subheader("Thống Kê Mô Tả Sai Số")
        st.dataframe(stats.style.format('{:.4f}'))

    # Hiển thị table chi tiết
    st.subheader("Data Chi Tiết")
    if selected_model in ['SARIMA', 'LSTM']:
        numeric_cols = ['Actual', 'Predicted', 'Error', 'RMSE', 'MAE', 'MAPE']
        format_dict = {col: '{:.2f}' for col in numeric_cols if col in df.columns}
        st.dataframe(df.style.format(format_dict))
    elif selected_model == 'XGBoost':
        numeric_cols = ['Week', 'Actual', 'Predicted', 'Error', 'RMSE', 'MAE', 'MAPE']
        format_dict = {col: '{:.2f}' for col in numeric_cols if col in df.columns and col != 'Week'}
        st.dataframe(df.style.format(format_dict))

    # Trực quan biểu đồ
    st.subheader("Biểu Đồ Trực Quan")

    if selected_model in ['SARIMA', 'LSTM'] and all(col in df.columns for col in ['Week', 'Actual', 'Predicted']):
        fig1 = px.line(df, x='Week', y=['Actual', 'Predicted'], 
                       title=f"Actual vs Predicted cho Mã {selected_code} - {selected_model}",
                       labels={'value': 'Giá Trị', 'variable': 'Loại'})
        fig1.update_layout(hovermode='x unified')
        st.plotly_chart(fig1, use_container_width=True)
        
        if 'Error' in df.columns:
            fig2 = px.line(df, x='Week', y='Error', 
                           title=f"Sai Số (Error) theo Tuần cho Mã {selected_code} - {selected_model}",
                           markers=True)
            fig2.update_traces(line_color='red')
            fig2.update_layout(hovermode='x unified')
            st.plotly_chart(fig2, use_container_width=True)
    elif selected_model == 'XGBoost' and all(col in df.columns for col in ['Week', 'Actual', 'Predicted']):
        fig1 = px.line(df, x='Week', y=['Actual', 'Predicted'], 
                       title=f"Actual vs Predicted cho Mã {selected_code} - {selected_model}",
                       labels={'value': 'Giá Trị', 'variable': 'Loại'})
        fig1.update_layout(hovermode='x unified')
        st.plotly_chart(fig1, use_container_width=True)
        
        if 'Error' in df.columns:
            fig2 = px.line(df, x='Week', y='Error', 
                           title=f"Sai Số (Error) theo Tuần cho Mã {selected_code} - {selected_model}",
                           markers=True)
            fig2.update_traces(line_color='red')
            fig2.update_layout(hovermode='x unified')
            st.plotly_chart(fig2, use_container_width=True)

    # Lưu vào session
    st.session_state.forecast_result = df
    st.session_state.selected_code = selected_code
    st.session_state.selected_model = selected_model
    st.success("Trực quan hoàn tất! Kết quả lưu để xuất ở Page 3.")
else:
    st.error("Data rỗng.")

# Footer
st.markdown("---")
