from Pilotos import Pilotos
from equipe import Equipe
from piloto import Piloto
from etapa import Etapa
from bateria import Bateria
from grid import Grid
from temporada import Temporada
from classe import Classe
from carro import Carro

import os
import pymysql
from http import HTTPStatus
from flask_cors import CORS
from flask import Flask, redirect, request, jsonify, url_for, abort
from db import Database
from config import DevelopmentConfig as devconf

host = os.environ.get('FLASK_SERVER_HOST', devconf.HOST)
port = os.environ.get('FLASK_SERVER_PORT', devconf.PORT)
version = str(devconf.VERSION).lower()
url_prefix = str(devconf.URL_PREFIX).lower()
route_prefix = f"/{url_prefix}/{version}"


def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={f"{route_prefix}/*": {"origins": "*"}})
    app.config.from_object(devconf)
    return app


def get_response_msg(data, status_code):
    message = {
        'status': status_code,
        'data': data if data else 'No records found'
    }
    response_msg = jsonify(message)
    response_msg.status_code = status_code
    return response_msg


def json_login(dados):
    return {
        "uuid": dados[0],
        "senha": dados[1],
        "isAdmin": dados[2]
    }


app = create_app()
wsgi_app = app.wsgi_app
db = Database(devconf)


## ==============================================[ Routes - Start ]

