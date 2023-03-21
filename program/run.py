
from scraper_main import scraper
from book_choose import book_chooser
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.getcwd()),'yt_api'))
from yt_uploading import upload

#Random book choosing
book_summ, category = book_chooser()

book = ' '.join(book_summ.split()[:-1:])

print(f'Making {book.title()} - {category} Summary...')
scraper(book)
print(f'{book.title()} Production Over...')

print('Uploading on YT')
upload(book)

with open(os.path.join(os.path.dirname(os.getcwd()),'books_list','booksMade.txt'), 'a') as f:
	f.write(f'{book} - {category}\n')

BOOK_BASE = os.path.join(os.path.dirname(os.getcwd()),'books_list', 'categories')
with open(os.path.join(BOOK_BASE, f'{category}.txt'), 'r') as f:
	books = f.read().split('\n')
books.remove(book_summ)
with open(os.path.join(BOOK_BASE, f'{category}.txt'), 'w') as f:
	f.write('\n'.join(books))
with open(os.path.join(BOOK_BASE, 'booksMade.txt'), 'w') as f:
	f.write(book_summ+'\n')