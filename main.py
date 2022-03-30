import requests
import pandas
import tqdm
import os
import lotto_module
import datetime
import math


# date = datetime.datetime.strptime("2002-12-07", "%Y-%m-%d")
# date_now = datetime.datetime.now()
#
# time_diff = date_now - date
#
# print(math.floor(time_diff.days / 7) + 1)
#
# print(time_diff)


# drw_history = lotto_module.Lotto_history()

# 해야할일
# 1. 로또 데이터 베이스에서 1회차~가장 최근꺼 까지 request로 받아온 후 csv에 저장(업데이트)

# lotto_history_df = {
#     "drwNo": [],
#     "drwNoDate": [],
#     "totSellamnt": [],
#     "firstWinamnt": [],
#     "firstPrzwnerCo": [],
#     "drwtNo1": [],
#     "drwtNo2": [],
#     "drwtNo3": [],
#     "drwtNo4": [],
#     "drwtNo5": [],
#     "drwtNo6": [],
#     "bnusNo": [],
# }

columns = ["drwNo", "drwNoDate", "totSellamnt", "firstWinamnt", "firstPrzwnerCo", "drwtNo1", "drwtNo2", "drwtNo3", "drwtNo4", "drwtNo5", "drwtNo6", "bnusNo"]

df = pandas.DataFrame(columns=columns)

for drwNo in tqdm.tqdm(range(1, 5)):
    req_url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
    req_result = requests.get(req_url)
    result_json = req_result.json()
    if result_json["returnValue"] == "success":
        new_row = {}
        for key, value in result_json.items():
            if key in columns:

                new_row[key] = value

        print(pandas.DataFrame.from_dict(new_row))

        # df = pandas.concat([df, pandas.DataFrame.from_dict(new_row)], axis=1, ignore_index=True)

print(df)
df.to_csv("history.csv")


# print(os.path.isfile("history.csv"))
#
# df = pandas.read_csv("history.csv")
# df_dict = df.to_dict()
# print(df_dict)


# for drwNo in tqdm.tqdm(range(1, 5)):
#     req_url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
#     req_result = requests.get(req_url)
#     result_json = req_result.json()
#     if result_json["returnValue"] == "success":
#         for key, value in result_json.items():
#             if key in lotto_history_df.keys():
#                 lotto_history_df[key].append(value)
#
# df = pandas.DataFrame()
# df = df.from_dict(lotto_history_df)
# df.to_csv("history.csv")
# print(df)
