import datetime

from flask import Flask, render_template, redirect, request, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

import repo

app = Flask(__name__)
app.secret_key = 'secret'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)


# z9cr7NBvKwHZIqW3


@app.route('/', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if repo.check_user_password(username, password):
            logged_user = repo.get_users_by_username(username)
            flash('Login realizado com sucesso!', category='success')
            login_user(logged_user, remember=True)
            if logged_user.tipo_usuario == 'ADM':
                return redirect('/alerta')
            else:
                return redirect('/frequencia/0')
        else:
            flash('Usuário ou senha inválidos!', category='error')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/turma')
@login_required
def turmas():
    return render_template('turma.html', turmas=repo.get_all_turmas())


@app.route('/turma/delete/<int:id>', methods=['POST'])
@login_required
def delete_turma(id: int):
    turma = repo.get_turma_by_id(id)
    repo.delete_turma(turma)
    return redirect('/turma')


@app.route('/turma/save/', methods=['POST'])
@login_required
def save_turma():
    turma = request.form['nome_turma']
    ano_letivo = request.form['ano_letivo']
    repo.create_turma(ano_letivo=ano_letivo, turma=turma.upper())
    return redirect('/turma')


@app.route('/alerta', methods=['GET'])
@login_required
def alerta():
    alertas = repo.get_all_alertas()
    return render_template('alerta.html', alertas=alertas)


@app.route('/alerta/check/<int:fk_aluno>/<int:fk_dia_letivo>', methods=['POST'])
@login_required
def check_alerta(fk_aluno: int, fk_dia_letivo: int):
    repo.check_alerta_by_id(fk_aluno, fk_dia_letivo)
    return redirect('/alerta')


@app.route('/alunos', methods=['GET', 'POST'])
@login_required
def alunos():
    if request.method == 'GET':
        return render_template('alunos.html', turmas=repo.get_all_turmas_vigentes(), alunos=repo.get_all_alunos())
    else:
        nome = request.form['nome']
        id_turma = request.form['id_turma']
        repo.create_aluno(nome=nome, fk_turma=int(id_turma))
        return redirect('/alunos')


@app.route('/responsaveis/<int:id>', methods=['GET', 'POST'])
@login_required
def responsaveis(id: int):
    if request.method == 'GET':
        return render_template('responsaveis.html',
                               responsaveis=repo.get_responsaveis_by_aluno(id),
                               aluno=repo.get_aluno_by_id(id))
    else:
        nome = request.form['nome']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        relacao = request.form['relacao']

        repo.create_responsavel(nome=nome, telefone=telefone, relacao=relacao, fk_aluno=id, endereco=endereco)
        return redirect('/responsaveis/' + str(id))


@app.route('/responsaveis/delete/<int:id>', methods=['POST'])
@login_required
def delete_responsavel(id: int):
    responsavel = repo.get_responsavel_by_id(id)
    repo.delete_responsavel(responsavel)
    return redirect('/responsaveis/' + str(responsavel.fk_aluno))


@app.route('/frequencia/<int:id>', methods=['GET', 'POST'])
@login_required
def frequencia(id: int):
    lista_preenchida = False
    if id == 0:
        alunos = None
        turma_atual = None
    else:
        turma_atual = repo.get_turma_by_id(id)
        alunos = repo.get_all_alunos_by_turma(id)
        lista_preenchida = len(repo.get_lista_presenca_by_dia_letivo_and_turma(repo.get_dia_letivo_atual().id, id)) > 0
        if len(alunos) == 0:
            alunos = None
    if request.method == 'POST':
        if len(alunos) != 0:
            for aluno in alunos:
                presente = request.form[str(aluno.id)] == '1'
                repo.create_lista_presenca(fk_aluno=aluno.id,
                                           fk_dia_letivo=repo.get_dia_letivo_atual().id,
                                           presente=presente,
                                           fk_usuario=current_user.username)
                if not presente:
                    repo.create_alerta(fk_aluno=aluno.id,
                                       fk_dia_letivo=repo.get_dia_letivo_atual().id,
                                       fk_usuario_aviso=current_user.username)
        return redirect('/frequencia/' + str(id))
    return render_template('frequencia.html',
                           dia_letivo=repo.get_dia_letivo_atual(),
                           alunos=alunos,
                           turmas=repo.get_all_turmas_vigentes(), turma_atual=turma_atual,
                           lista_preenchida=lista_preenchida)


@app.route('/dia_letivo/abrir', methods=['POST'])
@login_required
def abrir_dia_letivo():
    repo.create_dia_letivo()
    return redirect('/frequencia/0')


@app.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    if request.method == 'POST':
        if request.form['senha'] != request.form['confirmar_senha']:
            flash('As senhas não conferem!', category='error')
        else:
            username = request.form['username']
            password = request.form['senha']
            nome = request.form['nome']
            tipo_usuario = request.form['tipo_usuario']
            repo.create_user(username=username, password=password, nome=nome, tipo_usuario=tipo_usuario)
        return redirect('/usuarios')
    return render_template('usuarios.html')


@app.route('/historico/<int:turma>/<int:dia_letivo>', methods=['GET'])
@login_required
def historico(turma: int, dia_letivo: int):
    lista_presenca = repo.get_lista_presenca_by_dia_letivo_and_turma(dia_letivo, turma)
    return render_template('historico.html', turmas=repo.get_all_turmas(),
                           dias_letivos=repo.get_all_dias_letivos(),
                           lista_presenca=lista_presenca,
                           turma_id=turma, dia_id=dia_letivo)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return repo.get_users_by_username(user_id)


if __name__ == '__main__':
    app.run(debug=False)
