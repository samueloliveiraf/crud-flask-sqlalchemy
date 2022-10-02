from sqlalchemy import create_engine
from decouple import config
import requests


def test_connection_db():
    engine = create_engine(config('DATA_BASE_URL'))
    if engine.connect():
        return True
    else:
        return False


def test_route_insert():
    json_user = {'email': 'test', 'username': 'test'}
    url = 'http://localhost:5000/insert'

    retorne = requests.post(url, json=json_user)

    if retorne.status_code == 200:
        return True
    else:
        return False


def test_route_delete():
    json_user = {'id': 1}
    url = 'http://localhost:5000/delete'

    retorne = requests.post(url, json=json_user)

    if retorne.status_code == 200:
        return True
    elif retorne.status_code == 404:
        return True
    else:
        return False


def test_route_edit():
    json_user = {'id': 1, 'email': 'Annnaa', 'username': 'Annnsaa'}
    url = 'http://localhost:5000/edit'

    retorne = requests.post(url, json=json_user)

    if retorne.status_code == 200:
        return True
    elif retorne.status_code == 404:
        return True
    else:
        return False


def test_route_list():
    url = 'http://localhost:5000/list'

    retorne = requests.get(url)

    if retorne.status_code == 200:
        return True
    else:
        return False

