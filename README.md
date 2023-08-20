# Technical Challange: Scraping Offers from E-commerce Products

English (EN) | [Portuguese (PT-BR)](./README-pt.md) 
This repository contains all the content developed for the Technical Challenge for a Data Engineering internship role at Birdie (I got hired - yay).

## Challenge Description

Here's a brief description of the challenge to provide context for the problem:

1. Download and store the content of a list of 40,000 offer URLs ([`offers.csv`](./offers.csv)).
2. Extract and store at least the title and price of the products to make them queryable.
3. Provide a way to query the stored content.
4. Prepare a presentation about the architecture of the solution.

The URLs contain offers from three large Brazilian e-commerce retailers. 

## Tech Used

For data collection and preparation, I used **Python**. The URLs provided via CSV were used to create a **Pandas** Dataframe structure with complementary data. The **Requests** package was used to make HTTP requests to retrieve the content of the pages provided in the respective links for each row in the dataframe. The **BeautifulSoup** library was used to parse the content from each page, and the data was inserted into the empty columns of each dataframe row.

To speed up the data collection process, the **Multiprocessing** library was used to distribute the workload among multiple threads. Each thread received a subset of the dataframe and carried out the process of running the requests and processing the results (using the aforementioned libraries). The data was collected and inserted into a **MongoDB** instance, which was configured and managed through the online platform **MongoDB Atlas**. The **MongoDB Compass** platform was used to simplify the process of querying and managing the database.

Finally, to exemplify a use case of the database, **Jupyter Notebooks** (Jupyter Lab version) were made to connect to the database via the public user (with read-only access). The **PyMongo** library was used to establish the connection. Using the **Dash**, **Plotly**, and **IPyWidgets** libraries, two applications were created. The first one allows users to make queries with different filters on the database without having to modify the code. Users can sort, filter again, and download the data obtained from the query. Another example was created where users can retrieve cost data for products from different brands, obtaining the lowest, highest, and average prices for the offers. The results were displayed graphically in a dash application.

## File Tree

Several different files have been created to solve this problem. Below is a list that explains the purpose of the main files and folders in these directories.

* [`GIFS/`](./GIFS): Folder containing the GIFs used for the README.
* [`Casas Bahia/`](./Casas%20Bahia): Directory with CSV files containing collected and non-collected data for Casas Bahia websites, collection logs, exception logs.
* [`Magazine Luiza/`](./Magazine%20Luiza): Directory with CSV files containing collected and non-collected data for Magazine Luiza websites, collection logs, exception logs.
* [`Mercado Livre/`](./Mercado%20Livre): Directory with CSV files containing collected and non-collected data for Mercado Livre websites, collection logs, exception logs.
* [`MongoDB/`](./MongoDB): Scripts for database creation and a Jupyter notebook for running queries with basic use cases (filters, search, and export).
* [`header_rotation.py`](./header_rotation.py): Used to organize headers, user agents, and random selection used for HTTP requests.
* [`multithread_df.py`](./multithread_df.py): Define a function that receives a dataframe and a function as inputs. Multiple threads are used to split the dataframe and apply the function's operations on the dataframe.
* [`parser.py`](./parser.py): Script containing the function used to iterate over the links. For each link, an HTTP request is made, and the returned web content is analyzed for data extraction using BeautifulSoup.
* [`prepara_offers.py`](./prepara_offers.py):  Entry point script. It uses `offers.csv` to obtain the links and generates the tables for each site (Casas Bahia, Magazine Luiza, etc.).
* [`update_CasasBahia.py`](./update_CasasBahia.py): Script that loads data from the Casas Bahia folder and finds all links with missing data. The data that has already been obtained is kept as is. It runs indefinitely until all links have been obtained.
* [`update_MagazineLuiza.py`](./update_MagazineLuiza.py):  Script that loads data from the Magazine Luiza folder and finds all links with missing data. The data that has already been obtained is kept as is. It runs indefinitely until all links have been obtained.
* [`update_MercadoLivre.py`](./update_MercadoLivre.py): Script that loads data from the Mercado Livre folder and finds all links with missing data. The data that has already been obtained is kept as is. It runs indefinitely until all links have been obtained.

## How to use this repository

The first step is to execute the prepara_offers.py script. This script resets all the CSVs and logs so that the only data in the dataframe are the links. It may be necessary to adjust the directory (as I executed it in a pre-configured IDE, I had no issues).

