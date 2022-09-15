#!/usr/bin/env python
# coding: utf-8

import re
import string
import unicodedata

# importing
import numpy as np
import pandas as pd
import requests
import spacy
from bs4 import BeautifulSoup

nlp = spacy.load('en_core_web_sm')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords


# parsing text from 8-ks

def get_soup(link):
    """
    function that returns soup object of a 8-k link
    """
    try:
        request = requests.get(link)
        soup = BeautifulSoup(request.content, 'html5lib', from_encoding='ascii')

    except:
        soup = 'na'

    return soup


# cleaning text by removing punctuation and stopwords, as well as lemmatization
punctuations = string.punctuation
sw = stopwords.words('english')


def clean_text(link):
    """
    function that generates a soup to process text and output sentiment scores
    """
    # empty list for sentiment data
    sentiment_list = np.empty(shape=0, dtype=object)

    # requesting the doc from link
    soup = get_soup(link)

    # extracting text from soup
    try:
        for section in soup.findAll('html'):

            try:
                # removing tables
                for table in section('table'):
                    table.decompose()

                # converting to unicode
                section = unicodedata.normalize('NFKD', section.text)
                section = section.replace('\t', ' ').replace('\n', '').replace('/s', '').replace('\'', '')

            except AttributeError:
                section = str(section.encode('utf-8'))

            # joining, removing unecessary characters, and truncating text
            text = ''.join(section)
            text = re.sub('\s+', ' ', text).strip()
            text = text[:40000]

            # creating spacy nlp variable to tokenize and remove punctuation
            doc = nlp(text)

            doc = [token.lemma_.lower().strip() for token in doc]
            doc = [token for token in doc if token.isalpha()]
            doc = [token for token in doc if token not in punctuations and token not in sw]

            # joining text and getting sentiment
            doc = ' '.join(doc)

            analyzer = SentimentIntensityAnalyzer()
            sentiment = analyzer.polarity_scores(doc)

    # output blank tokens and 0 sentiment for any link in case of error

    except:

        # outputs empty sentiment when no sentiment it present
        sentiment = np.ndarray({'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0})

    sentiment_list = np.append(sentiment_list, sentiment)

    # transposing each type of sentiment (pos, neg, neu) into separate features
    sentiment_df = pd.DataFrame({'sentiment': sentiment_list})

    return sentiment_df
