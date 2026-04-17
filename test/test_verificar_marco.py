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
from src.service.analytics_service import verificar_marco
from datetime import date

def test_marco():

    """
    funcão para busca dados no banco de dados
    """
    #  dados test
    admissao = date(2023, 4, 3) #ano #mes # dia

    # 1 mês exato
    hoje = date(2027, 4, 3)
    verificar = verificar_marco(admissao, hoje)  # ✅ ["🎉 1 mês de casa! 🎉"]
    print(verificar)


    assert verificar is not None