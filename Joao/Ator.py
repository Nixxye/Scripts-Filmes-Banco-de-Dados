import csv
from PuxaPessoa import csv_para_hashmap  # Supondo que está funcionando corretamente.
from Normalizar import normalizar_nome

# Função para processar e normalizar os dados
def processar_dados(caminho_csv, id_map):
    nova_tabela = []

    # Abrir e ler o arquivo CSV
    with open(caminho_csv, mode="r", encoding="utf-8") as arquivo:
        leitor_csv = csv.DictReader(arquivo)

        for linha in leitor_csv:
            nome = linha["primaryName"]
            nome_normalizado = normalizar_nome(nome)

            # Obter o ID do hashmap
            id_ = id_map.get(nome_normalizado)

            if id_:
                # Normalizar os valores necessários e montar a nova tabela
                filme = linha["knownForTitle"]
                filme = normalizar_nome(filme)

                nascimento = linha["birthYear"]
                falecimento = linha["deathYear"] if linha["deathYear"] else "null"

                nova_tupla = (id_, nascimento, falecimento, filme)
                nova_tabela.append(nova_tupla)
            else:
                print(f"Não achou o ID para o nome: {nome_normalizado}")

    return nova_tabela

# Carregar o HashMap e o arquivo CSV
hashmap = csv_para_hashmap("hashmapPessoa.csv")  # Certifique-se de que este arquivo exista e esteja correto
caminho = "../Original/Pessoa/Ator/combined.csv"  # Caminho para o arquivo de entrada

# Processar os dados
nova_tabela = processar_dados(caminho, hashmap)

# Escrever os dados normalizados em um novo arquivo CSV
with open("ator.csv", 'w', encoding='utf-8', newline='') as arquivo_saida:
    escritor = csv.writer(arquivo_saida)
    
    # Escrever o cabeçalho com os nomes em português
    escritor.writerow(['id', 'ano-nascimento', 'ano-falecimento', 'filme'])
    
    # Escrever os dados normalizados
    escritor.writerows(nova_tabela)

print("Arquivo 'ator.csv' gerado com sucesso!")
