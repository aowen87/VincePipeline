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
        padx = 2
        pady = 8
        pad = '0.2i'
        width = 41

        # ACISS connect widgets
        userlabel = Label(self, text = 'ACISS Username: ')
        userlabel.grid(row = 0, column = 0, sticky = W, padx = padx, pady = pady)

        self._username = Entry(self)
        self._username.grid(row = 0, column = 1, sticky = W, padx = padx, pady = pady)

        pwdlabel = Label(self, text = 'password: ')
        pwdlabel.grid(row = 1, column = 0, sticky = W, padx = padx, pady = pady)

        self._password = Entry(self, show = '*')
        self._password.grid(row = 1, column = 1, sticky = W, padx = padx, pady = pady)

        emaillabel = Label(self, text = 'email: ')
        emaillabel.grid(row = 2, column = 0, sticky = W, padx = padx, pady = pady)

        self._email = Entry(self)
        self._email.grid(row = 2, column = 1, sticky = W, padx = padx, pady = pady)

        checkbox_desc = Label(self, text = 'select the pipelines you want to run : ')
        checkbox_desc.grid(row = 3, column = 0, padx = padx, pady = pady)

        self._conv_var = BooleanVar()
        conv_check = Checkbutton(self, text = 'Run .meth Conversion', variable = self._conv_var)  
        conv_check.grid(row = 4, column = 0, padx = padx, pady = pady)

        self._comp_var = BooleanVar()
        comp_check = Checkbutton(self, text = 'Run Methylome Comparisons', variable = self._comp_var) 
        comp_check.grid(row = 4, column = 1, padx = padx, pady = pady)

        self._avg_var = BooleanVar()
        avg_check = Checkbutton(self, text = 'Run Average Methylations', variable = self._avg_var)  
        avg_check.grid(row = 4, column = 2, padx = padx, pady = pady)

        progress_box = Frame(self)
        scroll = Scrollbar(progress_box)
        scroll.pack(side = RIGHT, fill = Y)
        self._message_txt = Text(progress_box, height = 8)
        self._message_txt.pack()

        masternb = Notebook(self)
        comp_frame = Frame(masternb, padding = pad)
        conv_frame = Frame(masternb, padding = pad)
        avg_frame = Frame(masternb, padding = pad)

        # .meth file conversion widgets
        conv_input_label = Label(conv_frame, text = 'Converted BRAT-BW Files Directory: ', width = width)
        conv_input_label.grid(row = 0, column = 0, sticky = W, padx = padx, pady = pady)

        self._conv_input_entry = Entry(conv_frame)
        self._conv_input_entry.grid(row = 0, column = 1, sticky = E, padx = padx, pady = pady)

        conv_output_label = Label(conv_frame, text = 'Results Directory: ', width = width)
        conv_output_label.grid(row = 1, column = 0, sticky = W, padx = padx, pady = pady)

        self._conv_output_entry = Entry(conv_frame)
        self._conv_output_entry.grid(row = 1, column = 1, sticky = E, padx = padx, pady = pady)

        # methylome comparison widgets
        comp_input_label = Label(comp_frame, text = 'Files to Compare directory: ', width = width)
        comp_input_label.grid(row = 0, column = 0, sticky = W, padx = padx, pady = pady)

        self._comp_input_entry = Entry(comp_frame)
        self._comp_input_entry.grid(row = 0, column = 1, sticky = E, padx = padx, pady = pady)

        comp_output_label = Label(comp_frame, text = 'Results Directory: ', width = width)
        comp_output_label.grid(row = 1, column = 0, sticky = W, padx = padx, pady = pady)

        self._comp_output_entry = Entry(comp_frame)
        self._comp_output_entry.grid(row = 1, column = 1, sticky = E, padx = padx, pady = pady)

        wt_meth_label = Label(comp_frame, text = '.meth of WT Sample: ', width = width)
        wt_meth_label.grid(row = 2, column = 0, sticky = W, padx = padx, pady = pady)

        self._wt_meth_entry = Entry(comp_frame)
        self._wt_meth_entry.grid(row = 2, column = 1, sticky = E, padx = padx, pady = pady)

        wt_hmr_label = Label(comp_frame, text = '.hmr of WT Sample: ', width = width)
        wt_hmr_label.grid(row = 3, column = 0, sticky = W, padx = padx, pady = pady)

        self._wt_hmr_entry = Entry(comp_frame)
        self._wt_hmr_entry.grid(row = 3, column = 1, sticky = E, padx = padx, pady = pady)

        # Average methylation widgets
        text_directory_label = Label(avg_frame, text="Sorted Text Directory: ", width = width)
        text_directory_label.grid(row=0, column=0, sticky=W, padx=padx, pady = pady)

        self._text_directory_entry = Entry(avg_frame)
        self._text_directory_entry.grid(row=0, column=1, sticky=W, padx=padx, pady = pady)

        roi_label = Label(avg_frame, text="Region of Interest*: ", width = width)
        roi_label.grid(row=1, column=0, sticky=W, padx=padx, pady = pady)

        self._roi_entry = Entry(avg_frame)
        self._roi_entry.grid(row=1, column=1, sticky=W, padx=padx, pady = pady)

        roi_description = Label(avg_frame, 
                                text = "    *Should be a .bed file or a fastq file to build .bed from" )
        roi_description.grid(row=2,column=0, padx=padx, pady = pady, columnspan=1)

        linkage_label = Label(avg_frame, text="Linkage Group: ", width = width)
        linkage_label.grid(row=3, column=0, sticky=W,  padx=padx, pady = pady)

        self._linkage_entry = Entry(avg_frame)
        self._linkage_entry.grid(row=3, column=1, sticky=W, padx=padx, pady = pady)

        window_label = Label(avg_frame, text="Window Size: ", width = width)
        window_label.grid(row=4, column=0, sticky=W, padx=padx, pady = pady)

        self._window_entry = Entry(avg_frame)
        self._window_entry.grid(row=4, column=1, sticky=W, padx=padx, pady = pady)

        masternb.add(conv_frame, text='.meth Conversion', sticky = N+E+S+W)
        masternb.add(comp_frame, text='Methylome Comparison', sticky = N+E+S+W)
        masternb.add(avg_frame, text='Meth Averages', sticky = N+E+S+W)

        masternb.grid(row = 7, column = 0, columnspan = 3, padx = padx, pady = pady)

        progress_box.grid(row = 8, column = 0, columnspan = 3, padx = padx, pady = pady)

        conv_pipe = Button(self, text = 'Run Pipeline(s)', command = self.run_pipeline)
        conv_pipe.grid(row = 9, column = 2, sticky = E, padx = padx, pady = pady)

    def run_pipeline(self):

        # pipeline checkboxes
        meth_convert = self._conv_var.get()
        meth_compare = self._comp_var.get()
        avg_meth = self._avg_var.get()

        # methylation file conversion variables
        convert_input = self._conv_input_entry.get()
        convert_output = self._conv_output_entry.get()

        # methylome comparison variables
        comp_input = self._comp_input_entry.get()
        comp_output = self._comp_output_entry.get()
        wt_meth = self._wt_meth_entry.get()
        wt_hmr = self._wt_hmr_entry.get()

        # average methylation variables
        text_directory = self._text_directory_entry.get()
        roi = self._roi_entry.get()
        linkage = self._linkage_entry.get()
        window = self._window_entry.get()

        username = self._username.get()
        password = self._password.get()
        email = self._email.get()

        command = '(cd /research/CIS454/vince/pipeline; qsub -M {} -v '.format(email)
        vars = [email, username]
        keys = []

        pipelines = {
        'meth_convert': {'command': 'brat_bw_dir={},meth_output={},'.format(
                                                convert_input, convert_output), 
                       'var': [convert_input, convert_output]},
        'meth_compare': {'command': 'meth_dir={},diff_out={},wt_meth={},wt_hmr={},'.format(
                                                comp_input, comp_output, wt_meth, wt_hmr),
                       'var': [comp_output, comp_input, wt_meth, wt_hmr]},
        'avg_meth': {'command': 'txt_directory={},roi={},linkage={},window={},'.format(
                            text_directory, roi, linkage, window),
                   'var': [text_directory, roi, linkage, window]}
        }

        pbs_files = {('meth_convert',): ' meth_convert.pbs', 
                     ('meth_compare',): ' meth_compare.pbs', 
                     ('avg_meth',): ' ave_meth.pbs', 
                     ('meth_convert', 'meth_compare'): ' conv_comp.pbs', 
                     ('meth_convert', 'avg_meth'): ' conv_avg.pbs',
                     ('meth_compare', 'avg_meth'): ' comp_avg.pbs',
                     ('meth_convert', 'meth_compare', 'avg_meth'): ' meth_pipe.pbs'}

        passed = True


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
            self._message_txt.insert(INSERT, "All entry windows must be filled\n") 
