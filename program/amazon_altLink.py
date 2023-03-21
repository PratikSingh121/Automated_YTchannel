def amazon_altLink(book_name):

	import os
	from bs4 import BeautifulSoup
	import lxml

	from selenium.webdriver import Chrome
	from webdriver_manager.chrome import ChromeDriverManager
	from selenium.webdriver.common.keys import Keys

	init_link = f'https://www.amazon.in/s?k={"+".join(book_name.split())}&i=stripbooks&ref=nb_sb_noss_1'

	ch = ChromeDriverManager()
	driver = Chrome(ch.install())
	driver.implicitly_wait(10)

	driver.get(init_link)
	html = driver.page_source
	driver.close()

	soup = BeautifulSoup(html, 'lxml')

	links = soup.find_all('a', class_='a-link-normal a-text-normal', href = True)
	print("Links are : \t"+links)
	for i in links:
		counter = 0
		for j in book_name.split():
			if str(j).title() in str(i['href']) or str(j).lower() in ['of', 'a' , 'the', 'an', 'is', 'to', 'be']:
				counter += 1
		if counter/len(book_name.split())*100 >= 60:
			link = i['href']
			break
	link = 'https://www.amazon.in'+link
	link = '/'.join(link.split('/')[0:6])+'/'
	print(link)
	return link