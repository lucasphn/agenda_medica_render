from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime, date
from typing import Optional
import re

def is_valid_cpf(cpf: str) -> bool:
    return re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf) is not None

class ClienteBase(BaseModel):

    nome: str
    data_nascimento: Optional[date]
    cpf: str
    uf: Optional[str]
    cidade: Optional[str]
    bairro: Optional[str]
    rua: Optional[str]
    numero: Optional[str]
    email: Optional[EmailStr]
    telefone: Optional[str]


class ClienteCreate(ClienteBase):
    # impedindo que o nome e cpf fiquem em branco
    @validator('nome', 'cpf')
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('O campo nome e/ou cpf não podem estar vazios.')
        return value
    
    # impedindo que o cpf não esteja no padrão correto
    @validator('cpf')
    def validate_cpf(cls, value, values, **kwargs):
        if not is_valid_cpf(value):
            raise ValueError('CPF inválido')
        return value

class ClienteResponse(ClienteBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ClienteUpdate(BaseModel):

    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    cpf: Optional[str] = None
    uf: Optional[str] = None
    cidade: Optional[str] = None
    bairro: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
 

