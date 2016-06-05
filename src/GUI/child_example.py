__author__ = 'Hiranmayi Duvvuri'
__date__ = '06/02/2016'
__description__ = """
GUI child class blank
"""

from tkinter import *
from tkinter.ttk import *
from paramiko import *
from interface_class import Interface

class NAMEInterface(Interface):

    def __init__(self, parent):
        Interface.__init__(self, parent)

        userlabel = Label(self, text = 'ACISS Username: ')
        userlabel.grid(row = 0, column = 0)

        self._username = Entry(self)
        self._username.grid(row = 0, column = 1)

        pwdlabel = Label(self, text = 'password: ')
        pwdlabel.grid(row = 1, column = 0)

        self._password = Entry(self, show = '*')
        self._password.grid(row = 1, column = 1)

        emaillabel = Label(self, text = 'email: ')
        emaillabel.grid(row = 2, column = 0)

        self._email = Entry(self)
        self._email.grid(row = 2, column = 1)

        progress_box = Frame(self)
        scroll = Scrollbar(progress_box)
        scroll.pack(side = RIGHT, fill = Y)
        self._message_txt = Text(progress_box, height = 8)
        self._message_txt.pack()



        #### FILL IN SPECIFIC GUI FUNCTIONS
        #### WHEN MAKING RUN_PIPELINE BUTTON, use function call self.run_pipeline



        ### CHANGE ROW TO LAST ROW
        progress_box.grid(row = x, column = 0, columnspan = 2)

    def run_pipeline(self):

        #### FILL IN REST OF VARIABLES
        

        username = self._username.get()
        password = self._password.get()
        email = self._email.get()

        ### FILL IN COMMAND AND VARIABLES
        command = '' 
        vars = [email, username]

        
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
    tk.wm_title('NAME')
    NAMEInterface(tk).pack()
    tk.mainloop()