from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean# Importamos os tipos de dados que usaremos nas colunas
from sqlalchemy.orm import declarative_base # A base declarativa cria um vínculo entre a classe Python e a tabela do banco de dados

# Criamos a Base. Todos os nossos modelos vão 'herdar' dessa Base
Base = declarative_base()

# classe da tabela danalista modelo. 
class login_table(Base):

    # O atributo __tablename__ informa ao SQLAlchemy qual é o nome exato da tabela lá no MySQL
    __tablename__ = "d_analista" # ← exatamente igual ao MySQLante

    # Definimos cada uma das colunas. A 'primary_key=True' indica que 'id' é o que diferencia uma linha da outra (tipo um CPF único)
    # Autoincrement=True significa que o próprio banco vai adicionar +1 a cada nova linha

    ID_analista = Column(Integer, primary_key=True)
    loguin = Column(String(255))
    nome_completo = Column(String(255)) # ← nome completo pessoa
    jornada = Column(String(255))    # ← coluna legada
    turno = Column(String(255))      # ← turno do operador (M=Manhã, T=Tarde, N=Noite)
    admissao = Column(String(255))   # ← data
    aniversario = Column(Date)
    banco = Column(String(255))      # ← 'SEMEAR', 'AGORACRED' ou 'ADM'
    atividade = Column(String(255))  # ← se está ativo ou não
    imagem = Column(String(255))     # ← imagem do operador
    email = Column(String(255))      # ← email operador
    
   
