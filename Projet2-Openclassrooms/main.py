import requests
from bs4 import BeautifulSoup


URL_TO_GET = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
r = requests.get(URL_TO_GET)
r.headers['content-type']
soup = BeautifulSoup(r.text, 'html.parser')

results = {}
product_page_url=""
review_rating=""
image_url=""

print('=================================')
print('=================================')
print('=================================')

results['title'] = soup.find_all('div', class_ ="product_main")[0].h1.string
table_book_info = soup.findAll('tr')
results['universal_product_code'] = table_book_info[0].td.string
#get prices while excluding the first char
results['price_excluding_tax'] = table_book_info[2].td.string[1::]
results['price_including_tax'] = table_book_info[3].td.string[1::]
nb_books = table_book_info[5].td.string
nb_books = nb_books.split()
results['number_available'] = nb_books[2][1::]
#get last p html tag which match the description section
#do not know which one is better
description = soup.find('article').findAll('p')[-1]
description = soup.find(id='product_description').findNext('p').text
results['product_description'] = description
#Get category info
category = soup.find('ul', attrs={'class': 'breadcrumb'})
category = category.find_all('a')[2].text
results['category'] = category

print(results)
print("u-u-u-u-u-u-u-u")
print("u-u-u-u-u-u-u-u")
print("u-u-u-u-u-u-u-u")

