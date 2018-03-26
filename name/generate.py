from random import randint


def get_noun():
    noun = ''
    noun_count = randint(1, 500)
    with open("name/nouns.txt") as f:
        count = 1
        for line in f:
            word = line.replace("\n", "")
            if count == noun_count:
                noun = word
                break
            count += 1
    return noun

def get_adj():
    adj = ''
    adj_count = randint(1, 500)
    with open("name/adjectives.txt") as f:
        count = 1
        for line in f:
            word = line.replace("\n", "")
            if count == adj_count:
                adj = word
                break
            count += 1
    return adj


def random_name():
    noun = get_noun()
    adjective = get_adj()
    qa_num = str(randint(1, 9999))

    return adjective+"-"+noun+".qa"+qa_num

