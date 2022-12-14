from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import trange

def main():
    """A simple script that gathers Date, Title, and Link from virology.ws blog using BeautifulSoup.
    This version of the blog scraper should be a bit more user friendly to use at home, or for the novice coder.
    Please feel free to use, modify, or imporove.
    """
    max_page = get_max_page()
    create_table = scrape_blog(max_page)
    write_table(create_table)


def get_max_page():
    """Searches for the last page in the blog"""
    print('Looking at blog page: ')
    
    #The starting point in range is 410. Will be adjusted higher as blog pages increase.
    #This is used to keep down requests to the blog server.
    for i in range(410, 10000):
        url = f'http://www.virology.ws/page/{i}'
        print(i)
        r = requests.get(url)
        if r.status_code != 200:
            max_page = i
            print(f'\nThe last page in the blog is {max_page}\n')
            break
    return max_page

def scrape_blog(max_page):
    """Gathers/creates a table of blog posts"""
    print('Gathering blog post information...')
    
    table = []

    for i in trange(1, max_page):

        url = f'http://www.virology.ws/page/{i}'
        r = requests.get(url)
        if r.status_code != 200:
            break
        else:
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
    return table
                    
def write_table(table):
    df = pd.DataFrame(data=table, columns=['Date', 'Title', 'Link'])
    df.to_csv('Virology_Blog.csv', index=False)
    return df
    

if __name__=='__main__':
    main()
