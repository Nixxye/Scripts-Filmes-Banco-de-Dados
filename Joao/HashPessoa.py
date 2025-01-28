import csv
from Normalizar import normalizar_nome

# Caminho dos arquivos CSV originais
caminho_ator = '../Original/Pessoa/Ator/combined.csv'
caminho_diretor = '../Original/Pessoa/Diretor/diretores-de-obras-nao-publicitarias-brasileiras.csv'

# Caminho do arquivo para salvar o HashMap (id, nome)
caminho_hashmap = 'hashmapPessoa.csv'

# HashMap para gerar IDs baseados no nome
id_map = {}
id_atual = 1

def get_or_create_id(nome):
    """ Gera um ID único para o nome, ou retorna o ID existente se já criado """
    global id_atual
    if nome not in id_map:
        id_map[nome] = id_atual
        id_atual += 1
    return id_map[nome]

# Função para ler e processar os CSVs
def processar_csv(caminho_csv, delimitador):
    """ Função que processa cada CSV e gera o HashMap de IDs e Nomes """
    with open(caminho_csv, 'r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv, delimiter=delimitador)  # Definindo o delimitador de cada arquivo
        try:
            cabecalho = next(leitor)  # Lê o cabeçalho (primeira linha), ignoramos mas pode ser útil
        except StopIteration:
            print(f"O arquivo {caminho_csv} está vazio.")
            return

        # Gerar o HashMap de IDs e nomes
        for linha in leitor:
            if linha:  # Verifica se a linha não está vazia
                nome = normalizar_nome(linha[0])  # Modificar o nome para minúsculas e remover espaços extras
                get_or_create_id(nome)  # Gera o ID para o nome, se não existir

# Processar os arquivos de atores (vírgula) e diretores (ponto e vírgula)
processar_csv(caminho_ator, ',')  # Delimitador vírgula para o arquivo de atores
processar_csv(caminho_diretor, ';')  # Delimitador ponto e vírgula para o arquivo de diretores

# Salvar o HashMap (ID, Nome) em um novo arquivo CSV
with open(caminho_hashmap, 'w', encoding='utf-8', newline='') as arquivo_saida:
    escritor = csv.writer(arquivo_saida)
    
    # Escrever o cabeçalho do arquivo HashMap
    escritor.writerow(['id', 'nome'])
    
    # Escrever cada par (ID, Nome) no arquivo
    for nome, id_artista in id_map.items():
        escritor.writerow([id_artista, nome])

print(f"HashMap salvo em '{caminho_hashmap}' com sucesso!")
