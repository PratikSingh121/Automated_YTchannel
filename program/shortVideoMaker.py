def shortVideoMaker(exp_path, book_name, FORMAT):
	from moviepy import editor
	from gtts import gTTS
	from PIL import Image
	from mutagen.mp3 import MP3
	import os
	import numpy as np
	import cv2 as cv
	from pathlib import Path	

	img = cv.imread(os.path.join(exp_path, 'coverphoto.jpg'))
	height,width = img.shape[0:2]

	if FORMAT == 'lesson':
		with open(os.path.join(exp_path,'lessons_short.txt'), 'r') as f:
			text = f.read()
		lang = 'en'
		speech = gTTS(text = text, lang = lang, slow = False)
		speech.save(os.path.join(exp_path,'speech.mp3'))

		voice = MP3(os.path.join(exp_path,'speech.mp3'))
		length = voice.info.length

		path_images = Path(f'{exp_path}')
		images = list(path_images.glob('coverphoto.jpg'))
		image_list = list()
		for image_name in images:
			image = Image.open(image_name).resize((720,1280), Image.ANTIALIAS)
			image_list.append(image)

		image_list[0].save(os.path.join(exp_path,'video.gif'), save_all = True, append_images = image_list[1:], duration = length)

		video = editor.VideoFileClip(os.path.join(exp_path, 'video.gif'))
		video.write_videofile(os.path.join(exp_path, 'video.mp4'))
		video = editor.VideoFileClip(os.path.join(exp_path, 'video.mp4'))
		audio = editor.AudioFileClip(os.path.join(exp_path, 'speech.mp3'))
		final_video = video.set_audio(audio)
		final_video.write_videofile(os.path.join(exp_path,'lessons_short.mp4'), fps = 60)

	print('Making oneSent Short:')

	with open(os.path.join(exp_path,'oneSentScript.txt'), 'r') as f:
		text = f.read()
	lang = 'en'
	speech = gTTS(text = text, lang = lang, slow = False)
	speech.save(os.path.join(exp_path,'speech.mp3'))

	voice = MP3(os.path.join(exp_path,'speech.mp3'))
	length = voice.info.length

	video = editor.VideoFileClip(os.path.join(exp_path, 'video.gif'))
	video.write_videofile(os.path.join(exp_path, 'video.mp4'))
	video = editor.VideoFileClip(os.path.join(exp_path, 'video.mp4'))
	audio = editor.AudioFileClip(os.path.join(exp_path, 'speech.mp3'))
	final_video = video.set_audio(audio)
	final_video.write_videofile(os.path.join(exp_path,'oneSent.mp4'), fps = 60)