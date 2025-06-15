from crawling import fetch_html
from player_parser import parse_players
from exporterToexcel import save_to_excel
import os
import random
import time
import requests
from requests.exceptions import RequestException, Timeout

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

def fetch_html(url, max_retries=5, timeout=40):
    headers = {"User-Agent": USER_AGENT}
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except (RequestException, Timeout) as e:
            print(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 3))
            else:
                print(f"All retries failed for {url}")
                return None

def main():
    save_dir = r"C:\BigData\2425Teams\Liga-Argentina"
    os.makedirs(save_dir, exist_ok=True)

    urls = [
        "https://www.transfermarkt.com/club-atletico-san-martin-sj-/startseite/verein/10511/saison_id/2024",
        "https://www.transfermarkt.com/cd-riestra/startseite/verein/19775/saison_id/2024"
         ]

    for idx, url in enumerate(urls, start=1):
        print(f"{idx}번째 사이트 처리 중: {url}")
        html = fetch_html(url)
        if html:
            players = parse_players(html)
            filename = os.path.join(save_dir, f"transfermarkt_{idx}.xlsx")
            save_to_excel(players, filename)
            print(f"{filename} 저장 완료!")
        # 요청 간 랜덤 대기
        if idx < len(urls):
            time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    main()
