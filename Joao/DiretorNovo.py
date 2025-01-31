import csv
from PuxaPessoa import csv_para_hashmap  # Supondo que está funcionando corretamente.
from Normalizar import normalizar_nome

# Carregar o hashmap de IDs
print("Carregando o HashMap...")
id_map = csv_para_hashmap("hashmapPessoa.csv")
print(f"HashMap carregado com {len(id_map)} entradas.")

combined_tabela = {}

# Ler o arquivo de diretores
print("Processando arquivo 'combined.csv'...")
with open("../Original/Pessoa/Ator/combined.csv", mode="r", encoding="utf-8") as arquivo:
    leitor_csv = csv.DictReader(arquivo)
    contador = 0

    for linha in leitor_csv:
        contador += 1
        if contador % 1000 == 0:
            print(f"Processadas {contador} linhas de 'combined.csv'...")

        nome = linha["primaryName"]
        nome_normalizado = normalizar_nome(nome)

        # Separar as profissões
        profissoes = linha["primaryProfession"].split(",")
        
        if "director" in profissoes:
            id_ = id_map.get(nome_normalizado)
            if id_:
                if id_ not in combined_tabela:
                    combined_tabela[id_] = "null"  # Garantir que não haja duplicados
            else:
                print(f"Não achou o ID para o nome: {nome_normalizado}")

print(f"Arquivo 'combined.csv' processado. Total de linhas: {contador}")

# Ler o arquivo de diretores de obras não publicitárias
print("Processando arquivo 'diretores-de-obras-nao-publicitarias-brasileiras.csv'...")
obras_n_publicitarias_tabela = {}

with open("../Original/Pessoa/Diretor/diretores-de-obras-nao-publicitarias-brasileiras.csv", mode="r", encoding="utf-8") as arquivo:
    leitor_csv = csv.reader(arquivo, delimiter=';')
    next(leitor_csv)  # Pula o cabeçalho
    contador = 0

    for linha in leitor_csv:
        contador += 1
        if contador % 1000 == 0:
            print(f"Processadas {contador} linhas de 'diretores-de-obras-nao-publicitarias-brasileiras.csv'...")

        nome = linha[0]
        pais = linha[1]
        if pais == "Não Informado":
            pais = "null"
        else:
            pais = normalizar_nome(pais)
        
        nome_normalizado = normalizar_nome(nome)

        id_ = id_map.get(nome_normalizado)
        if id_:
            if id_ not in obras_n_publicitarias_tabela:
                obras_n_publicitarias_tabela[id_] = pais  # Garantir que não haja duplicados
        else:
            print(f"Não achou o ID para o nome: {nome_normalizado}")

print(f"Arquivo 'diretores-de-obras-nao-publicitarias-brasileiras.csv' processado. Total de linhas: {contador}")

# Combinar as tabelas e garantir que não haja duplicatas
tabela_final = combined_tabela.copy()

for id_, pais in obras_n_publicitarias_tabela.items():
    # Caso o ID já exista em `combined_tabela`, não vamos adicioná-lo novamente
    if id_ not in tabela_final:
        tabela_final[id_] = pais

print(f"Tabela final combinada. Total de diretores: {len(tabela_final)}")

# Escrever a tabela final no arquivo CSV
print("Escrevendo arquivo final 'diretor.csv'...")
with open("diretor.csv", 'w', encoding='utf-8', newline='') as arquivo_saida:
    escritor = csv.writer(arquivo_saida)
    
    # Escrever o cabeçalho
    escritor.writerow(['id', 'pais-de-origem'])
    
    # Escrever os dados da tabela final
    for id_, pais in tabela_final.items():
        escritor.writerow([id_, pais])

print("Arquivo 'diretor.csv' gerado com sucesso!")

# Gerar arquivo de INSERTs SQL em blocos de 1000
print("Gerando arquivo SQL 'diretor_inserts.sql'...")
with open("diretor_inserts.sql", 'w', encoding='utf-8') as arquivo_sql:
    tamanho_bloco = 1000
    for i in range(0, len(tabela_final), tamanho_bloco):
        bloco = list(tabela_final.items())[i:i + tamanho_bloco]

        arquivo_sql.write("INSERT INTO BD1_Filmes_Diretor (D_Id_Pessoa, Pais_De_Origem) VALUES\n")

        # Gerar as linhas de inserção, tratando o 'pais' como NULL quando necessário
        linhas = [
            f"({id_}, NULL)" if pais == "null" else f"({id_}, '{pais}')" 
            for id_, pais in bloco
        ]
        
        arquivo_sql.write(",\n".join(linhas) + ";\n\n")

print("Arquivo SQL 'diretor_inserts.sql' gerado com sucesso!")
