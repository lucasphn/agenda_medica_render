from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from enum import Enum
from datetime import datetime, date
from typing import Optional

class HoraBase(Enum):
    hora1 = '9:00'
    hora2 = '9:30'
    hora3 = '10:00'
    hora4 = '10:30'
    hora5 = '11:00'
    hora6 = '11:30'
    hora7 = '12:00'
    hora8 = '13:30' 
    hora9 = '14:00'
    hora10 = '14:30'
    hora11 = '15:00'
    hora12 = '15:30'
    hora13 = '16:00'
    hora14 = '16:30'
    hora15 = '17:00'

class TiposAgendamento(Enum):
    tipo1 = 'Consulta'
    tipo2 = 'Retorno'
    tipo3 = 'Exames'
    tipo4 = 'Cirurgias'

class AgendaBase(BaseModel):
    data_agendada: date
    hora_agendada: str
    nome_paciente: str
    nome_medico: str
    categoria_agendamento: str
    price: PositiveFloat
    email_paciente: EmailStr
    description: Optional[str] = None

    @validator('hora_agendada')
    def check_hora(cls, v):
        if v in [item.value for item in HoraBase]:
            return v
        raise ValueError('Hora Inválida')

    @validator('categoria_agendamento')
    def check_tipos(cls, v):
        if v in [item.value for item in TiposAgendamento]:
            return v
        raise ValueError('Tipo Inválido')

class AgendaCreate(AgendaBase):
    pass 

class AgendaResponse(AgendaBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AgendaUpdate(BaseModel):

    data_agendada: Optional[date] = None
    hora_agendada: Optional[str] = None
    nome_paciente: Optional[str] = None
    nome_medico: Optional[str] = None
    categoria_agendamento: Optional[str] = None
    price: Optional[PositiveFloat] = None
    email_paciente: Optional[EmailStr] = None
    description: Optional[str] = None
 
    @validator('hora_agendada')
    def check_hora(cls, v):
        if v in [item.value for item in HoraBase]:
            return v
        raise ValueError('Hora Inválida')

    @validator('nome_medico')
    def check_medicos(cls, v):
        if v in [item.value for item in NomeMedicos]:
            return v
        raise ValueError('Nome Inválido')

    @validator('categoria_agendamento')
    def check_tipos(cls, v):
        if v in [item.value for item in TiposAgendamento]:
            return v
        raise ValueError('Tipo Inválido')

