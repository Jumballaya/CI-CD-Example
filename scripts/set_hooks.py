import os
import github


github_key = os.getenv("GITHUB_KEY")
aws_config = {
    "aws_key": os.getenv("AWS_KEY"),
    "aws_secret": os.getenv("AWS_SECRET"),
    "sns_topic": os.getenv("SNS_TOPIC"),
    "sns_region": "us-east-1",
}
g = github.Github(github_key)


def set_up():
    repo = None
    try:
        repo = g.get_user().get_repo(os.getenv("GITHUB_REPO"))
    except github.GithubException as e:
        print(e)
        return
    hooks = repo.get_hooks()
    sns_hook = 0
    for hook in hooks:
        if hook.name == 'amazonsns':
            sns_hook = hook
    if sns_hook == 0:
        return

    sns_hook.edit(
        "amazonsns",
        aws_config,
        add_events=['pull_request', 'pull_request_review_comment', 'commit_comment'],
    )



set_up()
