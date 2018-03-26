from stack import make_stack, remove_stack
from gh import pull_request as pr
from name import generate
from cache import redis


# Pull Request action
# @param {integer} pr_num - pull request number
def pull_request(pr_num, commit):
    # 1. Save the pull request number
    cached = redis.get(pr_num)

    # 2. If the instance is already registered, skip it
    if cached != None:
        return

    # 3. Make the server's name
    name = generate.random_name()

    # 4. Create server
    make_stack.init(name, commit)

    # 5. Write to the Redis server
    redis.write(pr_num, name)

    # 6. Comment on github
    pr.comment(pr_num, '@jumballaya -- [server is ready for QA](http://'+ name +'.pburris.me)')

    print(pr_num, name)


# Close Request action
# @param {integer} pr_num - pull request number
def close_request(pr_num):
    # 1. Get the server name
    name = redis.get(pr_num)

    # 2. Shutdown servers
    remove_stack.init(name)

    # 3. Delete the entry from redis
    redis.delete(pr_num)

    print(pr_num, name)
