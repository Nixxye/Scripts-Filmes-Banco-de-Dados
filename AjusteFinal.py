import pandas as pd

def AjustaFilme():
    # Carregar as tabelas
    filmes = pd.read_csv("Novo/Filme/Filme.csv", encoding="utf-8", low_memory=False, dtype=str)
    produtores = pd.read_csv("Novo/Produtor/Produtor.csv", encoding="utf-8", low_memory=False, dtype=str)
    diretores = pd.read_csv("Novo/Pessoa/Diretor/Diretor.csv", encoding="utf-8", low_memory=False, dtype=str)
    diretores['CPB_ROE'] = diretores['CPB_ROE'].str.lower()
    # Adicionar a coluna 'idProdutor' na tabela 'filme', usando o 'CPB_ROE' como chave de correspondência
    # Filtrar apenas as linhas da tabela 'diretores' onde 'CPB_ROE' não é nulo
    diretores_filtrados = diretores.dropna(subset=['CPB_ROE'])

    # Adicionar a coluna 'idDiretor' na tabela 'filme', usando o 'CPB_ROE' como chave de correspondência
    filmes = filmes.merge(diretores_filtrados[['CPB_ROE', 'Id_Diretor']], on='CPB_ROE', how='left')

    # A coluna 'CPB_ROE' de 'filmes' corresponde ao 'CPB_ROE' em 'produtores'
    filmes = filmes.merge(produtores[['CPB_ROE', 'Id_Produtor']], on='CPB_ROE', how='left')


    # Eliminar as linhas da tabela 'produtor' que possuem o mesmo CNPJ
    produtores = produtores.drop_duplicates(subset=['CNPJ'])

    # Retirar as colunas 'CNPJ' e 'CPB_ROE' da tabela 'produtor'
    produtores = produtores.drop(columns=['CNPJ', 'CPB_ROE'])
    # Retirar a coluna 'CPB' da tabela 'diretores' após a junção
    diretores = diretores.drop(columns=['CPB_ROE'])

    # Salvar os arquivos resultantes
    filmes.to_csv("filme_atualizado.csv", index=False, encoding="utf-8")
    produtores.to_csv("produtor_atualizado.csv", index=False, encoding="utf-8")
    diretores.to_csv("diretor_atualizado.csv", index=False, encoding="utf-8")

def AjustaOscar():
    oscarPremio = pd.read_csv("Novo/Oscar/the_oscar_award_tratado_com_ids.csv", encoding="utf-8", low_memory=False, dtype=str)
    oscarNomes = pd.read_csv("Novo/Oscar/the_oscar_award_names.csv", encoding="utf-8", low_memory=False, dtype=str)

    pessoas = pd.read_csv("Novo/Pessoa/hashmapPessoa.csv", encoding="utf-8", low_memory=False, dtype=str)
    filmes = pd.read_csv("Novo/Filme/Filme.csv", encoding="utf-8", low_memory=False, dtype=str)

    oscarPremio = oscarPremio.merge(filmes[['Id_Filme', 'Titulo_Original']], left_on='film', right_on='Titulo_Original', how='left')
    pessoas = pessoas.rename(columns={'id': 'id_pessoa'})
    oscarNomes = oscarNomes.merge(pessoas[['nome', 'id_pessoa']], left_on='name', right_on='nome', how='left')
    oscarPremio = oscarPremio.drop(columns=['Titulo_Original'])
    oscarNomes = oscarNomes.drop(columns=['nome'])
    oscarPremio = oscarPremio.drop_duplicates(subset=['id'], keep='first')
    oscarNomes.to_csv("oscarNomes.csv", index=False, encoding="utf-8")
    oscarPremio.to_csv("oscarPremio.csv", index=False, encoding="utf-8")

def AjustaAvaliações():
    avaliações = pd.read_csv("Novo/Avaliacao/Avaliacao.csv", encoding="utf-8", low_memory=False, dtype=str)
    filmes = pd.read_csv("Novo/Filme/Filme.csv", encoding="utf-8", low_memory=False, dtype=str)

    avaliações = avaliações.merge(filmes[['Id_Filme', 'Titulo_Original']], left_on='Filme', right_on='Titulo_Original', how='left')
    avaliações = avaliações.drop(columns=['Titulo_Original'])
    avaliações = avaliações.drop_duplicates(subset=['Id'], keep='first')
    avaliações.to_csv("avaliacoes.csv", index=False, encoding="utf-8")

def AjustaBilheteria():
    bilheteria = pd.read_csv("Novo/Bilheteria/Bilheteria.csv", encoding="utf-8", low_memory=False, dtype=str)
    filmes = pd.read_csv("Novo/Filme/Filme.csv", encoding="utf-8", low_memory=False, dtype=str)

    bilheteria = bilheteria.merge(filmes[['Id_Filme', 'Titulo_Original']], left_on='Filme', right_on='Titulo_Original', how='left')
    bilheteria = bilheteria.drop(columns=['Titulo_Original'])
    bilheteria = bilheteria.drop_duplicates(subset=['Id_Bilheteria'], keep='first')
    bilheteria.to_csv("bilheteria.csv", index=False, encoding="utf-8")

AjustaFilme()
AjustaOscar()
AjustaAvaliações()
AjustaBilheteria()