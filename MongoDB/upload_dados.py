# Carregamento de bibliotecas
import pymongo
import pandas as pd
import numpy as np
import os

# Constantes que devem ser ajustadas de acordo com o ambiente de execucacao
PATH = "C:/Users/1513 X-MXTI/Documents/MEGAsync/MEGAsync Uploads/faculdade/Outros/Data Science/Desafio Birdie/repo/scraper-produtos"
# PATH = "C:/scraper-produtos"
STR_MONGO_CONECT = "mongodb+srv://gustavo-adm:nbzH4jangMGccvVp@cluster-desafiobirdie.43lqn.mongodb.net/links_ofertas?retryWrites=true&w=majority"
#STR_MONGO_CONECT = "mongodb+srv://<user-name>:<password>@<cluster>.mongodb.net/<dbName>?retryWrites=true&w=majority"


# Mudanca de Path para poder carregar os arquivos - eh necessario ajustar de acordo com onde voce esta executando este script
os.chdir(PATH)

# Carregamento dos dados coletados
casas_bahia_offers = pd.read_csv('Casas Bahia/casas_bahia_offers.csv', sep=";",index_col=0)
casas_bahia_offers['nome_produto'] = casas_bahia_offers['nome_produto'].fillna('')

magazine_luiza_offers = pd.read_csv('Magazine Luiza/magazine_luiza_offers.csv', sep=";",index_col=0)
magazine_luiza_offers['nome_produto'] = magazine_luiza_offers['nome_produto'].fillna('')

mercado_livre_offers = pd.read_csv('Mercado Livre/mercado_livre_offers.csv', sep=";",index_col=0)
mercado_livre_offers['nome_produto'] = mercado_livre_offers['nome_produto'].fillna('')

# Montando os dados  para criar dicicionario
dados_completos = pd.concat([casas_bahia_offers,magazine_luiza_offers,mercado_livre_offers])
dados_completos = dados_completos[dados_completos['nome_produto'] != '']
dados_completos['preco_produto'] = dados_completos['preco_produto'].replace(0, np.NaN)
dados_completos['numero_vendas_vendedor'] = dados_completos['numero_vendas_vendedor'].replace(0, np.NaN)
dados_completos['dcr_produto'] = dados_completos['dcr_produto'].replace('', np.NaN)

# Conexao ao cluster que contem os dados - no caso eh o projeto que defini no MongoDB Atlas.
cluster = pymongo.MongoClient(STR_MONGO_CONECT)

# Selecionando qual banco de dados deve ser utilizado
db = cluster['links_ofertas']

# Definindo o nome da colecao que vai conter os dados
collection = db['dados_links']			

# Convertendo para dicionario - neste caso documentos
dados_dict = dados_completos.to_dict('records')

# Fazendo a insercao dos documentos.
collection.insert_many(dados_dict)

# Inserindo indice para poder buscar por nome produto - otimiza as consultas
collection.create_index([("nome_produto", pymongo.TEXT)], default_language='portuguese');

