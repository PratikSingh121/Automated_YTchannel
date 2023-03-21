def book_chooser():
	import os
	import random

	BOOK_BASE = os.path.join(os.path.dirname(os.getcwd()),'books_list')
	with open(os.path.join(BOOK_BASE, 'categories.txt'), 'r') as f:
		categories = f.read()

	cat_list = categories.strip().split('\n')

	with open(os.path.join(BOOK_BASE, 'booksMade.txt'), 'r') as f:
		booksMade = f.read().split()

	while True:
		category = random.choice(cat_list)
		with open(os.path.join(BOOK_BASE, 'categories', f'{category}.txt'), 'r') as f:
			books_list = f.read().strip().split('\n')

		book = random.choice(books_list)
		if book in booksMade or '*' in book:
			continue
		else:
			break

	return book,category