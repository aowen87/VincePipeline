__author__ = 'Alister Maguire'
__date__ = '05/31/2016'
__description__ = "A child of ttk.Notebook to be used in various pipelines."
from tkinter import ttk

class masterNotebook(ttk.Notebook):
    '''
    A ttk notebook with set dimensions. The primary purpose
    of creating a separate class for this notebook is for 
    the possibility of adding expansions/themes to 
    the notebook in the future.
    '''
    
    def __init__(self, master):
        ttk.Notebook.__init__(self, master, width=700, height=670)
        self.pack()
        
    def addFrame(self, frame, fText):
        self.add(frame, text=fText, state='normal')

        
        
