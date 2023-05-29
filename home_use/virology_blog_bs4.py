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


def previous_max_page():
    with open('page.txt', 'r') as previous_last_page:
        page = previous_last_page.read()
    
    return int(page)


def write_max_page(max_page):
    with open('page.txt', '+w') as last_page:
        last_page.write(str(max_page))
    
    return


def get_max_page():
    """Searches for the last page in the blog"""
    print('Looking at blog page: ')
    
    starting_page = previous_max_page()
    
    for i in range(starting_page, 10000):
        url = f'https://virology.ws/virology-posts/{i}'
        print(i)
        r = requests.get(url)
        if r.status_code != 200:
            max_page = i
            print(f'\nThe last page in the blog is {max_page}\n')
            write_max_page(max_page)
            break
            
    return max_page


def scrape_blog(max_page):
    """Gathers/creates a table of blog posts"""
    
    table = []

    for i in range(1, max_page):

        url = f'http://www.virology.ws/page/{i}'
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
    df.to_csv('Virology_Blog.csv', index=False)
    return df
    

if __name__=='__main__':
    main()
