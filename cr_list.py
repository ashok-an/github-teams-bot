"""
{
  "abkannan": {
    "number": 8479,
    "author": "mlinga",
    "title": "Mlinga sfe lindt"
  },
"""
import json

def get_json_data(file_path="data/cr-list.json"):
    with open(file_path, 'r') as fd:
        data = json.load(fd)
    return data


def get_cr_list(userid):
    data = get_json_data()
    result = data.get(userid, {})
    return [result, ] if result else []
