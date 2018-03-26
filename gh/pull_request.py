import github
import os

key = os.getenv("GITHUB_KEY")
g = github.Github(key)


def comment(pr_id, text):
    repo = None
    try:
        repo = g.get_user().get_repo(os.getenv("GITHUB_REPO"))
    except github.GithubException as e:
        print(e)
        return

    pull = repo.get_pull(pr_id)
    pull.create_issue_comment(text)
