# coding: utf-8

import json
import twitter
from pymongo import MongoClient
from flask import Flask
from flask import send_from_directory
from flask import request
from flask import jsonify

# Força todo o servidor a trabalhar com UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Dados para autenticação OAuth na API Twitter v1.1
CONSUMER_KEY = 'PDJp3Rp6zGOMs1pq3d35aL0lf'
CONSUMER_SECRET = '9OklpzVyMtrY5e0pwvQ0qtSDPv8fzUZ775CdP0ajwi3VpUhI14'
ACCESS_TOKEN_KEY = '194807206-x3H4bzLeOtVh35t8smQAobspdU4Dcs4UxiOod8sL'
ACCESS_TOKEN_SECRET = 'iImDE899l5ASwdHaeb26jUxgBvb2ZOU3UE9J7EZQOEcKI'

# Autenticação na API
api = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN_KEY,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Classificador default
DEFAULT_CLASSIFIER = '{"categories":{"Positivo":true,"Negativo":true},"docCount":{"Positivo":2,"Negativo":19},"totalDocuments":21,"vocabulary":{"2015":true,"bom":true,"legal":true,"interessante":true,"timo":true,"fant":true,"stico":true,"ruim":true,"feio":true,"horr":true,"vel":true,"terr":true,"p":true,"ssimo":true,"droga":true,"bosta":true,"De":true,"todos":true,"os":true,"aplicativos":true,"que":true,"voc":true,"usa":true,"nenhum":true,"melhor":true,"o":true,"aplicativo":true,"j":true,"est":true,"dentro":true,"de":true,"Seu":true,"cora":true,"whatsapp":true,"vai":true,"ser":true,"bloqueado":true,"no":true,"brasil":true,"todo":true,"ainda":true,"bem":true,"eu":true,"moro":true,"em":true,"carazinho":true,"Recebi":true,"comunicado":true,"do":true,"bloqueio":true,"WhatsApp":true,"Brasil":true,"senti":true,"as":true,"vistas":true,"escurecerem":true,"cai":true,"e":true,"agora":true,"estou":true,"aqui":true,"na":true,"enfermaria":true,"":true,"RT":true,"ivannmonteiro":true,"Mark":true,"Zuckerberg":true,"compre":true,"logo":true,"Vai":true,"resolver":true,"toda":true,"essa":true,"bagun":true,"a":true,"To":true,"mal":true,"vpn":true,"minha":true,"net":true,"fica":true,"tipo":true,"muito":true,"Lula":true,"culpa":true,"colonizadores":true,"por":true,"atrasos":true,"educa":true,"gera":true,"pol":true,"mica":true,"Portugal":true,"https":true,"t":true,"co":true,"qUvIvLdIEl":true,"Mas":true,"um":true,"mesmo":true,"Nossa":true,"vc":true,"bilingue":true,"Fala":true,"portugu":true,"s":true,"fala":true,"Depois":true,"dessa":true,"piada":true,"vou":true,"ali":true,"me":true,"esfaquear":true,"ja":true,"volto":true,"Minha":true,"galeria":true,"ta":true,"cheia":true,"foto":true,"CamillaAlencarr":true,"te":true,"fude":true,"tu":true,"lol":true,"quem":true,"joga":true,"kingofpopis":true,"faz":true,"meia":true,"hora":true,"q":true,"tentando":true,"cagar":true,"n":true,"sai":true,"da":true,"porra":true,"meu":true,"cu":true,"pfvr":true,"seja":true,"ano":true,"Meu":true,"cabelo":true,"entendendo":true,"rezenbela":true,"Acho":true,"engra":true,"ado":true,"agr":true,"aqueles":true,"ficavam":true,"falando":true,"mudando":true,"totalmente":true,"opini":true,"pra":true,"levar":true,"unf":true,"ou":true,"mute":true,"brogui":true,"foi":true,"chamar":true,"receita":true,"deixou":true,"ela":true,"tua":true,"pregui":true,"abs":true,"Carolgatte_":true,"EU":true,"ODEIO":true,"ESSA":true,"BOSTA":true,"rezenicornio":true,"fiquei":true,"mimimi":true,"nem":true,"pedindo":true,"desculpa":true,"ter":true,"falado":true,"rezende_evil":true,"Gente":true,"namoro":true,"com":true,"Helena":true,"deu":true,"ok":true,"Parem":true,"ficar":true,"merda":true,"mano":true,"Tentei":true,"at":true,"ir":true,"aguentando":true,"marialuuizaa_":true,"Kuetlem":true,"b":true,"bada":true},"vocabularySize":205,"wordCount":{"Positivo":13,"Negativo":321},"wordFrequencyCount":{"Positivo":{"bom":1,"legal":1,"interessante":1,"timo":1,"fant":1,"stico":1,"Minha":1,"galeria":1,"ta":1,"cheia":1,"de":1,"foto":1,"bosta":1},"Negativo":{"2015":1,"ruim":2,"feio":1,"horr":1,"vel":2,"terr":1,"p":1,"ssimo":1,"droga":1,"bosta":15,"De":1,"todos":1,"os":1,"aplicativos":1,"que":7,"voc":4,"usa":1,"nenhum":1,"melhor":1,"o":16,"aplicativo":1,"j":2,"est":2,"dentro":1,"de":6,"Seu":1,"cora":1,"whatsapp":1,"vai":2,"ser":1,"bloqueado":1,"no":2,"brasil":1,"todo":1,"ainda":1,"bem":1,"eu":3,"moro":1,"em":2,"carazinho":1,"Recebi":1,"comunicado":1,"do":5,"bloqueio":1,"WhatsApp":1,"Brasil":3,"senti":1,"as":1,"vistas":1,"escurecerem":1,"cai":1,"e":6,"agora":2,"estou":1,"aqui":2,"na":2,"enfermaria":1,"":8,"RT":6,"ivannmonteiro":1,"Mark":1,"Zuckerberg":1,"compre":1,"logo":1,"Vai":1,"resolver":1,"toda":1,"essa":2,"bagun":1,"a":6,"To":1,"mal":1,"vpn":1,"minha":1,"net":1,"fica":1,"tipo":1,"muito":1,"Lula":1,"culpa":1,"colonizadores":1,"por":2,"atrasos":1,"educa":1,"gera":1,"pol":1,"mica":1,"Portugal":1,"https":1,"t":5,"co":1,"qUvIvLdIEl":1,"Mas":1,"um":3,"mesmo":2,"Nossa":1,"vc":1,"bilingue":1,"Fala":1,"portugu":1,"s":5,"fala":1,"Depois":1,"dessa":1,"piada":1,"vou":1,"ali":1,"me":1,"esfaquear":1,"ja":1,"volto":1,"Minha":1,"galeria":1,"ta":1,"cheia":1,"foto":1,"CamillaAlencarr":1,"te":1,"fude":1,"tu":1,"lol":1,"quem":1,"joga":1,"kingofpopis":1,"faz":1,"meia":1,"hora":1,"q":3,"tentando":1,"cagar":1,"n":7,"sai":1,"da":1,"porra":1,"meu":2,"cu":1,"pfvr":1,"seja":1,"ano":1,"Meu":1,"cabelo":1,"entendendo":1,"rezenbela":1,"Acho":2,"engra":2,"ado":2,"agr":2,"aqueles":2,"ficavam":2,"falando":3,"mudando":2,"totalmente":2,"opini":2,"pra":2,"levar":2,"unf":2,"ou":2,"mute":2,"brogui":1,"foi":2,"chamar":1,"receita":1,"deixou":1,"ela":1,"tua":1,"pregui":1,"abs":1,"Carolgatte_":1,"EU":1,"ODEIO":1,"ESSA":1,"BOSTA":1,"rezenicornio":1,"fiquei":1,"mimimi":1,"nem":1,"pedindo":1,"desculpa":1,"ter":1,"falado":1,"rezende_evil":1,"Gente":1,"namoro":1,"com":1,"Helena":1,"deu":1,"ok":1,"Parem":1,"ficar":1,"merda":1,"mano":1,"Tentei":1,"at":1,"ir":1,"aguentando":1,"marialuuizaa_":1,"Kuetlem":1,"b":1,"bada":1}},"options":{}}'

