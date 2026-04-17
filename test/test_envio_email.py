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
from src.service.email_service import enviar_email_teste

def test_teste_email():

    destinatario = "controladoria@simfacilita.com.br"
    result = enviar_email_teste(destinatario)

    assert result is not None