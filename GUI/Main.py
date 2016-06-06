__author__ = 'Alister Maguire'
__date__ = '05/31/2016'
__description__ = "Main class to launch a pipeline notebook."

from masterNotebook import *
from bratFrame import *
from comparison_gui import *
from convert_gui import *
from tkinter import Tk

if __name__ == "__main__":
    '''
    Create and launch a notebook containing several
    pipeline widgets that connect to the ACISS server. 
    '''
    root = Tk()
    root.wm_title('ACISS Pipelines')
    notebook     = masterNotebook(root)
    brat_pipe    = BratInterface(notebook)
    meth_compare = MethCompInterface(notebook)
    meth_convert = MethConvInterface(notebook)
    notebook.addFrame(brat_pipe, 'BRAT Pipe')
    notebook.addFrame(meth_convert, 'Meth Conversion Pipe')
    notebook.addFrame(meth_compare, 'Meth Comparison Pipe')
    root.mainloop()
    