#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as pd
import requests

def scrape_blog_front_page():
    """Gathers/creates a table of blog first page"""    
    table = []

    url = 'http://www.virology.ws/page/1'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    for element in soup.find_all('div', {'class': 'site-inner'}):
        dates = element.find_all('time', {'itemprop':'datePublished'})
        title = element.find_all('h2', {'itemprop':'headline'})
        link = element.find_all('a', {'class':'entry-title-link'}, href=True)
        for date, title, link in zip(dates, title, link):
            row = []
            row.append(date.text)
            row.append(title.text)
            row.append(link['href'])
            table.append(row)

    df = pd.DataFrame(data=table, columns=['Date', 'Title', 'Link'])
    return df

df_scrape = scrape_blog_front_page()
df_old = pd.read_csv('https://raw.githubusercontent.com/bbennett80/virology_blog/main/virology_blog.csv')
df_append = df_scrape[~df_scrape.Title.isin(df_old.Title)]
pd.concat([df_append, df_old]).to_csv('virology_blog.csv', index=False)
