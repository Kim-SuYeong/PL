from bs4 import BeautifulSoup

def parse_players(html):
    soup = BeautifulSoup(html, 'html.parser')
    players = []

    for tr in soup.find_all('tr', class_=['odd', 'even']):
        # 이름 추출 로직 수정
        name_tag = tr.select_one('td.posrela table.inline-table td.hauptlink a')
        player_name = name_tag.get_text(strip=True) if name_tag else None

        # 몸값 추출 (기존 로직 유지)
        value_tag = tr.find('td', class_='rechts hauptlink')
        market_value = value_tag.find('a').get_text(strip=True) if value_tag and value_tag.find('a') else None

        if player_name and market_value:
            players.append({'Name': player_name, 'Market Value': market_value})

    return players