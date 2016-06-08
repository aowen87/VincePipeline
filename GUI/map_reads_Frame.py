'''
Created on May 17, 2016

@author: Alister Maguire, Pat Johnson
'''
from tkinter import *
from tkinter import font
from paramiko import *
from interface_class import Interface

class ChipInterface(Interface):
	
	def __init__(self, master):
		'''
		Set up the main GUI interface and all class variables. 
		'''	 
		Interface.__init__(self, master)
		
		#class variables
		self._chip_directory	= ''
		self._genome			= ''
		self._usrname			= ''
		
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
		chip_directory_label			= Label(self, padx=PADX, pady=PADY, text="Chip Reads Directory: ")
		self._chip_directory_entry		= Entry(self, bd=5)
		genome_label					= Label(self, padx=PADX, pady=PADY, text="Genome*: ")
		self._genome_entry				= Entry(self, bd=5)
		genome_description 				= Label(self, padx=PADX, pady=PADY, 
												text = "	*If building a genome, pass the name of a fasta file.  Otherwise a genome directory" )
		Start							= Button(self, text='RUN PIPELINE', font=cur_font, command=self.run_pipeline)

		#GUI structure
		user_name_label.grid(row=0, column=0, sticky=W, padx=PADX+30)
		self._user_name_entry.grid(row=0, column=1, sticky=W, padx=PADX+30)
		pwd_label.grid(row = 1, column = 0, sticky=W, padx=PADX+30)
		self._password_entry.grid(row = 1, column = 1, sticky=W, padx=PADX+30)
		chip_directory_label.grid(row=2, column=0, sticky=W, padx=PADX+30)
		self._chip_directory_entry.grid(row=2, column=1, sticky=W, padx=PADX+30)
		genome_label.grid(row=3, column=0, sticky=W, padx=PADX+30)
		self._genome_entry.grid(row=3, column=1, sticky=W, padx=PADX+30)
		genome_description.grid(row=5,column=0, sticky=N+E+S+W, padx=PADX+5, pady=2,columnspan=2)
		progress_box.grid(row=6, column=0, sticky=N+E+S+W, padx=PADX+5, pady=PADY,columnspan=2)
		Start.grid(row=7, column=1, sticky=E, padx=50, pady=PADY)
		self._user_name_entry.focus_set()
	
	
	def initiatePipe(self):
		'''
		Runs the chip_pipe pipeline to map reads to a genome for display
		on IGV (for ChipSeq)
		'''
		#Retrieve entries
		passed = True
		self._chip_directory	= self._chip_directory_entry.get()
		self._genome			= self._genome_entry.get()
		self._usrname			= self._user_name_entry.get()
		self._password 			= self._password_entry
		vars = [self._usrname, self._genome, self._chip_directory]
		
		for var in vars:
			if var == '':
				passed = False
					
		if passed:			
			
			command = "(cd ChipReads/FinalTest; qsub -v chip_directory={},genome={} chip_pipe.pbs)".format(self._chip_directory, self._genome)
			self._message_text.insert(INSERT, command)
			
			self.aciss_connect(command, self._usrname, self._password)
		else:
			self._message_text.insert(INSERT, "All entry windows must be filled\n") 
	
	
	def run_pipeline(self):
		'''
		Connect to ACISS and run the pipeline with the user given 
		input. 
		'''
		self.initiatePipe()
		
		
		
		
	

