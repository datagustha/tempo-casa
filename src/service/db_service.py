"""
SERVIÇO DE ACESSO AO BANCO DE DADOS
====================================

ARQUIVO: db_service.py
LOCAL: src/services/

RESPONSABILIDADE:
- Única camada do sistema que se comunica diretamente com o MySQL
- Todas as consultas ao banco passam por este arquivo
- Suporta dois bancos: SEMEAR e AGORACRED

PRINCÍPIOS:
- Nenhuma outra parte do sistema faz consultas diretas ao banco
- Todas as funções usam `with Session(engine) as session` (fecha automaticamente)
- Retornam dados em formatos simples (dicionários, listas)
- Funções de busca recebem dicionário do operador (vindo de operador_login)

ESTRUTURA DO ARQUIVO:
1. FUNÇÕES DE 
2. FUNÇÕES DE 
3. FUNÇÕES DE 
4. FUNÇÕES DE 
5. FUNÇÕES 
"""

from src.models.loginmodel import login_table
from sqlalchemy.orm import Session
from src.config.database import engine
from sqlalchemy import text

def try_connection():

    """
    TESTA CONEXAO COM O BANDO DE DADOS

    Se bem sucessidade retorna true!
    """

    # 1. abrir uma conexao

    with Session(engine) as session:

        # 2. tentar conexao 
        try:
           
            con = session.execute(text("select 1"))
            return True


        except Exception as e:
            print('\n\n----------- Connection failed ! ERROR : ', e)
            return False

def fetch_data(login_busca: str = None):
    """
    BUSCA DADOS DE LOGIN NO BANCO DE DADOS.
    
    O QUE FAZ:
    - Busca dados de um operador
    - Abre uma sessão com o banco
    - Para cada linha do Banco:
      a) Verifica se o registro já existe (evita duplicatas)
      b) Adiciona na sessão
    - Se erro, faz rollback (desfaz tudo)
 
    
    ARGS:
        login_busca: oparador input com os dados processados
    
    RETORNO:
        None (apenas printa mensagens no terminal)
    """

    if login_busca == None:
        print(f" ⚠️ Você precisa passar um login primeiro!")

    with Session(engine) as session:
        
        try:
            # 1. fazer query

            operador = session.query(login_table).filter(
                login_table.loguin ==  login_busca
            ).first()

            # 2. se não encontrar login

            if not operador:
                print(f"❌ Não foi encontrado Login para: {login_busca}")

            # 3. caso encontrado

            data = {
                "login"     : operador.loguin,
                "nome"      : operador.nome_completo,
                "admissao"  : operador.admissao,
                "banco"     : operador.banco,
                "atividade" : operador.atividade,
                "imagem"    : operador.imagem,
                "email"     : operador.email,

            }

            print(f"Operador: {login_busca} - ✅ Encontrado!\n")
            data_formst = [ print(f"{dado[0]} : {dado[1]}") for dado in ( data.items() )]
            
            return data

        except Exception as e:
            print(f"[ERRO] Erro: {str(e)}")
            return None

def fetch_dataall():
    """
    BUSCA DADOS DE LOGIN NO BANCO DE DADOS.
    
    O QUE FAZ:
    - Busca dados de todosum operadores
    - Abre uma sessão com o banco
    - Para cada linha do Banco:
      a) Verifica se o registro já existe (evita duplicatas)
      b) Adiciona na sessão
    - Se erro, faz rollback (desfaz tudo)
 
    
    ARGS:
        login_busca: oparador input com os dados processados
    
    RETORNO:
        list: Lista de dicionários, cada um com os dados de um operador
              Exemplo: [
                  {'login': '2552GUSTHAVO', 'nome': 'LUIZ...', ...},
                  {'login': '2552VIVIAN', 'nome': 'VIVIAN...', ...},
              ]
    """


    with Session(engine) as session:
        
        try:
            # 1. fazer query
            # Busca TODOS os operadores
            operadores  = session.query(login_table).all()
            # 2. se não encontrar login

            if not operadores:
                print(f"❌ Nenhum operador encontrado!")
                return []

            # Lista para guardar todos os operadores
            lista_operadores = []

            for operador in operadores:

                admissao_valida = (
                    operador.atividade == "ativo" and 
                    operador.admissao is not None and
                    operador.admissao != "" and
                    operador.admissao not in ['0000-00-00', '0000/00/00']
                )

                if operador.atividade == "ativo" and admissao_valida:

                    data = {
                        "login"      : operador.loguin,
                        "nome"       : operador.nome_completo,
                        "admissao"   : operador.admissao,
                        "aniversario": operador.aniversario,
                        "banco"      : operador.banco,
                        "atividade"  : operador.atividade,
                        "imagem"     : operador.imagem,
                        "email"      : operador.email,
                        

                    }
                    lista_operadores.append(data)

            print(f"✅ {len(lista_operadores)} operador(es) encontrado(s)!")
            return lista_operadores
            

        except Exception as e:
            print(f"[ERRO] Erro: {str(e)}")
            return None


