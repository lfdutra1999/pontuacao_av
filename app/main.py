import mysql.connector
from equipe import Equipe
from piloto import Piloto
from etapa import Etapa
from bateria import Bateria
from grid import Grid
from temporada import Temporada
from random import randint
from flask import Flask, render_template, request, jsonify

cnx = mysql.connector.connect(user='rpm', password='meuovo', host='127.0.0.1', database='rpmesports')
app = Flask(__name__)


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


@app.route('/pilotos/<temporada>', methods=['GET'])
def get_pilotos(temporada):
    select = "SELECT pi.nome FROM pilotos pi, piloto_equipe_temporada pet, temporadas te where pi.id = pet.piloto_id and " \
             "pet.temporada_id = te.id and te.nome = \'{}\'".format(temporada)
    pilotos = []
    with cnx.cursor() as cur:
        cur.execute(select)
        out = cur.fetchall()
        for piloto in out:
            p = Piloto(piloto[0])
            p.criar(cnx)
            pilotos.append(p.serialize())
    return jsonify(pilotos)


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
            pontos =[]
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


@app.route('/cadastro/piloto', methods=['POST'])
def cadastro_piloto():
    try:
        content = request.json
        piloto = Piloto(content['nome'], content['steam_id'])
        piloto.criar(cnx)
        return "Piloto Cadastrado com sucesso", 200
    except Exception as e:
        print(e)
        return "erro", 500


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


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


def teste():
    # Criar pilotos
    pilotos = [Piloto("Leo Franco"), Piloto("Matheus Samuel"), Piloto("Julio Cesar"), Piloto("Luan Costa"),
               Piloto("Raul Gobbi"), Piloto("Lucas Tonon")]
    for piloto in pilotos:
        piloto.criar(cnx)
    # Criar equipes
    equipes = [Equipe("RPM Esports"), Equipe("Montdata"), Equipe("Compliance")]
    for equipe in equipes:
        equipe.criar(cnx)
    # Criar Temporada
    temporada = Temporada("T16")
    temporada.criar(cnx)
    # Relaciona pilotos com equipes na temporada
    for piloto in pilotos:
        equipe_id = randint(1, 3)
        temporada.relacionar_piloto_equipe(cnx, piloto.id, equipe_id)
    # Criar grids
    grids = [Grid("LIGHT", "AMS2", [[1, 25], [2, 20], [3, 18], [4, 16], [5, 14], [6, 12]]),
             Grid("F3", "AC", [[1, 29], [2, 25], [3, 20], [4, 18], [5, 16], [6, 14]]),
             Grid("LIGHT-AM", "ACC", [[1, 35], [2, 30], [3, 25], [4, 20], [5, 18], [6, 16]])]
    for grid in grids:
        grid.criar(cnx)
    # Criar etapas e baterias
    etapas = [Etapa("T16-E1-LIGHT", 1, 1, 1), Etapa("T16-E2-LIGHT", 1, 1, 1), Etapa("T16-E1-F3", 2, 1, 1),
              Etapa("T16-E2-F3", 2, 1, 1), Etapa("T16-E1-LIGHT-AM", 3, 1, 1), Etapa("T16-E2-LIGHT-AM", 3, 1, 1)]
    baterias = []
    for etapa in etapas:
        etapa.criar(cnx)
        contador = 1
        if etapa.id == 3 or etapa.id == 4:
            while contador <= 2:
                if contador == 1:
                    bateria = Bateria("{}-B{}{}".format(etapa.nome[:6], contador, etapa.nome[etapa.nome.rfind('-'):]),
                                      etapa.id, 1)
                else:
                    bateria = Bateria("{}-B{}{}".format(etapa.nome[:6], contador, etapa.nome[etapa.nome.rfind('-'):]),
                                      etapa.id, 0.5)
                bateria.criar(cnx)
                baterias.append(bateria)
                contador += 1
        else:
            bateria = Bateria("{}-B1{}".format(etapa.nome[:6], etapa.nome[etapa.nome.rfind('-'):]), etapa.id, 1)
            bateria.criar(cnx)
            baterias.append(bateria)
    # Pontuacao
    for etapa in etapas:
        for bateria in baterias:
            if etapa.id == bateria.etapa_id:
                posicao = 1
                bateria.criar(cnx)
                for piloto in pilotos:
                    bateria.pontuacao(cnx, posicao, piloto.id)
                    posicao += 1


if __name__ == "__main__":
    # teste()
    app.run(debug=True)
    print(1)
