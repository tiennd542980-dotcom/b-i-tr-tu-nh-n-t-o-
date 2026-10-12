import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cấu hình trang web
st.set_page_config(page_title="QUẢN LÝ ĐIỂM SINH VIÊN", layout="wide")

# 2. Tạo và xử lý dữ liệu
@st.cache_data
def load_data():
    data = {
        'Họ và tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
        'Chuyên cần': [8.0, 9.0, 7.0, 6.0, 5.5, 6.0, 6.5, 7.5, 5, 9.5],
        'Giữa kỳ':    [7.0, 8.5, 6.0, 6.0, 9.5, 5.5, 7.0, 6.5, 7.5, 9.0],
        'Cuối kỳ':    [8.5, 7.0, 6.5, 4.0, 7.5, 6.0, 8.5, 7.0, 4.0, 9.0]
    }
    df = pd.DataFrame(data)
    
    # Tính điểm tổng kết: 20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ
    df['Tong_ket'] = (df['Chuyên cần'] * 0.2 + df['Giữa kỳ'] * 0.3 + df['Cuối kỳ'] * 0.5).round(2)
    
    # Quy tắc xếp loại
    def xep_loai(score):
        if score >= 8.5:
            return 'Giỏi'
        elif score >= 7.0:
            return 'Khá'
        elif score >= 5.0:
            return 'Trung bình'
        else:
            return 'Yếu'
            
    df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)
    return df

df = load_data()

# 3. Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 4. Hiển thị bảng điểm
st.subheader("Bảng điểm chi tiết")
st.dataframe(df, use_container_width=True)

# 5. Hiển thị thông tin thống kê
st.subheader("Thông tin thống kê")
dtb = df['Tong_ket'].mean()
max_score = df['Tong_ket'].max()
min_score = df['Tong_ket'].min()
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

sv_max = ", ".join(df[df['Tong_ket'] == max_score]['Họ và tên'].tolist())
sv_min = ", ".join(df[df['Tong_ket'] == min_score]['Họ và tên'].tolist())

col1, col2, col3, col4 = st.columns(4)
col1.metric("ĐTB cả lớp", f"{dtb:.2f}")
col2.metric("Số SV đạt (>=5)", f"{so_sv_dat}/{len(df)}")
col3.metric("Điểm cao nhất", f"{max_score}")
col4.metric("Điểm thấp nhất", f"{min_score}")

st.write(f"• **Sinh viên điểm cao nhất ({max_score} điểm):** {sv_max}")
st.write(f"• **Sinh viên điểm thấp nhất ({min_score} điểm):** {sv_min}")

# 6. Tra cứu sinh viên theo danh sách xổ xuống (Selectbox)
st.subheader("Tra cứu điểm sinh viên")
selected_student = st.selectbox("Chọn sinh viên để xem thông tin chi tiết:", df['Họ và tên'].unique())

sv_info = df[df['Họ và tên'] == selected_student].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", sv_info['Chuyên cần'])
c2.metric("Giữa kỳ", sv_info['Giữa kỳ'])
c3.metric("Cuối kỳ", sv_info['Cuối kỳ'])
c4.metric("Tổng kết", sv_info['Tong_ket'])
c5.metric("Xếp loại", sv_info['Xep_loai'])

# 7. Biểu đồ cột điểm tổng kết
st.subheader("Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.barh(df['Họ và tên'], df['Tong_ket'], color='#4a90e2')
ax.set_xlabel('Điểm tổng kết')
ax.set_ylabel('Họ và tên')
ax.set_xlim(0, 10)
ax.invert_yaxis()
ax.grid(axis='x', linestyle='--', alpha=0.7)

st.pyplot(fig)

# 8. Họ tên và MSSV người tạo (hiển thị cỡ chữ nhỏ ở cuối trang)
st.markdown("---")
st.caption("Người thực hiện: [NGUYỄN ĐẮC TIÊN] - MSSV: [054207002980]")
