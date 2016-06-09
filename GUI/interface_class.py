__author__ = 'Hiranmayi Duvvuri, Alister Maguire'
__date__ = '06/01/2016'
__description__ = """
GUI parent class
"""

from tkinter import *
from tkinter.ttk import *
from paramiko import *
from abc import ABCMeta, abstractmethod

class Interface(Frame):

    __metaclass__ = ABCMeta

    def __init__(self, parent):
        Frame.__init__(self, parent, padding = '0.2i')

        pass

    @abstractmethod
    def run_pipeline(self):

        raise NotImplementedError

    def insert_text(self, string, text_box):
        """
        make text box active then disable after adding text.
        """    
        text_box.configure(state='normal')
        text_box.insert(INSERT, string)
        text_box.configure(state='disabled')


    def aciss_connect(self, command, username, pswd=None):
        """
        Connect to ACISS and send job with PBS.
        """

        if pswd == '':
            pswd = None

        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.load_system_host_keys()
            client.connect('aciss.uoregon.edu', username=username, password=pswd)
            self.insert_text("Connected to ACISS!\n", self._message_txt)
            self.insert_text('running pipeline...\n', self._message_txt)
            stdin, stdout, stderr = client.exec_command(command)
            terminalOut = stdout.readlines()
            for line in terminalOut:
                out = line + '\n'
                self._message_txt.insert(INSERT, out)
            client.close()   
        except Exception:
            self.insert_text("ERROR: unable to connect to ACISS...\n", self._message_txt)

