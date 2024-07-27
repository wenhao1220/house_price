import streamlit as st
import plotly.express as px
import pandas as pd

# 設置頁面配置
st.set_page_config(layout="wide")

st.title("虎尾房價視覺化儀表板(111年-113年)")

# 文件上传
uploaded_file = st.file_uploader("請上傳CSV文件", type="csv")

if uploaded_file is not None:
    # 加載清理後的CSV數據
    data = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    
    # 創建簡化的路段名稱列
    data['簡化路段'] = data['地段位置或門牌'].str.extract(r'^(虎尾鎮.*?路|虎尾鎮.*?街)')[0].fillna(data['地段位置或門牌'])
    
    # 提取簡化的唯一路段名稱用於下拉選單選項
    unique_simplified_areas = data['簡化路段'].dropna().unique()

    selected_simplified_area = st.selectbox('選擇簡化路段', unique_simplified_areas)

    # 根據選擇的簡化路段過濾數據
    filtered_data = data[data['簡化路段'] == selected_simplified_area]
    filtered_data = filtered_data.sort_values(by='單價', ascending=False)

    # 計算每個簡化路段的總平均價格
    average_price = filtered_data['單價'].mean()

    # 創建柱狀圖，並在每個柱子上顯示單價
    fig = px.bar(filtered_data, x='地段位置或門牌', y='單價',
                 labels={'地段位置或門牌': '門牌號', '單價': '每坪單價 (萬元)'},
                 title=f'{selected_simplified_area} 每筆交易資料的每坪單價',
                 color='單價',  # 根據單價改變顏色
                 color_continuous_scale=px.colors.sequential.Viridis)

    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')

    # 顯示圖表
    st.plotly_chart(fig)

    # 顯示表格
    st.write("### 總平均單價")
    st.table(pd.DataFrame({'路段': [selected_simplified_area], '總平均單價 (萬元)': [f'{average_price:.2f}']}))
else:
    st.write("請上傳CSV文件以查看數據")
