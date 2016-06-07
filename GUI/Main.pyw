__author__ = 'Alister Maguire'
__date__ = '05/31/2016'
__description__ = "Main class to launch a pipeline notebook."

from masterNotebook import masterNotebook
from bratFrame import BratInterface
from comparison_gui import MethCompInterface
from convert_gui import MethConvInterface
from tkinter import Tk
from map_reads_Frame import ChipInterface
from averag_meth_Frame import AvgMethInterface

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
    meth_avg     = AvgMethInterface(notebook)
    chip_seq     = ChipInterface(notebook)
    notebook.addFrame(brat_pipe, 'BRAT Pipe')
    notebook.addFrame(meth_convert, 'Meth Conversion Pipe')
    notebook.addFrame(meth_compare, 'Meth Comparison Pipe')
    notebook.addFrame(meth_avg, 'Meth Averages')
    notebook.addFrame(chip_seq, 'ChIP-seq Analysis')
    root.mainloop()
    