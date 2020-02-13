import util.config
from util.load import read_data_from_file
import re

#helper functions
def get_names_generic(tweet):
    potential_names = set(re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',tweet))
    return potential_names

def get_people(tweet):
    people_names = read_data_from_file('data/', util.config.current_year, 'people')
    matches = []
    potential_names = set(re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',tweet))
    for n in potential_names:
        if n in people_names:
            matches.append(n)
    return matches

def get_movie(tweet):
    movie_list = read_data_from_file('data/', util.config.current_year, 'movie')
    for m in movie_list:
        if m in tweet:
            return m

def filter_tweets_for_award(tweets, award):
    award_filtered_tweets = []
    if 'television' in award:
        for tweet in tweets:
            if 'elevision' in tweet:
                award_filtered_tweets.append(tweet)
        return award_filtered_tweets
    if 'director' in award:
        for tweet in tweets:
            if 'director' in tweet:
                award_filtered_tweets.append(tweet)
        return award_filtered_tweets
    elif 'supporting' in award:
        for tweet in tweets:
            if 'upporting' in tweet:
                award_filtered_tweets.append(tweet)
        return award_filtered_tweets
    elif 'actress' in award:
        if 'comedy' in award:
            for tweet in tweets:
                if 'ctress' in tweet and 'comedy' in tweet:
                    award_filtered_tweets.append(tweet)
            return award_filtered_tweets
        elif 'drama' in award:
            for tweet in tweets:
                if 'ctress' in tweet and 'drama' in tweet:
                    award_filtered_tweets.append(tweet)
            return award_filtered_tweets
        else:
            return tweets
    elif 'actor' in award:
        if 'comedy' in award:
            for tweet in tweets:
                if 'ctor' in tweet and 'comedy' in tweet:
                    award_filtered_tweets.append(tweet)
            return award_filtered_tweets
        elif 'drama' in award:
            for tweet in tweets:
                if 'ctor' in tweet and 'drama' in tweet:
                    award_filtered_tweets.append(tweet)
            return award_filtered_tweets
        else:
            return tweets
    else:
        return tweets


# function for extracting nominee names from twitter data
# data is a json file
# returns a dictionary mapping string (award) to string (nominee)
def extract(data):
    # Code goes here
    nominee_pattern = '\swins\s|\swon\s|est\sperformance|est\smovie\s|est\sMovie|est\spicture|est\sPicture'
    #temporarily read data from clean file
    #will need to read from the data parameter instead
    tweets = read_data_from_file('data/', util.config.current_year, 'clean')
    nominees = {}
    filtered_tweets = []
    for tweet in tweets:
        if re.search(nominee_pattern, tweet):
            filtered_tweets.append(tweet)
    #print filtered_tweets
    for award in util.config.official_award_list:
        award_words = award.split()
        award_nominees = []
        #print award
        award_filtered_tweets = filter_tweets_for_award(tweets, award)
        for tweet in award_filtered_tweets:
            tweet_words = tweet.lower().split()
            if len(set(award_words).intersection(set(tweet_words))) >= 4:
                if 'television' in award:
                    generic_names = get_names_generic(tweet)
                    for n in generic_names:
                        if 'Best' not in n and 'Comedy' not in n:
                            award_nominees.append(n)
                elif 'screenplay' in award or 'original' in award:
                    #look in movies file
                    award_nominees.append(get_movie(tweet))
                elif 'upporting' in award or 'erformance' in award or 'ctor' in award or 'ctress' in award:
                    people_list = get_people(tweet)
                    for p in people_list:
                        award_nominees.append(p)
                else:
                    #look in movies file
                    award_nominees.append(get_movie(tweet))
        deduped_nominees = {i:award_nominees.count(i) for i in award_nominees}
        #print deduped_nominees
        max = 0
        maxkey = ''
        for key,value in deduped_nominees.items():
            if value > max and key != None:
                max = value
                maxkey = key
        nominees[award] = maxkey
    return nominees
