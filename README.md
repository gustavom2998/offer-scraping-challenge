# Desafio Birdie: Coleta de Oferta de Produtos
Este repositório contém todo o conteúdo desenvolvido para o Desafio Técnico do processo seletivo de estágio como Engenheiro de dados da Birdie. 

## Resumo

Para a coleta e preparo dos dados, a linguagem de programação *Python* foi utilizada. Os dados de links foram estruturados dentro do Python utilizando dataframes da biblioteca *Pandas*. O pacote *Requests*  foi utilizado para fazer requisições HTTP para obter o conteúdo das páginas disponibilizadas nos respectivos links, de cada linha do dataframe. A biblioteca *Beautiful Soup* foi utilizada para analisar e extrair os conteúdo de cada página, e os dados encontrados foram inseridos nas colunas vazias de cada linha do dataframe. Para agilizar o processo de coleta de dados, a biblioteca *Multiprocessing* foi utilizada para dividir a carga de trabalho entre múltiplas threads, onde cada thread recebe um subconjunto do dataframe e realiza o processo de requisição e análise (com as bibliotecas anteriormente mencionadas). Os dados foram reunidos e inseridos em um banco de dados *MongoDB*, que foi configurado através da plataforma online *MongoDB Atlas*.  A plataforma *MongoDB Compass* foi utilizada para simplificar o processo de consultar e gerenciar o banco de dados. Por último, para exemplificar um caso de uso do banco de dados, o *Jupyter Notebooks* (na versão Jupyter Lab) foi utilizado para conectar com o banco de dados, através do usuário público (que pode apenas fazer consultas). Para estabelecer a conexão, a biblioteca *PyMongo* foi utilizada. Utilizando as bibliotecas *Dash*, *Plotly* e *IPyWidgets*, duas aplicações foram criadas. A primeira permite fazer queries com diferentes filtros no banco de dados, sem o usuário ter que mexer no código. O usuário pode ainda ordenar, filtrar novamente, e baixar os dados obtidos do query. Outro exemplo foi feito, onde o usuário pode consultar dados de custos de produtos sobre diferentes marcas, obtendo o preço mais barato, mais caro, e médio para as ofertas. O resultado foi demonstrado graficamente em uma aplicação dash. 

## Descrição do Desafio

Segue uma breve descrição do desafio para contextualizar o problema.

1. Baixar e armazenar o conteúdo de uma lista de 40 mil URLs de ofertas (`offers.csv` - disponibilizado no repositório).

2. Extrair e armazenar pelo menos o título e o preço dos produtos para que seja consultável. 

3. Fornecer uma forma de consultar pelo conteúdo armazenado.

4. Preparar uma apresentação sobre a arquitetura da solução.

## Arquivos Disponiblizados

Vários arquivos diferentes foram criados para resolver este problema. Abaixo está uma lista que explica o objetivo dos principais arquivos e pastas destes diretórios. 

* `GIFS/`: Pasta contendo os GIFs utilizados para o README.
* `Casas Bahia/`: Diretório com CSV com dados coletados e dados não coletados para os sites da Casas Bahia, logs de coleta, logs de exceções. 
* `Magazine Luiza/`: Diretório com CSV com dados coletados e dados não coletados para os sites da Magazine Luiza, logs de coleta, logs de exceções. 
* `Mercado Livre/`:  Diretório com CSV com dados coletados e dados não coletados para os sites do Mercado Livre, logs de coleta, logs de exceções. 
* `MongoDB/`: Possui os script para criação do banco de dados e um notebook Jupyter que conecta ao banco de dados, e possuí queries, e uma aplicação muito básica de consulta com filtros, search, e exportação dos resultados. 
* `header_rotation.py`: Utilizado para organizar os headers e lista de user agents, utilizado para as requisições HTTP. Contém funções para seleção de headers/user agents aleatórios.
* `multithread_df.py`: Define uma função que recebe um dataframe e uma função. Múltiplas threads são utilizadas para dividir o dataframe e aplicar as operações da função sob o dataframe.
* `parser.py`: Script contendo a função utilizada para iterar sobre os links. Para cada link, um request HTTP é feito e o conteúdo web retornado é analisado para extração de dados com o BeautifulSoup. 
* `prepara_offers.py`: Primeiro script que deve ser executado neste repositório. Utiliza o `offers.csv` para obter os links e gera as tabelas de cada site(Casas Bahia, Magazine Luiza, etc.).
* `update_CasasBahia.py`: Script que carrega os dados da pasta Casas Bahia e encontra todos os links que possui dados ausentes. Os dados que já foram obtidos são mantidos como estão. Executa indefinitivamente até todos os links forem obtidos. 
* `update_MagazineLuiza.py`:  Script que carrega os dados da pasta Magazine Luiza e encontra todos os links que possui dados ausentes. Os dados que já foram obtidos são mantidos como estão. Executa indefinitivamente até todos os links forem obtidos. 
* `update_MercadoLivre.py`:  Script que carrega os dados da pasta Mercado Livre e encontra todos os links que possui dados ausentes. Os dados que já foram obtidos são mantidos como estão. Executa indefinitivamente até todos os links forem obtidos. 

## Como utilizar

O primeiro passo é executar o Script `prepara_offers.py`. Este script reinicia todos os CSVs e logs para que os únicos dados no dataframe sejam os links. Pode ser necessário ajustar o diretório (como executei em uma IDE pré-configurada, não tive problemas).

