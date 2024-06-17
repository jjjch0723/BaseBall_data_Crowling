import requests
from bs4 import BeautifulSoup

def get_game_results(year, month, day):
    url = f"https://statiz.sporki.com/schedule/?year={year}&month={month}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []

    # 날짜에 해당하는 span 태그를 찾습니다.
    day_span = soup.find('span', class_='day', string=str(day))
    if not day_span:
        print(f"No data found for {year}-{month:02}-{day:02}")
        return results

    day_td = day_span.find_parent('td')
    if not day_td:
        print(f"No td element found for the day {day}")
        return results
    
    # 게임 정보를 포함하는 div.games 요소를 찾습니다.
    games_div = day_td.find('div', class_='games')
    if not games_div:
        print("No games div found")
        return results

    # 각 경기 정보를 포함하는 ul 태그를 찾습니다.
    ul_tags = games_div.find_all('ul')
    if not ul_tags:
        print("No ul tags found inside games div")
        return results

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

                        game_info['winning_team'] = winning_team
                        game_info['winning_score'] = winning_score
                        game_info['losing_team'] = losing_team
                        game_info['losing_score'] = losing_score

                        results.append(game_info)

    return results

# 사용 예제
year = 2024
month = 6
day = 16

game_results = get_game_results(year, month, day)
if not game_results:
    print("No game results found.")
else:
    for game in game_results:
        print(f"Winning Team: {game['winning_team']} with Score: {game['winning_score']}")
        print(f"Losing Team: {game['losing_team']} with Score: {game['losing_score']}")
        print()