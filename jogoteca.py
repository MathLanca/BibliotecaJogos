from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
from models import Jogo, Usuario
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = MySQL(app)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo', methods=['POST', ])
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)
    ## Obtendo arquivo upado
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{jogo.id}.jpg')
    return redirect(url_for('index'))


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo='Cadastre-se')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    id = request.form['id']
    senha = request.form['senha']
    if len(senha) > 8:
        flash('A senha deve ter até 8 caracteres')
    usuario = Usuario(id, nome, senha)
    usuario_dao.salvar(usuario)
    flash('Usuario cadastrado com sucesso!')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editar jogo', jogo=jogo, capa_jogo=f'capa{id}.jpg')


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/observar/<int:id>')
def observar(id):
    jogo = jogo_dao.busca_por_id(id)
    return render_template('observar.html', titulo='Ver Jogo', jogo=jogo, capa_jogo=f'capa{id}.jpg')


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:

        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha incorreta, tente novamete!')
            return redirect(url_for('login'))
    else:
        flash('nome de usuario incorreto, tente novamente!')
        return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuario logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


app.run(debug=True)
