from tkinter import *
from tkinter import messagebox
import time
import random
from mbox import mbox
import sys
from configparser import ConfigParser
import json
import os


# workouts from
# https://www.mensjournal.com/health-fitness/the-30-best-bodyweight-exercises-for-men/
class GUI:
	def __init__(self, master):
		self.master = master
		# Work time, workout time, exercises

		self.get_settings()
		
		self.c_min = self.cpu_minutes * 60
		self.e_min = self.exer_minutes * 60
		# workaround variable
		self.start = 0
		self.start2 = 1
		# box layout
		self.sbar = Scrollbar(master)
		self.txt = Text(master, height=5, width=60)
		self.sbar.pack(side=RIGHT, fill=Y)
		self.txt.pack(side=LEFT, fill=Y)
		self.sbar.config(command=self.txt.yview)
		self.txt.config(yscrollcommand=self.sbar.set)
		new_txt = "Time Between Breaks: " + str(self.cpu_minutes)
		new_txt2 = "Time for exercise: " + str(self.exer_minutes)
		self.txt.insert(END, new_txt + '\n')
		self.txt.insert(END, new_txt2 + '\n')
		self.but = Button(master, text="Stop", command=self.onclick)
		self.but.pack()
		self.loop()

	
	def get_settings(self):
		config = ConfigParser()
		config.read(os.path.abspath("C:\\Users\\Eric\\Desktop\\projects\\wtm\\config.ini"))
		self.cpu_minutes = config.getint('main', 'work_time')
		self.exer_minutes = config.getint('main', 'break_time')
		self.low_rand = config.getint('main', 'low_random')
		self.high_rand = config.getint('main', 'high_random')
		self.num_workouts = config.getint('main', 'num_of_workouts')
		self.exercises = json.loads(config.get('workouts', 'exercises'))
	
	def create_workouts(self):
		e = self.exercises
		ret_str = ""
		for x in range(self.num_workouts):
			num = str(random.randint(self.low_rand, self.high_rand + 1))
			wor = e[random.randint(0, len(e)-1)]
			ret_str = ret_str + wor + ": " + num + ", "
		ret_str = ret_str[:-2]
		return ret_str
        
        
	def loop(self):
		if self.start == 0:
			if self.start2 == 1:
				self.start2 = 0
				self.in_loop = self.master.after(self.c_min * 1000, self.loop)
			else:
				workout = self.create_workouts()
				self.txt.insert('1.0', '\n')
				self.txt.insert('1.0', str(workout) + '\n')
				mbox(str(workout), self.e_min)
				self.in_loop = self.master.after(self.c_min * 1000, self.loop)


	def onclick(self):
		if self.start == 1:
			print("Start")
			self.start = 0
			self.but["text"] = "Stop"
			self.master.update()
			self.loop()
		else:
			print("STOP")
			self.master.after_cancel(self.in_loop)
			self.start = 1
			self.but["text"] = "Start"
			self.master.update()


root = Tk()
root.config()
root.iconbitmap(r'C:\Users\Eric\Desktop\projects\wtm\logo.ico')
r = GUI(root)
root.mainloop()




