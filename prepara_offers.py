# Importacao de bibliotecas
import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
	
	# Carrega o CSV fornecido no inicio do desafio e chama a coluna de URL
	offers_df = pd.read_csv('offers.csv', sep="\n",names=["url"])
	
	# Extracao de substrings entre www. ou // até o .com.br - Obtem o nome da pagina sem acessar o link
	# Ex -> "https://www.mercadolivre.com.br" -> titulo = "mercadolivre"
	reg_ex = r'(www.|//)+(.*)(?=.com.br/)'
	titulos = offers_df["url"].str.extract(reg_ex)
	offers_df['titulo']=titulos[1]
	
	# Declaracao de colunas vazias --------------------------------------------
	# NOME DO PRODUTO armazenado como string. Inicialmente eh string vazia.
	offers_df['nome_produto'] = ""
	
	# PRECO DO PRODUTO armazenado como float. Inicialmento 0.
	offers_df['preco_produto'] =  pd.Series(np.zeros(len(offers_df),dtype=float))
	
	# DESCRICAO DO PRODUTO armazenado como string. Inicialmente eh string vazia.
	offers_df['dcr_produto'] = ""
	
	# VENDEDOR DO PRODUTO armazenado como string. Inicialmente eh vazia. 
	offers_df['vendedor_produto'] = ""
	
	# NUMERO DE VENDAS DO VENDEDOR armazenado como inteiro. Inicialmente 0.
	offers_df['numero_vendas_vendedor'] = pd.Series(np.zeros(len(offers_df),dtype=int))
	
	# Indicador booleano, se houve redirecionamento para acessar o URL. Inicialmente falso.
	offers_df['redirecionado'] = pd.Series(np.full(len(offers_df),False))
	
	# Separacao de links por titulo. Facilita a avaliacao de desempenho dos sites distintos.
	curr_dir = str(os.getcwd())
	
	# Filtragem e escrita dos dados referente a produtos da Casas Bahia
	casasbahia_df = offers_df[(offers_df['titulo']=='casasbahia')]
	casasbahia_df.to_csv(curr_dir+'/Casas Bahia/casas_bahia_offers.csv',sep=';')
	open("Casas Bahia/exceptions_log.txt", "w").close()
	open("Casas Bahia/execution_log.txt", "w").close()
	
	# Filtragem e escrita dos dados referente a produtos do Mercado Livre
	mercadolivre_df = offers_df[(offers_df['titulo']=='mercadolivre') | (offers_df['titulo']=='produto.mercadolivre')]
	#mercadolivre_df = mercadolivre_df.head(1000)
	mercadolivre_df.to_csv(curr_dir+'/Mercado Livre/mercado_livre_offers.csv',sep=';')
	open("Mercado Livre/exceptions_log.txt", "w").close()
	open("Mercado Livre/execution_log.txt", "w").close()
	
	# Filtragem e escrita dos dados referente a produtos da Magazine Luiza
	magazineluiza_df = offers_df[(offers_df['titulo']=='magazineluiza')]
	#magazineluiza_df = magazineluiza_df.head(100)
	magazineluiza_df.to_csv(curr_dir+'/Magazine Luiza/magazine_luiza_offers.csv',sep=';')
	open("Magazine Luiza/exceptions_log.txt", "w").close()
	open("Magazine Luiza/execution_log.txt", "w").close()
	