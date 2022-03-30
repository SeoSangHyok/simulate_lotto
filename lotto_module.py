import requests
import pandas
import tqdm
import os
from datetime import *
import math


class Lotto_db:
    def __init__(self):
        self.df_database = None
        
        df_schema = ["drwNo", "drwNoDate", "totSellamnt", "firstWinamnt", "firstPrzwnerCo", "drwtNo1", "drwtNo2", "drwtNo3", "drwtNo4", "drwtNo5", "drwtNo6", "bnusNo"]
        my_last_drawNo = 0
        db_csv_name = "lotto_db.csv"
        if os.path.isfile(db_csv_name):
            self.df_database = pandas.read_csv(db_csv_name)
            my_last_drawNo = self.df_database["drwNo"].iat[-1]
        else:            
            self.df_database = pandas.DataFrame(columns=df_schema)

        # 가장 최근의 로또 회차 계산
        # 오늘 날짜와 최초 로또 실시 일자의 날짜 차이를 계산해서 주로 나눈다.
        time_diff = datetime.now() - datetime.strptime("2002-12-07", "%Y-%m-%d")
        lastest_drawNo = math.floor(time_diff.days / 7) + 1

        print("로또 DB 최신화...")
        for drwNo in tqdm.tqdm(range(my_last_drawNo+1, lastest_drawNo+1)):
            req_url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
            result = requests.get(req_url).json()
            if result["returnValue"] == "success":
                new_row = {}
                for key, value in result.items():
                    if key in df_schema:
                        new_row[key] = value
                self.df_database.loc[len(self.df_database)] = new_row
            
        self.df_database.to_csv(db_csv_name, index=False)

    
    def cal_same_number_percentage(self):
        same_no_info = {
            "total_count": len(self.df_database),
            "same_no_count": [0,0,0,0,0,0,0]
        }
        
        print("같은번호가 다음회차에 연속으로 나올 확률을 계산합니다...")
        prev_drwno_list = []
        for row, value in tqdm.tqdm(self.df_database.iterrows(), total = self.df_database.shape[0]):
            drwno_list = [value["drwtNo1"], value["drwtNo2"], value["drwtNo3"], value["drwtNo4"], value["drwtNo5"], value["drwtNo6"]]
            same_no_count = 0
            for item in drwno_list:
                if item in prev_drwno_list:
                    same_no_count += 1
            same_no_info["same_no_count"][same_no_count] += 1

            prev_drwno_list = drwno_list
            
        print(f"same_no_info : {same_no_info}")
            