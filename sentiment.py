"""
Author: Shubham Bhatnagar
Date Created: 01/05/2020

Purpose: Sentiment analysis on tweets obtained about covid
- Following this:
    https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
"""

#%% Imports

import random
import re
import string
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

from nltk import FreqDist

from nltk import classify
from nltk import NaiveBayesClassifier


#%% Function defintions


# Defining script to read in tweets from Twint.py
def read_tweets(country):
    with open(r'./Tweets/tweets_{}.txt'.format(country), 'rb') as f:
        lines = str(f.read())
    lines = [l.replace('\\n', '') for l in lines.split('-----Line of Text------------')]

    return lines


# Removing Noise from Data

# Adding some more words to stop_list:
def remove_noise(tweet_tokens, stop_words =()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        # removing any https tags
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)

        # Removing any twitter handles
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        # Removing an emoji unicode characters
        token = re.sub("\\\\x..","",token)

        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

           
    return cleaned_tokens


#%% Main script

# Reading tweets created using Twint.py
country = 'us'
data_tweets = read_tweets(country)

# Working with the sample tweets
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')

# =============================================================================
# Tokenizing all tweets
# =============================================================================

positive_tweets_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tweets_tokens = twitter_samples.tokenized('negative_tweets.json')
data_tweets_tokens = [word_tokenize(x) for x in data_tweets]

# =============================================================================
# Normalizing tweets
# =============================================================================

# Adding more random words that need to be removed
most_common = ['covid','covid-19','covid_19','coronavirus','{}'.format(country),'http','...','people','state']
stop_words = stop_words + most_common


positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []
data_cleaned_tokens_list = []

for tokens in positive_tweets_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in negative_tweets_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in data_tweets_tokens:
    data_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

# =============================================================================
# Determining Word Density
# =============================================================================

# Writing a function to get all possible words in tweets

# Using a generator function for memory purposes
def get_all_words(cleaned_tokens_list):
    
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

all_pos_words = get_all_words(data_cleaned_tokens_list)
freq_dist_pos = FreqDist(all_pos_words)

# =============================================================================
# Machine Learning Model: Naive Bayes Classifier (positive, negative classes)
# =============================================================================

# Generator function to yield dictionary with key=token, value= True
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)
data_tokens_for_test = get_tweets_for_model(data_cleaned_tokens_list)


# Splitting dataset for training and test 

positive_dataset = [(tweet_dict, "Positive")
                    for tweet_dict in positive_tokens_for_model]

negative_dataset = [(tweet_dict, "Negative")
                    for tweet_dict in negative_tokens_for_model]


dataset = positive_dataset + negative_dataset

random.shuffle(dataset)

train_data = dataset[:7000]
test_data = dataset[7000:]

classifier = NaiveBayesClassifier.train(train_data)


# Testing with country data
import ipdb; ipdb.set_trace()
classified_tweets = []
for tweet in data_tokens_for_test:
    classified_tweets.append(classifier.classify(dict([token, True] for token in tweet)))
    
for i in range(10):
    print('Tweet: ', data_tweets[i])
    print('Class: ', classified_tweets[i])
    print('\n')

