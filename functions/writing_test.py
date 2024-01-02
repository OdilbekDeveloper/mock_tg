import requests
from elements.urls import api


def get_essays_unchecked(id):
    url = f"{api}/api/essays/get/unchecked/{id}/"

    response = requests.get(url)

    print(response.text)
    print(response.status_code)
    return response


def get_users_writing_unchecked():
    url = f"{api}/api/users/get/writing/unchecked"

    response = requests.get(url)

    return response


def create_writing(band_score, comment, section1_id, section2_id, userid, answer1_id, answer2_id):
    post_url = f'{api}/api/writing_test/create/{userid}/{section1_id}/{section2_id}/{answer1_id}/{answer2_id}/'

    payload_data = {
        'comment': comment,
        'band_score': band_score,
    }

    response = requests.post(post_url, data=payload_data)
    print(response)
    if response.status_code == 201:
        return True
    else:
        return False