import json
from stack import actions



def hello(event, context):
    response = {"statusCode": 200, "body": json.dumps({})}
    message = json.loads(event['Records'][0]['Sns']['Message'])

    print(message)

    if message['action'] == 'opened':
        pr_num = message['number']
        commit = message['pull_request']['head']['sha']
        actions.pull_request(pr_num, commit)
    elif message['action'] == 'closed':
        pr_num = message['number']
        actions.close_request(pr_num)
    else:
        print(message)

    return response
