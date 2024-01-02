import requests
from functions.user_data import get_user_data
import json
from elements.urls import mysite


def check_balance_for_test(telegram_id):
    res = get_user_data(telegram_id)
    res_json = json.loads(res)
    balance = res_json['balance']

    url = f"{mysite}/api/get/test_details/"
    res2 = requests.get(url).text

    try:

        res2_data = json.loads(res2)

        if res2_data['price1'] <= balance:
            return True
        else:
            return False
    except Exception as err:
        print(err)


def get_prices():
    url = f"{mysite}/api/get/test_details/"
    res2 = requests.get(url).text

    res2_data = json.loads(res2)

    return  res2_data