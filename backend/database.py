import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
# SQLALCHEMY_DATABASE_URL = os.environ.get('URL_DATABASE_POSTGRES') preparado para receber uma variável de ambiente
SQLALCHEMY_DATABASE_URL = 'postgresql://user:password@postgres/mydatabase'
# Criando o motor do banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessão de banco de dados, é quem vai exectuar as queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base para os modelos declarativos
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db # a instrução 'yield' manterá a conexão do banco aberta
    finally:
        db.close()