# Servidor HTTP
app = Flask(__name__)
app.debug = True

STATIC_DIR = ''

@app.route('/')
def index():
    '''
        Página inicial
    '''
    return send_from_directory(STATIC_DIR , 'index.html')


@app.route('/api/twitter/search')
def query():
    '''
        Busca termo no Twitter
        Argumentos: q (query)
    '''

    MAX_RESULTS = 100

    try:
        query = request.args.get('q')
        resp = api.GetSearch(term=query, count=MAX_RESULTS)
        json_r = {'tweets': [r.AsDict() for r in resp]}
    except:
        json_r = {'tweets': []}

    return jsonify(json_r)


@app.route('/api/mongodb/classifiers')
def classifiers():
    '''
        Recupera todos os classificadores persistidos no MongoDB
    '''
    # Conecta ao MongoDB
    cliente = MongoClient('mongodb://localhost:27017/')
    banco = cliente['bd_classificadores']

    classificadores = {};

    # Recupera os classificadores
    colecao_classificadores = banco['classificadores']

    # Se a coleção estiver vazia, insere o
    # classificador de sentimentos deafult
    if not colecao_classificadores.count():
        colecao_classificadores.insert_one({'nome': 'sentimentos', 'dados': DEFAULT_CLASSIFIER})

    for c in colecao_classificadores.find():
        classificadores[c['nome']] = c['dados']

    return jsonify(classificadores)


