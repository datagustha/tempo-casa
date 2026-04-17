"""
data_processor.py
Camada de análise: lê os arquivos brutos de cada banco ,
aplica transformações com Pandas, e retorna os DataFrames prontos.

Paths relativos ao projeto — compatível com VPS Ubuntu e Windows.
"""

import os
import pathlib
import pandas as pd
import numpy as numpy
from IPython.display import display


def _processar_arquivo(dados: list):
    """
    Lê e transforma uma lista de dicionários.
    Retorna um DataFrame tratado, ou None em caso de falha.
    """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    print(f"\n  📄 Processando: arquivo!\n")

    try:
        # 1. Leitura
        df = pd.DataFrame(dados)

        if df.empty:
            print("❌ Sem dados!")
            return None

        # 2. TRATAR DATAS INVÁLIDAS
        df["admissao"] = df["admissao"].replace(
            ['0000/00/00', '0000-00-00', '', None], 
            pd.NA
        )
        df["admissao"] = pd.to_datetime(df["admissao"], errors='coerce').dt.date
        df = df[df['admissao'].notna()]

        # 3. Manter somente ativos
        df = df[df["atividade"] == "ativo"]

        # 4. 🔥 TRATAR IMAGEM: Substituir NaN por string vazia
        df["imagem"] = df["imagem"].fillna("").replace([pd.NA, None, float('nan')], "")
        
        # Se quiser, também pode converter para string explicitamente
        df["imagem"] = df["imagem"].astype(str)
        df.loc[df["imagem"] == "nan", "imagem"] = ""

        # 5. Ordenar por nome
        df = df.sort_values(by="nome").reset_index(drop=True)

        return df

    except Exception as e:
        print(f"  ❌ Erro ao processar: {e}")
        return None

def _processar_arquivo_data(dados):

    """
    Processa o arquivo de um banco específico.
    e retorna o DataFrame final.

    Args:
        dados: retornar a data da processar arquivos
        nome: retornar Nome completo do operador
    """

    print(f"\n{'─' * 50}")
    print(f"▶ Processando dados: nome.upper()")
    print(f"{'─' * 50}")

    try:
        df = _processar_arquivo(dados)

        # data da admissao
        data = df["admissao"].iloc[0]

        print(f'Data para verificação: {data}')

        return data

    except Exception as e:
        print(f"  ❌ Erro ao processar: {e}")
        return None

    


