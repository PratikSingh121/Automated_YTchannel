def template(FOLDER, title, oneSent, content, lessons, FORMAT):
	import os
	import re

	def deEmojify(text):
	    regrex_pattern = re.compile(pattern = "["
	        u"\U0001F600-\U0001F64F"  # emoticons
	        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
	        u"\U0001F680-\U0001F6FF"  # transport & map symbols
	        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
	                           "]+", flags = re.UNICODE)
	    return regrex_pattern.sub(r'',text)

	LongScript = f'\nHello there. Welcome back to my channel. Today we will be discussing {" ".join(title.split()[:-1:])} Summary in under 5 minutes. Donot forget to subscribe for a new book summary everyday. But for now,Lets get started.\n'
	for key,value in content.items():
		LongScript += key+'\n'
		LongScript += value+'\n'
	LongScript += f'That was {" ".join(title.split()[:-1:])} Summary. For more summaries do subscribe to my channel and comment below the book you want me to make summary of. See you in the next Video,till then,Good Bye.'

	oneSentScript = f'{" ".join(title.split()[:-1:])} in 1 line:\n'
	oneSentScript += ':'.join(oneSent.split(':')[1:])
	oneSentScript = oneSentScript + 'To get the complete summary in under 5 minutes,visit the channel and dont forget to subscribe.'

	if FORMAT == 'lesson':
		LongScript = f"\n{title}\n\n\n" + LongScript

		lessons_short = f"3 lessons from {' '.join(title.split()[:-1:])}\n"
		for i in lessons:
			lessons_short += f'{i}\n'
		lessons_short = deEmojify(lessons_short)
		lessons_short = lessons_short + 'To get the complete summary in under 5 minutes,visit the channel and dont forget to subscribe.'
		with open(os.path.join(FOLDER,'lessons_short.txt'), 'w') as f:
			f.write(lessons_short)

	LongScript = deEmojify(LongScript)
	oneSentScript = deEmojify(oneSentScript)
	with open(os.path.join(FOLDER,'LongScript.txt'), 'w') as f:
		f.write(LongScript)
	with open(os.path.join(FOLDER,'oneSentScript.txt'), 'w') as f:
		f.write(oneSentScript)
