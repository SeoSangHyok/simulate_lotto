import requests
import pandas
import tqdm
import os
from datetime import *
import math


class Lotto_history:
    def __init__(self):
        self.last_drawNo = 0
        history_csv_name = "history.csv"
        if os.path.isfile(history_csv_name):
            self.df_draw_history = pandas.read_csv(history_csv_name)
            self.last_drawNo = self.df_draw_history["drwNo"].iat[-1]

        # 가장 최근의 로또 회차 계산
        # 오늘 날짜와 최초 로또 실시 일자의 날짜 차이를 계산해서 주로 나눈다.
        time_diff = datetime.now() - datetime.strptime("2002-12-07", "%Y-%m-%d")

        print("가장 마지막 회차까지 로또정보 로딩...")
        for drwNo in tqdm.tqdm(range(self.last_drawNo+1, math.floor(time_diff.days / 7)) + 1):
            req_url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
            req_result = requests.get(req_url).json()


