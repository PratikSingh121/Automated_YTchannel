def scraper(book_name):
	import requests
	import os
	from bs4 import BeautifulSoup
	import lxml

	from amazon_bookCover import coverScraper
	from amazon_altLink import amazon_altLink
	from Longvideomaker import LongVideoMaker
	from template import template
	from shortVideoMaker import shortVideoMaker
	#No need to use selenium if you get blocked by requests.Just change the headers cause thats what selenium actually does.
	headers = {
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
	}
	book_name = book_name
	FOLDER = os.path.join(os.path.dirname(os.getcwd()), 'exported', book_name)
	os.makedirs(FOLDER, exist_ok = True)
	''' Making the html file of fourminutebooks.com for the first time
	driver.get('https://fourminutebooks.com/book-summaries/')
	html = driver.page_source
	with open('fourminutebooks.html', 'w') as f:
		f.write(html)
	'''#no need to use it again,Html is already saved...Also,We can use requests with headers value next time
	#fourminutebooks.com link finding
	with open('fourminutebooks.html', 'r') as f:
		html = f.read()

	soup = BeautifulSoup(html, 'lxml')

	list = soup.find_all('a', class_='post_title w4pl_post_title', href = True)

	for book in list:
		if book_name.lower()+ ' summary' == (book.text).lower():
			link = book['href']

	response = requests.get(link, headers = headers, timeout=5)
	book_html = response.text
	response.close()
	book_soup = BeautifulSoup(book_html, 'lxml')

	#Amazon Link finding for book Cover
	buttonList = book_soup.find_all('a', class_ = 'btn btn-default btn-lg', href = True)
	amazon_link = ''
	if len(buttonList)==0:
		amazon_link = amazon_altLink(book_name)
	else:
		for info in buttonList:
			if 'amazon' in info.text.lower():
				amazon_link = info['href']
	if amazon_link == '':
		amazon_link = amazon_altLink(book_name)

	coverScraper(book_name, amazon_link)

	'''---------------------------------Summary Scraping----------------------------------------'''
	#Title
	summ_title = book_soup.find('h1', class_='entry-title')
	title = summ_title.get_text()

	#decomposing last three buttons
	for button in book_soup.find_all('a', class_ = 'btn btn-default btn-lg'):
		button.decompose()

	#Finding Lessons Headings
	def topics_filter(soup,headline):
		topics_filtered = [i.text for i in soup.find_all(headline)]
		return topics_filtered

	for headline in ['h2','h3']:
		topics = topics_filter(book_soup,headline)
		lessons = []
		for i in topics:
			if 'Lesson' in i:
				lessons.append(i)
		if len(lessons)!=0:
			break
	if lessons == []:
		FORMAT = 'summary'
	else:
		FORMAT = 'lesson'

	#Full Text
	content = {}

	#One Sentence
	oneSent = book_soup.p.get_text()
	#print(oneSent)

	#All Content
	allh2 = book_soup.find_all('h2')
	for i in allh2:
		para = i.find_next_siblings(['p','ol','ul','h2'])
		this_para = ''
		for j in para:
			if j.name == 'p':
				this_para += j.get_text()+'\n'
			elif j.name == 'ol' or j.name == 'ul':
				children = j.findChildren('li')
				for count,element in enumerate(children):
					li = element.get_text()
					this_para += f'\n{count+1}. {li}.'
			elif j.name == 'h2':
				break
			# elif j.name == 'blockquote':
			# 	extra = j.find_all('p')
			# 	print(extra)
			# 	for ext in extra:
			# 		this_para += ext.get_text()+'\n'
			else:
				continue
		content[i.get_text()] = this_para
		this_para = ''

	content = {key:val for key, val in content.items() if val.strip() != '' and key.lower() != "audio summary" and key.lower() != "video summary"}

	#Tags
	tags = ''
	tags_soup = soup.find_all('a', rel = 'category tag')
	for element in tags_soup:
		tags += element.get_text()+'\n'
	with open(os.path.join(FOLDER, 'tags.txt'), 'w') as f:
		f.write(tags)

	#------------------------------------Scraping Over----------------------------------------

	template(FOLDER, title, oneSent, content, lessons, FORMAT)

	print('Making Video Frame : This might take about a minute')
	LongVideoMaker(FOLDER, book_name)

	print('Making Shorts:')
	shortVideoMaker(FOLDER, book_name, FORMAT)
