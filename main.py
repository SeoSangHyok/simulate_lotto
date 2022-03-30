import requests
import pandas
import tqdm
import os
import lotto_module
import datetime
import math


lotto_db = lotto_module.Lotto_db()
lotto_db.cal_same_number_percentage()

