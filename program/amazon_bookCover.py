def coverScraper(book_name,amazon_link):
	import requests
	import os
	import cv2 as cv
	from bs4 import BeautifulSoup

	from selenium.webdriver import Chrome
	from webdriver_manager.chrome import ChromeDriverManager
	from selenium.webdriver.common.keys import Keys

	response = requests.get(amazon_link, timeout=5)
	if response.status_code != 200:
		link = '/'.join(response.url.split('/')[0:6])+'/'

	ch = ChromeDriverManager()
	driver = Chrome(ch.install())
	driver.implicitly_wait(10)

	driver.get(link)
	html = driver.page_source
	driver.close()
	soup = BeautifulSoup(html, 'lxml')

	cover = soup.find('img', id = 'imgBlkFront', src = True)
	image = cover['src']
	with open(os.path.join(os.path.dirname(os.getcwd()), 'exported', book_name, 'coverphoto.jpg'), 'wb') as f:
		res = requests.get(image)
		f.write(res.content)
