import header_rotation
import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import json
import re

# Funcao que recebe um dataframe com links e colunas vazias. Preenche as colunas vazias com as informacoes que forem encontradas.
def parser_url_df(df):
	# Reset index pois o dataframe foi dividido.
	df = df.reset_index(drop=True)
	
	# Processo atual - Para pegar o numero do worker - para logging
	current = multiprocessing.current_process()
	
	# Tamanho do dataframe que este worker esta resolvendo
	df_len = len(df)
	
	# Para cada link do dataframe
	for i in range(df_len):
		
		# Escolhe header aleatorio - feito fora do bloco para poder logar o header - alguns comentarios pois foi para experimentos.
		#my_header = header_rotation.get_random_header()
		#if(df['titulo'][i] == 'magazineluiza'):
		my_header =  header_rotation.get_random_casasbahia_header()
		
		# Tenta fazer o request para o link
		try:
			
			# Tenta obter o conteudo do link - caso a resposta http nao for ok - raise exception
			response = requests.get(df['url'][i], headers=my_header)
			response.raise_for_status()
		
			# Parsing do conteudo retornado
			soup = BeautifulSoup(response.text, "lxml")
			
			# Identficando se houve redirecionamento para chear no link ou nao
			if (response.history):
				df.loc[i,'redirecionado'] = True
			else:
				df.loc[i,'redirecionado'] = False
			
			# Print com o numero de links ja processados e o numero do worker.
			print(i,"/",df_len,"    Worker:    ", current)
	
	        # -------------------------- Parser para Mercado Livre -------------------------------
			if((df['titulo'][i] == 'produto.mercadolivre') | (df['titulo'][i] == 'mercadolivre')):
				
				# Obtendo o nome do produto para o Mercado Livre
				nome_produto = soup.find(class_='ui-pdp-title')
				if(nome_produto):
					df.loc[i,'nome_produto']= nome_produto.text.replace(';',' ')
				
				
				# Descricao do produto para o mercado livre
				dcr_produto = soup.find(class_='ui-pdp-description__content')
				if(dcr_produto):
					df.loc[i,'dcr_produto']= dcr_produto.text.replace('\r',' ').replace(';',' ')
				
				# Preco do produto - Pode ser encontrado ou nao - SE for - entra no if, se nao, no elif
				preco_produto = soup.find(class_='ui-pdp-price__second-line')
				if(preco_produto):
					# Caso possui desconto - remove informacao
					if('%' in preco_produto.text):
						preco_produto = soup.find(class_='ui-pdp-price__second-line').find(class_='price-tag ui-pdp-price__part')
					
					# Remove simbolos e ponto milhar
					preco_produto=preco_produto.text.replace('R$','').replace('.','')
					
					# Substitui virgula decimal por ponto para conversao para float
					df.loc[i,'preco_produto']= float(preco_produto.replace(',','.'))
					
				# Caso nao foi encontrado o preco na pagina e nome nao eh vazio, pode ser necessario clicar no botao para obter os precos
				elif(df['nome_produto'][i] != ''):
					
					# Obtem o botao que contem o link
					new_link_pos = soup.find(class_='andes-button andes-button--loud')
					
					# Obtem posicao de inicio do link
					aux = str(new_link_pos).find("formaction=")
					
					# Pega link ate final do codigo do botao e depois ate o final do link
					my_url = str(new_link_pos)[aux+12:]
					my_url = my_url[:my_url.find('"')]
					
					# Clica no botao para obter precos
					response = requests.get(my_url, headers=my_header)
					response.raise_for_status()
					soup = BeautifulSoup(response.text, "lxml")
					
					# Repete processo de extracao do preco do produto para o mercado livre
					preco_produto = soup.find(class_='ui-pdp-price__second-line').find(class_='price-tag ui-pdp-price__part')
					preco_produto=preco_produto.text.replace('R$','').replace('.','')
					df.loc[i,'preco_produto']= float(preco_produto.replace(',','.'))
				
				# Extrai nome do vendedor do produto do mercado livre
				vendedor_produto = soup.find(class_='ui-pdp-seller__header__title')
				if(vendedor_produto):
					# Remove a tag de vendedor oficial e vendido por - limpeza simples de dados
					vendedor_produto = vendedor_produto.text.replace("Vendido por",'')
					df.loc[i,'vendedor_produto']= vendedor_produto.replace(';',' ').replace('Loja oficial','')
				
				# Obtem o numero de vendas do produto
				numero_vendas_vendedor = soup.find(class_='ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller__header__subtitle')
				if(numero_vendas_vendedor):
					# Remove caracteres irrelevantes e mantem apenas o inteiro.
					df.loc[i,'numero_vendas_vendedor']= int(numero_vendas_vendedor.text[:-7].replace('MercadoLíder | ','').replace('.',''))
			# -------------------------- Parser para Magazine Luiza -------------------------------
			elif(df['titulo'][i] == 'magazineluiza'):
				
				# Extrai o nome do produto para o link - Pode ser que o nome esteja nesta classe caso o item esteja com estoque
				nome_produto = soup.find(class_='header-product__title')
				if(nome_produto):
					df.loc[i,'nome_produto']= nome_produto.text.replace(';',' ')
				# Se nao estava na classe, entao ta na classe de titulo para produto indisponivel
				else:
					nome_produto =  soup.find(class_='header-product__title--unavailable')
					if(nome_produto):
						df.loc[i,'nome_produto']= nome_produto.text.replace(';',' ')
				
				# Codigo utilizado para identificar qual user agents a magazine luiza estava aceitando
