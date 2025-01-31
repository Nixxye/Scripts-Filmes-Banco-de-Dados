import pandas as pd
import os
import re
from unidecode import unidecode

import pandas as pd
import os
import re
from unidecode import unidecode

# Definir o caminho da pasta onde estão os arquivos CSV
arquivo = "Original/SalaDeCinema/salas.csv"

df = pd.read_csv(arquivo, sep=';', encoding='utf-8', low_memory=False, dtype=str)
df = df[['REGISTRO_SALA', 'NOME_SALA', 'SITUACAO_SALA', 'ASSENTOS_SALA', 'ASSENTOS_CADEIRANTES', 'ASSENTOS_MOBILIDADE_REDUZIDA', 'ASSENTOS_OBESIDADE','ACESSO_ASSENTOS_COM_RAMPA', 'ACESSO_SALA_COM_RAMPA', 'BANHEIROS_ACESSIVEIS', 'NOME_GRUPO_EXIBIDOR']]

# Salvar em um novo CSV
arquivoSaida = "Novo/SalaDeCinema/SalasDeCinema.csv"
df.to_csv(arquivoSaida, sep=',')
print(f"Arquivo agrupado salvo em {arquivoSaida}")