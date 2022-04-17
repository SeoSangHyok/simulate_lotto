import requests
import pandas
import tqdm
import os
import lotto_module
import datetime
import math


lotto_db = lotto_module.Lotto_db()
lotto_db.cal_same_number_percentage()
lotto_db.check_continuity_no()

# 이전게임에서 두번이상 나온 번호가 있는경우 제외
# 한게임에 연속된 숫자가 3개 이상나온경우 제외
# 한게임에 2숫자가 연속된 것이 두세트 이상 나오면 제외 

