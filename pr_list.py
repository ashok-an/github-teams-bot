def load_pr_data(data_file='data/pr-list-data.csv'):
    with open(data_file, 'r') as fd:
        data = fd.readlines()
    data = [ i.strip() for i in data if data ]
    data.reverse() # we want latest PR first
    return data


# 12501,anjanagr,main,CSCvx08886.main.hidden_cmd_issu,open,2021-02-25 15:56:00,CSCvx08886 Remove test client cmd
def process_pr_data(raw_data):
    output = []
    for i in raw_data:
        tokens = i.split(',')
        if len(tokens) > 6:
            _dict = {}
            for f in ['number', 'userid', 'base', 'head', 'state', 'created', 'title']:
                _dict[f] = tokens.pop(0)
            _dict['title'] = _dict['title'] if len(_dict['title']) < 40 else _dict['title'][:39] + '...'
            output.append(_dict)

    return output


raw_data = load_pr_data()


def get_pr_list(userid):
    pr_data = process_pr_data(raw_data)
    output = [ i for i in pr_data if i['userid'] == userid ]
    return output[:9]
