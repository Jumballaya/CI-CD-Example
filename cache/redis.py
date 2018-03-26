from redis import Redis




def write(key, val):
    r = Redis(host="github-test.gub2f2.0001.use1.cache.amazonaws.com", port=6379)
    return r.set(key, val)

def get(key):
    r = Redis(host="github-test.gub2f2.0001.use1.cache.amazonaws.com", port=6379)
    b = r.get(key)
    if b == None:
        return None
    return b.decode("utf-8")

def delete(key):
    r = Redis(host="github-test.gub2f2.0001.use1.cache.amazonaws.com", port=6379)
    return r.delete(key)
