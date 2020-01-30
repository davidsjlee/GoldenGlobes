# function for extracting award names from twitter data
# data is a json file
# returns a list of strings (awards)
def extract(data):
    # Code goes here
    awards = set()

    # naive approach - identify relation words
    # completeness = 0.04768292682926829
    # spelling = 0.8283969243244079
    # consider for 2013 subset, ggtest.json
    stop_words = ['drama', 'musical', 'comedy', 'television', 'film', 'picture']

    for obj in data:
        isAward = False
        to_add = 'best'
        tweet = obj['text'].lower()
        tweet_tokens = tweet.split()
        for token in tweet_tokens:
            if isAward:
                to_add += ' ' + token

            if token in stop_words:
                isAward = False
                awards.add(to_add)

            if not 'best' == token:
                continue
            else:
                isAward = True


    return list(awards)
