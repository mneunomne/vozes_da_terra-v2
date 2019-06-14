from tkinter import *
fullscreen = False

class GUI:
	def __init__(self, root):
		self.root = root
		self.widget = Label(self.root, text='')
		self.w, self.h = root.winfo_screenwidth(), root.winfo_screenheight()
		self.root.overrideredirect(fullscreen)
		self.root.geometry("%dx%d+0+0" % (self.w, self.h))
		self.root.configure(background="blue")
		# self.root.config(cursor="")

	def update(self):
		self.root.update_idletasks()
		self.root.update()

	def set_state(self, state):
		print('change state!!!', state)
		if state == 'ECHO':
			self.change_color("green")
		if state == 'RANDOM':
			self.change_color("red")
		elif state == 'PLAYING':
			self.change_color("blue")
		self.update()

	def change_color(self, color):
		print('change color:', color)
		self.root.configure(background=color)
  
	def display_text(self, text):
		self.widget.pack_forget()
		self.widget = Label(self.root, text=text)
		self.widget.pack()
		self.update()