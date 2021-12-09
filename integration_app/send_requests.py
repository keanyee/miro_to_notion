import requests
import json


def get(url, headers):
    response = requests.get(url, headers=headers)
    return response


def post(url, headers, data=None):
    if data:
        return requests.post(url, headers=headers, data=json.dumps(data))
    return requests.post(url, headers=headers)


def patch(url, headers, data):
    return requests.patch(url, headers=headers, data=json.dumps(data))
