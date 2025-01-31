# contagem de id a partir de 0 ou 1?
# tirar coluna cerimony?
# tirei aspas duplas e simples de nomes
# renomear colunas


import re
import numpy as np
import pandas as pd
from unidecode import unidecode



def treat_oscar_table(oscar_table_path, oscar_char_correct_path, oscar_table_treated_path,oscar_table_treated_ids_path,name_ids_path ):
  # correcoes de characteres no csv puro
  with open(oscar_table_path, 'r', encoding='utf-8') as file:
    content = file.read()

  content = content.replace(';,', ',') \
                  .replace('""', ' ')  # aspas de nomes

  with open(oscar_char_correct_path, 'w', encoding='utf-8') as file:
    file.write(content)


  
  df_oscar_tratado = pd.read_csv(oscar_char_correct_path)

  # Substituicoes gerais
  df_oscar_tratado = df_oscar_tratado.map(
    lambda x:( unidecode(
                #re.sub(r'\b(-for-|in-recognition)[^,]*', '',
                x.strip()
                .lower()
                .replace("(", "")#
                .replace(")", "")#
                .replace("[", "")#
                .replace("]", "")#
                .replace(",  ", ",")
                .replace(", ", ",")
                # .replace(" ,", ",")
                # .replace("  ,", ",")
                .replace(";  ", ";")
                .replace("; ", ";")
                #.replace(". ", ".")
                .replace(":  ", ":")
                .replace(": ", ":")
                .replace(" ", "-")
                .replace("---", "-")
                .replace("--", "-")
                .replace('-"', '"')
                .replace('"-', '"')
                .replace(";", ',')
                .replace('art-direction:', '')
                .replace('interior-decoration:', '')
                .replace('set-decoration:', '')
                .replace('musical-settings:', '')
                .replace('production-design:', '')
                .replace('screenplay-by-', '')
                .replace('music-by-', '')
                .replace('music-and-lyric-by-', '')
                .replace('lyric-by-', '')
                # .replace(';story-by-', ',')
                .replace('story-by-', '')
                
                .replace('written-by-', '')
                .replace('written-for-the-screen-by-', '')
                .replace('adaptation-score-by-', '')
                .replace('song-score-by', '')
                .replace('photographic-effects-by-', '')
                .replace('sound-effects-by-' ,'')
                .replace(",sound-director", '')
                .replace('screenplaydialogue-by-', '')
                .replace('adaptation-by-', '')
                .replace('head-of-department-score-by-', '')
                .replace('head-of-department-thematic-', '')
                .replace('lyrics-by-', '')
                .replace('dialogue-by-', '')
                .replace('adapted-for-the-screen-by-', '')
                .replace('musical-director-score-by-', '')
                .replace('special-visual-effects-by-', '')
                .replace('special-audible-effects-by-' ,'')
                .replace('audible-effects-by-', '')
                .replace('visual-effects-by-', '')
                .replace("orchestral-score-by-", '')
                .replace("ballet-photography-by-", '')
                .replace(',associate-producer', '')
                .replace(',executive-producer', '')
                .replace(',producers', '')
                .replace(',producer', '')
                
                

                .replace('production-design:', '')
                .replace(':actor', '')

              
                #.replace('-and-', ',')# tira da categoria tmb

              )#)
                if isinstance(x, str)
                else x)
  )

  # Regex pra retirar lixo
  pattern = (
      r"^(to|made-by)-([a-zA-Z0-9-]+),.*"
      r"|(-for-.*)"
      r"|(-in-(recognition|appreciation).*)"
      r"|(-with-.*)"
      r"|(-voted-by.*)"
      r"|(-a-master.*)"
      r"|(-best-.*)"
  )
  df_oscar_tratado['name'] = df_oscar_tratado['name'].map(
      lambda x: re.sub(pattern, r"\2", x) if isinstance(x, str) else x
  )

  # Retirar lixo (excecao) e padronizacoes
  df_oscar_tratado['name'] = df_oscar_tratado['name'].map(
    lambda x:(x.replace(".-film-sponsored-by-the-disabled-american-veterans", '')
              .replace("stories-by-quentin-tarantino", '')
              .replace("whose-dynamic-performances-resonate-across-genres", '')
              .replace("generations-of-audiences-worldwide.", '')
              .replace("-who-achieved-greatness-as-a-player", '')
              .replace("commemorative-award-recognizing-the-unique", '')
              .replace("outstanding-contribution-of-", '')
              .replace("the-motion-picture-relief-fund-acknowledging-the-outstanding-services-to-the-industry-during-the-past-year-of-the-motion-picture-relief-fund", '')
              .replace("its-progressive-leadership.-presented-to-", '')
              .replace("stefan-arsenijevi?", 'stefan-arsenijevic')

              .replace(",jr", '-jr')
              .replace(",inc.", '-inc.')

              .replace('bosnia-&-herzegovina', 'bosnia-and-herzegovina')

                  if isinstance(x, str)
                else x))


  # Separar elementos de lista por and e &, exceto alguns
  df_oscar_tratado['name'] = df_oscar_tratado['name'].map(
      lambda x: x.replace('-and-', ',') if isinstance(x, str) and x not in ['bosnia-and-herzegovina'] else x
  )
  df_oscar_tratado['name'] = df_oscar_tratado['name'].map(
      lambda x: x.replace('-&-', ',') if isinstance(x, str) and x not in ['australian-news-&-information-bureau', 'bosnia-&-herzegovina', 'bausch-&-lomb-optical-company'] else x
  )

  # Trocar True e False por 1 e 0
  df_oscar_tratado = df_oscar_tratado.map(
    lambda x: 1 if x is True 
        else (0 if x is False
        else x)
  )


  df_oscar_tratado.to_csv(oscar_table_treated_path, index=False)


  # Separacao em 2 tabelas
  names = []
  ids = []
  for id, row in df_oscar_tratado.iterrows():
    name = row['name']
    if isinstance(name, str):
      name_list = name.split(',')
      for name in name_list:
        if name != '' and name != 'associates' and name != 'his-associates' and name != 'film-associates' and name != 'in-cooperation':
          names.append(name)
          ids.append(id) # id+1

  df_names = pd.DataFrame({
    'name': names,
    'id': ids
  })


  df_oscar_tratado['id'] = np.arange(0, len(df_oscar_tratado)) #(1, len(df_oscar_tratado)+1)
  df_oscar_tratado.drop(columns=['name'], inplace=True)
  df_oscar_tratado = df_oscar_tratado[['id', 'year_ceremony', 'category', 'winner', 'film']]
  df_oscar_tratado.to_csv(oscar_table_treated_ids_path, index=False)
  df_names.to_csv(name_ids_path, index=False)



if __name__ == '__main__':
  treat_oscar_table(
    oscar_table_path             = 'Original/Oscar/the_oscar_award.csv',
    oscar_char_correct_path      = 'Original/Oscar/the_oscar_award_char_correct.csv',
    oscar_table_treated_path     = "Novo/Oscar/the_oscar_award_tratado.csv",
    oscar_table_treated_ids_path = "Novo/Oscar/the_oscar_award_tratado_com_ids.csv",
    name_ids_path                = "Novo/Oscar/the_oscar_award_names.csv"
  )