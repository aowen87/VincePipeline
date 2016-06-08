'''
Created on May 17, 2016

@author: Alister Maguire, Pat Johnson
'''
from tkinter import *
from tkinter import font
from paramiko import *
from tkinter import ttk
from interface_class import Interface

class AvgMethInterface(Interface):
	
	def __init__(self, parent):
		'''
		Set up the main GUI interface and all class variables. 
		'''	 
		Interface.__init__(self, parent)
		
		#class variables
		self._text_directory	= ''
		self._roi				= ''
		self._usrname			= ''
		self._linkage			= ''
		self._window			= ''
		
		#fonts, colors, padding, etc. 
		PADX = 2
		PADY = 11
		cur_font = font.Font(family="Courier New", size=13, weight="bold")
		progress_box = Frame(self, relief=SUNKEN, background='white', borderwidth=5)
		scroll = Scrollbar(progress_box)
		scroll.pack(side=RIGHT, fill=Y)
		self._message_text = Text(progress_box, height=7)
		self._message_text.pack()

		#Labels and entries	   
		user_name_label					= Label(self, padx=PADX, pady=PADY, text="ACISS user name: ")
		self._user_name_entry			= Entry(self, bd=5)
		pwd_label 						= Label(self, padx=PADX, pady=PADY, text = 'password: ')
		self._password_entry 			= Entry(self, bd=5, show = '*')
		text_directory_label			= Label(self, padx=PADX, pady=PADY, text="Sorted Text Directory: ")
		self._text_directory_entry		= Entry(self, bd=5)
		roi_label						= Label(self, padx=PADX, pady=PADY, text="Region of Interest*: ")
		self._roi_entry					= Entry(self, bd=5)
		roi_description 				= Label(self, padx=PADX, pady=PADY, 
											text = "	*Should be a .bed file or a fastq file to build .bed from" )
		linkage_label					= Label(self, padx=PADX, pady=PADY, text="Linkage Group: ")
		self._linkage_entry				= Entry(self, bd=5)
		window_label					= Label(self, padx=PADX, pady=PADY, text="Window Size: ")
		self._window_entry				= Entry(self, bd=5)
		
		Start							= Button(self, text='RUN PIPELINE', font=cur_font, command=self.runPipe)
		self._user_name_entry.focus_set()
	
		#GUI structure
		
		
		user_name_label.grid(row=0, column=0, sticky=W, padx=PADX+30)
		self._user_name_entry.grid(row=0, column=1, sticky=W, padx=PADX+30)
		pwd_label.grid(row = 1, column = 0, sticky=W, padx=PADX+30)
		self._password_entry.grid(row = 1, column = 1, sticky=W, padx=PADX+30)
		text_directory_label.grid(row=2, column=0, sticky=W, padx=PADX+30)
		self._text_directory_entry.grid(row=2, column=1, sticky=W, padx=PADX+30)
		roi_label.grid(row=3, column=0, sticky=W, padx=PADX+30)
		self._roi_entry.grid(row=3, column=1, sticky=W, padx=PADX+30)
		roi_description.grid(row=4,column=0, sticky=N+E+S+W, padx=PADX+5, pady=2,columnspan=1)
		linkage_label.grid(row=5, column=0, sticky=W, padx=PADX+30)
		self._linkage_entry.grid(row=5, column=1, sticky=W, padx=PADX+30)
		window_label.grid(row=6, column=0, sticky=W, padx=PADX+30)
		self._window_entry.grid(row=6, column=1, sticky=W, padx=PADX+30)
		progress_box.grid(row=7, column=0, sticky=N+E+S+W, padx=PADX+5, pady=PADY,columnspan=2)
		Start.grid(row=8, column=1, sticky=E, padx=50, pady=PADY)
	
	
	def initiatePipe(self):
		'''
		Runs the chip_pipe pipeline to map reads to a genome for display
		on IGV (for ChipSeq)
		'''
		#Retrieve entries
		passed = True
		self._text_directory	= self._text_directory_entry.get()
		self._roi				= self._roi_entry.get()
		self._usrname			= self._user_name_entry.get()
		self._password 			= self._password_entry
		self._roi				= self._roi_entry.get()
		self._linkage			= self._linkage_entry.get()
		self._window			= self._window_entry.get()
		
		vars = [self._usrname, self._text_directory,self._roi,self._linkage,self._window]
		
		for var in vars:
			if var == '':
				passed = False
					
		if passed:			
			
			command = "(cd meth/trial2; qsub -v txt_directory={},roi={},linkage={},window={} ave_meth.pbs)".format(
							self._text_directory,self._roi, self._linkage, self._window)
			self._message_text.insert(INSERT, command)
			
			self.aciss_connect(command, self._usrname, self._password)
		else:
			self._message_text.insert(INSERT, "All entry windows must be filled\n") 
	
	
	
	
	def runPipe(self):
		'''
		Connect to ACISS and run the pipeline with the user given 
		input. 
		'''
		self.initiatePipe()
		
		
		
		
	  

