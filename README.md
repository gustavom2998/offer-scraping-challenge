# Desafio Birdie: Coleta de Oferta de Produtos
Este repositório contém todo o conteúdo desenvolvido para o Desafio Técnico do processo seletivo de estágio como Engenheiro de dados da Birdie. 

## Resumo

Para a coleta e preparo dos dados, a linguagem de programação *Python* foi utilizada. Os dados de links foram estruturados dentro do Python utilizando a dataframes da biblioteca *Pandas*. O pacote *Requests*  foi utilizado para fazer requisições HTTP para obter o conteúdo das páginas disponibilizadas nos respectivos links, de cada linha do dataframe. A biblioteca *Beautiful Soup* foi utilizada para analisar e extrair os conteúdo de cada página, e os dados encontrados foram inseridos nas colunas vazias de cada linha do dataframe. Para agilizar o processo de coleta de dados, a biblioteca *Multiprocessing* foi utilizada para dividir a carga de trabalho entre múltiplas threads, onde cada thread recebia um subconjunto do dataframe e realiza o processo de requisição e análise (com as bibliotecas anteriormente mencionadas). Finalmente, os dados foram reunidos e inseridos em um banco de dados *MongoDB*, configurado através da plataforma online *MongoDB Atlas*.  A GUI *MongoDB Compass* para simplificar o processo de consultas e gerenciar o banco de dados. Por último, para exemplificar um caso de uso do banco de dados, o *Jupyter Notebooks* (na versão Jupyter Lab) foi utilizado para conectar ao banco de dados com o usuário público (que pode apenas fazer consultas). Para estabelecer a conexão, a biblioteca *PyMongo* foi utilizada. Utilizando as bibliotecas *Dash*, *Plotly* e *IPyWidgets*, duas aplicações foram criadas. A primeira permite fazer queries com filtres no banco de dados, sem o usuário ter que mexer no código. O usuário pode ainda ordenar, novamente filtrar, e baixar os dados obtidos do query. Outro exemplo foi feito onde o usuário pode consultar dados de custos de produtos sobre diferentes marcas, obtendo o preço mais barato, mais caro, e médio para as ofertas. O resultado foi demonstrado graficamente em uma aplicação dash. 

## Descrição do Desafio

Segue uma breve descrição do desafio para contextualizar o problema.

1. Baixar e armazenar o conteúdo de uma lista de 40 mil URLs de ofertas (`offers.csv` - disponibilizado no repositório).

2. Extrair e armazenar pelo menos o título e o preço dos produtos para que seja consultável. 

3. Fornecer uma forma de consultar pelo conteúdo armazenado.

4. Prepare uma apresentação sobre a arquitetura da solução.

## Arquivos Disponiblizados

Vários arquivos diferentes foram criados para resovter este problema. Abaixo está uma lista que explica o objetivo dos principais arquivos e pastas destes diretórios. 

