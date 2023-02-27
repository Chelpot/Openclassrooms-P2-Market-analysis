import math
import os

import requests
import pandas as pd

from bs4 import BeautifulSoup

URL_WEBSITE = 'https://books.toscrape.com'

# Create images/output directories if it doesn't exist
try:
    os.mkdir("images")
except OSError as error:
    print(error)
try:
    os.mkdir("output")
except OSError as error:
    print(error)

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
    print(url)
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
    try:
        description = soup.find(id='product_description').findNext('p').text
        results['product_description'] = description
    except AttributeError as error:
        print(error)
        results['product_description'] = "No description"


    # Category
    category = soup.find('ul', attrs={'class': 'breadcrumb'})
    category = category.find_all('a')[2].text
    results['category'] = category

    # Review rating
    results['review_rating'] = get_review_rating()

    # Image URL
    url_end = soup.find('img').attrs['src']
    image_url = URL_WEBSITE + url_end[5::]
    results['image_url'] = image_url

    # URL for page product
    results['product_page_url'] = url

    return results


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
    return categories_url


def get_pages_url_for_category(url):
    r = requests.get(url)
    r.headers['content-type']
    soup = BeautifulSoup(r.text, 'html.parser')

    pages_url = []
    data = soup.find(class_='form-horizontal')
    data = data.findAll('strong')

    number_of_books = int(data[0].text)
    nb_pages = 0

    # If category have more than 1 page
    if len(data) > 1:
        number_of_books_per_page = int(data[2].text)
        nb_pages = math.ceil(number_of_books / number_of_books_per_page)

        for i, page in enumerate(range(0, nb_pages)):
            url = create_indexed_url(i, url)
            pages_url.append(url)
    # If category only have 1 page
    else:
        url = create_indexed_url(0, url)
        pages_url.append(url)

    return pages_url


def create_indexed_url(i, url):
    url = str(url).split('/')
    url.pop(-1)
    url = '/'.join(url)
    url += '/'
    if i == 0:
        url += 'index.html'
    else:
        url += 'page-{}.html'.format(i + 1)
    return url


def scrap_list_books_url(url):
    r = requests.get(url)
    r.headers['content-type']
    soup = BeautifulSoup(r.text, 'html.parser')

    list_books_url = []
    list_books_tag = soup.find('ol', class_='row')
    list_books_tag = list_books_tag.findAll('li')

    for book in list_books_tag:
        book = book.find('h3')
        url = URL_WEBSITE + "/catalogue/" + book.find('a').attrs['href'][9::]
        list_books_url.append(url)

    return list_books_url

def save_img(data):
    img = requests.get(data['image_url']).content
    img_name = data['image_url'].split('/')[-1]
    img_category = data['category']
    with open('images/{}'.format(img_name), 'wb') as handler:
        handler.write(img)

#Search the home page for all categories url
for category_url in get_all_categories_url().values():
    list_data = []
    #Get all the pages url from a category
    list_pages_url = get_pages_url_for_category(category_url)
    for url in list_pages_url:
        print(url)
        for book_url in scrap_list_books_url(url):
            # Get all data scraped from a product page
            data = scrap_from_url(book_url)
            list_data.append(data)
            save_img(data)

    category_name = list_data[0]['category']

    #Save data from each category in a different csv file
    df = pd.DataFrame.from_dict(list_data)
    df.to_csv('output/{}.csv'.format(category_name), index=False, header=True)

