import mysql.connector
from equipe import Equipe
from piloto import Piloto
from etapa import Etapa
from grid import Grid
from temporada import Temporada
from random import randint
from flask import Flask, render_template, request, redirect

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


def get_pilotos():
    select = "SELECT nome FROM pilotos"
    pilotos = []
    with cnx.cursor() as cur:
        cur.execute(select)
        out = cur.fetchall()
        for piloto in out:
            pilotos.append(piloto[0])
    return pilotos


def get_equipes():
    select = "SELECT nome FROM equipes"
    equipes = []
    with cnx.cursor() as cur:
        cur.execute(select)
        out = cur.fetchall()
        for equipe in out:
            equipes.append(equipe[0])
    return equipes


@app.route('/resultado/etapa/<etapa>')
def resultado_etapa(etapa):
    et = Etapa(etapa, 1, 1)
    et.criar(cnx)
    cab = ['Posicao', 'Piloto', 'Equipe', 'Pontos']
    out = et.print_pontuacao(cnx)
    return render_template('table.html', cab=cab, title=et.nome, out=out)


@app.route('/resultado/temporada/<temporada>')
def resultado_temporada(temporada):
    temp = Temporada(temporada)
    temp.criar(cnx)
    cab = ['Equipe', 'Pontos']
    out = temp.pontos_equipe(cnx)
    return render_template('table.html', cab=cab, title=temp.nome, out=out)


@app.route('/cadastro/piloto', methods=['GET', 'POST'])
def cadastro_piloto():
    if request.method == 'GET':
        return render_template('cadastro_piloto.html')
    if request.method == 'POST':
        piloto = Piloto(request.form['nome'])
        piloto.criar(cnx)
        return redirect('/cadastro/piloto')


@app.route('/cadastro/equipe', methods=['GET', 'POST'])
def cadastro_equipe():
    if request.method == 'GET':
        return render_template('cadastro_equipe.html')
    if request.method == 'POST':
        equipe = Equipe(request.form['nome'])
        equipe.criar(cnx)
        return redirect('/cadastro/equipe')


@app.route('/cadastro/equipe_piloto', methods=['GET', 'POST'])
def cadastro_equipe_piloto():
    if request.method == 'GET':
        pilotos = get_pilotos()
        equipes = get_equipes()
        return render_template('piloto_equipe.html', pilotos=pilotos, equipes=equipes)
    if request.method == 'POST':
        temporada = Temporada('T16')
        temporada.criar(cnx)
        piloto = Piloto(request.form['piloto'])
        piloto.criar(cnx)
        equipe = Equipe(request.form['equipe'])
        equipe.criar(cnx)
        temporada.relacionar_piloto_equipe(cnx, piloto.id, equipe.id)
        return redirect('/cadastro/equipe_piloto')


@app.route('/cadastro/grid', methods=['GET', 'POST'])
def cadastro_grid():
    if request.method == 'GET':
        return render_template('cadastro_grid.html')
    if request.method == 'POST':
        grid = Grid(request.form['nome'], request.form['sim'])
        grid.criar(cnx)
        return redirect('/cadastro/grid')


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
    grids = [Grid("LIGHT", "AMS2"), Grid("F3", "AC"), Grid("LIGHT-AM", "ACC")]
    for grid in grids:
        grid.criar(cnx)
    with cnx.cursor() as cur:
        insert = "INSERT INTO grid_pontos (grid_id, posicao, pontos) VALUES (1, 1, 25), (1, 2, 20), (1, 3, 18), (1, 4, 16), (1, 5, 14), (1, 6, 12), (2, 1, 29), (2, 2, 25), (2, 3, 20), (2, 4, 18), (2, 5, 16), (2, 6, 14), (3, 1, 35), (3, 2, 29), (3, 3, 25), (3, 4, 22), (3, 5, 20), (3, 6, 18)"
        cur.execute(insert)
        cnx.commit()
    # Criar etapas
    etapas = [Etapa("T16-E1-LIGHT", 1, 1), Etapa("T16-E2-LIGHT", 1, 1), Etapa("T16-E1-F3", 2, 1),
              Etapa("T16-E2-F3", 2, 1), Etapa("T16-E1-LIGHT-AM", 3, 1), Etapa("T16-E2-LIGHT-AM", 3, 1)]
    for etapa in etapas:
        etapa.criar(cnx)
        etapa.pontos_etapa(cnx)
        # Pontuacao
        posicao = 1
        for piloto in pilotos:
            etapa.pontuacao(cnx, posicao, piloto.id)
            posicao += 1
        etapa.print_pontuacao(cnx)
        for grid in grids:
            grid.pontuacao_piloto(cnx)
        temporada.pontos_equipe(cnx)


if __name__ == "__main__":
    # teste()
    app.run(debug=True)
    print(1)
