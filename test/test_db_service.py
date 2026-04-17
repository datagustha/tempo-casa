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
from src.service.db_service import try_connection, fetch_data, fetch_dataall

# def test_testar_conexao():

#     """
#     funcão para testar conexao com banco de dados
#     """

#     result = testar_conexao()

#     if result:
#         print('\n\n----------- Connection successful !')

#     assert result is not None

# def test_buscar_login():

#     """
#     funcão para busca dados no banco de dados
#     """
#     login = "2552GUSTHAVO"
#     result = fetch_data(login)

#     if result:
#         print(result)

#     assert result is not None

def test_buscar_todos():

    """
    funcão para busca dados no banco de dados
    """
    # login = "2552GUSTHAVO"
    result = fetch_dataall()
    print(type(result))

    # if result:
    #     dados = [print(operador[: 3]) for operador in enumerate(result)]

    assert result is not None