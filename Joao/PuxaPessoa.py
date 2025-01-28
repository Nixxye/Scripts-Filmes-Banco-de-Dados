import csv

def csv_para_hashmap(caminho_arquivo):
    hashmap = {}
    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        leitor_csv = csv.reader(arquivo)
        next(leitor_csv)  # Pular o cabeçalho
        for linha in leitor_csv:
            id_ = int(linha[0])  # Converter o ID para inteiro
            nome = linha[1]
            hashmap[nome] = id_  # Nome como chave, ID como valor
    return hashmap
