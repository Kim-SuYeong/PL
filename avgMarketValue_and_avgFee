import pymongo
import pandas as pd
import plotly.graph_objs as go

# 1. MongoDB 연결
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Football"]
collection = db["PL"]

# 2. Aggregation pipeline with text 정제
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

# 3. Aggregation 실행
cursor = collection.aggregate(pipeline)
df = pd.DataFrame(list(cursor))
df.rename(columns={"_id": "Season"}, inplace=True)

# 4. trace1, trace2 생성
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

# 5. 레이아웃 설정 및 출력
layout = go.Layout(
    title="Average Market Value vs Transfer Fee by Season (Unit: Ten million euros)",
    xaxis=dict(title="Season"),
    yaxis=dict(title="Average Value (€m)"),
    barmode='group'
)

fig = go.Figure(data=[trace1, trace2], layout=layout)
fig.show()
