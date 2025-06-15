from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["Final_Project"]
collection = db["All_Leagues_Data"]

# 2. 필요한 열만 불러오기
cols = [
    "Market Value", "Goals", "Assists", "Minutes", "Age",
    "Yellow Cards", "Progressive Carries", "npxG + xAG/90"
]
df = pd.DataFrame(list(collection.find({}, {col: 1 for col in cols})))

# 3. 결측치 제거
df = df.dropna(subset=cols)

# 4. 상관계수 계산
corr_matrix = df[cols].corr()

# 5. Plotly 히트맵 시각화
fig = px.imshow(
    corr_matrix,
    color_continuous_scale="plasma",
    title="Market Value 및 주요 지표 간 상관계수 히트맵",
    labels=dict(x="지표", y="지표", color="상관계수"),
    aspect="auto"
)

fig.update_layout(
    xaxis_tickangle=45,
    font=dict(family="Arial", size=12),
    width=700,
    height=600
)

fig.show()
