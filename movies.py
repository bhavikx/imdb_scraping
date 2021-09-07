import requests
from bs4 import BeautifulSoup
import re

import pandas as pd

url = 'https://www.imdb.com/chart/top'
res = requests.get(url)
html = BeautifulSoup(res.text, 'html.parser')

print("Request Status:",res.status_code)
print("")

movie_name = [i.get_text() for i in html.select('td.titleColumn a')]
ratings = [i.get_text() for i in html.select('td.ratingColumn strong')]
year = [i.get_text() for i in html.select('td.titleColumn span')]

href = ["https://m.imdb.com"+i.attrs.get('href') for i in html.select('td.posterColumn a')]

moviesd = {'movie':[], 'year':[], 'runtime':[], 'ratings':[], 'description':[]}

for n in range(0,10):
    mres = requests.get(href[n])
    mhtml = BeautifulSoup(mres.text, 'html.parser')

    runtime = mhtml.select('ul.TitleBlockMetaData__MetaDataList-sc-12ein40-0 li.ipc-inline-list__item')
    
    print(movie_name[n] ,'◾',year[n][1:-1],'◾', runtime[-1].get_text() ," ⭐", ratings[n])
    
    des = mhtml.select('span.GenresAndPlot__TextContainerBreakpointL-cum89p-1')
    print(des[0].get_text())

    print("----------------------------------------------------------")    

    moviesd['movie'].append(movie_name[n])
    moviesd['year'].append(year[n][1:-1])
    moviesd['runtime'].append(runtime[-1].get_text())
    moviesd['ratings'].append(ratings[n])
    moviesd['description'].append(des[0].get_text())

movies = pd.DataFrame(moviesd)
print(movies)
movies.to_csv('movies.csv')