@app.route('/api/mongodb/classifiers/info')
def info_classifiers():
    '''
        Retorna informações sobre todos os classificadores persistidos no MongoDB
    '''
    # Conecta ao MongoDB
    cliente = MongoClient('mongodb://localhost:27017/')
    banco = cliente['bd_classificadores']

    info_classificadores = {'info': []};

    # Recupera os classificadores
    colecao_classificadores = banco['classificadores']

    for c in colecao_classificadores.find():
        info_classificadores['info'].append({'nome': c['nome'], 'tamanho': len(str(c['dados'])), 'categorias': json.loads(c['dados'])['categories'].keys()
})

    return jsonify(info_classificadores)


@app.route('/api/mongodb/classifier/new')
def new_classifier():
    '''
        Persiste um novo classificador no MongoDB
        Argumentos: nome e dados
    '''
    # Conecta ao MongoDB
    cliente = MongoClient('mongodb://localhost:27017/')
    banco = cliente['bd_classificadores']

    # Argumentos
    arg_nome = request.args.get('nome')
    arg_dados = request.args.get('dados')

    if arg_nome and arg_dados:
        colecao_classificadores = banco['classificadores']
        colecao_classificadores.insert_one({'nome': arg_nome, 'dados': arg_dados})
        json_r = {'status': 'ok'}
    else:
        json_r = {'status': 'error'}

    return jsonify(json_r)


@app.route('/api/mongodb/classifier/update')
def update_classifier():
    '''
        Atualiza um classificador com seu novo treinamento
        Argumentos: nome e dados
    '''
    # Conecta ao MongoDB
    cliente = MongoClient('mongodb://localhost:27017/')
    banco = cliente['bd_classificadores']
    colecao_classificadores = banco['classificadores']

    try:
        # Argumentos
        arg_nome = request.args.get('nome')
        arg_dados = request.args.get('dados')

        # Obtém o classificador e o modifica
        c = colecao_classificadores.find_one({'nome': arg_nome})
        c['dados'] = arg_dados
        colecao_classificadores.save(c)

        json_r = {'status': 'ok'}

    except:
        json_r = {'status': 'error'}

    return jsonify(json_r)


@app.route('/api/mongodb/classifier/remove')
def remove_classifier():
    '''
        Remove um classificador
        Argumento: nome
    '''
    # Conecta ao MongoDB
    cliente = MongoClient('mongodb://localhost:27017/')
    banco = cliente['bd_classificadores']
    colecao_classificadores = banco['classificadores']

    try:
        # Argumentos
        arg_nome = request.args.get('nome')

        # Obtém o classificador e o modifica
        colecao_classificadores.remove({'nome': arg_nome})

        json_r = {'status': 'ok'}

    except:
        json_r = {'status': 'error'}

    return jsonify(json_r)


@app.route('/<path:path>')
def static_proxy(path):
    '''
        Mídia estática (img, css, js)
    '''
    try:
        return send_from_directory(STATIC_DIR , path)
    except:
        return send_from_directory(STATIC_DIR , 'index.html')


if __name__ == "__main__":
    app.run()