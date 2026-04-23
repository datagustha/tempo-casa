"""
main.py — Orquestrador Principal
Segue o fluxo: 
para cada operador .
"""

import locale
import sys
import os
import pathlib

# Garante que o Python encontre os módulos src/
diretorio_raiz = pathlib.Path(__file__).resolve().parent
sys.path.append(str(diretorio_raiz))



# Carrega variáveis de ambiente do .env ANTES de qualquer import interno
from dotenv import load_dotenv
load_dotenv()

from src.service.db_service import fetch_dataall
from src.analysis.data_processor import _processar_arquivo
from src.service.analytics_service import verificar_marco
from src.service.email_service import enviar_aniversario, enviar_tempo_casa
from src.service.analytics_service import verificar_aniversario


def main():
    print("=" * 60)
    print("  FLUXO MENSAGENS AUTOMATIZADOS")
    print("=" * 60)

    # ── PASSO 1: Puxar dados ──────────────────────────────────────────────
    # retornar dados do banco de dados

    dados = fetch_dataall()

     # ── PASSO 2: Conveter dicionario para df ──────────────────────────────────────────────

    df = _processar_arquivo(dados)
    print()

    # ── PASSO 3: verificar para cada operador se comemora ──────────────────────────────────────────────
    from datetime import date
    hoje = date.today()
    print(hoje)
    

    for index, row in df.iterrows():

        nome = row["nome"]
        admissao = row["admissao"]
        aniversario = row["aniversario"]
        print(f"{index} - {nome}: Ad: {admissao} - Niver: {aniversario if aniversario else 'Não cadastrado'}")

        # verifiar se completou 

        verificar_tempo_casa = verificar_marco(admissao, hoje)
        verifica_niver = verificar_aniversario(hoje, aniversario)

        if verifica_niver:
            # pegar os dados do operador
            email = row["email"]
            nome = row["nome"]
            login = row["login"]
            msg = verifica_niver

            enviar_aniversario(
            destinatario=email,
            nome=nome,
            imagem=row.get("imagem")  # URL da foto do operador
        )

            print(f"✅ Mensagem de aniversário enviado para {email}")

            


        if verificar_tempo_casa:

            # pegar os dados do operador
            email = row["email"]
            nome = row["nome"]
            login = row["login"]
            msg = verificar_tempo_casa[0]

             # Enviar para o OPERADOR
            enviar_tempo_casa(
                destinatario=email,
                nome=nome,
                login=login,
                mensagem=msg,
                imagem = row.get("imagem")
            )

            # Enviar para o ADM (cópia)
            email_ADM = "adm@simfacilita.com.br"  # 👈 CORRIGIDO!
            enviar_tempo_casa(
                destinatario=email_ADM,
                nome=nome,
                login=login,
                mensagem=msg,
                imagem = row.get("imagem")
            )

            # Enviar para o ADM (cópia)
            email_financeiro = "financeiro@simfacilita.com.br"  # 👈 CORRIGIDO!
            enviar_tempo_casa(
                destinatario=email_financeiro,
                nome=nome,
                login=login,
                mensagem=msg,
                imagem = row.get("imagem")
            )

            print(f"  ✅ {verificar_tempo_casa[0]} enviado para {nome}")
            continue


if __name__ == "__main__":
    main()