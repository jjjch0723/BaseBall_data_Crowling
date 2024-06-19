import statsapi
import json
from datetime import datetime, timedelta

# 어제 날짜를 YYYYMMDD 형식으로 가져오기
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
file_date = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

# 어제 날짜로 경기 결과 가져오기
games = statsapi.schedule(date=yesterday)

# 결과 저장 리스트
results = []

# 각 경기 결과 처리
for game in games:
    away_team = game['away_id']
    home_team = game['home_id']
    away_score = game['away_score']
    home_score = game['home_score']
    status = game['status']
    
    if status == 'Final':
        if away_score > home_score:
            win_team = away_team
            lose_team = home_team
            win_score = away_score
            lose_score = home_score
        else:
            win_team = home_team
            lose_team = away_team
            win_score = home_score
            lose_score = away_score
    else:
        win_team = ""
        lose_team = ""
        win_score = ""
        lose_score = ""

    result = {
        "DATE": yesterday,
        "WINTEAM": str(win_team),
        "LOSETEAM": str(lose_team),
        "WINSCORE": str(win_score),
        "LOSESCORE": str(lose_score),
        "STATUS": status
    }
    results.append(result)

# 로그 출력
if results:
    print(f"어제 완료된 경기를 찾았습니다: {results}")
else:
    print("어제 완료된 경기를 찾을 수 없습니다.")

# 결과를 저장
file_path = f"C:\\DevTool\\BaseBall\\BaseBall_data_Crowling\\json\\todaysGames\\{file_date}MLBresult.json"
with open(file_path, 'w') as json_file:
    json.dump(results, json_file, indent=4)
print(f"결과가 {file_path}에 저장되었습니다.")
