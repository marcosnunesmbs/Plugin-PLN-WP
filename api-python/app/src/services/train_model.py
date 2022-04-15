import spacy
import pandas as pd
import random
import numpy as np
import spacy
from spacy.training import Example
from src.utils.sanitizer import sanitizer
from sklearn.metrics import confusion_matrix, accuracy_score

def train():
  train_db = pd.read_csv('./recursos/base_treinamento.txt', encoding = 'utf-8')
  train_db['texto'] = train_db['texto'].apply(sanitizer)

  test_db = pd.read_csv('./recursos/base_teste.txt', encoding = 'utf-8')
  test_db['texto'] = test_db['texto'].apply(sanitizer)

  base_dados_final = []
  for texto, emocao in zip(train_db['texto'], train_db['emocao']):
    if emocao == 'alegria':
      dic = ({'ALEGRIA': True, 'MEDO': False})
    elif emocao == 'medo':
      dic = ({'ALEGRIA': False, 'MEDO': True})

    base_dados_final.append([texto, dic.copy()])
    
  modelo = spacy.blank('pt')
  categorias = modelo.add_pipe("textcat")
  categorias.add_label("ALEGRIA")
  categorias.add_label("MEDO")

  optimizer = modelo.initialize()
  for epoca in range(4):
    random.shuffle(base_dados_final)
    losses = {}
    for raw_text, entity_offsets in base_dados_final:
        doc = modelo.make_doc(raw_text)
        example = Example.from_dict(doc, {"cats": entity_offsets})
        modelo.update([example], sgd=optimizer, losses=losses)
    if epoca % 1 == 0:
      print(losses)
      
  modelo.to_disk("modelo")
  model = spacy.load("./modelo")

  predict = []
  for texto in test_db['texto']:
    result = model(texto)
    predict.append(result.cats)
    
  predict_final = []
  for pred in predict:
    if pred['ALEGRIA'] > pred['MEDO']:
      predict_final.append('alegria')
    else:
      predict_final.append('medo')

  predict_final = np.array(predict_final)
  real_answers = test_db['emocao'].values

  acuracy = accuracy_score(real_answers, predict_final)
  cm = confusion_matrix(real_answers, predict_final)
  
  return {
    'acuracy': acuracy,
    'cofusion_matrix': cm.tolist()
  }