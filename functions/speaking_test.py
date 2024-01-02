import requests
from elements.urls import api
import json

def create_speakingtest(userid, comment, audio, band_score):
    post_url = f'{api}/api/speakingtest/create/{userid}/'

    payload_data = {
        'comment': comment,
        'band_score': band_score,
    }

    response = requests.post(post_url, data=payload_data, files={'audio': audio})

    print(response.status_code)
    return response


def question_speaking(part):
    url = f'{api}/api/speaking_section/{part}/'
    
    response = requests.get(url)

    res_data = json.loads(response.text)

    img_url = f"{api}{res_data['img']}"

    

    return img_url