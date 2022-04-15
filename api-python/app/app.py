from flask import Flask
from flask import jsonify
from src.services.analize import analize
from src.services.train_model import train

app = Flask(__name__)

@app.route('/')
def welcome():
    result =  {  
            'App Name': 'TCC - Marcos Nunes',
            'Description': 'A PLN service to wordpress comments'
         }
    return jsonify(result)

@app.route('/analize/<post_id>')
def analize_post(post_id):
    result = analize(post_id)
    return result

@app.route('/train')
def train_model():
    result = train()
    return result