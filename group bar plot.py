from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import re

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["Final_Project"]
collection = db["All_Leagues_Data"]

# 2. 데이터 불러오기
df = pd.DataFrame(list(collection.find({}, {
    "League": 1,
    "Position": 1,
    "Market Value": 1
})))

# 3. Market Value 전처리
def convert_market_value(val):
    if pd.isna(val):
        return None
    val = str(val).lower().replace("€", "").replace("¢æ", "").strip()
    if val.endswith("k"):
        return float(val[:-1]) * 1_000
    elif val.endswith("m"):
        return float(val[:-1]) * 1_000_000
    try:
        return float(val)
    except:
        return None

df["Market Value"] = df["Market Value"].apply(convert_market_value)
df.dropna(subset=["League", "Position", "Market Value"], inplace=True)

# 4. 포지션 필터링
df = df[df["Position"].isin(["FW", "MF", "DF", "GK"])]

# 5. 리그 정제 및 매핑
df["League"] = df["League"].astype(str).str.lower().str.strip()
df["League"] = df["League"].apply(lambda x: re.sub(r"[^a-z0-9\s]", "", x))

league_map = {
    "bundesliga": "Bundesliga",
    "pl": "PL",
    "laliga": "Laliga",
    "ligue1": "Franceligue",
    "seriea": "Italy"
}

def map_league(league):
    league = league.replace(" ", "")
    for key, name in league_map.items():
        if key in league:
            return name
    return None

df["League"] = df["League"].apply(map_league)
df.dropna(subset=["League"], inplace=True)

# 6. Market Value 단위 변환
df["Market Value (천만 파운드)"] = df["Market Value"] / 10_000_000

# 7. 평균 Market Value 계산
grouped = df.groupby(["League", "Position"], as_index=False)["Market Value (천만 파운드)"].mean()

# 8. 시각화 (색상: Market Value 크기, 포지션은 텍스트로 표시)
fig = px.bar(
    grouped,
    y="League",
    x="Market Value (천만 파운드)",
    color="Market Value (천만 파운드)",
    text="Position",
    orientation="h",
    color_continuous_scale="plasma",
    title="주요 5개 리그의 포지션별 평균 Market Value",
    labels={
        "League": "리그",
        "Market Value (천만 파운드)": "평균 Market Value"
    }
)

fig.update_traces(
    textposition="inside",
    insidetextanchor="start"
)

fig.update_layout(
    height=700,
    width=1000,
    font=dict(family="Arial", size=13),
    showlegend=False
)

fig.show()
