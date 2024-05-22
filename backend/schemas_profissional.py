from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProfissionalBase(BaseModel):

    nome: str
    area_atuacao: Optional[str]


class ProfissionalCreate(ProfissionalBase):
    pass


class ProfissionalResponse(ProfissionalBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProfissionalUpdate(BaseModel):

    nome: Optional[str] = None
    area_atuacao: Optional[str] = None

 

