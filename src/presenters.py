import string
from math import inf
from nltk import pos_tag
from nltk.metrics.distance import edit_distance
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# function for extracting presenter names from twitter data
# data is a json file
# returns dictionary mapping string (award) to list of strings (presenters)
def extract(data, awards):
    # Code goes here

    # initialize set of keys using the hardcode awardslist
    raw_presenters = {a : {} for a in awards}

    stop_words = stopwords.words('english')
    verbs = ['presented', 'presents', 'present']

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
                # grab person name first and last
                person_name = tweet_tokens[j] + ' ' + person_name
                person_name_size += 1

            if person_name_size != 2:
                continue
            else:
                person_name.rstrip()

            while k < len(tweet_tokens) - 1:
                k += 1
                if tweet_tokens[k] != 'best':
                    continue
                else:
                    # account for end of sentences
                    for t in tweet_tokens[k:len(tweet_tokens)]:
                        if t == '.':
                            break
                        else:
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

            if person_name in raw_presenters[true_award]:
                raw_presenters[true_award][person_name] += 1
            else:
                raw_presenters[true_award][person_name] = 1

    presenters = {a : [] for a in awards}

    for a in raw_presenters:
        for p in raw_presenters[a]:
            if raw_presenters[a][p] > 0:
                presenters[a].append(p)

    return presenters
