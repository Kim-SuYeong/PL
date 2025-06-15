import requests

def fetch_html(url, timeout=20):
    """URL에서 HTML을 받아오는 함수"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
