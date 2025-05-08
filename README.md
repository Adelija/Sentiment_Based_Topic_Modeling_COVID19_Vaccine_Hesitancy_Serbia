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

## Repository Structure

- `SentimentAnalysis/`: Scripts for preprocessing, training, and evaluating relevance and sentiment classifiers.
- `TopicModeling/`: Scripts and notebooks for coherence evaluation and topic modeling using LDA/NMF.
- `ids_tweet/`: Tweet IDs related to vaccine hesitancy, used for hydration.
- `README.md`: Project overview and instructions.

## How to Hydrate Tweets

### Hydrating using Twarc (CLI)

First install Twarc and tqdm:

```bash
pip3 install twarc
pip3 install tqdm
```

Configure Twarc with your Twitter API tokens (you must apply for a Twitter developer account first):

```bash
twarc2 configure
```

Run the script. The hydrated Tweets will be stored in the same folder as the Tweet-ID file, saved as a compressed JSONL file:

```bash
twarc2 hydrate ids.txt tweets.jsonl
```

### Hydrating using Tweepy (Python)

```python
import tweepy

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, retry_count=5, retry_delay=2, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
api.statuses_lookup(list_of_ids)  # Consider limitations in Tweepy documentation
```

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

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/vaccine-hesitancy-serbia.git
   cd vaccine-hesitancy-serbia
   ```

2. **Set up the environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the analysis**:
   - Use the notebooks in the appropriate folders to follow the data processing and modeling steps.

## Citation

If you use this work, please cite the original paper:

> Ljajić A, Prodanović N, Medvecki D, Bašaragin B, Mitrović J. Uncovering the Reasons Behind COVID-19 Vaccine Hesitancy in Serbia: Sentiment-Based Topic Modeling. J Med Internet Res. 2022 Nov 17;24(11):e42261. doi: 10.2196/42261.
