#!/usr/bin/env python3
import requests
import lxml.html
import pandas as pd

dates = []
titles = []
links = []

#i = 1  start from first page of blog
i = 1
print('Seaching virology.ws for blog posts')

while True: 
    url = f'https://www.virology.ws/page/{i}'
    i += 1
    response = requests.get(url)
    if response.status_code != 200:
        break
    else:
        soup = lxml.html.fromstring(response.content)
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
df = pd.DataFrame(data = data)

#df.to_html('virology_blog.html', render_links=True)
df.to_csv('virology_blog.csv', index=False)
