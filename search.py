from googleapiclient.discovery import build
from tabulate import tabulate
import settings


def search_engine(args):
    resource = build('customsearch', 'v1', developerKey=settings.search_engine_api_key).cse()
    result = resource.list(q=args, cx=settings.search_engine_id).execute()
    search_result = result['items'][0:5]
    return search_result


def list_to_table(result_list):
    tabular_result = tabulate([[res['title'], res['link'], res['snippet']] for res in result_list],
                              headers=['title |', 'url |', 'snippet '])
    return tabular_result


def list_to_markdown(result_list):
    output = []
    for r in result_list:
        title = r['htmlTitle'].replace('<b>', '**').replace('</b>', '**')
        snippet = r['htmlSnippet'].replace('<b>', '**').replace('</b>', '**').replace('<br>', '')
        url = r['link']
        output.append({'title': title, 'snippet': snippet, 'url': url})

    return output


if __name__ == '__main__':
    import json
    query = 'rename a git branch'
    _results = search_engine(query)
    results = list_to_markdown(_results)
    print(results)

