"""import pandas as pd
import os

# 저장할 폴더 경로 (원하는 경로로 변경)
save_dir = r"C:\BigData\2425Teams\J1-League"

# 병합 결과 파일 경로
output_path = os.path.join(save_dir, "merged.xlsx")

# 데이터 불러오기
df1 = pd.read_excel(r'C:\BigData\2425Teams\J1-League\merged.xlsx')
df2 = pd.read_excel(r'C:\BigData\2425Teams\J1-League\Fagiano Okayama.xlsx')

# 병합 (예시: 'player' 컬럼 기준)
merged = pd.merge(
    df1, 
    df2, 
    on='player', 
    how='outer',  
)

# 결과 저장
merged.to_excel(output_path, index=False)
print(f"결과 파일 저장 완료: {output_path}")"""

import pandas as pd
import os

# 저장 경로 설정
save_dir = r"C:\BigData\2425Teams\K-League"
os.makedirs(save_dir, exist_ok=True)
output_path = os.path.join(save_dir, "merged_final.xlsx")

# 병합할 파일 목록 (최초 파일은 전체 스탯, 나머지는 팀별 파일)
files = [
    "K-League.xlsx", # 최초
    "FC Seoul.xlsx",                  
    "Daegu FC.xlsx",         # 이하 추가 파일 
    "Daejeon Hana Citizen.xlsx",
    "FC Anyang.xlsx",
    "FC Seoul.xlsx",   
    "Gangwon FC.xlsx",  
    "Gimcheon Sangmu.xlsx",  
    "Gwangju FC.xlsx",        
    "Jeju SK.xlsx",  
    "Jeonbuk Hyundai Motors.xlsx",  
    "Pohang Steelers .xlsx",  
    "Suwon FC.xlsx",  
    "Ulsan HD FC.xlsx"
]

# 1. 최초 데이터 불러오기 (기존 merged.xlsx)
df_merged = pd.read_excel(os.path.join(save_dir, files[0]))

# merged에 Market Value 컬럼이 없으면 생성
if 'Market Value' not in df_merged.columns:
    df_merged['Market Value'] = None  # 또는 빈 문자열 등

# 나머지 파일을 순차적으로 병합
for file in files[1:]:
    df_team = pd.read_excel(os.path.join(save_dir, file))
    # player와 Market Value만 추출
    df_team = df_team[['player', 'Market Value']]
    # Market Value가 비어있지 않은 경우만 업데이트
    df_team = df_team.dropna(subset=['Market Value'])
    # merged의 Market Value를 팀 파일의 값으로 업데이트
    for idx, row in df_team.iterrows():
        mask = df_merged['player'] == row['player']
        df_merged.loc[mask, 'Market Value'] = row['Market Value']

# 결과 저장
df_merged.to_excel(output_path, index=False)
print(f"결과 저장 완료: {output_path}")






