import unicodedata

def remover_acentos(texto):
    # Decompor os caracteres acentuados para separar diacríticos
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Filtrar apenas os caracteres que não são diacríticos
    texto_sem_acento = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
    return texto_sem_acento

def normalizar_nome(nome):
    nome = remover_acentos(nome)  # Remove acentos
    nome = nome.strip()           # Remove espaços no início e no fim
    nome = " ".join(nome.split()) # Remove múltiplos espaços no meio
    nome = nome.lower()           # Converte para minúsculas
    nome = nome.replace(" ", "-") # Substitui espaços por hífens
    return nome