* `Casas Bahia/`: Diretório com CSV com dados coletados e dados não coletados para os sites da Casas Bahia, logs de coleta, logs de exceções. 
* `Magazine Luiza/`: Diretório com CSV com dados coletados e dados não coletados para os sites da Magazine Luiza, logs de coleta, logs de exceções. 
* `Mercado Livre/`:  Diretório com CSV com dados coletados e dados não coletados para os sites do Mercado Livre, logs de coleta, logs de exceções. 
* `MongoDB/`: Possuí os script para criação do banco de dados e um notebook Jupyter que conecta ao banco de dados, e possuí queries, e uma aplicação muito básica de consulta com filtros, search, e exportação dos resultados. 
* `header_rotation.py`: Utilizado para organizar os headers e lista de user agents, utilizado para as requisições HTTP. Contém funções para seleção de headers/user agents aleatórios.
* `multithread_df.py`: Define uma função que recebe um dataframe e uma função. Múltiplas threads são utilizadas para dividir o dataframe e aplicar as operações da função sob o dataframe.
* `parser.py`: Script contendo função utilizada para iterar sobre os links. Para cada link, um request HTTP é feito e o conteúdo web retornado é analisado para extração de dados com o BeautifulSoup. 
* `prepara_offers.py`: Primeiro script que deve ser executado neste repositório. Utiliza o `offers.csv` para obter os links e gera as tabelas de cada site(Casas Bahia, Magazine Luiza, etc.).
* `update_CasasBahia.py`: Script que carrega os dados da pasta Casas Bahia e encontra todos os links que possuí dados ausentes. Os dados que já foram obtidos são mantidos como estão. Executa indefinitivamente até todos os links forem obtidos. 
* `update_MagazineLuiza.py`:  Script que carrega os dados da pasta Magazine Luiza e encontra todos os links que possuí dados ausentes. Os dados que já foram obtidos são mantidos como estão. Executa indefinitivamente até todos os links forem obtidos. 
* `update_MercadoLivre.py`:  Script que carrega os dados da pasta Mercado Livre e encontra todos os links que possuí dados ausentes. Os dados que já foram obtidos são mantidos como estão. Executa indefinitivamente até todos os links forem obtidos. 

## Como utilizar

O primeiro passo é executar o Script `prepara_offers.py`. Este script reinicia todos os CSVs e logs para que os únicos dados que estejam presentes são os links. Pode ser necessário ajustar o diretório (como executei em uma IDE pré-configurada, não tive problemas).

Em sequência, pode-se executar qualquer um dos scripts `update_CasasBahia.py`, `update_MazineLuiza.py` ou  `update_MercadoLivre.py`. Eles podem ser executados em paralelo. Cada script inicia o processo de requisições utilizando todos os links, e pausa por um tempo (em torno) de 15 minutos. Cada script utiliza múltiplas threads, então pode ser pesado executar-los na máquina local. Seria interessante utilizar uma máquina virtual na nuvem com alto poder de processamento, assim um grande número de threads poderia ser utilizado. No GIF abaixo, um exemplo da execução dos scripts utilizando apenas 200 links de cada site foi disponibilizado. Para compreender o porque nem todos sites retornaram todos os links, veja a seção de resultados. Um pequeno corte foi adicionado para a coleta dos linkks da Magazine Luiza e Mercado Livre, pois eles são mais demorados. 

<div style="height: 0; padding-bottom: calc(53.85%); position:relative; width: 100%;"><iframe allow="autoplay; gyroscope;" allowfullscreen height="100%" referrerpolicy="strict-origin" src="https://www.kapwing.com/e/605ceb4c93e27f003dc65452" style="border:0; height:100%; left:0; overflow:hidden; position:absolute; top:0; width:100%" title="Embedded content made on Kapwing" width="100%"></iframe></div><p style="font-size: 12px; text-align: right;"></a></p>

