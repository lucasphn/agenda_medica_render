from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import AgendaResponse, AgendaUpdate, AgendaCreate
from schemas_cliente import ClienteResponse, ClienteUpdate, ClienteCreate
from schemas_profissional import ProfissionalResponse, ProfissionalUpdate, ProfissionalCreate
from typing import List
from crud import (create_agendamento, get_agendamentos, get_agendamento, get_agendamento_nome, get_agendamento_profissional, delete_agendamento, update_agendamento)
from crud_cliente import (create_cliente, get_clientes, get_cliente,get_cliente_name, delete_cliente, update_cliente)
from crud_profissional import (create_profissional, get_profissionais, get_profissional,get_profissional_name, delete_profissional, update_profissional)

'''
Aqui neste arquivo vamos transformar todas as nossas funções do crud em requisições de uma API que irá se comunicar com o nosso banco de dados
'''

router = APIRouter()


@router.post("/agenda/", response_model=AgendaResponse)
def create_agenda_route(agendamento: AgendaCreate, db: Session = Depends(get_db)):
    return create_agendamento(db=db, agenda=agendamento)


@router.get("/agenda/", response_model=List[AgendaResponse])
def read_all_agenda_route(db: Session = Depends(get_db)):
    agendamentos = get_agendamentos(db)
    return agendamentos

# SELECT de um agendamento específico
@router.get("/agenda/id/{id_agendamento}", response_model=AgendaResponse)
def read_agendamento_route(id_agendamento: int, db: Session = Depends(get_db)):
    db_agendamento = get_agendamento(db, id_agendamento=id_agendamento)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado. Tente outro código, por favor.")
    return db_agendamento

# Lista de Agendamento por nome do paciente
@router.get("/agenda/nome/{nome_paciente}", response_model=List[AgendaResponse])
def read_agendamento_nome_route(nome_paciente: str, db: Session = Depends(get_db)):
    db_agendamento = get_agendamento_nome(db, nome_paciente=nome_paciente)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado. Tente outro código, por favor.")
    return db_agendamento
# Lista de Agendamento por profissional
@router.get("/agenda/profissional/{nome_profissional}", response_model=List[AgendaResponse])
def read_agendamento_profissional_route(nome_profissional: str, db: Session = Depends(get_db)):
    db_agendamento = get_agendamento_profissional(db, nome_profissional=nome_profissional)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado. Tente outro código, por favor.")
    return db_agendamento


# DELETE de um agendamento específico
@router.delete("/agenda/{id_agendamento}", response_model=AgendaResponse)
def delete_agendamento_route(id_agendamento: int, db: Session = Depends(get_db)):
    db_agendamento = delete_agendamento(db, id_agendamento=id_agendamento)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado. Tente outro código, por favor.")
    return db_agendamento

# UPDATE de um agendamento específico
@router.put("/agenda/{id_agendamento}", response_model=AgendaResponse)
def update_agendamento_route(id_agendamento: int, agenda: AgendaUpdate, db: Session = Depends(get_db)):
    db_agendamento = update_agendamento(db, id_agendamento=id_agendamento, agenda=agenda)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado. Tente outro código, por favor.")
    return db_agendamento

## ************************************** INICIANDO API CADASTRO DE CLIENTE ************************************************************

@router.post("/clientes/", response_model=ClienteResponse)
def create_cliente_route(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return create_cliente(db=db, cliente=cliente)

@router.get("/clientes/", response_model=List[ClienteResponse])
def read_all_cliente_route(db: Session = Depends(get_db)):
    clientes = get_clientes(db)
    return clientes


# SELECT de um cliente específico por ID
@router.get("/clientes/id/{id_cliente}", response_model=ClienteResponse)
def read_cliente_route(id_cliente: int, db: Session = Depends(get_db)):
    db_cliente = get_cliente(db, id_cliente=id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado. Tente outro código, por favor.")
    return db_cliente

# SELECT de um cliente específico por nome
@router.get("/clientes/nome/{nome_cliente}", response_model=ClienteResponse)
def read_cliente_nome_route(nome_cliente: str, db: Session = Depends(get_db)):
    db_cliente = get_cliente_name(db, nome=nome_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado. Tente outro código, por favor.")
    return db_cliente

# DELETE de um cliente específico
@router.delete("/clientes/{id_cliente}", response_model=ClienteResponse)
def delete_cliente_route(id_cliente: int, db: Session = Depends(get_db)):
    db_cliente = delete_cliente(db, id_cliente=id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado. Tente outro código, por favor.")
    return db_cliente

# UPDATE de um cliente específico
@router.put("/clientes/{id_cliente}", response_model=ClienteResponse)
def update_cliente_route(id_cliente: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = update_cliente(db, id_cliente=id_cliente, cliente=cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado. Tente outro código, por favor.")
    return db_cliente

## ************************************** INICIANDO API CADASTRO DE PROFISSIONAL ************************************************************

@router.post("/profissional/", response_model=ProfissionalResponse)
def create_profissional_route(profissional: ProfissionalCreate, db: Session = Depends(get_db)):
    return create_profissional(db=db, profissional=profissional)

@router.get("/profissional/", response_model=List[ProfissionalResponse])
def read_all_profissional_route(db: Session = Depends(get_db)):
    profissional = get_profissionais(db)
    return profissional


# SELECT de um registro específico por ID
@router.get("/profissional/id/{id_profissional}", response_model=ProfissionalResponse)
def read_profissional_route(id_profissional: int, db: Session = Depends(get_db)):
    db_profissional = get_profissional(db, id_profissional=id_profissional)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado. Tente outro código, por favor.")
    return db_profissional

# SELECT de um registro específico por nome
@router.get("/profissional/nome/{nome_profissional}", response_model=ProfissionalResponse)
def read_profissional_nome_route(nome_profissional: str, db: Session = Depends(get_db)):
    db_profissional = get_profissional_name(db, nome=nome_profissional)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado. Tente outro código, por favor.")
    return db_profissional

# DELETE de um registro específico
@router.delete("/profissional/{id_profissional}", response_model=ProfissionalResponse)
def delete_profissional_route(id_profissional: int, db: Session = Depends(get_db)):
    db_profissional = delete_profissional(db, id_profissional=id_profissional)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado. Tente outro código, por favor.")
    return db_profissional

# UPDATE de um registro específico
@router.put("/profissional/{id_profissional}", response_model=ProfissionalResponse)
def update_profissional_route(id_profissional: int, profissional: ProfissionalUpdate, db: Session = Depends(get_db)):
    db_profissional = update_profissional(db, id_profissional=id_profissional, profissional=profissional)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado. Tente outro código, por favor.")
    return db_profissional