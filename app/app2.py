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


app = create_app()
wsgi_app = app.wsgi_app
db = Database(devconf)

## ==============================================[ Routes - Start ]

## /api/v1/pilotos
@app.route(f"{route_prefix}/pilotos", methods=['GET'])
def get_pilotos():
    try:
        query = f"SELECT BIN_TO_UUID(uuid), username, password, isAdmin FROM piloto"
        records = db.run_query(query=query)
        response = get_response_msg(records, HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))

## /api/v1/piloto?uuid=<piloto_uuid>
@app.route(f"{route_prefix}/piloto", methods=['GET'])
def get_piloto():
    try:
        if request.method == 'GET':
            uuid = request.args.get('uuid', type=str)
            query = f"SELECT nome, sobrenome, nickname, steamid, whatsapp, chavepix, cidade, estado, controlador, linkcanal FROM piloto_informacoes WHERE piloto_uuid = UUID_TO_BIN('{uuid}')"
            records = db.run_query(query=query)
            response = get_response_msg(records, HTTPStatus.OK)
            db.close_connection()
            return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))

## /api/v1/getcity?country=IND
@app.route(f"{route_prefix}/getcity", methods=['GET'])
def getdata():
    try:
        countrycode = request.args.get('country', default='IND', type=str)
        query = f"SELECT * FROM world.city WHERE COUNTRYCODE='{countrycode.upper()}'"
        records = db.run_query(query=query)
        response = get_response_msg(records, HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/getcitycodes
@app.route(f"{route_prefix}/getcitycodes", methods=['GET'])
def getcitycodes():
    try:
        query = f"SELECT distinct(COUNTRYCODE) FROM world.city"
        records = db.run_query(query=query)
        response = get_response_msg(records,  HTTPStatus.OK)
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




cnx = mysql.connector.connect(user='rpm', password='meuovo', host='192.168.15.9', database='rpmesports')
app = Flask(__name__)
CORS(app)


def print_pontos():
    cont = 1
    while cont <= 3:
        select = "SELECT nome FROM pilotos where id = {}".format(cont)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            print("Piloto: {}".format(out[0]))
        select = "SELECT SUM(gp.pontos) FROM pontuacao p inner join etapas e on p.etapa_id = e.id inner join grids g on e.grid_id = g.id inner join grid_pontos gp on gp.grid_id = g.id where p.posicao = gp.posicao and p.piloto_id = {} group by p.piloto_id".format(
            cont)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            print("\tTotal Pontos: {}".format(out[0]))
        select = "SELECT e.nome, gp.pontos FROM pontuacao p inner join etapas e on p.etapa_id = e.id inner join grids g on e.grid_id = g.id inner join grid_pontos gp on gp.grid_id = g.id where p.posicao = gp.posicao and p.piloto_id = {}".format(
            cont)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchall()
            for i in out:
                print("\t\tEtapa: {}\n\t\t\tPonto: {}".format(i[0], i[1]))
        cont += 1


@app.route('/temporadas', methods=['GET'])
def get_temporadas():
    select = "SELECT id, nome  FROM temporadas order by id"
    temporadas = []
    with cnx.cursor() as cur:
        cur.execute(select)
        out = cur.fetchall()
        for temporada in out:
            temporadas.append({"id": temporada[0], "nome": temporada[1]})
    return jsonify(temporadas)


@app.route('/pilotos', methods=['GET'])
def get_pilotos():
    retorno = {}
    select = "SELECT BIN_TO_UUID(uuid) FROM piloto"
    pilotos = []
    with cnx.cursor() as cur:
        cur.execute(select)
        out = cur.fetchall()
        for piloto in out:
            pilotos.append({'uuid': piloto[0]})
    retorno['pilotos'] = pilotos
    return retorno, 200


@app.route('/piloto', methods=['GET', 'POST', 'OPTIONS'])
def cadastro_piloto():
    retorno = {}
    if request.method == 'OPTIONS':
        return "OK",200
    elif request.method == 'GET':
        try:
            uuid = request.args.get('uuid')
            piloto = Piloto(uuid)
            piloto.select_informacoes(cnx)
            retorno = jsonify(piloto.serialize())
            return retorno, 200
        except Exception as e:
            print(e)
            return e, 500
    else:
        try:
            uuid = request.args.get('uuid')
            content = request.json
            piloto = Piloto(uuid, content['login'], content['senha'], content['nome'], content['sobrenome'], content['nickname'], content['steamid'],
                                   content['whatsapp'], content['chavepix'], content['cidade'], content['estado'],
                                   content['controlador'], content['linkcanal'])
            piloto.criar(cnx)
            return "Piloto Cadastrado com sucesso", 200
        except Exception as e:
            print(e)
            return "erro", 500

@app.route('/login', methods=['POST'])
def login():
    retorno = {}
    try:
        content = request.json
        with cnx.cursor() as cur:
            sql = "SELECT count(*) FROM piloto WHERE username = \'{username}\'".format(username=content['login'])
            cur.execute(sql)
            out = cur.fetchone()
            if out[0] == 0: return "Não autorizado", 200
        sql = "SELECT BIN_TO_UUID(uuid), password FROM piloto WHERE username = \'{username}\'".format(username=content['login'])
        with cnx.cursor() as cur:
            cur.execute(sql)
            out = cur.fetchone()
            retorno['uuid'] = out[0]
            retorno['senha'] = out[1]
            return retorno, 200
    except Exception as e:
        print(e)
        return e, 500


@app.route('/equipes/<temporada>', methods=['GET'])
def get_equipes(temporada):
    select = "SELECT distinct eq.nome FROM equipes eq, piloto_equipe_temporada pet, temporadas te where eq.id = pet.equipe_id and " \
             "pet.temporada_id = te.id and te.nome = \'{}\'".format(temporada)
    equipes = []
    with cnx.cursor() as cur:
        cur.execute(select)
        out = cur.fetchall()
        for equipe in out:
            e = Equipe(equipe[0])
            e.criar(cnx)
            equipes.append(e.serialize())
    return jsonify(equipes)


@app.route('/grids/<temporada>', methods=['GET'])
def get_grids(temporada):
    select = "SELECT DISTINCT gr.id, gr.nome FROM grids gr, etapas et, temporadas te WHERE gr.id = et.grid_id and " \
             "et.temporada_id = te.id and te.nome = \'{}\'".format(temporada)
    grids = []
    with cnx.cursor() as cur:
        cur.execute(select)
        out = cur.fetchall()
        for grid in out:
            select = "SELECT posicao, pontos from grid_pontos where grid_id = {}".format(grid[0])
            pontos = []
            with cnx.cursor() as cur2:
                cur2.execute(select)
                out2 = cur2.fetchall()
                for ponto in out2:
                    pontos.append({"posicao": ponto[0], "pontos": ponto[1]})
            grids.append({"id": grid[0], "nome": grid[1], "pontuacao": pontos})
    return jsonify(grids)


@app.route('/resultado/bateria/<bateria>')
def resultado_bateria(bateria):
    bat = Bateria(bateria, 1, 1)
    bat.criar(cnx)
    out = bat.pontuacao_bateria(cnx)
    return jsonify(out)


@app.route('/resultado/etapa/<etapa>')
def resultado_etapa(etapa):
    et = Etapa(etapa, 1, 1)
    et.criar(cnx)
    out = et.pontuacao_etapa(cnx)
    return jsonify(out)


@app.route('/resultado/temporada/<temporada>')
def resultado_temporada(temporada):
    temp = Temporada(temporada)
    temp.criar(cnx)
    out = temp.pontos_equipe(cnx)
    return jsonify(out)


@app.route('/resultado/grid/<grid>')
def resultado_grid(grid):
    grid = Grid(grid, "teste")
    grid.criar(cnx)
    out = grid.pontuacao_piloto(cnx)
    return jsonify(out)


@app.route('/cadastro/equipe', methods=['POST'])
def cadastro_equipe():
    try:
        content = request.json
        equipe = Equipe(content['nome'])
        equipe.criar(cnx)
        return "Equipe Criada com sucesso.", 200
    except Exception as e:
        print(e)
        return "erro", 500


@app.route('/cadastro/equipe_piloto', methods=['POST'])
def cadastro_equipe_piloto():
    try:
        content = request.json
        temporada = Temporada(content['temporada'])
        temporada.criar(cnx)
        piloto = Piloto(content['piloto'])
        piloto.criar(cnx)
        equipe = Equipe(content['equipe'])
        equipe.criar(cnx)
        temporada.relacionar_piloto_equipe(cnx, piloto.id, equipe.id)
        return "Piloto {} atrelado a equipe {} na temporada {}".format(piloto.nome, equipe.nome, temporada.nome), 200
    except Exception as e:
        print(e)
        return "erro", 500


@app.route('/cadastro/grid', methods=['POST'])
def cadastro_grid():
    try:
        content = request.json
        grid = Grid(content['nome'], content['sim'], content['pontos'])
        grid.criar(cnx)
        return "Grid {} criado com sucesso".format(grid.nome)
    except Exception as e:
        print(e)
        return "erro", 500


@app.route('/cadastro/etapa', methods=['POST'])
def cadastro_etapa():
    content = request.json
    temporada = Temporada(content['temporada'])
    temporada.criar(cnx)
    grid = Grid(content['grid'])
    grid.criar(cnx)
    etapa = Etapa(content['etapa'], grid.id, temporada.id, content['multiplicador'])
    etapa.criar(cnx)
    return "Etapa {} criada para o grid {} na temporada {}".format(etapa.nome, grid.nome, temporada.nome)


@app.route('/cadastro/bateria', methods=['POST'])
def cadastro_bateria():
    content = request.json
    etapa = Etapa(content['etapa'])
    etapa.criar(cnx)
    bateria = Bateria(content['nome'], etapa.id, content['multiplicador'])
    bateria.criar(cnx)
    return "Bateria {} criada para a etapa {}".format(bateria.nome, etapa.nome)


@app.route('/pontuacao/<bateria>', methods=['POST'])
def pontuacao(bateria):
    bat = Bateria(bateria)
    bat.criar(cnx)
    content = request.json
    for linha in content['pontos']:
        piloto = Piloto(linha[0])
        print(piloto.nome)
        piloto.criar(cnx)
        bat.pontuacao(cnx, linha[1], piloto.id)
    return "Pontuação da bateria {} aplicada com sucesso".format(bateria)

