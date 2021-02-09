#!/usr/bin/env python3
import requests
import lxml.html
import pandas as pd

dates = []
titles = []
links = []
#i = 1  start from first page of blog
# i = 1
print('Seaching virology.ws for blog posts')
url = 'https://www.virology.ws/'
r = requests.get(url)
soup = lxml.html.fromstring(r.content)
for d in range(1, 11):
    date = str(soup.xpath(f'/html/body/div/div/div/main/article[{d}]/header/p/time/text()'))
    title = str(soup.xpath(f'/html/body/div/div/div/main/article[{d}]/header/h2/a/text()'))
    link = str(soup.xpath(f'/html/body/div/div/div/main/article[{d}]/header/h2/a/@href'))
    date_form = date.strip("[]'")
    if not date_form:
        break
    dates.append(date_form)
    title_form = title.strip("[]'")
    titles.append(title_form)
    link_form = link.strip("[]'")
    links.append(link_form)
    print(f'Gathering information from {date} post.')

data = {'Date': dates, 'Title': titles, 'Link': links} 
df_scrape = pd.DataFrame(data = data)

df_old = pd.read_csv('https://raw.githubusercontent.com/bbennett80/virology_blog/main/virology_blog.csv')

df_append = df_scrape[~df_scrape.Title.isin(df_old.Title)]

df_append.append(df_old).to_csv('virology_blog.csv', index=False)
