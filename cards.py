from pyadaptivecards.card import AdaptiveCard
from pyadaptivecards.inputs import Text, Number, Choices
from pyadaptivecards.components import TextBlock, Column, Fact
from pyadaptivecards.actions import Submit
from pyadaptivecards.options import Colors, HorizontalAlignment, Spacing
from pyadaptivecards.container import Container, ColumnSet, FactSet

import teams_sdk

###############################
## MENU card
###############################
def get_menu_card():
    greeting = TextBlock("Hi there, pick your action")

    choice_list = []
    choice_list.append({'title': 'List Pull requests', 'value': 'pr_list'})
    choice_list.append({'title': 'List code review requests', 'value': 'cr_list'})
    choice_list.append({'title': 'Fetch PR check status', 'value': 'pr_details'})
    choice_list.append({'title': 'Search for git/github issues', 'value': 'search'})
    choice_list.append({'title': 'Open support request', 'value': 'support'})
    menu = Choices(id='choice', separator=True,choices=choice_list)

    submit = Submit(title="Submit")

    return AdaptiveCard(body=[greeting, menu], actions=[submit])


###############################
## INPUT cards
###############################
def get_pr_list_input_card():
    greeting = TextBlock("Enter <user-id> for PR lookup")
    user_id = Text('pr_list.user_id', placeholder="...")
    submit = Submit(title="Search")

    return AdaptiveCard(body=[greeting, user_id], actions=[submit])


def get_cr_list_input_card():
    greeting = TextBlock("Enter <user-id> for PR reviewer lookup")
    user_id = Text('cr_list.user_id', placeholder="...")
    submit = Submit(title="Search")

    return AdaptiveCard(body=[greeting, user_id], actions=[submit])


def get_pr_details_input_card():
    greeting = TextBlock("Enter PR number")
    number = Number('pr_details.pr_number', placeholder='12345')
    submit = Submit(title="Fetch")

    return AdaptiveCard(body=[greeting, number], actions=[submit])


def get_search_input_card():
    greeting = TextBlock("Enter you search string w.r.to git/github")
    query = Text('query_string', placeholder="...")
    submit = Submit(title="Search")

    return AdaptiveCard(body=[greeting, query], actions=[submit])


def get_support_input_card():
    greeting1 = TextBlock("PR number (optional)")
    number = Number('support.pr_number', placeholder='12345')
    greeting2 = TextBlock("Issue details")
    query = Text('support.details', placeholder="...")
    submit = Submit(title="Submit")

    return AdaptiveCard(body=[greeting1, number, greeting2, query], actions=[submit])


###############################
## OUTPUT cards
###############################
def get_pr_list_output_card(userid, results):
    body = []
    body.append(TextBlock(f"Latest PRs for **{userid}**", isSubtle=True))
    
    repo = 'https://gh-xr.scm.engit.cisco.com/xr/iosxr'
    for r in results:
        pr_markdown = "[{n}]({r}/pull/{n})".format(n=r['number'], r=repo)
        number = Column([TextBlock(pr_markdown, weight='bold', horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='60px')
        title = Column([TextBlock(r['title'], weight='bold', horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='500px')

        state = Column([TextBlock(f"` {r['state']} `", horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='150px')
        head_markdown = "[{h}]({r}/tree/{h})".format(h=r['head'], r=repo)
        head = Column([TextBlock(head_markdown, weight='bold', horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='300px')
        arrow = Column([TextBlock('➔', color=Colors.ACCENT), ], separator=True, width='50px')
        base_markdown = "[{b}]({r}/tree/{b})".format(b=r['base'], r=repo)
        base = Column([TextBlock(base_markdown, weight='bold', horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='100px')

        container = Container([ColumnSet([number, title]), ColumnSet([state, head, arrow, base])], separator=True, spacing=Spacing.MEDIUM)
        body.append(container)

    return AdaptiveCard(body=body)


def get_cr_list_output_card(userid, results):
    body = []
    body.append(TextBlock(f"Code reviews assigned to **{userid}**", isSubtle=True))
    
    repo = 'https://gh-xr.scm.engit.cisco.com/xr/iosxr'
    for r in results:
        pr_markdown = "[{n}]({r}/pull/{n})".format(n=r['number'], r=repo)
        number = Column([TextBlock(pr_markdown, weight='bold', horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='100px')
        title = Column([TextBlock(r['title'], weight='bold', horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='500px')
        author = Column([TextBlock(f"` {r['author']} `", horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='150px')

        container = Container([ColumnSet([number, title, author]),], separator=True, spacing=Spacing.MEDIUM)
        body.append(container)

    return AdaptiveCard(body=body)

def get_pr_details_output_card(pr_number, results):
    body = []
    repo = 'https://gh-xr.scm.engit.cisco.com/xr/iosxr'
    if results:
        pr_markdown = "[{n}]({r}/pull/{n})".format(n=pr_number, r=repo)
        number = Column([TextBlock(pr_markdown, weight='bold', horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='60px')
        summary = Column([TextBlock(results['summary'], horizontalAlignment=HorizontalAlignment.LEFT), ], separator=True, width='500px')
        body.append(Container([ColumnSet([number, summary])]))

        facts = []
        for i in results["checks"]:
            name = i['name']
            if i["status"] == 'success':
                value = '✔'
            elif i["status"] == 'failure':
                value = '✘'
            else:
                value = f'`{i["status"]}`'
            facts.append(Fact(name, value))
        # for
        body.append(FactSet(facts))
    else:
        body.append(TextBlock(f'No details found for {pr_number}'))

    return AdaptiveCard(body=body)

def get_search_output_card(query, results):
    body = []
    body.append(TextBlock(f"Results for **{query}**", isSubtle=True))

    for r in results:
        url = "[{}]({})".format(r['title'], r['url'])
        body.append(TextBlock(url, weight='bold', color=Colors.ACCENT))
        body.append(TextBlock(r['snippet'], wrap=True, separator=True))
        body.append(TextBlock(''))

    return AdaptiveCard(body=body)


def get_support_output_card(query, results):
    pass


if __name__ == '__main__':
    import json
    import teams_sdk
    import search
    import sys
    user = sys.argv[1] if len(sys.argv) == 2 else 'nashok'

    import pr_details
    for i in [13559, 13524]:
        results = pr_details.get_pr_details(i)
        card = get_pr_details_output_card(i, results)
        #print(json.dumps(card.to_dict(), sort_keys=True, indent=4))
        teams_sdk.send_card_to_user(user, card)
    
