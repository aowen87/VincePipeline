#!/usr/bin/python3
__author__ = 'Alister Maguire'
__date__ = '05/31/2016'
__description__ = "Main class to launch a pipeline notebook."

from masterNotebook import masterNotebook
from bratFrame import BratInterface
from tkinter import Tk
from tkinter.ttk import Style
from map_reads_Frame import ChipInterface
from meth_pipe_gui import MethInterface

if __name__ == "__main__":
    '''
    Create and launch a notebook containing several
    pipeline widgets that connect to the ACISS server. 
    '''
    root = Tk()
    style = Style()
    style.theme_use('clam')
    root.wm_title('ACISS Pipelines')
    notebook     = masterNotebook(root)
    brat_pipe    = BratInterface(notebook)
    meth_pipe    = MethInterface(notebook)
    chip_seq     = ChipInterface(notebook)
    notebook.addFrame(brat_pipe, 'BRAT Pipe')
    notebook.addFrame(meth_pipe, 'Methylation Pipeline')
    notebook.addFrame(chip_seq, 'ChIP-seq Analysis')
    root.mainloop()
    
