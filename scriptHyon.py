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
            # Substituir hífen por espaço
            df.loc[:, coluna] = df[coluna].str.replace("-", " ", regex=False)
            # Remover aspas duplas e outras pontuações
            df.loc[:, coluna] = df[coluna].str.replace(r'[“”"]', "", regex=True)
            if coluna != 'DURACAO_TOTAL_MINUTOS':
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

# tabelaObras = "Original/Filme/obras-nao-pub-estrangeiras-2018.csv"
tabelaRotten = "Original/Filme/rotten_tomatoes_movies.csv"
tabelaSaida = "Novo/Filme/Filme.csv"
tabelaLancamento = "Original/Filme/lancamentos-comerciais-por-distribuidoras.csv"
diretorioObras = "Original/Filme/"

dfRotten = pd.read_csv(tabelaRotten, sep=',', encoding='utf-8', low_memory=False)
dataframes = []
for arquivo in os.listdir(diretorioObras):
    # Verifica se o arquivo começa com o prefixo e termina com ".csv"
    if arquivo.startswith("obras-nao-pub-brasileiras") and arquivo.endswith(".csv"):
        # Extrai o ano do nome do arquivo
        ano = arquivo.split("-")[-1].split(".csv")[0]
        
        # Lê o arquivo CSV com separador ';'
        caminho_completo = os.path.join(diretorioObras, arquivo)
        df = pd.read_csv(caminho_completo, sep=";", dtype={'DURACAO_TOTAL_MINUTOS': str})
        df['TITULO_BRASIL'] = df['TITULO_ORIGINAL']
        
        # Adiciona a coluna do ano
        df["Ano"] = int(ano)
        
        # Adiciona o DataFrame à lista
        dataframes.append(df)

for arquivo in os.listdir(diretorioObras):
    # Verifica se o arquivo começa com o prefixo e termina com ".csv"
    if arquivo.startswith("obras-nao-pub-estrangeiras") and arquivo.endswith(".csv"):
        # Extrai o ano do nome do arquivo
        ano = arquivo.split("-")[-1].split(".csv")[0]
        
        # Lê o arquivo CSV com separador ';'
        caminho_completo = os.path.join(diretorioObras, arquivo)
        df = pd.read_csv(caminho_completo, sep=";", dtype={'DURACAO_TOTAL_MINUTOS': str})
        
        # Adiciona a coluna do ano
        df["Ano"] = int(ano)
        
        # Adiciona o DataFrame à lista
        dataframes.append(df)

dfLancamentos = pd.read_csv(tabelaLancamento, sep=';', encoding='utf-8', low_memory=False)
dfLancamentos = aplicar_transformacoes(dfLancamentos)

# Concatena todos os DataFrames
dfObras = pd.concat(dataframes, ignore_index=True)

dfRotten = aplicar_transformacoes(dfRotten)
dfObras = aplicar_transformacoes(dfObras)

df_resultante = pd.merge(dfObras, dfLancamentos, on='TITULO_ORIGINAL', how='outer')
df_resultante = pd.merge(dfRotten, df_resultante, left_on='title', right_on='TITULO_ORIGINAL', how='outer')
# ADD público, renda,
df_resultante["CPB_ROE"] = df_resultante["CPB"].fillna(df_resultante["ROE"]).fillna(df_resultante["CPB_ROE"])
df_resultante = df_resultante[['TITULO_ORIGINAL', 'TITULO_BRASIL', 'TIPO_OBRA_x', 'SUBTIPO_OBRA', 'DURACAO_TOTAL_MINUTOS', 'audienceScore','tomatoMeter', 'Ano', 'PAIS_OBRA', 'PUBLICO_TOTAL', 'RENDA_TOTAL', 'CPB_ROE']]
df_resultante['Id_Filme'] = df_resultante.index

df_resultante = df_resultante.rename(columns={
    'TITULO_ORIGINAL': 'Titulo_Original',
    'TITULO_BRASIL': 'Titulo_pt/br',
    'DURACAO_TOTAL_MINUTOS': 'Duracao',
    'TIPO_OBRA_x': 'Genero',
    'SUBTIPO_OBRA': 'Subtipo_Obra',
    'audienceScore': 'NotaPublico',
    'tomatoMeter': 'NotaCritica',
    'PAIS_OBRA': 'Pais_Obra',
    'PUBLICO_TOTAL': 'Publico',
    'RENDA_TOTAL': 'Renda'
})

# Remove linhas onde 'Titulo_Original' e 'Titulo_pt/br' estejam vazios
df_resultante = df_resultante.dropna(subset=['Titulo_Original', 'Titulo_pt/br'], how='any')

# Transforma ano em inteiro
df_resultante['Ano'] = df_resultante['Ano'].fillna(0).astype(int)

# Criar a tabela GENEROS com TITULO_ORIGINAL
generos = df_resultante[['Titulo_Original', 'Genero']].drop_duplicates()
subgeneros = df_resultante[['Titulo_Original', 'Subtipo_Obra']].drop_duplicates()
subgeneros = subgeneros.rename(columns={'Subtipo_Obra': 'Genero'})

# Remove os casos em que subgenero está vazio ou não é informado
subgeneros = subgeneros[subgeneros['Genero'].notna() & (subgeneros['Genero'] != "nao-informado")]

# Concatena o genero e subgenero
generos = pd.concat([generos[['Titulo_Original', 'Genero']], subgeneros[['Titulo_Original', 'Genero']]], ignore_index=True)

# Excluir a coluna TIPO_OBRA_X da tabela df_resultante
df_resultante = df_resultante.drop(columns=['Genero', 'Subtipo_Obra'])

# Arquivo csv
df_resultante.to_csv(tabelaSaida, sep=',', index=False)
generos['Id'] = generos.index
generos.to_csv('Generos.csv', sep=',', index=False)

print(f"Arquivo agrupado salvo em {tabelaSaida}")
print("Tabela GENEROS criada e salva como Generos.csv")