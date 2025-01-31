import pandas as pd
import os
import re
from unidecode import unidecode

colunasAPreservar = ['DURACAO_TOTAL_MINUTOS', 'creationDate', 'DATA_SITUACAO_SALA', 'DATA_INICIO_FUNCIONAMENTO_SALA', 'DATA_SITUACAO_COMPLEXO']

# Função para aplicar as transformações em todas as colunas
def ajusta(df):
    # Para cada coluna do DataFrame
    for coluna in df.columns:
        # Aplicar as transformações se a coluna for do tipo string
        if df[coluna].dtype == 'object' and coluna not in colunasAPreservar:
            # Substituir hífen por espaço
            df[coluna] = df[coluna].str.replace("-", " ", regex=False)
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
            # Remover qualquer pontuação (exceto letras, números, espaços e hífens)
            df[coluna] = df[coluna].str.replace(r"[^\w\s-]", "", regex=True)    
    return df

# Pasta de origem
pasta_origem = "./Novo"

# Percorrer todas as subpastas
for root, _, files in os.walk(pasta_origem):
    for file in files:
        if file.endswith(".csv"):
            caminho_arquivo = os.path.join(root, file)
            
            # Carregar CSV
            df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8', low_memory=False)
            
            # Aplicar ajustes
            df = ajusta(df)
            
            # Salvar com o mesmo nome e caminho
            df.to_csv(caminho_arquivo, sep=',', index=False, encoding='utf-8')
            print(f"Arquivo processado: {'BD1_Filmes' + caminho_arquivo}")