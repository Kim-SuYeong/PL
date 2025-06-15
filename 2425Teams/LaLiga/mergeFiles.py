import pandas as pd

def merge_excel_files(base_file, file_list, key_column='player', value_column='Market Value', output_file='laligamerged_resultFile0521.xlsx'):
    base_df = pd.read_excel(base_file)

    for file in file_list:
        temp_df = pd.read_excel(file)
        if value_column in temp_df.columns:
            temp_df = temp_df[[key_column, value_column]]
        else:
            continue
        
        # 병합 시 suffixes 지정
        base_df = pd.merge(
            base_df, temp_df, 
            on=key_column, how='left', 
            suffixes=('', '_new')
        )
        # 새 값이 있으면 덮어쓰기
        base_df[value_column] = base_df[f'{value_column}_new'].combine_first(base_df[value_column])
        # 중복 열 삭제
        base_df = base_df.drop(columns=[f'{value_column}_new'])

    base_df.to_excel(output_file, index=False)
    return f'Merged file saved as {output_file}'

base_file = r"C:\BigData\2425Teams\LaLiga\La_liga_Data.xlsx"
file_list = [
    'Athletic_Bilbao_players_market_value.xlsx', 'Atlético de Madrid_players_market_value.xlsx',
    'CA Osasuna_players_market_value.xlsx', 'CD Leganés_players_market_value.xlsx','Celta de Vigo_players_market_value.xlsx',
    'Deportivo Alavés_players_market_value.xlsx','FC Barcelona_players_market_value.xlsx','Getafe CF_players_market_value.xlsx','Girona FC_players_market_value.xlsx',
    'Rayo Vallecano_players_market_value.xlsx','RCD Espanyol Barcelona_players_market_value.xlsx','RCD Mallorca_players_market_value.xlsx',
    'Real Betis Balompié_players_market_value.xlsx','Real Madrid_players_market_value.xlsx','Real Sociedad_players_market_value.xlsx','Real Valladolid CF_players_market_value.xlsx',
    'Sevilla FC_players_market_value.xlsx','UD Las Palmas_players_market_value.xlsx','Valencia CF_players_market_value.xlsx','Villarreal CF_players_market_value.xlsx'
]

merge_excel_files(base_file, file_list)