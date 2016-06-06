__author__ = 'Hiranmayi Duvvuri'
__date__ = '06/01/2016'
__description__ = """
GUI for part of methylation pipeline.
"""

from tkinter import *
from tkinter.ttk import *
from paramiko import *
from interface_class import Interface

class MethCompInterface(Interface):

    def __init__(self, parent):
        Interface.__init__(self, parent)

        # Style
        padx = 2
        pady = 8

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

        progress_box = Frame(self)
        scroll = Scrollbar(progress_box)
        scroll.pack(side = RIGHT, fill = Y)
        self._message_txt = Text(progress_box, height = 8)
        self._message_txt.pack()

        # methylome comparison widgets
        comp_input_label = Label(self, text = 'Files to Compare directory: ')
        comp_input_label.grid(row = 3, column = 0, sticky = W, padx = padx, pady = pady)

        self._comp_input_entry = Entry(self)
        self._comp_input_entry.grid(row = 3, column = 1, sticky = W, padx = padx, pady = pady)

        comp_output_label = Label(self, text = 'Results Directory: ')
        comp_output_label.grid(row = 4, column = 0, sticky = W, padx = padx, pady = pady)

        self._comp_output_entry = Entry(self)
        self._comp_output_entry.grid(row = 4, column = 1, sticky = W, padx = padx, pady = pady)

        wt_meth_label = Label(self, text = '.meth of WT Sample: ')
        wt_meth_label.grid(row = 5, column = 0, sticky = W, padx = padx, pady = pady)

        self._wt_meth_entry = Entry(self)
        self._wt_meth_entry.grid(row = 5, column = 1, sticky = W, padx = padx, pady = pady)

        wt_hmr_label = Label(self, text = '.hmr of WT Sample: ')
        wt_hmr_label.grid(row = 6, column = 0, sticky = W, padx = padx, pady = pady)

        self._wt_hmr_entry = Entry(self)
        self._wt_hmr_entry.grid(row = 6, column = 1, sticky = W, padx = padx, pady = pady)

        progress_box.grid(row = 7, column = 0, columnspan = 2, padx = padx, pady = pady)

        conv_pipe = Button(self, text = 'Start Sample Comparisons', command = self.run_pipeline)
        conv_pipe.grid(row = 8, column = 1, sticky = E, padx = padx, pady = pady)

    def run_pipeline(self):

        # methylome comparison variables
        comp_input = self._comp_input_entry.get()
        comp_output = self._comp_output_entry.get()
        wt_meth = self._wt_meth_entry.get()
        wt_hmr = self._wt_hmr_entry.get()

        username = self._username.get()
        password = self._password.get()
        email = self._email.get()

        command = '(cd /research/CIS454/vince/pipeline; qsub -M {} -v input={},output={},wt_meth={},wt_hmr={} meth_compare.pbs)'.format(
                                                email, comp_input, comp_output, wt_meth, wt_hmr)
        vars = [email, username, comp_output, comp_input, wt_meth, wt_hmr]

        passed = True

        for var in vars:
            if var == '':
                passed = False

        if passed:
            self.aciss_connect(command, username, password)
        else:
            self._message_txt.insert(INSERT, "All entry windows must be filled\n") 