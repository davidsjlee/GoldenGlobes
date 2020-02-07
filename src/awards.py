import string

# function for extracting award names from twitter data
# data is a json file
# returns a list of strings (awards)
def extract(data):
    # Code goes here
    raw_awards = {}

    # REDO APPROACH GIVEN CONSTRAINTS

    stop_words = ['drama', 'musical', 'television', 'film', 'picture']

    for obj in data:
        isAward = False
        to_add = 'best'

        # CLEAN
        tweet = obj['text'].lower()
        tweet.translate(str.maketrans('', '', string.punctuation))

        tweet_tokens = tweet.split()
        for token in tweet_tokens:
            if token == 'tv':
                token = 'television'

            if isAward:
                to_add += ' ' + token

            if token in stop_words:
                isAward = False
                if to_add in raw_awards:
                    raw_awards[to_add] += 1
                else:
                    raw_awards[to_add] = 1

            if not 'best' == token:
                continue
            else:
                isAward = True

    awards = []

    for award in raw_awards:
        if raw_awards[award] > 30 and len(award.split()) > 3:
            awards.append(award)

    return list(awards)