Em sequência, pode-se executar qualquer um dos scripts `update_CasasBahia.py`, `update_MazineLuiza.py` ou  `update_MercadoLivre.py`. Eles podem ser executados em paralelo. Cada script inicia o processo de requisições utilizando todos os links, e pausa por um tempo (em torno) de 15 minutos. Cada script utiliza múltiplas threads, então pode ser pesado executá-los na máquina local. Utilizar uma máquina virtual na nuvem com alto poder de processamento é uma possibilidade interessante, onde um grande número de threads poderia ser utilizado. Temos abaixo um exemplo da execução dos scripts utilizando apenas 200 links de cada site foi disponibilizado. Para compreender o por que nem todos sites retornaram todos os links, veja a seção de resultados. Um pequeno corte foi adicionado para a coleta dos links da Magazine Luiza e Mercado Livre, pois eles são mais demorados. 

![alt text](GIFS/teste_coleta.gif)


Quando estiver satisfeito com o número de links coletados (pode ser consultado através do log de execução), o script `MongoDB/upload_dados.py` pode ser utilizado para fazer o upload dos dados, armazenando em um cluster do MongoDB Atlas. Para isso, é necessário ter configurado um cluster com usuários de acesso e também com IPs de acesso. Para confirmar que os resultados foram realmente disponibilizados na plataforma, mostramos abaixo o schema da coleção disponibilizada através do MongoDB Compass.

![alt text](GIFS/teste_bd.gif)


Para este projeto, foram configurados dois usuários. Um para fins de administração, que poderia atualizar, remover e inserir dados. Outro usuário também foi criado, este com privilégios apenas de consultas. Este usuário foi disponibilizado, e qualquer um pode utilizar as informações para acessar e consultar o banco de dados. A configuração de acesso de rede foi feita de modo que qualquer um pode acessar o banco de dados.

```
user: public_user
password: KiwhjUOdauK06lzg
collection: links_ofertas
```

Para conexões no Python, utilize *PyMongo* com este usuário:

```
client = pymongo.MongoClient("mongodb+srv://public_user:KiwhjUOdauK06lzg@cluster-desafiobirdie.43lqn.mongodb.net/links_ofertas?retryWrites=true&w=majority")
db = client.dados_links

```

## Resultados obtidos

Para os diferentes sites, foi necessário adotar diferentes estratégias para tentar coletar o máximo de conteúdo possível. Logo, diferentes resultados foram encontrados. 

Para os links da Casas Bahia conseguimos coletar 6.080 de 6.080 links. A coleta foi finalizada em 3 execuções utilizando 12 threads.  A partir da primeira execução, que durou 5 minutos, 6.076 links já haviam sido coletados. O delay adotado foi de 15 minutos.

Para os links do Mercado Livre conseguimos obter 340 de 340 links, e 14.073 de 16.167 do Produtos Mercado Livro (Possui estrutura diferente da página que é apenas Mercado Livre, por isso tratamos como separado). O processo de coleta deste foi o mais demorado, onde foi necessário executar o script ao longo de dois dias. A partir dos 10.477 links iniciais que foram coletados em uma única execução, aparentemente os links restantes necessitavam de múltiplas tentativas de acesso para carregar a página. Isto foi confirmado através de acesso de links manuais. Para a coleta, 10 execuções foram realizadas com 12 threads e 20 execuções foram realizadas com 12 threads, dando um total de 30 execuções. Delays tanto de 5 minutos quanto 15 minutos foram utilizados.

Para os links da Magazine Luiza conseguimos obter 4.231 de 17.413 links. Para a coleta 3 execuções foram realizadas utilizando 12 threads e 9 execuções foram realizadas utilizando 6 threads. A partir da terceira execução nenhum link adicional foi encontrado. Inicialmente um delay de 5 minutos foi utilizado, porém, para tentar melhorar os resultados, um delay de 15 minutos foi adotado posteriormente. Também acessamos algumas dezenas de links aleatórios manualmente e eles não funcionaram. Vale ressaltar que conseguimos acessar alguns links "novos" obtidos manualmente do site da Magazine Luiza, logo, é válido sugerir que não há problemas no script necessariamente. Pode ser também que algo esteja errado com o cabeçalho utilizado, mas inúmeros testes foram realizados e esta questão ficou em aberta. Seria possível extrair novos links para melhorar este resultado, mas fazer isto fugia do escopo do desafio e necessitaria de mais alguns dias. 

Temos um exemplo de uma aplicação no Notebook Jupyter disponibilizado no arquivo `MongoDB/consumo_dados.ipynb`, que cria uma conexão com o banco de dados e define alguns queries escritos em Python. Utilizamos os queries para criar uma simples interface gráfica onde o usuário pode digitar os filtros que deseja utilizar, e o resultado da consulta é aberto como uma tabela no Dash. Observação: Para funcionar, é necessário ter configurado o Jupyter Dash. 

![alt text](GIFS/teste_consulta.gif)

No mesmo arquivo de exemplo, uma consulta também foi escrita para encontrar o preço mínimo, médio e máximo de um produto nos quatro sites diferentes (Casas Bahia, Magazine Luiza, Mercado Livre e Produto Mercado Livre). Criamos uma aplicação dash que faz esta consulta para três marcas de celulares diferentes, e permite ver três gráficos interativos diferentes com um dropdown, que permite selecionar a marca do celular, que como consequência atualiza o gráfico.


![alt text](GIFS/teste_plots.gif)
