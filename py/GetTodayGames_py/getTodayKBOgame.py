import requests
from bs4 import BeautifulSoup
import json
import os

# 저장 디렉토리 설정
save_dir = 'C:/DevTool/BaseBall/BaseBall_data_Crowling/json/todaysGames'
os.makedirs(save_dir, exist_ok=True)

# 팀 이름과 팀 코드 매핑
team_id_map = {
    "두산": 6002,
    "LG": 5002,
    "KT": 12001,
    "SSG": 9002,
    "NC": 11001,
    "KIA": 2002,
    "롯데": 3001,
    "삼성": 1001,
    "한화": 7002,
    "키움": 10001
}

# Base URL
base_url = "https://statiz.sporki.com/schedule/?year={year}&month={month}"

# Headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Function to parse a single page and extract game results
def parse_page(year, month, day):
    data = []
    url = base_url.format(year=year, month=month)
    print(f"Fetching data from URL: {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # 날짜에 해당하는 span 태그를 찾습니다.
    day_span = soup.find('span', class_='day', string=str(day))
    if not day_span:
        print(f"No data found for {year}-{month:02}-{day:02}")
        return data

    day_td = day_span.find_parent('td')
    if not day_td:
        print(f"No td element found for the day {day}")
        return data
    
    # 게임 정보를 포함하는 div.games 요소를 찾습니다.
    games_div = day_td.find('div', class_='games')
    if not games_div:
        print("No games div found")
        return data

    # 각 경기 정보를 포함하는 ul 태그를 찾습니다.
    ul_tags = games_div.find_all('ul')
    if not ul_tags:
        print("No ul tags found inside games div")
        return data

    for ul in ul_tags:
        li_tags = ul.find_all('li')

        for li in li_tags:
            game_info = {}
            a_tag = li.find('a')
            if a_tag:
                # 이긴 팀과 진 팀 정보를 포함하는 span 태그를 찾습니다.
                team_spans = li.find_all('span', class_='team')
                score_spans = li.find_all('span', class_='score')
                lead_span = li.find('span', class_='score lead')

                if len(team_spans) == 2 and len(score_spans) == 2 and lead_span:
                    # winning_team_span을 찾을 때, style 속성의 공백을 제거하고 정확히 일치하도록 수정
                    winning_team_span = next((span for span in team_spans if 'color:#FFFFFF' in span.get('style', '').replace(' ', '')), None)
                    if winning_team_span:
                        winning_team = winning_team_span.get_text(strip=True)
                        winning_score = lead_span.get_text(strip=True)
                        losing_team = None
                        losing_score = None
                        
                        for span in team_spans:
                            if span != winning_team_span:
                                losing_team = span.get_text(strip=True)
                                break

                        for span in score_spans:
                            if span != lead_span:
                                losing_score = span.get_text(strip=True)
                                break

                        # 매핑된 팀 코드로 변환
                        win_team_code = team_id_map.get(winning_team)
                        lose_team_code = team_id_map.get(losing_team)

                        if win_team_code and lose_team_code:
                            game_info = {
                                "DATE": f"{year}-{month:02d}-{day:02d}",
                                "WINTEAM": str(win_team_code),
                                "LOSETEAM": str(lose_team_code),
                                "WINSCORE": str(winning_score),
                                "LOSESCORE": str(losing_score)
                            }

                            data.append(game_info)

    return data

# 사용 예제
year = 2024
month = 6
day = 15

game_results = parse_page(year, month, day)
if not game_results:
    print("No game results found.")
else:
    # Save the data to a JSON file
    file_path = os.path.join(save_dir, "20240615KBOresult.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(game_results, f, ensure_ascii=False, indent=4)

    print(f"경기 결과가 {file_path} 파일에 성공적으로 저장되었습니다.")