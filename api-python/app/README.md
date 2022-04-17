# APLICAÇÃO PARA ANÁLISE DE SENTIMENTOS
## REQUISITOS
Todos os requisitos de set-up do python estão no arquivo requirements.txt

```sh
pip install -r /path/to/requirements.txt
```

## BASE URL
Primeiro troque o endereço da variável base_url para a url de seu blog no arquivo /src/services/analize.py

## RODE A APLICAÇÃO
Exceute os comandos abaixo para a aplicação flask rodar

```sh
source FLASK_APP=app.py #use set em ambiente linux no lugar de source
flask run
```

## TREINE SEU MODELO
Para treinar o modelo acesse a rota /train. 
Caso queira colocar mais frases, modifique os arquivos base_treinamento.txt e base_texte.txt adicionando mais frases com seus respectivos rótulos.