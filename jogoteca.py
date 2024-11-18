from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'Puzzle', 'Ataria')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Allan Ribeiro', 'allan.ribeiro', 'senha1')
usuario2 = Usuario('Antônio Ribeiro', 'antonio.ribeiro', 'senha2')
usuario3 = Usuario('Clariça Rodrigues', 'clarica.rodrigues', 'senha3')

lista = [jogo1, jogo2, jogo3]
usuarios = {usuario1.nickname: usuario1, usuario2.nickname: usuario2, usuario3.nickname: usuario3}

app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    try:
        usuario_nome = request.form['usuario']
        senha_informada = request.form['senha']
        
        # Verifica se o usuário existe
        if usuario_nome in usuarios:
            usuario = usuarios[usuario_nome]
            
            # Verifica a senha
            if senha_informada == usuario.senha:
                session['usuario_logado'] = usuario.nickname
                flash(usuario.nickname + ' logado com sucesso!')
                proxima_pagina = request.form['proxima']
                return redirect(proxima_pagina)
            else:
                flash('Senha incorreta')
        else:
            flash('Usuário não encontrado')
    except KeyError as e:
        flash(f'Erro no formulário: campo {str(e)} ausente.')
    except Exception as e:
        flash(f'Ocorreu um erro inesperado: {str(e)}')

    # Retorna ao login em qualquer erro
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logou efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)