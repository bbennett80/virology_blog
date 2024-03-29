#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as pd
import requests

def main():
    """A simple script that gathers Date, Title, and Link from virology.ws blog using BeautifulSoup.
    This version of the blog scraper should be a bit more user friendly to use at home, or for the novice coder.
    Please feel free to use, modify, or imporove.
    """
    max_page = get_max_page()
    create_table = scrape_blog(max_page)
    write_table(create_table)


def get_max_page():
    """finds the last blog page number"""
    
    url = f'https://virology.ws/virology-posts/'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    
    block = soup.find_all('ul', {'class': 'page-numbers'})
    
    for element in block:
        page = element.find_all('a', {'class': 'page-numbers'})
        max_page = page[2].text
        
    return int(max_page)


def scrape_blog(max_page):
    """Gathers/creates a table of blog posts"""
    
    table = []
    
    max_page = get_max_page()
    print(f'There are {max_page} pages to look through.\n')

    for i in range(1, max_page+1):
        print('Looking at blog page: ', i)


        url = f'https://virology.ws/virology-posts/page/{i}'
        r = requests.get(url)
        if r.status_code != 200:
            break
        else:
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')

            for element in soup.find_all('div', {"class": "uabb-blog-post-content"}):
                dates = element.find_all('span', {'class':'uabb-meta-date'})
                titles = element.find_all('a', {'tabindex': '0'})

                for date, title in zip(dates, titles):
                    row = []
                    row.append(date.text.strip('\n\r\t'))
                    row.append(title.text)
                    row.append(title['href'])
                    table.append(row)
    return table
                    
def write_table(table):
    df = pd.DataFrame(data=table, columns=['Date', 'Title', 'Link'])
    df.to_csv('virology_blog.csv', index=False)
    return df
    

if __name__=='__main__':
    main()
