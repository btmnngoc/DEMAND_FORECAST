import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Weekly Forecast Demo", layout="wide")


st.title("QUẢN LÝ MÃ SẢN PHẨM")
# --- Đọc dữ liệu trực tiếp từ thư mục data
DATA_PATH = "data/2025.01. Dữ liệu giả định (1).xlsx"
df_raw = pd.read_excel(DATA_PATH, sheet_name="Danh mục xuất hàng")

# Đọc dữ liệu từ sheet "Danh mục vật tư giả định"
df_master = pd.read_excel(DATA_PATH, sheet_name="Danh mục vật tư giả định")
df_master.columns = df_master.columns.str.strip().str.replace("\n"," ").str.replace("  "," ")

tab1, tab2, tab3 = st.tabs(["Tìm kiếm sản phẩm", "Nhóm chức năng", "Chủng loại sản phẩm"])

with tab1:
    st.subheader("Tìm kiếm mã sản phẩm")
    search_code = st.text_input("Nhập mã hoặc tên sản phẩm")
    if search_code:
        result = df_master[
            df_master["Mã"].astype(str).str.contains(search_code, case=False)
            | df_master["Tên"].astype(str).str.contains(search_code, case=False)
            | df_master["Tên tiếng Anh"].astype(str).str.contains(search_code, case=False)
        ]
        if not result.empty:
            st.success(f"Tìm thấy {len(result)} kết quả")
            st.dataframe(result)
            # Hiển thị bảng chi tiết xuất hàng theo mã đã chọn và biểu đồ xu hướng
            selected_codes = result["Mã"].unique()
            filtered_export = df_raw[df_raw["ItemCode"].isin(selected_codes)]
            st.write("Chi tiết xuất hàng theo mã đã chọn:")
            agg_export = filtered_export.groupby(["ItemCode","DocDate"], as_index=False)["Quantity"].sum()
            st.dataframe(agg_export)
            if not filtered_export.empty:
                fig = px.line(agg_export, x="DocDate", y="Quantity", color="ItemCode", markers=True, title="Xu hướng xuất hàng theo thời gian")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Không tìm thấy sản phẩm nào phù hợp.")

with tab2:
    st.subheader("Danh sách theo Nhóm chức năng")
    group_selected = st.selectbox("Chọn nhóm chức năng", df_master["Nhóm chức năng"].unique())
    df_group = df_master[df_master["Nhóm chức năng"] == group_selected]
    st.dataframe(df_group[["Mã", "Tên", "Chủng loại sản phẩm", "Xuất xứ"]])
    # Hiển thị bảng chi tiết xuất hàng theo mã đã chọn và biểu đồ xu hướng
    selected_codes = df_group["Mã"].unique()
    filtered_export = df_raw[df_raw["ItemCode"].isin(selected_codes)]
    available_codes = filtered_export["ItemCode"].unique()
    codes_to_show = st.multiselect("Chọn mã để hiển thị", available_codes, default=available_codes)
    filtered_export = filtered_export[filtered_export["ItemCode"].isin(codes_to_show)]
    st.write("Chi tiết xuất hàng theo mã đã chọn:")
    agg_export = filtered_export.groupby(["ItemCode","DocDate"], as_index=False)["Quantity"].sum()
    st.dataframe(agg_export)
    if not filtered_export.empty:
        fig = px.line(agg_export, x="DocDate", y="Quantity", color="ItemCode", markers=True, title="Xu hướng xuất hàng theo thời gian")
        st.plotly_chart(fig, use_container_width=True)
    if st.button("➡️ Dự báo nhu cầu", key="forecast_tab2"):
        st.switch_page("pages/2 Dự báo nhu cầu.py")

with tab3:
    st.subheader("Thống kê theo Chủng loại sản phẩm")
    category_counts = df_master["Chủng loại sản phẩm"].value_counts().reset_index()
    category_counts.columns = ["Chủng loại", "Số lượng mã"]

    st.bar_chart(category_counts.set_index("Chủng loại"))

    st.dataframe(category_counts)

    selected_category = st.selectbox("Chọn Chủng loại sản phẩm để xem chi tiết", df_master["Chủng loại sản phẩm"].unique())
    df_category = df_master[df_master["Chủng loại sản phẩm"] == selected_category]
    st.dataframe(df_category[["Mã", "Tên", "Xuất xứ", "Nhóm chức năng"]])
    # Hiển thị bảng chi tiết xuất hàng theo mã đã chọn và biểu đồ xu hướng
    selected_codes = df_category["Mã"].unique()
    filtered_export = df_raw[df_raw["ItemCode"].isin(selected_codes)]
    available_codes = filtered_export["ItemCode"].unique()
    codes_to_show = st.multiselect("Chọn mã để hiển thị", available_codes, default=available_codes)
    filtered_export = filtered_export[filtered_export["ItemCode"].isin(codes_to_show)]
    st.write("Chi tiết xuất hàng theo mã đã chọn:")
    agg_export = filtered_export.groupby(["ItemCode","DocDate"], as_index=False)["Quantity"].sum()
    st.dataframe(agg_export)
    if not filtered_export.empty:
        fig = px.line(agg_export, x="DocDate", y="Quantity", color="ItemCode", markers=True, title="Xu hướng xuất hàng theo thời gian")
        st.plotly_chart(fig, use_container_width=True)
    if st.button("➡️ Dự báo nhu cầu", key="forecast_tab3"):
        st.switch_page("pages/2 Dự báo nhu cầu.py")