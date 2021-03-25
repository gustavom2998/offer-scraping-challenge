import time
import numpy as np
import pandas as pd
import multithread_df
import parsers
import os

if __name__=='__main__': 
	
	numero_threads = 12
	curr_dir = str(os.getcwd())
	
	try:
		# Repete o processo por tempo indeterminado
		novos_links = 1
		
		while (novos_links > 0):
			
			with open(curr_dir + '/Casas Bahia/execution_log.txt','a') as file:
			
			
				my_str = "\nInicio de execucao em:" + time.strftime('%b %d %Y %H:%M:%S',time.localtime()) + " com " + str(numero_threads) + ' threads.\n'
				print(my_str)
				file.write(my_str)
				
				# Leitura da tabela da Casas Bahia e substituicao de NAs por valores corretos
				link_df = pd.read_csv('Casas Bahia/casas_bahia_offers.csv', sep=";",index_col=0)
				#link_df['nome_produto'] = link_df['nome_produto'].fillna('')
				link_df['dcr_produto'] = link_df['dcr_produto'].fillna('')
				link_df['vendedor_produto'] = link_df['vendedor_produto'].fillna('')
				link_df['numero_vendas_vendedor'] = link_df['numero_vendas_vendedor'].astype(int)
				
				# Updated DF vai possuir links sem dados
				updated_df = link_df
				# Link DF vai possuir apenas os links com dados completos
				link_df = link_df.dropna()
				
				my_str = '\nProdutos adquiridos ate agora: ' + str(len(link_df)) + "/" +  str(len(updated_df)) + '\n'
				file.write(my_str)
				print(my_str)
				
				# Updated DF possui apenas links que nao estao com dados completos
				updated_df = updated_df[updated_df['url'].isin(link_df['url'])==False]
				
				# Chamada de execucao de atualizacao de links incompletos
				updated_df = multithread_df.parallelize_dataframe(updated_df,parsers.parser_url_df,numero_threads)
				
				# Atualiza para ter todos os links completos + links completados + links incompletos
				aux_novos_links = len(updated_df) - sum(updated_df['nome_produto'].isna())
				
				# Escreve numero de links novos addicionados
				my_str =  str(aux_novos_links) + ' novos links acessados.\n'
				file.write(my_str)	
				print(my_str)
				
				novos_links = aux_novos_links
				
				updated_df = updated_df.append(link_df)
				
				# Salva isso para ser utilizado na proxima execucao
				updated_df.to_csv('Casas Bahia/casas_bahia_offers.csv',sep=';')
				
				
				# Configurando o sleep da thread para repetir o processo
				time_sleep = 900 + np.random.randint(0,100)
				my_str = "Desligando a thread por " + str(time_sleep) + "s em: " + time.strftime('%b %d %Y %H:%M:%S',time.localtime()) + "...\n"
				print(my_str)
				file.write(my_str)
			
			time.sleep(time_sleep)
		
	except Exception as e:
		print(e)