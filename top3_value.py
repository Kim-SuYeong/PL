import pymongo
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# 1. MongoDB 연결
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Football"]
collection = db["PL"]

# 2. 데이터 로딩 및 전처리
df = pd.DataFrame(list(collection.find({})))
if "_id" in df.columns:
    df.drop(columns=["_id"], inplace=True)

df = df[['Season', 'Name', 'Market value', 'Fee(이적료)']].dropna()
df['Market value'] = df['Market value'].str.replace('€', '').str.replace('m', '').astype(float)
df['Fee'] = df['Fee(이적료)'].str.replace('€', '').str.replace('m', '').astype(float)
df.drop(columns=['Fee(이적료)'], inplace=True)

# 3. 시즌 목록
seasons = df['Season'].unique()
seasons.sort()
num_seasons = len(seasons)

# 4. subplot 만들기
cols = 2
rows = (num_seasons + 1) // cols
fig = make_subplots(
    rows=rows,
    cols=cols,
    subplot_titles=[str(season) for season in seasons]
)

# 5. 시즌별 subplot 추가
row = col = 1
for season in seasons:
    season_df = df[df['Season'] == season]
    names = season_df['Name'].tolist()
    market_values = season_df['Market value'].tolist()
    fees = season_df['Fee'].tolist()

    # trace1: Market Value
    trace1 = go.Bar(
        x=names,
        y=market_values,
        name='Market Value',
        marker=dict(color='rgb(49,130,189)', opacity=0.7),
        text=market_values,
        textposition='auto',
        showlegend=(row == 1 and col == 1)
    )

    # trace2: Transfer Fee
    trace2 = go.Bar(
        x=names,
        y=fees,
        name='Transfer Fee',
        marker=dict(color='rgb(255,127,14)', opacity=0.7),
        text=fees,
        textposition='auto',
        showlegend=(row == 1 and col == 1)
    )

    # subplot에 trace 추가
    fig.add_trace(trace1, row=row, col=col)
    fig.add_trace(trace2, row=row, col=col)

    # 위치 조정
    col += 1
    if col > cols:
        row += 1
        col = 1

# 6. 전체 레이아웃 설정
fig.update_layout(
    height=300 * rows,
    width=1000,
    title_text="Market Value vs Transfer Fee by Season (Unit: Ten million euros)",
    barmode='group'
)

# 7. x축 레이블 회전
fig.update_xaxes(tickangle=0)

# 8. 출력
fig.show()
