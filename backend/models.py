from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from database import Base

"""
Neste arquivo você pode incluir seus schemas de banco de dados, para que o ORM possa criar as tabelas conforme sua definição.

"""



class AgendaModel(Base):
    __tablename__ = 'agenda_medica'  # esse será o nome da tabela

    id = Column(Integer, primary_key=True, index=True)
    data_agendada = Column(Date, index=True)
    hora_agendada = Column(String, index=True)
    nome_paciente = Column(String, index=True)
    nome_medico = Column(String, index=True)
    categoria_agendamento = Column(String, index=True)
    price = Column(Float, index=True)
    email_paciente = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)

class ClienteModel(Base):
    __tablename__ = 'cadastro_cliente' 

    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String, index=True)
    data_nascimento = Column(Date, index=True)
    cpf = Column(String, index=True)
    uf = Column(String, index=True)
    cidade = Column(String, index=True)
    bairro = Column(String, index=True)
    rua = Column(String, index=True)
    numero = Column(String, index=True)
    email = Column(String, index=True)
    telefone = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default = func.now(), index=True)

class ProfissionalModel(Base):
    __tablename__ = 'cadastro_profissional'

    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String, index=True)
    area_atuacao = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default = func.now(), index=True)   