import util.config
from util.load import read_data_from_file
from math import inf
from nltk.metrics import edit_distance
import string
import re


# #helper functions
# def get_names_generic(tweet):
#     potential_names = set(re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',tweet))
#     return potential_names
#
# def get_people(tweet):
#     people_names = read_data_from_file('data/', util.config.current_year, 'people')
#     matches = []
#     potential_names = set(re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',tweet))
#     for n in potential_names:
#         if n in people_names:
#             matches.append(n)
#     return matches
#
# def get_movie(tweet):
#     movie_list = read_data_from_file('data/', util.config.current_year, 'movie')
#     for m in movie_list:
#         if m in tweet:
#             return m
#
# def filter_tweets_for_award(tweets, award):
#     award_filtered_tweets = []
#     if 'television' in award:
#         for tweet in tweets:
#             if 'elevision' in tweet:
#                 award_filtered_tweets.append(tweet)
#         return award_filtered_tweets
#     if 'director' in award:
#         for tweet in tweets:
#             if 'director' in tweet:
#                 award_filtered_tweets.append(tweet)
#         return award_filtered_tweets
#     elif 'supporting' in award:
#         for tweet in tweets:
#             if 'upporting' in tweet:
#                 award_filtered_tweets.append(tweet)
#         return award_filtered_tweets
#     elif 'actress' in award:
#         if 'comedy' in award:
#             for tweet in tweets:
#                 if 'ctress' in tweet and 'comedy' in tweet:
#                     award_filtered_tweets.append(tweet)
#             return award_filtered_tweets
#         elif 'drama' in award:
#             for tweet in tweets:
#                 if 'ctress' in tweet and 'drama' in tweet:
#                     award_filtered_tweets.append(tweet)
#             return award_filtered_tweets
#         else:
#             return tweets
#     elif 'actor' in award:
#         if 'comedy' in award:
#             for tweet in tweets:
#                 if 'ctor' in tweet and 'comedy' in tweet:
#                     award_filtered_tweets.append(tweet)
#             return award_filtered_tweets
#         elif 'drama' in award:
#             for tweet in tweets:
#                 if 'ctor' in tweet and 'drama' in tweet:
#                     award_filtered_tweets.append(tweet)
#             return award_filtered_tweets
#         else:
#             return tweets
#     else:
#         return tweets
#
#
# # function for extracting winner names from twitter data
# # data is a json file
# # returns a dictionary mapping string (award) to string (winner)
# def extract(data):
#     # Code goes here
#     presenter_pattern = '\spresented\s|\spresents\s'
#     #temporarily read data from clean file
#     #will need to read from the data parameter instead
#     tweets = read_data_from_file('data/', util.config.current_year, 'clean')
#     presenters = {}
#     filtered_tweets = []
#     for tweet in tweets:
#         if re.search(presenter_pattern, tweet):
#             filtered_tweets.append(tweet)
#     #print filtered_tweets
#     for award in util.config.official_award_list:
#         award_words = award.split()
#         award_presenters = []
#         #print award
#         award_filtered_tweets = filter_tweets_for_award(tweets, award)
#         for tweet in award_filtered_tweets:
#             tweet_words = tweet.lower().split()
#             if len(set(award_words).intersection(set(tweet_words))) >= 4:
#                 if 'television' in award:
#                     generic_names = get_names_generic(tweet)
#                     for n in generic_names:
#                         if 'Best' not in n and 'Comedy' not in n:
#                             award_presenters.append(n)
#                 elif 'upporting' in award or 'erformance' in award or 'ctor' in award or 'ctress' in award:
#                     people_list = get_people(tweet)
#                     for p in people_list:
#                         award_presenters.append(p)
#                 else:
#                     #look in movies file
#                     award_presenters.append(get_movie(tweet))
#         deduped_presenters = {i:award_presenters.count(i) for i in award_presenters}
#         thr = sum(deduped_presenters.values()) * (9 / 10) / len(deduped_presenters)
#         pot_pres = []
#         for key,value in deduped_presenters.items():
#             if value > thr and key != None:
#                 pot_pres.append(key)
#         presenters[award] = pot_pres
#     return presenters

def extract(data):
    # initialize set of keys using the hardcode awardslist
    raw_presenters = {a : {} for a in util.config.official_award_list}
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

            for ta in util.config.official_award_list:
                dist = edit_distance(award_name, ta)
                if max_dist > dist:
                    true_award = ta
                    max_dist = dist

            if person_name in raw_presenters[true_award]:
                raw_presenters[true_award][person_name] += 1
            else:
                raw_presenters[true_award][person_name] = 1

    presenters = {a : [] for a in util.config.official_award_list}

    for a in raw_presenters:
        for p in raw_presenters[a]:
            if raw_presenters[a][p] > 0:
                presenters[a].append(p)

    return presenters
