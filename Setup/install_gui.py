__author__ = 'Hiranmayi Duvvuri'
__date__ = '06/18/2016'
__description__ = """
Installation GUI
"""

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from install import install
from clean import fullClean
import os, sys

class InstallInterface(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, padding = '0.2i')

        # Style
        PADX = 2
        PADY = 4
        pad = '0.2i'
        ENTRY_W = 30
        border = 5

        # Widgets

        progress_box = Frame(self, relief = SUNKEN, borderwidth = 5)
        scroll = Scrollbar(progress_box)
        scroll.pack(side = RIGHT, fill = Y)
        self._message_txt = Text(progress_box, height = 7)
        self._message_txt.config(state=DISABLED)
        self._message_txt.pack(fill = X)

        pathdirlabel = Label(self, text = 'ACISS install directory: ')
        pathdirlabel.grid(row = 0, column = 0, sticky = W, padx = PADX, pady = PADY)

        self._pathdir = Entry(self, width = ENTRY_W)
        self._pathdir.grid(row = 0, column = 1, sticky = W, padx = PADX, pady = PADY, columnspan = 2)

        userlabel = Label(self, text = 'ACISS user name: ')
        userlabel.grid(row = 1, column = 0, sticky = W, padx = PADX, pady = PADY)

        self._username = Entry(self, width = ENTRY_W)
        self._username.grid(row = 1, column = 1, sticky = W, padx = PADX, pady = PADY, columnspan= 2)

        pwdlabel = Label(self, text = 'password: ')
        pwdlabel.grid(row = 2, column = 0, sticky = W, padx = PADX, pady = PADY)

        self._password = Entry(self, show = '*', width = ENTRY_W)
        self._password.grid(row = 2, column = 1, sticky = W, padx = PADX, pady = PADY, columnspan = 2)

        genomelabel = Label(self, text = 'genome path: ')
        genomelabel.grid(row = 3, column = 0, sticky = W, padx = PADX, pady = PADY)

        self._genomepath = Entry(self, width = ENTRY_W - 10)
        self._genomepath.grid(row = 3, column = 1, sticky = W, padx = PADX, pady = PADY, columnspan = 2)

        genomebutton = Button(self, text = 'load genome', command = self.load_directory)
        genomebutton.grid(row = 3, column = 2, sticky = W, padx = PADX, pady = PADY)

        progress_box.grid(row = 4, column = 0, columnspan = 3, sticky=N+E+S+W, padx = PADX, pady = PADY)

        run_install = Button(self, text = 'Install Pipeline', command = self.run_setup)
        run_install.grid(row = 5, column = 1, columnspan = 1, sticky = E, padx = PADX, pady = PADY)

        run_uninstall = Button(self, text = 'Uninstall Pipeline', command = self.uninstall)
        run_uninstall.grid(row = 5, column = 2, columnspan = 1, sticky = E, padx = PADX, pady = PADY)

        self._pathdir.focus_set()

    def insert_text(self, string, text_box):
        """
        make text box active then disable after adding text.
        """    
        text_box.configure(state=NORMAL)
        text_box.insert(INSERT, string)
        text_box.configure(state=DISABLED)

    def load_directory(self):

        path_name = filedialog.askdirectory()
        self._genomepath.insert(INSERT, path_name)

    def run_setup(self):

        username = self._username.get()
        password = self._password.get()
        path_dir = self._pathdir.get()
        shortcut_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        genome_path = self._genomepath.get()

        #if os.path.join(shortcut_path, 'pipeline'):
        #    self.insert_text('The shortcut already exists!', self._message_txt)
        #    sys.exit(1)

        self.insert_text(shortcut_path, self._message_txt)

        install(username, password, path_dir, shortcut_path, genome_path)

    def uninstall(self):

        username = self._username.get()
        password = self._password.get()
        path_dir = self._pathdir.get()
        shortcut_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        cur_os = str(sys.platform).lower()
        if cur_os == 'darwin' or cur_os == 'linux':
            shortcut_path = shortcut_path + "/pipeline"
        elif cur_os == 'win32' or cur_os == 'cygwin':
            shortcut_path = shortcut_path + "\\pipeline"
        else:
            self.insert_text("Invalid or unsupported os: " + cur_os, self._message_text)
            sys.exit()
        #print(local_path)
        fullClean(username, password, path_dir, shortcut_path, cur_os)

if __name__ == '__main__':
    tk = Tk()
    tk.wm_title('Installation')
    InstallInterface(tk).pack()
    tk.mainloop()
