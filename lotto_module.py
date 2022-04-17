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

    
    def analysis_same_no(self):
        same_no_info = {
            "total_count": len(self.df_database),
            "same_no_count": [0, 0, 0, 0, 0, 0, 0]
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
        
        
    def check_continuity_no(self):
        print("한 게임에 연속된 번호가 몇게가 나올 수 있는지 계산합니다.")
        
        # 한게임에 연속된 숫자가 몇세트가 나올수 있는지 체크
        result_set = {}
        for row, value in tqdm.tqdm(self.df_database.iterrows(), total = self.df_database.shape[0]):
            drwno_list = [value["drwtNo1"], value["drwtNo2"], value["drwtNo3"], value["drwtNo4"], value["drwtNo5"], value["drwtNo6"]]
            
            list_index = 1
            continuity_set = []
            count = 1
            while list_index < len(drwno_list):
                if drwno_list[list_index] == drwno_list[list_index-1] + 1:
                    count += 1
                else:
                    continuity_set.append(count)
                    count = 1
                    
                list_index += 1
            
            continuity_set.append(count)
            continuity_set.sort()
            
            continuity_set = tuple(continuity_set)
            
            if result_set.get(continuity_set) == None:
                result_set[continuity_set] = 1
            else:
                result_set[continuity_set] += 1
            
                
            
            # same_no_count = 0
            # for item in drwno_list:
            #     if item in prev_drwno_list:
            #         same_no_count += 1
            # same_no_info["same_no_count"][same_no_count] += 1

            # prev_drwno_list = drwno_list
            
        print(f"result_set : {result_set}")
            
            

    def analysis_straight_no(self):
        print("각 숫자별로 연속된 숫자가 나오는 통계를 계산합니다.")

        straight_no_info = [0 for num in range(0, 46)]
        print(straight_no_info)

        for row, value in tqdm.tqdm(self.df_database.iterrows(), total=self.df_database.shape[0]):
            drwno_list = [value["drwtNo1"], value["drwtNo2"], value["drwtNo3"], value["drwtNo4"], value["drwtNo5"], value["drwtNo6"]]
            drwno_list.sort()
            for list_idx in range(0,5):
                # 연속된 숫자체크 2개까지만 체크하며 3개이상 연속된 숫자는 제외한다.
                if drwno_list[list_idx + 1] - drwno_list[list_idx] == 1:
                    if list_idx + 3 <= len(drwno_list):
                        if drwno_list[list_idx + 2] - drwno_list[list_idx + 1] != 1:
                            straight_no_info[drwno_list[list_idx]] += 1
                    else:
                        straight_no_info[drwno_list[list_idx]] += 1

        print(f"Straight no info : {straight_no_info}")

    def draw_lotto_num(self):
        pass
#       로또 넘버 뽑는 규칙은 아래와 같이 진행
#
