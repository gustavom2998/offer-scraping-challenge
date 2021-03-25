# Importacao de bibliotecas
import numpy as np
import pandas as pd
import multiprocessing

# Funcao para dividir operacao sobre dataframe em operacao em varios sub-dataframes com threads.
# Entrada: Dataframe a ser manipulado,
#          Referencia para a funcao a ser utilizada. Deve aplicar uma operacao a um dataframe e retornar o resultado.
#          Numero de nucleos a serem criados para executar a tarefa.
def parallelize_dataframe(df, func, n_cores=8):
	
	# Divisao de grupos de linhas do data frame
	df_split = np.array_split(df, n_cores)
	
	# Criacao da pool de threads para executar a tarefa
	pool = multiprocessing.Pool(n_cores)
	
	# Inicia o processamento paralelo.
	df = pd.concat(pool.map(func, df_split))
	
	# Encerramento e retorno do resultado.
	pool.close()
	pool.join()
	return df