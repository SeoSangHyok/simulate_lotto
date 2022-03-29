import requests


print("hello world!!")
j = requests.get("https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1008")

print(j.json())