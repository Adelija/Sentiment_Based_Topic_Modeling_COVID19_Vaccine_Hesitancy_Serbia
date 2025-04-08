# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:06:12 2022

@author: adela
"""
# PREUZETO SA https://stackoverflow.com/questions/32313062/what-is-the-best-way-to-obtain-the-optimal-number-of-topics-for-a-lda-model-usin
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from gensim.models import LdaModel, CoherenceModel
from gensim import corpora
import pandas as pd
import re 
import string


if __name__ == "__main__": 
    data=pd.read_csv('datasets/CeoSkup_normalizovan_za_BTM.csv')
    def words(text):
        dodatne_stop_reci=['ss','tj','moći','niti','ali','što','imati','znati','hteti','ako','ni','niti','ne','koji','kada','biti','ko','pre','itd', 'ma','bre','jel','korona','kovid','covid','čov','kov','cov','corona','coron','niko','ništa','nigde','moj','tvoj','naš','vaš','sad','neko','vakcina','vakcinisati','vakcinacija','vak','vakcinisanje','među','protiv','zašto','sebe','sem','pošto','on','npr','nešto','neka','neki','hajde','haha']
        regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
        text = regex.sub(" ", text.lower())
        words = text.split(" ")
        words = [re.sub('\S*@\S*\s?', '', sent) for sent in words]
        words = [re.sub('\s+', ' ', sent) for sent in words]
        words = [re.sub("\'", "", sent) for sent in words]
        words = [w for w in words if not len(w) < 2]
        words = [w for w in words if not w in dodatne_stop_reci]
        return words

    corpus= [words(x) for x in data['Leme']]

    dirichlet_dict = corpora.Dictionary(corpus)
    dirichlet_dict.filter_extremes(
    no_below=3,
    no_above=0.85
    #keep_n=1000
)
    bow_corpus = [dirichlet_dict.doc2bow(text) for text in corpus]
    
    # Considering 1-15 topi cs, as the last is cut off
    num_topics = list(range(16)[1:])
    num_keywords = 15
    
    LDA_models = {}
    LDA_topics = {}
    for i in num_topics:
        LDA_models[i] = LdaModel(corpus=bow_corpus,
                                 id2word=dirichlet_dict,
                                 num_topics=i,
                                 update_every=1,
                                 chunksize=len(bow_corpus),
                                 passes=20,
                                 alpha='auto',
                                 random_state=42)
        
        shown_topics = LDA_models[i].show_topics(num_topics=i, 
                                                 num_words=num_keywords,
                                                 formatted=False)
        LDA_topics[i] = [[word[0] for word in topic[1]] for topic in shown_topics]
        
    def jaccard_similarity(topic_1, topic_2):
        """
        Derives the Jaccard similarity of two topics
                
        Jaccard similarity:
            - A statistic used for comparing the similarity and diversity of sample sets
            - J(A,B) = (A ∩ B)/(A ∪ B)
            - Goal is low Jaccard scores for coverage of the diverse elements
            """
        intersection = set(topic_1).intersection(set(topic_2))
        union = set(topic_1).union(set(topic_2))
                        
        return float(len(intersection))/float(len(union))

        

        
    LDA_stability = {} 
    for i in range(0, len(num_topics)-1):
        jaccard_sims = []
        for t1, topic1 in enumerate(LDA_topics[num_topics[i]]): # pylint: disable=unused-variable
            sims = []
            for t2, topic2 in enumerate(LDA_topics[num_topics[i+1]]): # pylint: disable=unused-variable
                sims.append(jaccard_similarity(topic1, topic2))    
                
            jaccard_sims.append(sims)    
                
        LDA_stability[num_topics[i]] = jaccard_sims
                    
    mean_stabilities = [np.array(LDA_stability[i]).mean() for i in num_topics[:-1]]
                
    coherences = [CoherenceModel(model=LDA_models[i], texts=corpus, dictionary=dirichlet_dict, coherence='c_v').get_coherence()\
                              for i in num_topics[:-1]]
                    
    coh_sta_diffs = [coherences[i] - mean_stabilities[i] for i in range(num_keywords)[:-1]] # limit topic numbers to the number of keywords
    coh_sta_max = max(coh_sta_diffs)
    coh_sta_max_idxs = [i for i, j in enumerate(coh_sta_diffs) if j == coh_sta_max]
    ideal_topic_num_index = coh_sta_max_idxs[0] # choose less topics in case there's more than one max
    ideal_topic_num = num_topics[ideal_topic_num_index]
                    
                    #Finally graph these metrics across the topic numbers:
                        
                        
    plt.figure(figsize=(20,10))
    ax = sns.lineplot(x=num_topics[:-1], y=mean_stabilities, label='Average Topic Overlap')
    ax = sns.lineplot(x=num_topics[:-1], y=coherences, label='Topic Coherence')
                        
    ax.axvline(x=ideal_topic_num, label='Ideal Number of Topics', color='red')
    ax.axvspan(xmin=ideal_topic_num - 1, xmax=ideal_topic_num + 1, alpha=0.5, facecolor='grey')
                        
    y_max = max(max(mean_stabilities), max(coherences)) + (0.10 * max(max(mean_stabilities), max(coherences)))
    ax.set_ylim([0, y_max]) # za u_mass koherence podesiti na -14 a za c_v na -
    ax.set_xlim([1, num_topics[-1]-1])
                        
    ax.axes.set_title('Model Metrics per Number of Topics', fontsize=25)
    ax.set_ylabel('Metric Level', fontsize=20)
    ax.set_xlabel('Number of Topics', fontsize=20)
    plt.legend(fontsize=20)
    plt.show()   
                        