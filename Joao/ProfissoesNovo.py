import csv
from PuxaPessoa import csv_para_hashmap  # Supondo que está funcionando corretamente.
from Normalizar import normalizar_nome

# Função para processar os dados
def processar_dados(caminho_csv, id_map):
    nova_tabela = []

    # Abrir e ler o arquivo CSV
    with open(caminho_csv, mode="r", encoding="utf-8") as arquivo:
        leitor_csv = csv.DictReader(arquivo)

        for linha in leitor_csv:
            nome = linha["primaryName"]
            nome_normalizado = normalizar_nome(nome)

            # Separar as profissões
            profissoes = linha["primaryProfession"].split(",")
            
            # Verificar se há "actor" ou "actress" nas profissões
            if "actor" in profissoes or "actress" in profissoes:
                id_ = id_map.get(nome_normalizado)
                if id_:
                    for profissao in profissoes:
                        nova_tupla = (id_, profissao)
                        nova_tabela.append(nova_tupla)
                else:
                    print(f"Não achou o ID para o nome: {nome_normalizado}")

    return nova_tabela

# Carregar o HashMap e o arquivo CSV
hashmap = csv_para_hashmap("hashmapPessoa.csv")  # Certifique-se de que este arquivo exista e a função funcione corretamente
caminho = "../Original/Pessoa/Ator/combined.csv"  # Caminho para o arquivo de entrada

# Processar os dados e gerar a nova tabela
nova_tabela = processar_dados(caminho, hashmap)

#

with open("profissoes.csv", 'w', encoding='utf-8', newline='') as arquivo_saida:
    escritor = csv.writer(arquivo_saida)
    
    # Escrever o cabeçalho do arquivo HashMap
    escritor.writerow(['id', 'profissao'])
    
    # Escrever os dados da nova_tabela
    for tupla in nova_tabela:
        escritor.writerow(tupla)

print("Arquivo 'profissoes.csv' gerado com sucesso!")

