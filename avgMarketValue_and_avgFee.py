import pymongo
import pandas as pd
import plotly.graph_objs as go

# 1. MongoDB 연결
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Football"]
collection = db["PL"]

# 2. Aggregation pipeline
pipeline = [
    {
        "$match": {
            "Market value": {"$exists": True, "$ne": None},
            "Fee(이적료)": {"$exists": True, "$ne": None},
            "Season": {"$exists": True}
        }
    },
    {
        "$project": {
            "Season": 1,
            "Market value": {
                "$toDouble": {
                    "$replaceAll": {
                        "input": {
                            "$replaceAll": {
                                "input": "$Market value",
                                "find": "€",
                                "replacement": ""
                            }
                        },
                        "find": "m",
                        "replacement": ""
                    }
                }
            },
            "Fee": {
                "$toDouble": {
                    "$replaceAll": {
                        "input": {
                            "$replaceAll": {
                                "input": "$Fee(이적료)",
                                "find": "€",
                                "replacement": ""
                            }
                        },
                        "find": "m",
                        "replacement": ""
                    }
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$Season",
            "avgMarketValue": {"$avg": "$Market value"},
            "avgFee": {"$avg": "$Fee"}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]

# 3. Aggregation 실행 및 DataFrame 생성
cursor = collection.aggregate(pipeline)
df = pd.DataFrame(list(cursor))
df.rename(columns={"_id": "Season"}, inplace=True)

# 4. trace 생성
trace1 = go.Bar(
    x=df["Season"],
    y=df["avgMarketValue"],
    name="Market Value",
    marker=dict(color='rgb(49,130,189)', opacity=0.7),
    text=df["avgMarketValue"].round(2),
    textposition='auto'
)

trace2 = go.Bar(
    x=df["Season"],
    y=df["avgFee"],
    name="Transfer Fee",
    marker=dict(color='rgb(255,127,14)', opacity=0.7),
    text=df["avgFee"].round(2),
    textposition='auto'
)

# 5. 점선 정확한 위치 설정 (x축이 문자열이므로 약간 왼쪽에 위치시킴)
seasons = df["Season"].tolist()

# 두 시즌의 인덱스를 각각 구함
split_season1 = "2014-2015"
split_season2 = "2018-2019"

index1 = seasons.index(split_season1)
index2 = seasons.index(split_season2)

# 두 시즌 사이의 중간 위치 (예: 그래픽 경계선 그릴 위치로 활용 가능)
mid_index = (index1 + index2) / 2 + 0.08

# 점선을 정교하게 위치시키기 위해 xref='x' 사용 → 문자열 바로 왼쪽 보정값 사용
shapes = [
    dict(
        type='line',
        xref='paper',
        yref='paper',
        x0=mid_index / (len(seasons) - 1),  # 정규화 비율
        x1=mid_index / (len(seasons) - 1),
        y0=0,
        y1=1,
        line=dict(color='red', width=2, dash='dot')
    )
]


# 6. 레이아웃 구성
layout = go.Layout(
    title="Average Market Value vs Transfer Fee by Season (Unit: Ten million euros)",
    xaxis=dict(title="Season"),
    yaxis=dict(title="Average Value (€m)"),
    barmode='group',
    shapes=shapes
)

# 7. Figure 생성 및 표시
fig = go.Figure(data=[trace1, trace2], layout=layout)
fig.show()
