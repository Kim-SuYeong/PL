import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup, Comment

# 사이트 주소 리스트
urls = [
    'https://fbref.com/en/comps/11/stats/Serie-A-Stats',
    'https://fbref.com/en/comps/25/stats/J1-League-Stats',
    'https://fbref.com/en/comps/55/stats/K-League-1-Stats',
    'https://fbref.com/en/comps/70/stats/Saudi-Professional-League-Stats',
    'https://fbref.com/en/comps/31/stats/Liga-MX-Stats',
    'https://fbref.com/en/comps/23/stats/Eredivisie-Stats',
    'https://fbref.com/en/comps/28/stats/Eliteserien-Stats',
    'https://fbref.com/en/comps/61/stats/Primera-Division-Stats',
    'https://fbref.com/en/comps/44/stats/Liga-1-Stats',
    'https://fbref.com/en/comps/36/stats/Ekstraklasa-Stats',
    'https://fbref.com/en/comps/32/stats/Primeira-Liga-Stats',
    'https://fbref.com/en/comps/47/stats/Liga-I-Stats',
    'https://fbref.com/en/comps/52/stats/Premier-Division-Stats',
    'https://fbref.com/en/comps/30/stats/Russian-Premier-League-Stats',
    'https://fbref.com/en/comps/40/stats/Scottish-Premiership-Stats',
    'https://fbref.com/en/comps/54/stats/Serbian-SuperLiga-Stats',
    'https://fbref.com/en/comps/57/stats/Swiss-Super-League-Stats',
    'https://fbref.com/en/comps/29/stats/Allsvenskan-Stats',
    'https://fbref.com/en/comps/26/stats/Super-Lig-Stats',
    'https://fbref.com/en/comps/39/stats/Ukrainian-Premier-League-Stats',
    'https://fbref.com/en/comps/45/stats/Uruguayan-Primera-Division-Stats',
    'https://fbref.com/en/comps/22/stats/Major-League-Soccer-Stats',
    'https://fbref.com/en/comps/105/stats/Venezuelan-Primera-Division-Stats'

]

# 크롬 옵션 설정
options = Options()
options.add_argument('--headless')  # 창을 띄우지 않고 실행 (필요시 주석 해제)
options.add_argument('--start-maximized')  # 전체 창 크기로 실행
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# 드라이버 초기화
wd = webdriver.Chrome(options=options)

for idx, url in enumerate(urls):
    wd.get(url)
    print(f"접속 완료: {url}")

    # 테이블이 로드될 때까지 대기
    WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'table'))
    )
    time.sleep(3)  # 추가 대기

    # 페이지 소스 파싱
    soup = BeautifulSoup(wd.page_source, 'html.parser')

    # 1. 일반 테이블에서 데이터 추출
    table = soup.find('table')
    if table is not None:
        # 헤더 추출 (aria-label)
        thead = table.find('thead')
        header = []
        if thead is not None:
            header = [th.get('aria-label') for th in thead.find_all('th') if th.get('aria-label') is not None]
        # 행 데이터 추출
        tbody = table.find('tbody')
        rows = []
        if tbody is not None:
            for tr in tbody.find_all('tr'):
                row = [cell.get_text(strip=True) for cell in tr.find_all(['th', 'td'])]
                rows.append(row)
        # CSV 저장
        filename = f"site_{idx+1}_data.csv"
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"{filename} 저장 완료")
    else:
        print("일반 table이 없습니다.")

    # 2. 주석 내 테이블에서 데이터 추출
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for cidx, comment in enumerate(comments):
        comment_soup = BeautifulSoup(comment, 'html.parser')
        comment_table = comment_soup.find('table')
        if comment_table is not None:
            # 헤더 추출 (aria-label)
            comment_thead = comment_table.find('thead')
            comment_header = []
            if comment_thead is not None:
                comment_header = [th.get('aria-label') for th in comment_thead.find_all('th') if th.get('aria-label') is not None]
            # 행 데이터 추출
            comment_tbody = comment_table.find('tbody')
            comment_rows = []
            if comment_tbody is not None:
                for tr in comment_tbody.find_all('tr'):
                    row = [cell.get_text(strip=True) for cell in tr.find_all(['th', 'td'])]
                    comment_rows.append(row)
            # CSV 저장 (주석 내 테이블은 별도 파일로)
            filename_comment = f"site_{idx+1}_comment_{cidx+1}_data.csv"
            with open(filename_comment, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                if comment_header:
                    writer.writerow(comment_header)
                writer.writerows(comment_rows)
            print(f"{filename_comment} 저장 완료")

wd.quit()