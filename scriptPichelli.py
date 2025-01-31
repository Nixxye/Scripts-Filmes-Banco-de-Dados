# Mudar no MR o Id_Filme_Av para Filme

import pandas as pd
import string
import os
import re
from unidecode import unidecode

# Função para aplicar as transformações em todas as colunas
def aplicar_transformacoes(df):
    # Para cada coluna do DataFrame
    for coluna in df.columns:
        # Aplicar as transformações se a coluna for do tipo string
        if df[coluna].dtype == 'object':
            # Substituir underscore por espaço
            df[coluna] = df[coluna].str.replace("_", " ", regex=False)
            df[coluna] = df[coluna].str.replace("-", " ", regex=False)
            # Remover aspas simples, duplas e outras pontuações
            if coluna != 'creationDate':
                df[coluna] = df[coluna].str.replace(f"[{string.punctuation}]", "", regex=True) 
            # Remover espaços no início e no fim
            df[coluna] = df[coluna].str.strip()
            # Colocar tudo em minúsculo
            df[coluna] = df[coluna].str.lower()
            # Remover acentos
            df[coluna] = df[coluna].apply(lambda x: unidecode(x) if isinstance(x, str) else x)
            # Substituir espaço por hífen
            df[coluna] = df[coluna].str.replace(" ", "-", regex=False)
            # Corrigir múltiplos hífens para um único hífen
            df[coluna] = df[coluna].str.replace(r'-+', '-', regex=True)
    return df

tabelaRotten = "Original/Avaliacao/rotten_tomatoes_movie_reviews.csv"
tabelaSaida = "Novo/Avaliacao/Avaliacao.csv"
dfRotten = pd.read_csv(tabelaRotten, sep=',', encoding='utf-8', low_memory=False)
dfRotten = aplicar_transformacoes(dfRotten)

dfRotten['reviewState'] = dfRotten['reviewState'].replace({'fresh':1, 'rotten':0}).astype(int)
dfRotten = dfRotten[dfRotten.apply(lambda x: len(x) >= 4, axis=1)]
dfRotten[['year', 'month', 'day']] = dfRotten['creationDate'].str.split('-', expand= True)
dfRotten = dfRotten[['id', 'reviewId', 'year', 'month', 'day', 'criticName', 'isTopCritic', 'reviewState', 'reviewText']]
dfRotten = dfRotten.rename(columns={
    'id' : 'Filme',
    'reviewId' : 'Id',
    'reviewState' : 'Nota'
})

dfRotten.to_csv(tabelaSaida, sep=',', index=False)