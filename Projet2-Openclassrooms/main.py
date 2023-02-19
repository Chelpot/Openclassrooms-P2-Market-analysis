import requests
from bs4 import BeautifulSoup



def scrap_for_url(url):
    r = requests.get(URL_TO_GET)
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

URL_TO_GET = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
scrap_for_url(URL_TO_GET)