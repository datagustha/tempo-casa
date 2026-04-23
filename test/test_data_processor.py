"""
Ambiente de teste funcoes
"""
#bibliotecas
import os
import sys

# Para começar o teste precisamos voltar a raiz do projeto

# 1. Pegar o local atual do arquivo
file_current = os.path.abspath(__file__)
# print(f"current file:  {file_current}")

# 2. voltar para pasta do arquivo
level_path = os.path.dirname(file_current)
# print(f"current file path:  {level_path}")

# 3. voltar para pasta raiz
source_path = os.path.dirname(level_path)
# print(f"source file path:  {source_path}")

# 4. adcionar path no sys
sys.path.append(source_path)

# 5. importando funcoes
from src.analysis.data_processor import _processar_arquivo, _processar_arquivo_data
from src.service.db_service import fetch_dataall


# def test_processar_data():

#     # 1. buscar login

#     login_busca = "2552GUSTHAVO"
#     login = fetch_data(login_busca)

#     if login:
#         # print(type(login))
#         df = _processar_arquivo_data(login)
#         print(df)

#     assert login is not None


def test_processar_dataall():

    # 1. buscar login

    operadores = fetch_dataall()

    if operadores:
        # print(type(login))
        df = _processar_arquivo(operadores)
        print(df)
        print(df.columns)

    assert operadores is not None