#				if(df['nome_produto'][i]!=''):
#					with open('good_agent_magazineluiza.txt', 'a') as file:
#						file.write('\'')
#						file.write(my_header['User-Agent'])
#						file.write('\',\n')
				
				
				# Busca o preco do produto
				preco_produto = soup.find(class_='price-template__text')
				if(preco_produto):
					# Caso o preco do produto existe - remove o separador milhar
					preco_produto=preco_produto.text.replace('.','')
					# Troca virgula decimal para ponto e converte para float
					df.loc[i,'preco_produto']= float(preco_produto.replace(',','.'))
				
				
				dcr_produto = soup.find(class_='description__container-text')
				if(dcr_produto):
					df.loc[i,'dcr_produto']= dcr_produto.text.replace('\r',' ').replace(';',' ')
					
				vendedor_produto = soup.find(class_='seller-info-button js-seller-modal-button')
				if(vendedor_produto):
					df.loc[i,'vendedor_produto']= vendedor_produto.text.replace(';',' ')
					
			# -------------------------- Parser para Casas Bahia -------------------------------
			elif(df['titulo'][i] == 'casasbahia'):
				# Encontra o script que inicia a renderizacao da pagina
				produto_informacao_json = soup.find('script', type='application/json')
				
				if(produto_informacao_json):
					# Caso o script for encotrado, entao carrega a informacao do produto disponibilizado no JSON
					produto_informacao_json = produto_informacao_json.contents[0]
					
					produto_informacao_json = json.loads(produto_informacao_json)
					
					# Caso o JSON for encontrado no script
					if(produto_informacao_json):					
						
						# Extrai o nome do produto a partir do JSON
						nome_produto = produto_informacao_json['props']['initialState']['Product']['product']['name']
						if(nome_produto):
							df.loc[i,'nome_produto']= nome_produto.replace(';',' ')
						
						# Extrai a descricao do produto a partir do JSON
						dcr_produto = produto_informacao_json['props']['initialState']['Product']['product']['description']
						if(dcr_produto):
							# Remove qualquer HTML residual da descricao e \n consecutivso.
							dcr_produto =  re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', dcr_produto)
							dcr_produto = "".join([s for s in dcr_produto.strip().splitlines(True) if s.strip()])
							
							df.loc[i,'dcr_produto']= dcr_produto.replace(';',' ')
						
						# Monta link para obter informacao do preco da API da casas bahia - nao esta disponivile no json atual
						sku = produto_informacao_json['query']['sku']
						link_preco_produto = 'https://pdp-api.casasbahia.com.br/api/v2/sku/'+sku+'/price/source/CB'
						
						# Busca o conteudo da API e extrai
						preco_produto_json = requests.get(link_preco_produto, headers=my_header)
						soup2 = BeautifulSoup(preco_produto_json.text, "html.parser")
						
						preco_produto_json = json.loads(soup2.contents[0])
						
						# Extrai preco do produto a partir do JSON retorando da API
						preco_produto = preco_produto_json['sellPrice']['priceValue']
						if(preco_produto):
							df.loc[i,'preco_produto']= float(preco_produto)
						
						# Extrai vendedor do produto a partir do JSON retorando da API
						vendedor_produto = preco_produto_json['sellers'][0]['name']
						if(vendedor_produto):
							df.loc[i,'vendedor_produto']= vendedor_produto
					
			# Delay Aleatorio - Evitar bloqueios
			if( i < (0.7*df_len)):
				time.sleep(np.random.random()/8)
			else:
				time.sleep(np.random.random()/16)
				
		# Logging de erros
		except Exception as e:
			dir = ''
			if((df['titulo'][i] == 'produto.mercadolivre') | (df['titulo'][i] == 'mercadolivre')):
				dir = 'Mercado Livre/'
			elif (df['titulo'][i] == 'magazineluiza'):
				dir = 'Magazine Luiza/'
			elif (df['titulo'][i] == 'casasbahia'):
				dir = 'Casas Bahia/'
				
				with open(dir+'exceptions_log.txt', 'a') as file:
					# Anota o link que gerou o erro
					aux = 'Link que gerou o erro: ' + df['url'][i] + '\n'
					file.write(aux)
					
					# Anota o horario do erro
					file.write('Horario do erro: ' + time.strftime('%b %d %Y %H:%M:%S',time.localtime()) + '\n')
					
					# Anota a excessao gerada
					file.write(str(e))
					file.write('\n')
					
					file.write('\n================\n')
			pass
		finally:
			pass
					
	return df