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
        

    def aciss_connect(self, command, username, password=None):
        """
        Connect to ACISS and send job with PBS.
        """

        if password == '':
            password = None

        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.load_system_host_keys()
            client.connect('aciss.uoregon.edu', username=username, password=password)
            self._message_txt.insert(INSERT, "Connected to ACISS!\n")
            self._message_txt.insert(INSERT, 'running pipeline...\n')
            stdin, stdout, stderr = client.exec_command(command)
            terminalOut = stdout.readlines()
            for line in terminalOut:
                out = line + '\n'
                self._message_txt.insert(INSERT, out)
            client.close()   
        except Exception:
            self._message_txt.insert(INSERT, "ERROR: unable to connect to ACISS...\n")
