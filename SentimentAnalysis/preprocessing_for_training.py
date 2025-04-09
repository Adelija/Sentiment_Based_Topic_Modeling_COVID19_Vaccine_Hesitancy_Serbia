#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
from srtools import cyrillic_to_latin as c2l

# Load annotated dataset
dataset = pd.read_excel('annotated_tweets.xlsx', dtype={'id':str})

# Keep only necessary columns
tweets = dataset[['text', 'label', 'id']]
tweets = tweets[tweets['label'].notna()]
tweets = tweets[tweets['text'].notna()]

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

# Create binary relevance labels for relevance classifier:
# Label 1 → relevant tweet (has sentiment annotation)
# Label 0 → not relevant tweet annotated with label 10
df_relevance_classifier = tweets.copy(deep=True)
df_relevance_classifier['label'] = df_relevance_classifier['label'].replace([0, 1, 2], 1)
df_relevance_classifier['label'] = df_relevance_classifier['label'].replace([10], 0)

# Filtering tweets with valid sentiment labels (0–2) for sentiment classifier
df_sentiment_classifier = tweets[(tweets['label']>=0) & (tweets['label']<=2)]

# Ensure labels are integers
df_sentiment_classifier['label'] = df_sentiment_classifier['label'].astype(int)
df_relevance_classifier['label'] = df_relevance_classifier['label'].astype(int)

# Save processed datasets
df_relevance_classifier.reset_index(drop=True).to_pickle('./relevants_annotated.pickle')
df_sentiment_classifier.reset_index(drop=True).to_pickle('./sentiments_annotated.pickle')