![alt text](https://www.kapwing.com/e/605ceb4c93e27f003dc65452)


Quando estiver satisfeito com o número de links coletados (pode ser consultado através do log de execução), o script `MongoDB/upload_dados.py` pode ser utilizado para fazer o upload a um cluster do MongoDB Atlas. Para isso, é necessário ter configurado um cluster com usuários de acesso e também com IPs de acesso. Para confirmar que os resultados foram realmente disponibilizados na plataforma, mostramos abaixo o schema da coleção disponibilizada através do MongoDB Compass.

<div style="height: 0; padding-bottom: calc(56.28%); position:relative; width: 100%;"><iframe allow="autoplay; gyroscope;" allowfullscreen height="100%" referrerpolicy="strict-origin" src="https://www.kapwing.com/e/605ca75d66daba0099d59109" style="border:0; height:100%; left:0; overflow:hidden; position:absolute; top:0; width:100%" title="Embedded content made on Kapwing" width="100%"></iframe></div><p style="font-size: 12px; text-align: right;"></a></p>

![alt text](https://www.kapwing.com/e/605ca75d66daba0099d59109)


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

Para os links da Casas Bahia conseguimos coletar 6.080 de 6.080 links. A coleta foi finalizada em 3 execuções utilizando 12 threads, onde  a partir da primeira execução que durou 5 minutos 6076 links já haviam sido coletados. O delay adotado foi de 15 minutos.

Para os links do Mercado Livre conseguimos obter 340 de 340 links, e 14.073 de 16.167 do Produtos Mercado Livro. O processo de coleta desde foi o mais demorado, e executamos o script ao longo de dois dias. A partir dos 10.477 links iniciais que foram coletados em uma única execução, aparentemente os links restantes necessitavam de múltiplas tentativas de acesso para carregar a página. Isto foi confirmado através de acesso de links manuais. Para a coleta, 10 execuções foram realizadas com 12 threads e 20 execuções foram realizadas com 12 threads. Tanto delays de 5 minutos quanto 15 minutos foram utilizados.

Para os links da Magazine Luiza conseguimos obter 4.231 de 17.413 links. Para a coleta 3 execuções foram realizadas utilizando 12 threads e 9 execuções foram realizadas utilizando 6 threads. A partir da terceira execução nenhum link adicional foi encontrado. Inicialmente um delay de 5 minutos foi utilizado, porém, para tentar melhorar os resultados, um delay de 15 minutos foi adotado posteriormente. Também acessamos algumas dezenas de links aleatórios manualmente e eles não funcionaram. Vale ressaltar que conseguimos acessar alguns links "novos" obtidos manualmente do site da Magazine Luiza, logo, é válido sugerir que não há problemas no script necessariamente. Pode ser também que algo esteja errado com o cabeçalho utilizado, mas inúmeros testes foram realizados e esta questão ficou em aberta. Seria possível extrair novos links para melhorar este resultado, mas fazer isto fugia do escopo do desafio e necessitaria de mais alguns dias. 

Temos um exemplo de uma aplicação no Notebook Jupyter disponibilizado no arquivo `MongoDB/consumo_dados.ipynb`, que cria uma conexão com o banco de dados e define alguns queries escritas em Python. Utilizamos os queries para criar uma simples interface gráfica onde o usuário pode digitar os filtros que deseja utilizar, e o resultado da consulta é aberto como uma tabela no Dash. Observação: Para funcionar, é necessário ter configurado o Jupyter Dash. 

<div style="height: 0; padding-bottom: calc(56.25%); position:relative; width: 100%;"><iframe allow="autoplay; gyroscope;" allowfullscreen height="100%" referrerpolicy="strict-origin" src="https://www.kapwing.com/e/605cd625e0d2ff00d06a7c39" style="border:0; height:100%; left:0; overflow:hidden; position:absolute; top:0; width:100%" title="Embedded content made on Kapwing" width="100%"></iframe></div><p style="font-size: 12px; text-align: right;"></a></p>

![alt text](https://www.kapwing.com/e/605cd625e0d2ff00d06a7c39)

No mesmo arquivo de exemplo, uma consulta também foi escrita para encontrar o preço mínimo, médio e máximo de um produto nos quatro sites diferentes (Casas Bahia, Magazine Luiza, Mercado Livre e Produto Mercado Livre). Criamos uma aplicação dash que faz esta consulta para três marcas de celulares diferentes, e permite ver três gráficos interativos diferentes com um dropdown, que permite selecionar a marca do celular, que como consequência atualiza o gráfico.

<div style="height: 0; padding-bottom: calc(56.25%); position:relative; width: 100%;"><iframe allow="autoplay; gyroscope;" allowfullscreen height="100%" referrerpolicy="strict-origin" src="https://www.kapwing.com/e/605cd79293e27f003dc638a2" style="border:0; height:100%; left:0; overflow:hidden; position:absolute; top:0; width:100%" title="Embedded content made on Kapwing" width="100%"></iframe></div><p style="font-size: 12px; text-align: right;"></a></p>

![alt text](https://www.kapwing.com/e/605cd79293e27f003dc638a2)
