import requests
import pandas

# 해야할일
# 1. 로또 데이터 베이스에서 1회차~가장 최근꺼 까지 request로 받아온 후 csv에 저장(업데이트)

lotto_history_df = {
    "drwNo": [],
    "drwNoDate": [],
    "totSellamnt": [],
    "firstWinamnt": [],
    "firstPrzwnerCo": [],
    "drwtNo1": [],
    "drwtNo2": [],
    "drwtNo3": [],
    "drwtNo4": [],
    "drwtNo5": [],    
    "drwtNo6": [],    
    "bnusNo": [],            
}


for drwNo in range (1,5):
    req_url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
    req_result = requests.get(req_url)
    result_json = req_result.json()
    if result_json["returnValue"] == "success":
        for key, value in result_json.items():
            if key in lotto_history_df.keys():
                lotto_history_df[key].append(value)

df = pandas.DataFrame()
df = df.from_dict(lotto_history_df)
print(df)
