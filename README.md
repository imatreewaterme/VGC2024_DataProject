******VGC2024_DataProject******
**Dependencies**: numpy, pandas, BeautifulSoup, Matplotlib

**VGC 2024 Top Pokemon Movesets/Types data**

**Part I:**
Consume the data
Data Source: https://www.nimbasacitypost.com/2024/08/world-championships-2024.html
Scrape this page and extract the URL's with the Pokemon from each team on the list using BeautifulSoup to pull the hrefs (EG: https://pokepast.es/aa2521bd541f3858)
Scrape each of these pages and parse the data into a python dictionary, then write the dictionary for a CSV
Challenges: data inconsistencies require custom for clauses and conditional statements to parse properly.
Due to the small volume of data (just over 600 rows) I opted to write the data to a csv and will be doing data analysis with the pandas libary specifically dataframes. 

**Part II:**
Create Data Visualizations
Using Matplotlib to create data visualizations for key metrics
