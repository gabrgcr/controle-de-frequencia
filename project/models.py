# coding: utf-8
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, text, false, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DiaLetivo(Base):
    __tablename__ = 'dia_letivo'
    __table_args__ = (
        Index('LETIVO_UNICO', 'dia', 'mes', 'ano', unique=True),
    )

    id = Column(Integer, primary_key=True, unique=True)
    dia = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.dia}/{self.mes}/{self.ano}'


class Turma(Base):
    __tablename__ = 'turma'
    __table_args__ = (
        Index('turma_unico', 'ano_letivo', 'turma', unique=True),
    )

    turma = Column(String(2, 'utf8_bin'), nullable=False)
    ano_letivo = Column(String(4, 'utf8_bin'), nullable=False)
    id = Column(Integer, primary_key=True, unique=True)


class Usuario(Base, UserMixin):
    __tablename__ = 'usuario'

    username = Column(String(100, 'utf8_bin'), primary_key=True)
    password = Column(String(32, 'utf8_bin'), nullable=False)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    tipo_usuario = Column(String(45, 'utf8_bin'), nullable=False)
    nome = Column(String(200, 'utf8_bin'), nullable=False)

    def get_id(self):
        return str(self.username)


class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column(Integer, primary_key=True, unique=True)
    nome = Column(String(200, 'utf8_bin'))
    fk_turma = Column(ForeignKey('turma.id'), nullable=False, index=True)

    turma = relationship('Turma')


class ListaPresenca(Base):
    __tablename__ = 'lista_presenca'

    fk_aluno = Column(ForeignKey('aluno.id'), primary_key=True, nullable=False, index=True)
    fk_dia_letivo = Column(ForeignKey('dia_letivo.id'), primary_key=True, nullable=False, index=True)
    presente = Column(TINYINT, nullable=False)
    fk_usuario = Column(ForeignKey('usuario.username'), nullable=False, index=True)

    aluno = relationship('Aluno')
    dia_letivo = relationship('DiaLetivo')
    usuario = relationship('Usuario')


class Alerta(Base):
    __tablename__ = 'alertas'
    __table_args__ = (
        ForeignKeyConstraint(['fk_dia_letivo', 'fk_aluno'],
                             ['lista_presenca.fk_dia_letivo', 'lista_presenca.fk_aluno']),
        Index('fk_alertas_lista_presenca1_idx', 'fk_dia_letivo', 'fk_aluno')
    )

    fk_dia_letivo = Column(ForeignKey('dia_letivo.id'), primary_key=True, nullable=False)
    fk_aluno = Column(ForeignKey('aluno.id'), primary_key=True, nullable=False)
    feito_aviso = Column(Boolean, nullable=False, server_default=false())
    fk_usuario_aviso = Column(ForeignKey('usuario.username'), index=True)

    usuario = relationship('Usuario')
    dia_letivo = relationship('DiaLetivo')
    aluno = relationship('Aluno')


class ResponsavelAluno(Base):
    __tablename__ = 'responsavel_aluno'

    nome = Column(String(45, 'utf8_bin'))
    relacao = Column(String(45, 'utf8_bin'))
    telefone = Column(String(45, 'utf8_bin'))
    endereco = Column(String(45, 'utf8_bin'))
    id = Column(Integer, primary_key=True)
    fk_aluno = Column(ForeignKey('aluno.id'), nullable=False, index=True)

    aluno = relationship('Aluno')
