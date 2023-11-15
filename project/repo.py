import datetime

from sqlalchemy import true

from database import session
from models import *


def get_users_by_username(username: str):
    return session.query(Usuario).filter(Usuario.username == username).first()


def check_user_password(username: str, password: str):
    user = get_users_by_username(username)
    if user is not None:
        return user.password == password
    else:
        return False


def create_username(username: str, password: str, tipo_usuario: str, nome: str):
    user = Usuario(username=username, password=password, tipo_usuario=tipo_usuario, nome=nome)
    try:
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()


def create_turma(ano_letivo: str, turma: str):
    turma = Turma(ano_letivo=ano_letivo, turma=turma)
    try:
        session.add(turma)
        session.commit()
    except Exception as e:
        session.rollback()


def create_aluno(nome: str, fk_turma: int):
    aluno = Aluno(nome=nome, fk_turma=fk_turma)
    try:
        session.add(aluno)
        session.commit()
    except Exception as e:
        session.rollback()


def create_dia_letivo(dia: int, mes: int, ano: int):
    dia_letivo = DiaLetivo(dia=dia, mes=mes, ano=ano)
    try:
        session.add(dia_letivo)
        session.commit()
    except Exception as e:
        session.rollback()


def create_lista_presenca(fk_aluno: int, fk_dia_letivo: int, presente: bool, fk_usuario: str):
    lista_presenca = ListaPresenca(fk_aluno=fk_aluno, fk_dia_letivo=fk_dia_letivo, presente=presente,
                                   fk_usuario=fk_usuario)
    try:
        session.add(lista_presenca)
        session.commit()
    except Exception as e:
        session.rollback()


def get_all_turmas():
    return session.query(Turma).order_by(Turma.turma).all()


def get_all_turmas_vigentes():
    return session.query(Turma).filter(Turma.ano_letivo == str(datetime.datetime.now().year)).order_by(Turma.turma).all()


def get_all_alunos():
    alunos = session.query(Aluno).order_by(Aluno.fk_turma.asc(), Aluno.nome.asc()).all()
    alunos.sort(key=lambda x: x.turma.turma)
    return alunos


def get_all_alertas():
    return session.query(Alerta).order_by(Alerta.feito_aviso.asc(), Alerta.fk_dia_letivo.desc()).all()


def get_all_alunos_by_turma(fk_turma: int):
    return session.query(Aluno).filter(Aluno.fk_turma == fk_turma).all()


def get_turma_by_id(id: int):
    return session.query(Turma).filter(Turma.id == id).first()


def delete_turma(turma: Turma):
    try:
        session.delete(turma)
        session.commit()
    except Exception as e:
        session.rollback()


def check_alerta_by_id(fk_aluno: int, fk_dia_letivo: int):
    alerta = session.query(Alerta).filter(Alerta.fk_aluno == fk_aluno and Alerta.fk_dia_letivo == fk_dia_letivo).update(
        {Alerta.feito_aviso: true()})
    session.commit()
    return alerta


def get_responsaveis_by_aluno(id_aluno: int):
    return session.query(ResponsavelAluno).filter(ResponsavelAluno.fk_aluno == id_aluno).all()


def get_responsavel_by_id(id: int):
    return session.query(ResponsavelAluno).filter(ResponsavelAluno.id == id).first()


def delete_responsavel(responsavel: ResponsavelAluno):
    try:
        session.delete(responsavel)
        session.commit()
    except Exception as e:
        session.rollback()


def create_responsavel(nome, telefone, relacao, fk_aluno, endereco):
    responsavel = ResponsavelAluno(nome=nome, telefone=telefone, relacao=relacao, fk_aluno=fk_aluno, endereco=endereco)
    try:
        session.add(responsavel)
        session.commit()
    except Exception as e:
        session.rollback()


def create_dia_letivo():
    dia_letivo = DiaLetivo(dia=datetime.datetime.now().day, mes=datetime.datetime.now().month,
                           ano=datetime.datetime.now().year)
    try:
        session.add(dia_letivo)
        session.commit()
    except Exception as e:
        session.rollback()


def get_dia_letivo_atual():
    return session.query(DiaLetivo).filter(DiaLetivo.dia == datetime.datetime.now().day,
                                           DiaLetivo.mes == datetime.datetime.now().month,
                                           DiaLetivo.ano == datetime.datetime.now().year).first()


def get_aluno_by_id(id):
    return session.query(Aluno).filter(Aluno.id == id).first()


def create_alerta(fk_aluno, fk_dia_letivo, fk_usuario_aviso):
    alerta = Alerta(fk_aluno=fk_aluno, fk_dia_letivo=fk_dia_letivo, fk_usuario_aviso=fk_usuario_aviso)
    try:
        session.add(alerta)
        session.commit()
    except Exception as e:
        session.rollback()


def get_lista_presenca_by_dia_letivo_and_turma(id, fk_turma):
    query = session.query(ListaPresenca).join(Aluno).join(Turma)
    return query.filter(ListaPresenca.fk_dia_letivo == id, Turma.id == fk_turma).all()


def create_user(username, password, nome, tipo_usuario):
    user = Usuario(username=username,
                   password=password,
                   tipo_usuario=tipo_usuario,
                   nome=nome)
    try:
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()


def get_all_dias_letivos():
    return session.query(DiaLetivo).order_by(DiaLetivo.ano.desc(), DiaLetivo.mes.desc(), DiaLetivo.dia.desc()).all()
