from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["Final_Project"]
collection = db["All_Leagues_Data"]

# 2. 데이터 로드
df = pd.DataFrame(list(collection.find()))

# 3. 필요한 컬럼 필터링 및 전처리
df = df[["League", "Squad", "Position", "xG/90"]]

# 4. League == 'PL' 필터
df = df[df["League"] == "PL"]

# 5. xG가 숫자가 아니면 변환
df["xG/90"] = pd.to_numeric(df["xG/90"], errors="coerce")
df.dropna(subset=["xG/90", "Squad", "Position"], inplace=True)

# 6. 팀-포지션별 기대 득점 합계 계산
grouped = df.groupby(["Squad", "Position"], as_index=False)["xG/90"].sum()

# 7. Treemap 시각화
fig = px.treemap(
    grouped,
    path=["Squad", "Position"],
    values="xG/90",
    color="xG/90",
    color_continuous_scale="Blues",
    title="팀 및 포지션별 기대 골 (xG/90)"
)

fig.show()
