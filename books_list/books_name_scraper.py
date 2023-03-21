import requests
from bs4 import BeautifulSoup
import lxml

headers = {
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
	}



books = ''
category = 'future'
pages = 10
for page in range(1,int(pages)+1):
	response = requests.get(f'https://fourminutebooks.com/category/{category}/page/{page}/', headers = headers)
	html = response.text
	response.close()
	soup = BeautifulSoup(html, 'lxml')
	book_scrape = soup.find_all('h2')
	for _ in book_scrape:
		if _.get_text()=='Posts navigation':
			continue
		books += _.get_text()+'\n'

category = 'the Future'
with open(f'categories/{category}.txt', 'w') as f:
	f.write(books)