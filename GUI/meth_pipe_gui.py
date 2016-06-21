__author__ = 'Hiranmayi Duvvuri, Pat Johnson'
__date__ = '06/01/2016'
__description__ = """
GUI for part of methylation pipeline.
"""

from tkinter import *
from tkinter.ttk import *
from paramiko import *
from interface_class import Interface

class MethInterface(Interface):

	def __init__(self, parent):
		Interface.__init__(self, parent)

		# Style
		PADX = 2
		PADY = 4
		pad = '0.2i'
		ENTRY_W = 41
		border = 5

		# ACISS connect widgets
		userlabel = Label(self, text = 'ACISS user name: ')
		userlabel.grid(row = 0, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._username = Entry(self, width = ENTRY_W-11)
		self._username.grid(row = 0, column = 1, sticky = W, padx = PADX, pady = PADY, columnspan= 2)

		pwdlabel = Label(self, text = 'password: ')
		pwdlabel.grid(row = 1, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._password = Entry(self, show = '*', width = ENTRY_W-11)
		self._password.grid(row = 1, column = 1, sticky = W, padx = PADX, pady = PADY, columnspan = 2)

		emaillabel = Label(self, text = 'email: ')
		emaillabel.grid(row = 2, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._email = Entry(self, width = ENTRY_W-11)
		self._email.grid(row = 2, column = 1, sticky = W, padx = PADX, pady = PADY, columnspan = 2)

		checkbox_desc = Label(self, text = 'select the pipelines you want to run : ')
		checkbox_desc.grid(row = 3, column = 0, padx = PADX, pady = PADY)

		self._conv_var = BooleanVar()
		conv_check = Checkbutton(self, text = 'Run .meth Conversion', variable = self._conv_var)  
		conv_check.grid(row = 4, column = 0, padx = PADX, pady = PADY)
		self._conv_var.set(True)

		self._comp_var = BooleanVar()
		comp_check = Checkbutton(self, text = 'Run Methylome Comparisons', variable = self._comp_var) 
		comp_check.grid(row = 4, column = 1, padx = PADX, pady = PADY)

		self._avg_var = BooleanVar()
		avg_check = Checkbutton(self, text = 'Run Average Methylations', variable = self._avg_var)	
		avg_check.grid(row = 4, column = 2, padx = PADX, pady = PADY)

		progress_box = Frame(self, relief = SUNKEN, borderwidth = 5)
		scroll = Scrollbar(progress_box)
		scroll.pack(side = RIGHT, fill = Y)
		self._message_txt = Text(progress_box, height = 7)
		self._message_txt.config(state=DISABLED)
		self._message_txt.pack(fill = X)
		self._username.focus_set()

		masternb = Notebook(self)
		comp_frame = Frame(masternb, padding = pad)
		conv_frame = Frame(masternb, padding = pad)
		avg_frame = Frame(masternb, padding = pad)

		# .meth file conversion widgets
		conv_input_label = Label(conv_frame, text = 'Converted BRAT-BW Files Directory: ', width = ENTRY_W)
		conv_input_label.grid(row = 0, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._conv_input_entry = Entry(conv_frame)
		self._conv_input_entry.grid(row = 0, column = 1, sticky = E, padx = PADX, pady = PADY)

		conv_output_label = Label(conv_frame, text = 'Results Directory: ', width = ENTRY_W)
		conv_output_label.grid(row = 1, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._conv_output_entry = Entry(conv_frame)
		self._conv_output_entry.grid(row = 1, column = 1, sticky = E, padx = PADX, pady = PADY)

		# methylome comparison widgets
		comp_input_label = Label(comp_frame, text = 'Files to Compare directory: ', width = ENTRY_W)
		comp_input_label.grid(row = 0, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._comp_input_entry = Entry(comp_frame)
		self._comp_input_entry.grid(row = 0, column = 1, sticky = E, padx = PADX, pady = PADY)

		comp_output_label = Label(comp_frame, text = 'Results Directory: ', width = ENTRY_W)
		comp_output_label.grid(row = 1, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._comp_output_entry = Entry(comp_frame)
		self._comp_output_entry.grid(row = 1, column = 1, sticky = E, padx = PADX, pady = PADY)

		wt_meth_label = Label(comp_frame, text = '.meth of WT Sample: ', width = ENTRY_W)
		wt_meth_label.grid(row = 2, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._wt_meth_entry = Entry(comp_frame)
		self._wt_meth_entry.grid(row = 2, column = 1, sticky = E, padx = PADX, pady = PADY)

		wt_hmr_label = Label(comp_frame, text = '.hmr of WT Sample: ', width = ENTRY_W)
		wt_hmr_label.grid(row = 3, column = 0, sticky = W, padx = PADX, pady = PADY)

		self._wt_hmr_entry = Entry(comp_frame)
		self._wt_hmr_entry.grid(row = 3, column = 1, sticky = E, padx = PADX, pady = PADY)

		# Average methylation widgets
		text_directory_label = Label(avg_frame, text="Sorted Text Directory: ", width = ENTRY_W)
		text_directory_label.grid(row=0, column=0, sticky=W, padx=PADX, pady = PADY)

		self._text_directory_entry = Entry(avg_frame)
		self._text_directory_entry.grid(row=0, column=1, sticky=W, padx=PADX, pady = PADY)

		roi_label = Label(avg_frame, text="Region of Interest*: ", width = ENTRY_W)
		roi_label.grid(row=1, column=0, sticky=W, padx=PADX, pady = PADY)

		self._roi_entry = Entry(avg_frame)
		self._roi_entry.grid(row=1, column=1, sticky=W, padx=PADX, pady = PADY)

		linkage_label = Label(avg_frame, text="Linkage Group: ", width = ENTRY_W)
		linkage_label.grid(row=2, column=0, sticky=W,  padx=PADX, pady = PADY)

		self._linkage_entry = Entry(avg_frame)
		self._linkage_entry.grid(row=2, column=1, sticky=W, padx=PADX, pady = PADY)

		linkage_description = Label(avg_frame, 
								text = "*If more than 1 group separate with commas and no spaces. Ex: 1,2,3" )
		linkage_description.grid(row=3,column=0, padx=PADX, pady = PADY, columnspan=2)
		
		output_directory_label = Label(avg_frame, text="Output Directory: ", width = ENTRY_W)
		output_directory_label.grid(row=4, column=0, sticky=W, padx=PADX, pady = PADY)

		self._output_directory_entry = Entry(avg_frame)
		self._output_directory_entry.grid(row=4, column=1, sticky=W, padx=PADX, pady = PADY)

		window_label = Label(avg_frame, text="Window Size: ", width = ENTRY_W)
		window_label.grid(row=5, column=0, sticky=W, padx=PADX, pady = PADY)

		self._window_entry = Entry(avg_frame)
		self._window_entry.grid(row=5, column=1, sticky=W, padx=PADX, pady = PADY)

		masternb.add(conv_frame, text='.meth Conversion', sticky = N+E+S+W)
		masternb.add(comp_frame, text='Methylome Comparison', sticky = N+E+S+W)
		masternb.add(avg_frame, text='Meth Averages', sticky = N+E+S+W)

		masternb.grid(row = 7, column = 0, columnspan = 3, padx = PADX, pady = PADY, sticky=N+E+S+W)

		progress_box.grid(row = 8, column = 0, columnspan = 3, sticky=N+E+S+W, padx = PADX, pady = PADY)

		conv_pipe = Button(self, text = 'RUN PIPELINE(S)', command = self.run_pipeline)
		conv_pipe.grid(row = 9, column = 2, sticky = E, padx = PADX, pady = PADY)

	def run_pipeline(self):

		# pipeline checkboxes
		meth_convert =		self._conv_var.get()
		meth_compare =		self._comp_var.get()
		avg_meth =			self._avg_var.get()

		# methylation file conversion variables
		convert_input =		self._conv_input_entry.get()
		convert_output =	self._conv_output_entry.get()

		# methylome comparison variables
		comp_input =		self._comp_input_entry.get()
		comp_output =		self._comp_output_entry.get()
		wt_meth =			self._wt_meth_entry.get()
		wt_hmr =			self._wt_hmr_entry.get()

		# average methylation variables
		text_directory =	self._text_directory_entry.get()
		roi =				self._roi_entry.get()
		linkage =			self._linkage_entry.get()
		window =			self._window_entry.get()
		output =			self._output_directory_entry.get()

		username =			self._username.get()
		password =			self._password.get()
		email =				self._email.get()

		passed = True
		command = '(cd _PATH_INSERT_; qsub -M {} -v '.format(email)
		vars = [email, username]
		keys = []

		pipelines = {
		'meth_convert': {'command': 'brat_bw_dir={},meth_output={},'.format(
												convert_input, convert_output), 
					   'var': [convert_input, convert_output]},
		'meth_compare': {'command': 'meth_dir={},diff_out={},wt_meth={},wt_hmr={},'.format(
												comp_input, comp_output, wt_meth, wt_hmr),
					   'var': [comp_output, comp_input, wt_meth, wt_hmr]},
		'avg_meth': {'command': 'txt_directory={},roi={},linkage={},window={},output_directory={},'.format(
							text_directory, roi, linkage, window, output),
				   'var': [text_directory, roi, linkage, window, output]}
		}

		pbs_files = {('meth_convert',): ' meth_convert.pbs', 
					 ('meth_compare',): ' meth_compare.pbs', 
					 ('avg_meth',): ' ave_meth.pbs', 
					 ('meth_convert', 'meth_compare'): ' conv_comp.pbs', 
					 ('meth_convert', 'avg_meth'): ' conv_avg.pbs',
					 ('meth_compare', 'avg_meth'): ' comp_avg.pbs',
					 ('meth_convert', 'meth_compare', 'avg_meth'): ' meth_pipe.pbs'}


		for i, j in zip([meth_convert, meth_compare, avg_meth], ['meth_convert', 'meth_compare', 'avg_meth']):
			if i:
				command += pipelines[j]['command']
				vars.extend(pipelines[j]['var'])
				keys.append(j)

		command += pbs_files[tuple(keys)] + ')'
		for var in vars:
			if var == '':
				passed = False

		if passed:
			self.aciss_connect(command, username, password)
		else:
			self.insert_text("All entry windows must be filled (excluding email and password)\n", self._message_txt)
