import requests
from elements.urls import api

def Add_referral(referrer_id):
    url = f"{api}/api/referral/add/{referrer_id}/"

    response = requests.get(url=url)

    return response.status_code