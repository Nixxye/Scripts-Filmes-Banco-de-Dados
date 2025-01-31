import pandas as pd
import os
import re
from unidecode import unidecode

import pandas as pd
import os
import re
from unidecode import unidecode

# Função para aplicar as transformações em todas as colunas
def aplicar_transformacoes(df):
    # Para cada coluna do DataFrame
    for coluna in df.columns:
        # Aplicar as transformações se a coluna for do tipo string
        if df[coluna].dtype == 'object':
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

# Definir o caminho da pasta onde estão os arquivos CSV
pasta = "Original/Bilheteria"

# Obter todos os arquivos .csv na pasta
arquivos_csv = [f for f in os.listdir(pasta) if f.endswith('.csv')]

# Inicializar uma lista para armazenar os DataFrames
df_list = []

# Ler cada arquivo CSV e adicionar ao DataFrame
for arquivo in arquivos_csv:
    # Construir o caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    # Ler o arquivo CSV
    df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8', low_memory=False, dtype={'REGISTRO_SALA': str})
    
    # Adicionar o DataFrame à lista
    df_list.append(df)

# Concatenar todos os DataFrames em um único DataFrame
df_completo = pd.concat(df_list, ignore_index=True)

# Converter DATA_EXIBICAO para datetime e criar a coluna MES
df_completo['DATA_EXIBICAO'] = pd.to_datetime(df_completo['DATA_EXIBICAO'], format='%d/%m/%Y', errors='coerce')
df_completo['ANO'] = df_completo['DATA_EXIBICAO'].dt.year  # Extrair o ano

# Garantir que PUBLICO seja numérico (convertendo valores inválidos para 0)
df_completo['PUBLICO'] = pd.to_numeric(df_completo['PUBLICO'], errors='coerce').fillna(0)

# Agrupar por mês, título original e registro da sala, somando o público
df_agrupado = df_completo.groupby(
    ['TITULO_ORIGINAL', 'REGISTRO_SALA'], as_index=False
).agg({
    'ANO': 'first',                  # Mostrar o primeiro ANO
    'PUBLICO': 'sum',                # Somar a coluna PUBLICO
    'TITULO_BRASIL': 'first',        # Manter a primeira ocorrência
    'PAIS_OBRA': 'first'             # Manter a primeira ocorrência
})

# Renomear as colunas do DataFrame resultante
df_agrupado = df_agrupado.rename(columns={
    'ANO': 'Ano',
    'TITULO_ORIGINAL': 'Titulo_Original',
    'TITULO_BRASIL': 'Titulo_pt/br',
    'PAIS_OBRA': 'Pais_Obra',
    'REGISTRO_SALA': 'Registro_Sala',
    'PUBLICO': 'Publico'
})

df_agrupado = aplicar_transformacoes(df_agrupado)
df_agrupado.columns.values[0] = 'Id_Bilheteria'
# Salvar em um novo CSV
arquivoSaida = "Novo/Bilheteria/Bilheteria.csv"
df_agrupado.to_csv(arquivoSaida, sep=',')
print(f"Arquivo agrupado salvo em {arquivoSaida}")