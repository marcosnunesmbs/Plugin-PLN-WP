from ctypes import sizeof
import spacy
import pandas as pd
import requests
from src.utils.sanitizer import sanitizer
from spacy.lang.pt.stop_words import STOP_WORDS
from bs4 import BeautifulSoup
from collections import Counter

import string

def analize(post_id):
    base_url = 'http://localhost/devorando'
    
    URL = base_url+'/wp-json/wp/v2/comments?post='+post_id
    
    r = requests.get(url = URL)
    data = r.json()
    data = pd.json_normalize(data)
    
    punctuation = string.punctuation
    
    comments = data['content.rendered'].apply(sanitizer)
    
    model = spacy.load("./modelo")
    
    result = []
    a_score = []
    m_score = []
    
    for index, comment in enumerate(comments):
        previsao = model(sanitizer(comment))
        cats = previsao.cats
        
        a_score.append(cats['ALEGRIA'])
        m_score.append(cats['MEDO'])
        
        if cats['ALEGRIA'] > cats['MEDO']:
            result.append({
                'id': int(data['id'][index]),
                'comment': data['content.rendered'][index],
                'alegria': 1,
                'medo' : 0,
                'a_score': cats['ALEGRIA'],
                'm_score': cats['MEDO']
            })
        elif cats['ALEGRIA'] < cats['MEDO']:
            result.append({
                'id': int(data['id'][index]),
                'comment': data['content.rendered'][index],
                'alegria': 0,
                'medo' : 1,
                'a_score': cats['ALEGRIA'],
                'm_score': cats['MEDO']
            })
        else:
            result.append({
                    'id': int(data['id'][index]),
                    'comment': data['content.rendered'][index],
                    'alegria': 0,
                    'medo' : 0,
                    'a_score': cats['ALEGRIA'],
                    'm_score': cats['MEDO']
                })
            
    # best_medo = result
    best_medo = sorted([comment for comment in result if comment['medo'] > 0], key=lambda d: d['m_score'],reverse=True)
    
    best_alegria = sorted([comment for comment in result if comment['alegria'] > 0], key=lambda d: d['a_score'],reverse=True)
    
    undefined = [comment for comment in result if comment['alegria'] == comment['medo']]
            
    sentiments = {
        'Alegria': (sum(a_score)/len(a_score))*100,
        'Medo': (sum(m_score)/len(m_score))*100,
        'Indefinido': 100 - ((sum(a_score)/len(a_score))*100 + (sum(m_score)/len(m_score))*100)
    }
    
    comments = ' '.join(word for word in data['content.rendered'])
    text = BeautifulSoup(comments, "lxml").text
    sentence = ''.join([i for i in text if i not in punctuation])
    split_it = sentence.split()
    counter = Counter(split_it)
    most_common = counter.most_common(10)
    
    return {
        'sentiments': sentiments,
        'total_comments': len(result),
        'top_words': most_common,
        'top_medo': best_medo[0:3],
        'top_alegria': best_alegria[0:3],
        'top_undefineds': undefined[0:3]
    }