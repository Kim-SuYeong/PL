import pandas as pd

def save_to_excel(data, filename='players_market_value.xlsx'):
    """리스트 데이터를 엑셀 파일로 저장"""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)