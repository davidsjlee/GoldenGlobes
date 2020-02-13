# function for extracting host names from twitter data
# data is a json file
# returns a list of strings (hosts)
import nltk 
from nltk.corpus import *
from nltk.tokenize import *

def extract(data):
    hosts = set() 
    relevant_words = ['host', 'hosts', 'hosted'] 
    relevantTweets = []

    #extend list of stop words (i.e. words that will NOT be returned by query)
    stop_words = nltk.corpus.stopwords.words("english")
    stop_words.extend(['goldenglobes', 'golden', 'globes', 'gg', 'http', 'goldenglobe', 'ceremony', 'rt', 'next', 'year', 'best'])
    stop_words = set(stop_words)


    bigrams = [] 
    filtered_words = []

    #capture all of the tweets with words relevant to hosting
    for obj in data:  
    	tweet = obj['text'].lower()
    	tweet_tokens = tweet.split()
    	for token in tweet_tokens:
    		if token in relevant_words:
    			word_list = re.findall(r"['a-zA-Z]+\b", tweet)
    			#if ('rt' not in word_list) and ('retweet' not in word_list):
    			for word in word_list:
    				if word not in stop_words:
    					filtered_words.append(word)

    bigrams.extend(nltk.bigrams(filtered_words))

    #for the specified year there were 2 hosts 
    freq_dist = nltk.FreqDist(bigrams)
    highest_freq = freq_dist.most_common(2)
    host_1 = highest_freq[0][0][0] + ' ' + highest_freq[0][0][1]
    host_2 = highest_freq[1][0][0] + ' ' + highest_freq[1][0][1]

    hosts.add(host_1)
    hosts.add(host_2)
    print("hosts:", hosts)
    return list(hosts)
