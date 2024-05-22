from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas_profissional import ProfissionalUpdate, ProfissionalCreate
from models import ProfissionalModel

def get_profissional(db: Session, id_prossional: int):
    """
    função que recebe um id e retorna somente ele
    """
    return db.query(ProfissionalModel).filter(ProfissionalModel.id == id_prossional).first()

def get_profissional_name(db: Session, nome: str):
    """
    função que recebe um nome e retorna somente ele
    """
    return db.query(ProfissionalModel).filter(ProfissionalModel.nome == nome).first()

def get_profissionais(db: Session):
    """
    função que retorna todos os elementos
    """
    return db.query(ProfissionalModel).all()

def create_profissional(db: Session, profissional: ProfissionalCreate):
    """
    função que insere um novo cliente no banco
    """
    # Criar novo registro
    db_novo_registro = ProfissionalModel(**profissional.model_dump())
    db.add(db_novo_registro)
    db.commit()
    db.refresh(db_novo_registro)
    return db_novo_registro

def delete_profissional(db: Session, id_profissional: int):
    """
    função que deleta um cliente no banco
    """
    db_registro_del = db.query(ProfissionalModel).filter(ProfissionalModel.id == id_profissional).first()
    db.delete(db_registro_del)
    db.commit()
    return db_registro_del

def update_profissional(db: Session, id_profissional: int, profissional: ProfissionalUpdate):
    """
    função que atualiza um agendamento específico
    """
    db_registro_update = db.query(ProfissionalModel).filter(ProfissionalModel.id == id_profissional).first()

    if db_registro_update is None:
        return None

    if profissional.nome is not None:
        db_registro_update.nome = profissional.nome
    if profissional.area_atuacao is not None:
        db_registro_update.area_atuacao = profissional.area_atuacao
 
    db.commit()
    return db_registro_update