__author__ = 'Hiranmayi Duvvuri'
__date__ = '06/01/2016'
__description__ = """
GUI for part of methylation pipeline.
"""

from tkinter import *
from tkinter.ttk import *
from paramiko import *
from interface_class import Interface

class MethConvInterface(Interface):

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

        # .meth file conversion widgets
        conv_input_label = Label(self, text = 'Converted BRAT-BW Files Directory: ')
        conv_input_label.grid(row = 3, column = 0, sticky = W, padx = padx, pady = pady)

        self._conv_input_entry = Entry(self)
        self._conv_input_entry.grid(row = 3, column = 1, sticky = W, padx = padx, pady = pady)

        conv_output_label = Label(self, text = 'Results Directory: ')
        conv_output_label.grid(row = 4, column = 0, sticky = W, padx = padx, pady = pady)

        self._conv_output_entry = Entry(self)
        self._conv_output_entry.grid(row = 4, column = 1, sticky = W, padx = padx, pady = pady)


        progress_box.grid(row = 5, column = 0, columnspan = 2, padx = padx, pady = pady)

        conv_pipe = Button(self, text = 'Convert to .meth files', command = self.run_pipeline)
        conv_pipe.grid(row = 6, column = 1, sticky = E, padx = padx, pady = pady)

    def run_pipeline(self):

        # methylation file conversion variables
        convert_input = self._conv_input_entry.get()
        convert_output = self._conv_output_entry.get()

        username = self._username.get()
        password = self._password.get()
        email = self._email.get()

        command = 'qsub -M {} -v input={},output={} meth_convert.pbs'.format(
                                                email, convert_input, convert_output)
        vars = [email, username, convert_input, convert_output]

        passed = True

        for var in vars:
            if var == '':
                passed = False

        if passed:
            self.aciss_connect(command, username, password)
        else:
            self._message_txt.insert(INSERT, "All entry windows must be filled\n") 

if __name__ == '__main__':
    tk = Tk()
    tk.wm_title('Convert to .meth Files')
    MethConvInterface(tk).pack()
    tk.mainloop()