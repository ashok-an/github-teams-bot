"""
[
    {
        "pr_number": 13559,
        "checks": [
            {
                "name": "XR Commit",
                "status": "failure"
            },
            {
                "name": "Check Locked Components",
                "status": "success"
            },
            ...
            ],
        "summary": "15 of 16 success"
    },

"""
import json

def get_json_data(file_path="data/pr-details.json"):
    with open(file_path, 'r') as fd:
        data = json.load(fd)
    return data


def get_pr(pr_number, pr_list):
    for pr in pr_list:
        if pr.get('pr_number', 12345) == pr_number:
            return pr
    else:
        return {}


def get_pr_details(pr_number):
    data = get_json_data()
    return get_pr(pr_number, data)
