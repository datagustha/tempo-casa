"""
SERVIÇO DE CÁLCULOS E INDICADORES
==================================

ARQUIVO: analytics_service.py
LOCAL: src/services/

Este módulo contém funções para calcular tempo de casa e
verificar marcos importantes (1 mês, 6 meses, aniversários).
"""

import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta


# ================================================================
# 1. FUNÇÃO PARA VERIFICAR MARCOS (1 mês, 6 meses, aniversário)
# ================================================================

def verificar_marco(data_admissao: date, data_hoje: date) -> list:
    """
    Verifica se a data atual corresponde a um marco importante da data de admissão.
    
    Marcos considerados:
        - 1 mês exato de casa (mesmo dia no mês seguinte)
        - 6 meses exatos de casa (mesmo dia, 6 meses depois)
        - Cada ano completo (aniversário de admissão)
    
    Args:
        data_admissao (date): Data de entrada do operador na empresa
        data_hoje (date): Data atual (geralmente date.today())
    
    Returns:
        list: Lista de strings com as mensagens dos marcos atingidos.
              Retorna lista vazia se nenhum marco foi atingido.
    
    Examples:
        >>> from datetime import date
        >>> admissao = date(2023, 4, 3)
        >>> 
        >>> # 1 mês depois
        >>> verificar_marco(admissao, date(2023, 5, 3))
        ['🎉 1 mês de casa! 🎉']
        >>> 
        >>> # 6 meses depois
        >>> verificar_marco(admissao, date(2023, 10, 3))
        ['🎉 6 meses de casa! 🎉']
        >>> 
        >>> # 1 ano depois
        >>> verificar_marco(admissao, date(2024, 4, 3))
        ['🎉 1 ano(s) de casa! 🎉']
        >>> 
        >>> # 2 anos depois
        >>> verificar_marco(admissao, date(2025, 4, 3))
        ['🎉 2 ano(s) de casa! 🎉']
        >>> 
        >>> # Dia normal (sem marco)
        >>> verificar_marco(admissao, date(2024, 5, 15))
        []
    """

    
    marcos = []
    
    # ============================================================
    # 1. VERIFICAÇÃO DE 1 MÊS EXATO
    # ============================================================
    # Soma 1 mês à data de admissão usando relativedelta
    # Esta biblioteca respeita diferenças de dias entre meses
    # Ex: 31/01 + 1 mês = 28/02 (ou 29/02 em ano bissexto)
    # ============================================================
    if data_hoje == data_admissao + relativedelta(months=1):
        marcos.append("🎉 1 mês de casa! 🎉")
    
    # ============================================================
    # 2. VERIFICAÇÃO DE 6 MESES EXATO
    # ============================================================
    # Soma 6 meses à data de admissão
    # Útil para marcos semestrais
    # ============================================================
    if data_hoje == data_admissao + relativedelta(months=6):
        marcos.append("🎉 6 meses de casa! 🎉")
    
    # ============================================================
    # 3. VERIFICAÇÃO DE ANIVERSÁRIO (CADA ANO)
    # ============================================================
    # Condições para ser aniversário de admissão:
    #   1. Dia igual ao da admissão
    #   2. Mês igual ao da admissão
    #   3. Ano maior que o da admissão (já passou pelo menos 1 ano)
    # ============================================================
    if (data_hoje.day == data_admissao.day and 
        data_hoje.month == data_admissao.month and
        data_hoje.year > data_admissao.year):
        
        # Calcula quantos anos completou
        anos = data_hoje.year - data_admissao.year
        marcos.append(f"🎉 {anos} ano(s) de casa! 🎉")
    
    return marcos


# ================================================================
# 2. FUNÇÃO PARA CALCULAR TEMPO DE CASA
# ================================================================

def calcular_tempo_casa(df: pd.DataFrame) -> dict:
    """
    Calcula o tempo de casa do operador a partir de um DataFrame com a data de admissão.
    
    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'admissao'
    
    Returns:
        dict: Dicionário com as seguintes chaves:
            - dias (int): Total de dias desde a admissão
            - meses (int): Total de meses (aproximado, considerando 30 dias)
            - anos (int): Total de anos (aproximado, considerando 365 dias)
            - data_admissao (date): Data de admissão original
            - dias_restantes_proximo_ano (int): Dias faltando para completar 1 ano
    
    Example:
        >>> df = pd.DataFrame([{'admissao': '2023-04-03'}])
        >>> calcular_tempo_casa(df)
        {
            'dias': 1110,
            'meses': 37,
            'anos': 3,
            'data_admissao': datetime.date(2023, 4, 3),
            'dias_restantes_proximo_ano': 350
        }
    """
    hoje = date.today()
    admissao = df["admissao"].iloc[0].date()
    
    # Diferença em dias
    dias = (hoje - admissao).days
    
    # Conversões aproximadas (30 dias = 1 mês, 365 dias = 1 ano)
    meses = dias // 30
    anos = dias // 365
    
    return {
        "dias": dias,
        "meses": meses,
        "anos": anos,
        "data_admissao": admissao,
        "dias_restantes_proximo_ano": 365 - (dias % 365)
    }