from tkinter import *
from PIL import Image, ImageTk
import glob
import random

class GUI:
	def __init__(self, root, fullscreen):
		self.root = root
		self.widget = Label(self.root, text='')
		self.w, self.h = root.winfo_screenwidth(), root.winfo_screenheight()
		self.root.overrideredirect(fullscreen)
		self.root.geometry("%dx%d+0+0" % (self.w, self.h))
		self.root.configure(background="blue")
		self.imgLabel = Label(self.root)
		# self.root.config(cursor="")

	def update(self):
		self.root.update_idletasks()
		self.root.update()

	def display_image(self):
		imgpath = self.getRandomFile('images/')
		image = Image.open(imgpath)
		size = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
		image = image.resize(size, Image.ANTIALIAS)
		print('image', image)
		photo = ImageTk.PhotoImage(image)
		self.imgLabel.pack_forget()
		self.imgLabel = Label(self.root, image=photo)
		self.imgLabel.pack(fill=BOTH, expand=0)
		self.update()

	def set_state(self, state):
		print('change state!!!', state)
		return
		if state == 'ECHO':
			self.change_color("green")
		if state == 'RANDOM':
			self.change_color("red")
		elif state == 'PLAYING':
			self.change_color("blue")
		self.update()

	def change_color(self, color):
		return
		print('change color:', color)
		self.root.configure(background=color)
	
	def display_text(self, text):
		return
		self.widget.pack_forget()
		self.widget = Label(self.root, text=text)
		self.widget.pack()
		self.update()

	def listFiles(self, path):
		return glob.glob(path + '*.jpg')

	def getRandomFile(self, folder = 'images/'):
		files = self.listFiles(folder)
		filename = random.choice(files)
		return filename