## /api/v1/pilotos
@app.route(f"{route_prefix}/pilotos", methods=['GET'])
def get_pilotos():
    try:
        pilotos = Pilotos()
        query = pilotos.select_pilotos()
        records = db.run_query(query=query)
        pilotos.set_pilotos(records)
        response = get_response_msg(pilotos.serialize(), HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/piloto
@app.route(f"{route_prefix}/piloto", methods=['GET', 'POST', 'PUT'])
def api_piloto():
    try:
        uuid = request.args.get('uuid', type=str)
        if request.method == 'GET':
            piloto = Piloto(uuid)
            query = piloto.select_informacoes()
            records = db.run_query(query=query)
            piloto.set_informacoes(records[0])
            response = get_response_msg(piloto.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'POST':
            content = request.json
            piloto = Piloto(uuid, content['login'], content['senha'], content['nome'], content['sobrenome'],
                            content['nickname'], content['steamid'],
                            content['whatsapp'], content['chavepix'], content['cidade'], content['estado'],
                            content['controlador'], content['linkcanal'])
            query = piloto.criar()
            db.run_query(query=query[0])
            db.run_query(query=query[1])
            response = get_response_msg(piloto.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'PUT':
            content = request.json
            piloto = Piloto(uuid)
            query = piloto.atualiza_info(content['label'], content['valor'])
            db.run_query(query=query)
            response = get_response_msg(["piloto atualizado"], HTTPStatus.OK)
            db.close_connection()
            return response
        else:
            print(1)
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/pilotos
@app.route(f"{route_prefix}/login", methods=['GET'])
def api_login():
    try:
        username = request.args.get('username', type=str)
        query = "SELECT BIN_TO_UUID(uuid), password, isAdmin FROM piloto where username='{username}'".format(
            username=username)
        records = db.run_query(query=query)
        response = get_response_msg(json_login(records[0]), HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/temporadas
@app.route(f"{route_prefix}/temporadas", methods=['GET'])
def api_temporadas():
    try:
        temporadas = []
        query = 'SELECT BIN_TO_UUID(uuid), nome,  DATE_FORMAT(dtInicio, \"%Y-%m-%d\"), DATE_FORMAT(dtFim, \"%Y-%m-%d\") from temporada'
        records = db.run_query(query=query)
        for row in records:
            temporada = Temporada(row[0], row[1], row[2], row[3])
            temporadas.append(temporada.serialize())
        response = get_response_msg(temporadas, HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/temporada
@app.route(f"{route_prefix}/temporada", methods=['GET', 'POST', 'PUT'])
def api_temporada():
    try:
        uuid = request.args.get('uuid', type=str)
        if request.method == 'GET':
            temporada = Temporada(uuid)
            query = temporada.select()
            records = db.run_query(query=query)
            temporada.set_informacoes(records[0])
            response = get_response_msg(temporada.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'POST':
            content = request.json
            print(content)
            temporada = Temporada(uuid, content['nome'], content['dtInicio'], content['dtFim'])
            query = temporada.criar()
            print(query)
            db.run_query(query=query)
            response = get_response_msg(temporada.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'PUT':
            content = request.json
            temporada = Temporada(uuid, content['nome'], content['dtInicio'], content['dtFim'])
            query = temporada.atualizar()
            db.run_query(query=query)
            response = get_response_msg(temporada.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        else:
            print(1)
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/grids
@app.route(f"{route_prefix}/grids", methods=['GET'])
def api_grids():
    try:
        grids = []
        query = 'SELECT BIN_TO_UUID(uuid), BIN_TO_UUID(temporada_uuid), nome, simulador, dia_da_semana, link_onboard FROM grid'
        records = db.run_query(query=query)
        for row in records:
            grid = Grid(row[0], row[1], row[2], row[3], row[4], row[5])
            grids.append(grid.serialize())
        response = get_response_msg(grids, HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/temporada
@app.route(f"{route_prefix}/grid", methods=['GET', 'POST', 'PUT'])
def api_grid():
    try:
        uuid = request.args.get('uuid', type=str)
        if request.method == 'GET':
            grid = Grid(uuid)
            query = grid.selecionar()
            records = db.run_query(query=query)
            grid.set_informacoes(records[0])
            response = get_response_msg(grid.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'POST':
            content = request.json
            grid = Grid(uuid, content['temporada_uuid'], content['nome'], content['simulador'], content['diaDaSemana'],
                        content['linkOnboard'])
            query = grid.criar()
            db.run_query(query=query)
            response = get_response_msg(grid.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'PUT':
            content = request.json
            grid = Grid(uuid, content['temporada_uuid'], content['nome'], content['simulador'], content['diaDaSemana'],
                        content['linkOnboard'])
            query = grid.atualizar()
            db.run_query(query=query)
            response = get_response_msg(grid.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        else:
            print(1)
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/grids
@app.route(f"{route_prefix}/classes", methods=['GET'])
def api_classes():
    try:
        classes = []
        query = 'SELECT BIN_TO_UUID(uuid), nome, imagem FROM classe'
        records = db.run_query(query=query)
        for row in records:
            classe = Classe(row[0], row[1], row[2])
            classes.append(classe.serialize())
        response = get_response_msg(classes, HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/temporada
@app.route(f"{route_prefix}/classe", methods=['GET', 'POST', 'PUT'])
def api_classe():
    try:
        uuid = request.args.get('uuid', type=str)
        if request.method == 'GET':
            classe = Classe(uuid)
            query = classe.selecionar()
            records = db.run_query(query=query)
            classe.set_informacoes(records[0])
            response = get_response_msg(classe.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'POST':
            content = request.json
            classe = Classe(uuid, content['nome'])
            query = classe.criar()
            db.run_query(query=query)
            response = get_response_msg(classe.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'PUT':
            content = request.json
            classe = Classe(uuid, content['nome'])
            query = classe.atualizar()
            db.run_query(query=query)
            response = get_response_msg(classe.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        else:
            print(1)
    except pymysql.MySQLError as sqle:
        print(sqle)
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/grids
@app.route(f"{route_prefix}/carros", methods=['GET'])
def api_carros():
    try:
        carros = []
        query = 'SELECT BIN_TO_UUID(uuid), BIN_TO_UUID(classe_uuid), nome, imagem FROM carro'
        records = db.run_query(query=query)
        for row in records:
            carro = Carro(row[0], row[1], row[2], row[3])
            carros.append(carro.serialize())
        response = get_response_msg(carros, HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/temporada
@app.route(f"{route_prefix}/carro", methods=['GET', 'POST', 'PUT'])
def api_carro():
    try:
        uuid = request.args.get('uuid', type=str)
        classe_uuid = request.args.get('classeUuid', type=str)
        if request.method == 'GET':
            carro = Carro(uuid, classe_uuid)
            query = carro.selecionar()
            records = db.run_query(query=query)
            carro.set_informacoes(records[0])
            response = get_response_msg(carro.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'POST':
            content = request.json
            carro = Carro(uuid, classe_uuid, content['nome'])
            query = carro.criar()
            db.run_query(query=query)
            response = get_response_msg(carro.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        elif request.method == 'PUT':
            content = request.json
            carro = Carro(uuid, classe_uuid, content['nome'])
            query = carro.atualizar()
            db.run_query(query=query)
            response = get_response_msg(carro.serialize(), HTTPStatus.OK)
            db.close_connection()
            return response
        else:
            print(1)
    except pymysql.MySQLError as sqle:
        print(sqle)
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/uploadImagem
@app.route(f"{route_prefix}/upload", methods=['POST'])
def api_upload():
    try:
        tipo = request.args.get('tipo', type=str)
        uuid = request.args.get('uuid', type=str)
        content = request.json
        query = ""
        if tipo == 'classe':
            classe = Classe(uuid)
            query = classe.upload_imagem(content['imagem'])
        if tipo == 'carro':
            carro = Carro(uuid, content['classe_uuid'])
            query = carro.upload_imagem(content['imagem'])
        db.run_query(query=query)
        response = get_response_msg("Imagem atualizada!", HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/health
@app.route(f"{route_prefix}/health", methods=['GET'])
def health():
    try:
        db_status = "Connected to DB" if db.db_connection_status else "Not connected to DB"
        response = get_response_msg("I am fine! " + db_status, HTTPStatus.OK)
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('health'))


## =================================================[ Routes - End ]

## ================================[ Error Handler Defined - Start ]
## HTTP 404 error handler
@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):
    return get_response_msg(data=str(e), status_code=HTTPStatus.NOT_FOUND)


## HTTP 400 error handler
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(e):
    return get_response_msg(str(e), HTTPStatus.BAD_REQUEST)


## HTTP 500 error handler
@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return get_response_msg(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


## ==================================[ Error Handler Defined - End ]
if __name__ == '__main__':
    ## Launch the application
    app.run(host=host, port=port)
