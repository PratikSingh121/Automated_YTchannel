def LongVideoMaker(exp_path, book_name):
	from moviepy import editor
	import moviepy.audio.fx.all as afx
	from gtts import gTTS
	from PIL import Image
	from mutagen.mp3 import MP3
	import os
	import numpy as np
	import cv2 as cv
	from pathlib import Path
	import pyttsx3
	engine = pyttsx3.init()

	blank = np.zeros((720,1280,3), dtype='uint8')
	img = cv.imread(os.path.join(exp_path, 'coverphoto.jpg'))
	height,width = img.shape[0:2]
	scale = 720/height
	height = int(height*scale)
	width = int(width*scale)

	def rescaleframe(frame, scale = scale):
		height = int(frame.shape[0] * scale)
		width = int(frame.shape[1] * scale)
		dimensions = (width, height)	
		return cv.resize(frame, dimensions, interpolation = cv.INTER_CUBIC)
	img = rescaleframe(img)

	if (width%2) == 1:
		blank[0:1080,(640-int(width/2)):(640+int(width/2)+1)] = img
	else:
		blank[0:1080,(640-int(width/2)):(640+int(width/2))] = img
	cv.imwrite(os.path.join(exp_path, 'vid_image.jpg'),blank)

	with open(os.path.join(exp_path,'LongScript.txt'), 'r') as f:
		text = f.read()
	
	engine.setProperty('rate', 175)
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	engine.save_to_file(text, os.path.join(exp_path,'speech.mp3'))
	engine.runAndWait()
	engine.stop()

	voice = editor.AudioFileClip(os.path.join(exp_path,'speech.mp3'))
	length = voice.duration

	bgmusic = editor.AudioFileClip(os.path.join(os.path.dirname(os.getcwd()),'bgmusic','aesthetic.mp3'))
	bgmusic = afx.audio_loop( bgmusic, duration=length+3)
	bgmusic = afx.audio_normalize(bgmusic)
	bgmusic = afx.volumex(bgmusic, 0.1)
	bgmusic = afx.audio_fadeout( bgmusic, 3)
	bgmusic.write_audiofile(os.path.join(exp_path,'bgmusic.mp3'))
	bgmusic = editor.AudioFileClip(os.path.join(exp_path,'bgmusic.mp3'))
	final_audio = editor.CompositeAudioClip([voice, bgmusic])

	path_images = Path(f'{exp_path}')
	images = list(path_images.glob('vid_image.jpg'))
	image_list = list()
	for image_name in images:
		image = Image.open(image_name).resize((1240,720), Image.ANTIALIAS)
		image_list.append(image)


	image_list[0].save(os.path.join(exp_path,'video.gif'), save_all = True, append_images = image_list[1:], duration = length)

	video = editor.VideoFileClip(os.path.join(exp_path, 'video.gif'))
	video.write_videofile(os.path.join(exp_path, 'video.mp4'))
	video = editor.VideoFileClip(os.path.join(exp_path, 'video.mp4'))
	#audio = editor.AudioFileClip(os.path.join(exp_path, 'merged.mp3'))#
	final_video = video.set_audio(final_audio)
	final_video.write_videofile(os.path.join(exp_path,f'{book_name.title()}.mp4'), fps = 30)
