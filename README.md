# Uncovering the Reasons Behind COVID-19 Vaccine Hesitancy in Serbia: Sentiment-Based Topic Modeling

## Overview

This project implements the methodology from the study [Uncovering the Reasons Behind COVID-19 Vaccine Hesitancy in Serbia: Sentiment-Based Topic Modeling](https://pubmed.ncbi.nlm.nih.gov/36301673/). The goal is to analyze public sentiment towards COVID-19 vaccination in Serbia by classifying tweets and identifying underlying reasons for vaccine hesitancy using natural language processing (NLP) techniques.

## Methodology

The approach consists of the following steps:

1. **Data Collection**: Gathered two batches of tweets related to COVID-19 vaccination in Serbia.
2. **Data Annotation**:
   - First batch of 8,817 tweets manually annotated for relevance and sentiment (positive, negative, neutral).
   - Used this annotated data to train classifiers.
3. **Tweet Classification**:
   - **Relevance Classifier**: Identifies whether a tweet is relevant to COVID-19 vaccination.
   - **Sentiment Classifier**: Determines the sentiment polarity of relevant tweets.
4. **Topic Modeling**:
   - Applied Latent Dirichlet Allocation (LDA) and Non-negative Matrix Factorization (NMF) on tweets with negative sentiment to uncover main reasons for vaccine hesitancy.

## Results

- **Classifier Performance**:
  - Relevance Classifier F-scores: 0.91 (relevant), 0.96 (irrelevant).
  - Sentiment Classifier F-scores: 0.87 (negative), 0.85 (neutral), 0.85 (positive).

- **Identified Reasons for Vaccine Hesitancy**:
  1. Concerns over vaccine side effects.
  2. Doubts about vaccine effectiveness.
  3. Perception of insufficient testing.
  4. Mistrust in authorities.
  5. Belief in conspiracy theories.

## Repository Structure

- `data/`: Contains datasets used for training and evaluation.
- `notebooks/`: Jupyter notebooks demonstrating data processing and modeling steps.
- `models/`: Trained models for relevance and sentiment classification.
- `src/`: Source code for data preprocessing, model training, and evaluation.
- `README.md`: Project overview and instructions.





# COVID-19-vaccine-hesitancy-tweets
The repository contains a collection of tweets associated with vaccine hesitancy on Serbian Twitter. Tweet were collected by leveraging the Twitter search API filtered using keywords in Serbian. The collection is a combination of manually annotated negative tweets and automatically annotated negative tweets - 3286 in total. In line with Twitter's Terms of service, we provide only tweet IDs.
## How to Hydrate
### Hydrating using Twarc (CLI)

First install Twarc and tqdm

    pip3 install twarc
    pip3 install tqdm

Configure Twarc with your Twitter API tokens (note you must apply for a Twitter developer account first in order to obtain the needed tokens). You can also configure the API tokens in the script, if unable to configure through CLI.

    twarc2 configure
Run the script. The hydrated Tweets will be stored in the same folder as the Tweet-ID file, and is saved as a compressed jsonl file

    twarc2 hydrate ids.txt tweets.jsonl


### Hydrating using Tweepy:
    import tweepy
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, retry_count=5, retry_delay=2, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api.statuses_lookup(list_of_ids) #consider the limitations in tweepy documentation
