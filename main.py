import json
import time
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError
# from requests.exceptions import ReadTimeout
# from requests.exceptions import RequestException
# from requests.exceptions import HTTPError
# from requests.exceptions import Timeout
# from requests.exceptions import TooManyRedirects
BASE_URL = 'https://kvkk.gov.tr'
API_URL = "https://kvkk.gov.tr/veri-ihlali-bildirimi/?page="
# Example: https://kvkk.gov.tr/veri-ihlali-bildirimi/?page=1
# Static and Dynamic Variables
currentPage = 1
maxPage = 1
data = []

# Get Article Function
def getArticle(url):
    try:
        html_page = requests.get(url, timeout=20).content
        soup = BeautifulSoup(html_page, 'html.parser')
        article = soup.find('div', class_='blog-post-inner').find('div')
        return str(article)
    except ConnectTimeout:
        print('Request has timed out %s' % url)
        return ''
    except ConnectionError:
        print('Request has Connection Error %s' % url)
        return ''

# loop
while currentPage <= maxPage:
    url = API_URL + str(currentPage)
    try:
        html_page = requests.get(url, timeout=20).content
    except ConnectTimeout:
        print('Request has timed out %s' % url)
        continue
    except ConnectionError:
        print('Request has Connection Error %s' % url)
        continue

    soup = BeautifulSoup(html_page, 'html.parser')

    # Set Max Page
    if currentPage == 1:
        maxPage = int(soup.find_all('a', class_='page-link').pop().attrs['href'].split('=')[1])
        print('Max Page:',maxPage)
    print('Current Page:', currentPage)

    # Get Blog Data
    blogDate = soup.find('div', class_='blog-post-inner').find('p', class_='small-text').text
    blogTitle = soup.find('h3', class_='blog-post-title').text
    blogUrl = BASE_URL+soup.find('a', class_='arrow-link all-items').attrs['href']
    blogImage = BASE_URL+soup.find('div', class_='blog-post-image').find('img').attrs['src']
    blogContent = getArticle(blogUrl)
    time.sleep(3)

    # print('Blog Date:', blogDate)
    # print('Blog Title:', blogTitle)
    # print('Blog Url:', blogUrl)
    # print('Blog Image:', blogImage)
    # print('Blog Content:', blogContent)

    # Add Data to Array
    data.append({
        'date': blogDate,
        'title': blogTitle,
        'url': blogUrl,
        'image': blogImage,
        'content': blogContent
    })

    # Get Grid Data
    grid = soup.find_all('div', class_='col-lg-4 col-md-6 col-sm-12 pb-3')
    for item in grid:
        item = item.find('div', class_='blog-grid-item h-100 d-block')
        gridDate = item.find('span').text
        gridTitle = item.find('h4', class_='blog-grid-title').find('a').attrs['title']
        gridUrl = BASE_URL+item.find('a').attrs['href']
        gridImage = BASE_URL+item.find('img').attrs['src']
        gridContent = getArticle(gridUrl)
        time.sleep(3)

        # print('Grid Date:', gridDate)
        # print('Grid Title:', gridTitle)
        # print('Grid Url:', gridUrl)
        # print('Grid Image:', gridImage)
        # print('Grid Content:', gridContent)

        # Add Data to Array
        data.append({
            'date': gridDate,
            'title': gridTitle,
            'url': gridUrl,
            'image': gridImage,
            'content': gridContent
        })
    print('Page Completed:', currentPage)
    time.sleep(5)
    currentPage += 1

# file write
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

print('Total Data:', len(data))

# await request with python
# import requests
# r = requests.get('https://kvkk.gov.tr/veri-ihlali-bildirimi/?page=1')
# soup = BeautifulSoup(r.text, 'html.parser')


#print(soup.prettify())