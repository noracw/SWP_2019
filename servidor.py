# Servidor para a plataforma de Planetas do Star Wars

# importacoes
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from urllib.parse import parse_qs

# configuracoes da conexao com a base de dados
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'starWars_planets_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/starWars_planets_db'

mongo = PyMongo(app)
planets = mongo.db.planetsTable

# metodo GET - retorna todos os planetas ou so um planeta, procurado por nome ou id
@app.route('/planets', methods=['GET'])
def get_planets():  
  output = []
  # pega possiveis parametros da requisicao
  query_params = dict(parse_qs(request.query_string.decode("utf-8")))
  # se tiver algum parametro, procura por um planeta por nome ou id
  if query_params:
    # checa se a busca e por id
    if 'planetID' in query_params:
      # pega o valor e converte para um numero inteiro
      value = query_params['planetID'][0]
      ID = int(value)
      # procura na base de dados por id
      p = planets.find_one({'planetID' : ID})
      # checa se houve retorno valido - se sim, retorna o planeta - se nao, retorna que nao encontrou
      if p:
        output = {'planetID': p['planetID'],
                  'name' : p['name'], 
                  'climate' : p['climate'], 
                  'terrain' : p['terrain']} 
      else:
        output = "Esta id de planeta nao existe!"        
    #checa se a busca e por nome
    elif 'name' in query_params:
      # pega o valor e procura na base de dados por nome
      value = query_params['name'][0]
      p = planets.find_one({'name' : value})
      # checa se houve retorno valido - se sim, retorna o planeta - se nao, retorna que nao encontrou
      if p:
        output = {'planetID': p['planetID'],
                  'name' : p['name'], 
                  'climate' : p['climate'], 
                  'terrain' : p['terrain']} 
      else:
        output = "Este nome de planeta nao existe!"
    # o parametro utilizado nao e valido
    else:
      output = "Nenhum planeta foi encontrado com estes parametros!"
  # nenhum parametro, retorna todos os planetas da base de dados
  else:      
    for p in planets.find():
      output.append({'planetID': p['planetID'],
                     'name' : p['name'], 
                     'climate' : p['climate'], 
                     'terrain' : p['terrain']}) 
  # retorna o resultado obtido
  return jsonify({'result' : output})

# metodo POST - insere um planeta na base de dados
@app.route('/planets', methods=['POST'])
def add_planets():
  # coleta os dados do novo planeta
  name = request.json['name']
  climate = request.json['climate']
  terrain = request.json['terrain']
  ID = planets.count() + 1
  # insere na base de dados e pega o id padrao 
  planet_id = planets.insert({'planetID': ID, 
                              'name': name, 
                              'climate': climate, 
                              'terrain': terrain})
  # pega o novo planeta, ja inserido, para retorna-lo
  new_planet = planets.find_one({'_id': planet_id})
  output = {'planetID': new_planet['planetID'],
            'name' : new_planet['name'], 
            'climate' : new_planet['climate'], 
            'terrain' : new_planet['terrain']}
  return jsonify({'result' : output})

# metodo DELETE - exclui um planeta na base de dados atraves do nome
@app.route("/planets/<name>", methods=['DELETE'])
def remove_user(name):
  # deleta o planeta pelo nome
  d = planets.delete_one({"name": name})
  if d.deleted_count > 0 :
    output = "O planeta " + name + " foi excluido com sucesso."
  else:
    output = "O planeta " + name + " nao foi encontrado e por isso nao foi excluido."
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)

