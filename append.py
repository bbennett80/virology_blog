#!/usr/bin/env python3
import requests
import lxml.html
import pandas as pd

dates = []
titles = []
links = []

url = 'https://www.virology.ws/'
r = requests.get(url)
s = lxml.html.fromstring(r.content)

for d in range(1, 11):
    date = str(s.xpath(f'/html/body/div/div/div/main/article[{d}]/header/p/time/text()'))
    title = str(s.xpath(f'/html/body/div/div/div/main/article[{d}]/header/h2/a/text()'))
    link = str(s.xpath(f'/html/body/div/div/div/main/article[{d}]/header/h2/a/@href'))
    date_form = date.strip("[]'")
    
    dates.append(date_form)
    title_form = title.strip("[]'")
    titles.append(title_form)
    link_form = link.strip("[]'")
    links.append(link_form)

data = {'Date': dates, 'Title': titles, 'Link': links} 
df_scrape = pd.DataFrame(data = data)

df_old = pd.read_csv('https://raw.githubusercontent.com/bbennett80/virology_blog/main/virology_blog.csv')

df_append = df_scrape[~df_scrape.Title.isin(df_old.Title)]

df_append.append(df_old).to_csv('virology_blog.csv', index=False)
