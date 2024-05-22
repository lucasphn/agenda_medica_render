from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas_cliente import ClienteUpdate, ClienteCreate
from models import ClienteModel

def get_cliente(db: Session, id_cliente: int):
    """
    função que recebe um id e retorna somente ele
    """
    return db.query(ClienteModel).filter(ClienteModel.id == id_cliente).first()

def get_cliente_name(db: Session, nome: str):
    """
    função que recebe um nome e retorna somente ele
    """
    return db.query(ClienteModel).filter(ClienteModel.nome == nome).first()

def get_clientes(db: Session):
    """
    função que retorna todos os elementos
    """
    return db.query(ClienteModel).all()

def create_cliente(db: Session, cliente: ClienteCreate):
    """
    função que insere um novo cliente no banco
    """

    # Verificação de CPF e nome duplicados pode continuar no ORM
    if db.query(ClienteModel).filter(ClienteModel.cpf == cliente.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    if db.query(ClienteModel).filter(ClienteModel.nome == cliente.nome).first():
        raise HTTPException(status_code=400, detail="Nome já cadastrado.")

    # Criar novo cliente
    db_novo_registro = ClienteModel(**cliente.model_dump())
    db.add(db_novo_registro)
    db.commit()
    db.refresh(db_novo_registro)
    return db_novo_registro

def delete_cliente(db: Session, id_cliente: int):
    """
    função que deleta um cliente no banco
    """
    db_registro_del = db.query(ClienteModel).filter(ClienteModel.id == id_cliente).first()
    db.delete(db_registro_del)
    db.commit()
    return db_registro_del

def update_cliente(db: Session, id_cliente: int, cliente: ClienteUpdate):
    """
    função que atualiza um agendamento específico
    """
    db_registro_update = db.query(ClienteModel).filter(ClienteModel.id == id_cliente).first()

    if db_registro_update is None:
        return None

    if cliente.nome is not None:
        db_registro_update.nome = cliente.nome
    if cliente.data_nascimento is not None:
        db_registro_update.data_nascimento = cliente.data_nascimento
    if cliente.cpf is not None:
        db_registro_update.cpf = cliente.cpf
    if cliente.cidade is not None:
        db_registro_update.cidade = cliente.cidade
    if cliente.bairro is not None:
        db_registro_update.bairro = cliente.bairro
    if cliente.rua is not None:
        db_registro_update.rua = cliente.rua
    if cliente.numero is not None:
        db_registro_update.numero = cliente.numero
    if cliente.email is not None:
        db_registro_update.email = cliente.email
    if cliente.telefone is not None:
        db_registro_update.telefone = cliente.telefone

    db.commit()
    return db_registro_update