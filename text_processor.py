## to use properly, have file saved in same directory as notebook running
## run this line of code in other notebook: from text_processor import load_and_clean_model
## load_and_clean_model has 1 argument, file_path, which is the path for the csv file of unprocessed
## scraped jobs

import re
import numpy as np
import pandas as pd

import nltk
import spacy
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from textblob import Word
from wordcloud import WordCloud

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# First processing the words by tokenizing and reassembling to improve overall preprocessing and deletion of stop words

def tokenize_and_reassemble(text):
     sentences = nltk.sent_tokenize(text)
     filtered_text = ''
     for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        filtered_sent = ' '.join(words)
        filtered_text += filtered_sent + ' '
     return(filtered_text)

# The inital preprocessing largely deals with syntax 
# (all lowercases, no unecessary spaces, no digits, no new lines, no stop words) and lemmatizing

def init_preprocess_text(text):
    # change all the text to lowercase 
    text = text.lower()
    
    # deleting all tabs, spaces, and new lines
    text = re.sub(r'\s+', ' ', text)
    
    # deleting digits
    text = re.sub(r'\d+', '', text)
    
    # delete stop words
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    text = ' '.join(filtered_words)
    
    # lemmatize text
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    lem_words = [lemmatizer.lemmatize(word) for word in words]
    text = ' '.join(lem_words)
    
    return text

programming_languages = ["python", "java", "c++","c#", "javascript", "php",
                         "swift", "kotlin", "ruby","go", "rust", "typescript",
                         "scala", "lua", "perl","objective-c", "swift","dart",
                         "clojure", "groovy","F#","haskell", "erlang", "r", "julia", 'node.js']

databases = ["MySQL", "Oracle", "Microsoft SQL Server","PostgreSQL", "MongoDB", "Redis",
             "Cassandra", "Elasticsearch", "SQLite","Neo4j", "MariaDB", "Couchbase",
             "Amazon Web Services (AWS) Relational Database Service (RDS)",
             "Google Cloud SQL", "Azure SQL Database", "Firebase Realtime Database",
             "Apache HBase", "Apache Cassandra","Amazon DynamoDB", "Memcached", "CouchDB"]

cloud_platforms_dist = ["Amazon Web Services", "Microsoft Azure", "Google Cloud Platform (GCP)","IBM Cloud", 
                        "Oracle Cloud", "Salesforce Platform","Heroku", "DigitalOcean", "Rackspace","VMware", 
                        "OpenStack", "Kubernetes","Docker Swarm","Apache Hadoop", "Apache Spark","Apache Flink", 
                        "Apache Kafka", "Apache Mesos","Apache Storm", "Redis Cluster", "Cassandra","Elasticsearch", "Zookeeper"]

def get_relevancy_of_words(sample):
    vectorizer = TfidfVectorizer()

    # fit_transform the document and the words to check into their respective TF-IDF vectors
    document_vector = vectorizer.fit_transform([sample])
    pl_words_vector = vectorizer.transform(programming_languages)
    db_words_vector = vectorizer.transform(databases)
    cc_words_vector = vectorizer.transform(cloud_platforms_dist)


    # calculating cosine similarity between the document and the word vectors
    pl_sim_scores = cosine_similarity(document_vector, pl_words_vector)
    db_sim_scores = cosine_similarity(document_vector, db_words_vector)
    cc_sim_scores = cosine_similarity(document_vector, cc_words_vector)

    # output the similarity scores
    rel_languages = []
    rel_databases = []
    rel_cloud_dist = []

    for i, word in enumerate(programming_languages):
        if pl_sim_scores[0][i] > 0:
            rel_languages += [word]
    
    for i, word in enumerate(databases):
        if db_sim_scores[0][i] > 0:
            rel_databases += [word]

    for i, word in enumerate(cloud_platforms_dist):
        if cc_sim_scores[0][i] > 0:
            rel_cloud_dist += [word]


    return(rel_languages, rel_databases, rel_cloud_dist)

# determines top 5 bigrams from job description 
def get_top_bigrams(text):
    words = nltk.word_tokenize(text)

    # create a bigram finder object
    bigram_finder = BigramCollocationFinder.from_words(words)

    # apply a frequency filter to remove rare bigrams
    bigram_finder.apply_freq_filter(2)

    # use the PMI measure to score bigrams
    bigram_measures = BigramAssocMeasures()
    scored_bigrams = bigram_finder.score_ngrams(bigram_measures.pmi)
    sorted_bigrams = sorted(scored_bigrams, key=lambda x: x[1], reverse=True)
    
    # creat list for the bigrams, top_bigrams
    top_bigrams = [bigram[0] for bigram in sorted_bigrams[:5]]
    return top_bigrams

def load_and_clean_model(file_path):
    test = pd.read_csv(file_path).dropna()
    test.columns = ['Job_ID','Location','Title', 'Company','Date', 'Link', 'Description']

    # tokenizing job descriptions then reassembling
    test['Description'] = test['Description'].apply(tokenize_and_reassemble)
    
    # applying inital preprocessing function to data and swapping clean data into original test dataframe
    test['Description'] = test['Description'].apply(init_preprocess_text)

    # creating a new column within the test dataframe that houses the results from iterating the function, get_relevancy_of_words(), over each row element
    # Each element in test['Programming Languages] will be list within list of programming languages found and their similarity score

    proglang = [get_relevancy_of_words(test['Description'].iloc[i])[0] for i,x in enumerate(test['Description'])]
    db = [get_relevancy_of_words(test['Description'].iloc[i])[1] for i,x in enumerate(test['Description'])]
    cloud = [get_relevancy_of_words(test['Description'].iloc[i])[2] for i,x in enumerate(test['Description'])]

    test['Programming Languages'] = proglang
    test['Databases'] = db
    test['Cloud and or Distributed Computing Platforms'] = cloud
    
    # determining top 5 bigrams per review and creating column, bigrams, to house lists
    test['bigrams'] = test['Description'].apply(get_top_bigrams)

    return(test)