#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
from srtools import cyrillic_to_latin as c2l
from transformers import pipeline

# Load unannotated dataset
dataset = pd.read_excel('unannotated_tweets.xlsx')

# Keep only necessary columns
tweets = dataset[['text','id']]
tweets['id']=tweets['id'].apply(lambda xx: str(int(xx)))

# Preprocess text
def preprocess_texts(texts):
    texts = texts.apply(lambda xx:re.sub('http[\w://\.]+','',xx))            # remove URLs
    texts = texts.apply(lambda xx:re.sub('@\w+\s','',xx))                    # remove mentions
    texts = texts.apply(c2l)                                                 # transliterate from Cyrillic to Latin script
    texts = texts.apply(lambda xx:re.sub('[\U00002500-\U000EFFFF]','',xx))   # remove emojis and symbols
    texts = texts.apply(lambda xx:re.sub('#vojvodina','',xx))                # remove the most frequent hashtags in the dataset
    texts = texts.apply(lambda xx:re.sub('#COVID19','',xx))                  # remove the most frequent hashtags in the dataset
    texts = texts.apply(lambda xx:re.sub(r'\\n',' ',xx))                     # change newlines with spaces

    pattern = re.compile(r'(#)(\w+\b)')                                      # convert hashtags to plain words
    texts = texts.apply(lambda x: pattern.sub(r'\2', x))
    return texts

tweets['text'] = preprocess_texts(tweets['text'])

# INFERENCE WITH RELEVANCE CLASSIFIER
modelname_rel='./BERTICrelevants'
pipe_rel = pipeline("text-classification", model = modelname_rel)
relevance_predictions = pipe_rel(tweets['text'].to_list())

# KEEP ONLY RELEVANT TWEETS
mask=np.zeros(len(relevance_predictions),dtype=bool)
for index, piped in enumerate(relevance_predictions):
    if piped['label']=='LABEL_1':
        mask[index]=True
tweets=tweets[mask]

# INFERENCE WITH SENTIMENT CLASSIFIER ON RELEVANT TWEETS
modelname_sent = './BERTICsentiments'
pipe_sent =  pipeline("text-classification", model = modelname_sent)
sentiment_predictions = pipe_sent(tweets['text'].to_list())

# SAVING DATASETS
# Dataset with negative tweets
mask = np.zeros(len(sentiment_predictions),dtype=bool)
for index, piped in enumerate(sentiment_predictions):
    if piped['label']=='LABEL_0':
        mask[index]=True

tweets_neg = tweets[mask]
tweets_neg.to_csv(path_or_buf='negative_filtered.csv')

# Dataset with neutral tweets
mask = np.zeros(len(sentiment_predictions),dtype=bool)
for index, piped in enumerate(sentiment_predictions):
    if piped['label']=='LABEL_1':
        mask[index]=True

tweets_neutral = tweets[mask]
tweets_neutral.to_csv(path_or_buf='neutral_filtered.csv')

# Dataset with positive tweets
mask = np.zeros(len(sentiment_predictions),dtype=bool)
for index, piped in enumerate(sentiment_predictions):
    if piped['label']=='LABEL_2':
        mask[index]=True

tweets_pos = tweets[mask]
tweets_pos.to_csv(path_or_buf='positive_filtered.csv')




