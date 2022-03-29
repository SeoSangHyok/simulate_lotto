import requests


print("hello world!!")
j = requests.get("https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1008")

print(j.json())

# 해야할일
# 1. 로또 데이터 베이스에서 1회차~가장 최근꺼 까지 request로 받아온 후 csv에 저장(업데이트)
