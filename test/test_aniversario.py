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

# 5. funcoes uso

from src.service.analytics_service import _aniversario
from datetime import date

def test_testar_niver():

    hoje = date(2026,4,23)
    niver = date(2000,4,25)

    resultado = _aniversario(
        hoje,
        "Luiz Gusthavo",
        niver
    )

    if resultado:
        print(resultado)

    assert resultado is not None