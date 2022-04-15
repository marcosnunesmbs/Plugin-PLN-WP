import spacy
import string
from spacy.lang.pt.stop_words import STOP_WORDS
from bs4 import BeautifulSoup

pln = spacy.load('pt_core_news_sm')
stop_words = STOP_WORDS
punctuation = string.punctuation

def sanitizer(text):
  text = text.lower()
  text = BeautifulSoup(text, "lxml").text
  text = text.rstrip("\n")
  document = pln(text)
  
  list = []
  for token in document:
    list.append(token.lemma_)

  list = [word for word in list if word not in stop_words and word not in punctuation]
  list = ' '.join([str(elemento) for elemento in list if not elemento.isdigit()])

  return list