Next, you can execute any of the scripts [`update_CasasBahia.py`](./update_CasasBahia.py), [`update_MagazineLuiza.py`](./update_MagazineLuiza.py), or [`update_MercadoLivre.py`](./update_MercadoLivre.py). They can be run in parallel. Each script initiates the request process using all the links and pauses for a 15-minute interval. Each script uses multiple threads, so running them on a local machine might be resource-intensive. Using a cloud instance with high processing power is an interesting option, where a large number of threads could be utilized. Below is an example of script execution using only 200 links from each site. To understand why not all sites returned all the links, refer to the results section. A small time jump was made for collecting links from Magazine Luiza and Mercado Livre, as they take more time.

![alt text](GIFS/teste_coleta.gif)

When you are satisfied with the number of collected links (which can be checked through the execution log), the [`MongoDB/upload_dados.py`](./MongoDB/upload_dados.py) script can be used to upload the data, storing it in a MongoDB Atlas cluster. For this purpose, it's necessary to have configured a cluster with access users and permitted IPs. To confirm that the results have indeed been made available on the platform, we provide below the schema of the collection displayed through MongoDB Compass.

![alt text](GIFS/teste_bd.gif)


For this project, two users have been configured. One for administrative purposes, capable of updating, removing, and inserting data. Another user has also been created, with access limited to querying. This user has been made available, and anyone can use the information to access and query the database. The network access configuration has been set up in a way that allows anyone to access the database. This information was made available since this is a trial instance with limited resources to showcase this project. Normally, credentials wouldn't be published and we could instead have a REST API receive public user requests and return results, without having the risk of the public accessing any secrets or making any undesired changes to the data.

```
user: public_user
password: KiwhjUOdauK06lzg
collection: links_ofertas
```

For connections with Python, we can use the `PyMongo` package and the public credentials to query the data with a Python client:

```
client = pymongo.MongoClient("mongodb+srv://public_user:KiwhjUOdauK06lzg@cluster-desafiobirdie.43lqn.mongodb.net/links_ofertas?retryWrites=true&w=majority")
db = client.dados_links

```

## Results

Different strategies were necessary for collecting the maximum amount of content from the various retailers.

For Casas Bahia links, we managed to collect 6,080 out of 6,080 links. The collection was completed in 3 runs using 12 threads. From the first run, which lasted 5 minutes, 6,076 links were already collected. The delay used for retrying the collection was 15 minutes.

For the Mercado Livre links, we obtained 340 out of 340 links, and 14,073 out of 16,167 from Produtos Mercado Livre (which has a different structure from the regular Mercado Livre page, hence treated separately). The collection process for this site was the most time-consuming, requiring the script to be executed over two days. Starting from the initial 10,477 links collected in a single run, it appeared that the remaining links needed multiple access attempts to load the page. This was confirmed through manual link access. For the collection, 10 runs with 12 threads each and 20 runs with 12 threads each were conducted, totaling 30 runs. Delays of both 5 and 15 minutes were used.

For the Magazine Luiza links, we obtained 4,231 out of 17,413 links. The collection involved 3 runs with 12 threads and 9 runs with 6 threads. No additional links were found after the third run. Initially, a 5-minute delay was used, but to improve results, a 15-minute delay was later adopted. We also manually accessed a few dozen random links, and they didn't work. It's worth noting that we managed to access some "new" links obtained manually from the Magazine Luiza website, suggesting that the script isn't necessarily problematic. It's also possible that something might be wrong with the header used, but numerous tests were conducted, and this issue remained unresolved. It would be possible to extract new links to improve this result, but doing so would go beyond the scope of the challenge and would require a few more days.


We have an example of an application in the provided Jupyter Notebook file [`MongoDB/consumo_dados.ipynb`](MongoDB/consumo_dados.ipynb), which establishes a connection to the database and runs some queries with Python. We use these queries to create a simple graphical interface where the user can input the desired filters, and the query results are displayed as a table in Dash. Note: To make it work, it's necessary to have Jupyter Dash configured.

![alt text](GIFS/teste_consulta.gif)

In the same example file, a query was also written to find the minimum, average, and maximum prices of a product on four different sites (Casas Bahia, Magazine Luiza, Mercado Livre, and Produto Mercado Livre). We have created a Dash application that executes this query for three different mobile phone brands, enabling the visualization of three distinct interactive graphs through a dropdown menu. This dropdown menu allows the selection of a cellphone brand, which subsequently updates the graph accordingly.

![alt text](GIFS/teste_plots.gif)
