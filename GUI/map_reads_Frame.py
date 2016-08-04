'''
Created on May 17, 2016
@author: Alister Maguire, Pat Johnson
'''
from tkinter import *
from tkinter.ttk import *
from paramiko import *
from interface_class import Interface

class ChipInterface(Interface):

    def __init__(self, master):
        '''
        Set up the main _PATH_INSERT_ interface and all class variables. 
        '''  
        Interface.__init__(self, master)
        #fonts, colors, padding, etc. 
            
        PADX = 2
        PADY = 4
        ENTRY_W = 30
        progress_box = Frame(self, relief=SUNKEN, borderwidth=5)
        scroll = Scrollbar(progress_box)
        scroll.pack(side=RIGHT, fill=Y)
        self._message_txt = Text(progress_box, height=7)
        self._message_txt.config(state=DISABLED)
        self._message_txt.pack(fill = X)
        #Labels and entries   
        email_label                = Label(self, text="Email: ")
        self._email_entry          = Entry(self, width=ENTRY_W)
        usr_name_label             = Label(self, text="ACISS user name: ")
        self._usr_name_entry       = Entry(self, width=ENTRY_W)
        pswd_label                 = Label(self, text="ACISS password: ")
        self._pswd_entry           = Entry(self, show='*', width=ENTRY_W)
        chip_directory_label       = Label(self, text="Chip Reads Directory: ")
        self._chip_directory_entry = Entry(self, width = ENTRY_W)
        genome_label               = Label(self, text="Genome*: ")
        self._genome_entry         = Entry(self, width = ENTRY_W)
        genome_description         = Label(self, 
                                           text = ("*If building a genome, pass the name of a" +
                                           " fasta file.  Otherwise a genome directory" ))
        output_label                 = Label(self, text="Chip Output Directory: ")
        self._output_directory_entry = Entry(self, width = ENTRY_W)
        Start                        = Button(self, text='RUN PIPELINE', command=self.run_pipeline)
        #_PATH_INSERT_ structure
        email_label.grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        self._email_entry.grid(row=0, column=1, sticky=W, padx=PADX, pady=PADY)
        usr_name_label.grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        self._usr_name_entry.grid(row=1, column=1, sticky=W, padx=PADX, pady=PADY)
        pswd_label.grid(row=2, column=0, stick=W, padx=PADX, pady=PADY)
        self._pswd_entry.grid(row=2, column=1, sticky=W, padx=PADX, pady=PADY)

        chip_directory_label.grid(row=3, column=0, sticky=W, padx=PADX, pady=PADY)
        self._chip_directory_entry.grid(row=3, column=1, sticky=W, padx=PADX, pady=PADY)
        genome_label.grid(row=4, column=0, sticky=W, padx=PADX, pady=PADY)
        self._genome_entry.grid(row=4, column=1, sticky=W, padx=PADX, pady=PADY)
        genome_description.grid(row=5,column=0, sticky=N+E+S+W, padx=PADX, pady=PADY,columnspan=2)
        output_label.grid(row=6, column=0, sticky=W, padx=PADX, pady=PADY)
        self._output_directory_entry.grid(row=6, column=1, sticky=W, padx=PADX, pady=PADY)
        progress_box.grid(row=7, column=0, sticky=N+E+S+W, padx=PADX, pady=PADY,columnspan=2)
        Start.grid(row=8, column=1, sticky=E, padx=PADX, pady=PADY)
        self._usr_name_entry.focus_set()
    
    
    def run_pipeline(self):
        '''
          Runs the chip_pipe pipeline to map reads to a genome for display
          on IGV (for ChipSeq)
        '''
        #Retrieve entries
        passed            = True
        email             = self._email_entry.get()
        chip_directory    = self._chip_directory_entry.get()
        genome            = self._genome_entry.get()
        usrname           = self._usr_name_entry.get()
        password          = self._pswd_entry.get()
        output_directory    = self._output_directory_entry.get()
            
        vars = [usrname, genome, chip_directory, output_directory]
            
        for var in vars:
            if var == '':
                passed = False
                    
        if passed:          
            
            command = "(cd _PATH_INSERT_/mapChip; qsub -M {} -v chip_directory={},genome={},output_directory={} chip_pipe.pbs)".format(email, chip_directory, genome, output_directory)
            
            self.aciss_connect(command, usrname, password)
        else:
            self.insert_text("All entry windows must be filled (excluding email and password)\n", self._message_txt)
            
    
