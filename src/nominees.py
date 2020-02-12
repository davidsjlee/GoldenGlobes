import string
from math import inf
from nltk.metrics.distance import edit_distance
from nltk.corpus import stopwords

# function for extracting nominee names from twitter data
# data is a json file and awards is a list of actual awards
# returns a dictionary mapping string (award) to list of strings (nominees)
def extract(data, awards):
    # Code goes here

    # initialize set of keys using the hardcode awardslist
    raw_nominees = {a : {} for a in awards}

    pre_verbs = stopwords.words('english')
    verbs = ['nominated', 'chosen', 'picked', 'considered']

    for obj in data:
        person_name = ''
        award_name = ''

        # CLEAN
        tweet = obj['text'].lower()
        exclude = set(string.punctuation)
        tweet = ''.join(ch for ch in tweet if ch not in exclude)

        tweet_tokens = tweet.split()
        j = 0
        k = 0

        verb_found = False
        for i, token in enumerate(tweet_tokens):
            if token in verbs:
                j = i # person name search
                k = i # award name search
                verb_found = True

        if not verb_found:
            continue

        else:
            person_name_size = 0

            while person_name_size != 2 and j > 0:
                j -= 1
                if tweet_tokens[j] in pre_verbs:
                    continue
                else:
                    # grab person name first and last
                    person_name = tweet_tokens[j] + ' ' + person_name
                    person_name_size += 1

            if person_name_size != 2:
                continue
            else:
                person_name.lstrip()

            while k < len(tweet_tokens) - 1:
                k += 1
                if tweet_tokens[k] != 'best':
                    continue
                else:
                    # may need to account for end of sentences
                    for t in tweet_tokens[k:len(tweet_tokens)]:
                        award_name = award_name + ' ' + t
                        k = len(tweet_tokens) - 1


            if len(award_name.split()) <= 3:
                continue
            else:
                award_name.lstrip()

            # levenstein distances for awards to award_name
            max_dist = inf
            true_award = ''

            for ta in awards:
                dist = edit_distance(award_name, ta)
                if max_dist > dist:
                    true_award = ta
                    max_dist = dist

            if person_name in raw_nominees[true_award]:
                raw_nominees[true_award][person_name] += 1
            else:
                raw_nominees[true_award][person_name] = 1

    nominees = {a : [] for a in awards}

    for a in raw_nominees:
        for p in raw_nominees[a]:
            if raw_nominees[a][p] > 0:
                nominees[a].append(p)

    return nominees
