import math
import os

import requests
from bs4 import BeautifulSoup

URL_WEBSITE = 'https://books.toscrape.com'

#Create images directory if it doesn't exist
if not os.path.exists('images'):
   os.mkdir("images")

def scrap_from_url(url):
   r = requests.get(url)
   r.headers['content-type']
   soup = BeautifulSoup(r.text, 'html.parser')
   results = {}

   def get_review_rating():
       dict_numbers = {
           'One': 1,
           'Two': 2,
           'Three': 3,
           'Four': 4,
           'Five': 5
       }
       letter_number = soup.find(class_="star-rating").attrs['class'][1]
       return dict_numbers[letter_number]

   # Title
   results['title'] = soup.find_all('div', class_="product_main")[0].h1.string
   table_book_info = soup.findAll('tr')

   # UTC
   results['universal_product_code'] = table_book_info[0].td.string

   # Prices excluding and including tax
   # get prices while excluding the first char
   results['price_excluding_tax'] = table_book_info[2].td.string[1::]
   results['price_including_tax'] = table_book_info[3].td.string[1::]

   # Number of books available
   nb_books = table_book_info[5].td.string
   nb_books = nb_books.split()
   results['number_available'] = nb_books[2][1::]

   # Product description
   # get next <p> after product_description
   description = soup.find(id='product_description').findNext('p').text
   results['product_description'] = description

   # Category
   category = soup.find('ul', attrs={'class': 'breadcrumb'})
   category = category.find_all('a')[2].text
   results['category'] = category

   # Review rating
   results['review_rating'] = get_review_rating()

   # Image URL
   url_start = 'https://books.toscrape.com'
   url_end = soup.find('img').attrs['src']
   image_url = url_start + url_end[5::]
   results['image_url'] = image_url

   # URL for page product
   results['product_page_url'] = url

   print(results)



def get_all_categories_url():
    r = requests.get(URL_WEBSITE)
    r.headers['content-type']
    soup = BeautifulSoup(r.text, 'html.parser')

    categories_url = {}
    data = soup.find('ul', class_='nav-list')
    data = data.find('ul')
    data = data.findAll('a')
    for d in data:
       category_name = " ".join(d.text.split())
       category_url = URL_WEBSITE + "/" + d.attrs['href']
       categories_url[category_name] = category_url
    print(categories_url)
    return categories_url

def scrap_for_category(url):
    r = requests.get(url)
    r.headers['content-type']
    soup = BeautifulSoup(r.text, 'html.parser')

    pages_url = []
    data = soup.find(class_='form-horizontal')
    data = data.findAll('strong')

    number_of_books = int(data[0].text)
    nb_pages = 0

    #If category only have 1 page
    if len(data)>1:
        number_of_books_per_page = int(data[2].text)
        nb_pages = math.ceil(number_of_books/number_of_books_per_page)

        for i, page in enumerate(range(0, nb_pages)):
           url = create_indexed_url(i, url)
           print(url)
           pages_url.append(url)
    else:
        url = create_indexed_url(1, url)
        print(url)
        pages_url.append(url)

    return pages_url


def create_indexed_url(i, url):
    url = str(url).split('/')
    url.pop(-1)
    url = '/'.join(url)
    url += '/'
    url += 'page-{}.html'.format(i + 1)
    return url


for a in get_all_categories_url().values():
    scrap_for_category(a)
    print('================================')

