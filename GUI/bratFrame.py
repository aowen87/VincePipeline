__author__ = 'Alister Maguire'
__date__ = '05/17/2016'
__description__ = """The GUI for the launching and running bisulfiteMap.py 
and analyzing.py as a single pipeline. """

from tkinter import *
from tkinter import font
from paramiko import *
from interface_class import Interface

class BratInterface(Interface):
    
    def __init__(self, parent):
        '''
        Set up the main GUI interface and all class variables. 
        '''  
        Interface.__init__(self, parent)
        
        #fonts, colors, padding, etc. 
        ENTRY_W = 30
        PADX    = 2
        PADY    = 9
        cur_font     = font.Font(family="Courier New", size=13, weight="bold")
        progress_box = Frame(self, relief=SUNKEN, background='white', borderwidth=5)
        scroll       = Scrollbar(progress_box)
        scroll.pack(side=RIGHT, fill=Y)
        self._message_txt = Text(progress_box, height=7)
        self._message_txt.pack()

        #Labels and entries    
        email_label              = Label(self, padx=PADX, pady=PADY, text="Email: ")
        self._email_entry        = Entry(self, bd=5, width=ENTRY_W)
        usr_name_label           = Label(self, padx=PADX, pady=PADY, text="ACISS user name: ")
        self._usr_name_entry     = Entry(self, bd=5, width=ENTRY_W)
        pswd_label               = Label(self, padx=PADX, pady=PADY, text="ACISS password: ")
        self._pswd_entry         = Entry(self, bd=5, show='*', width=ENTRY_W)
        brat_dir_label           = Label(self, padx=PADX, pady=PADY, text="BRAT genome directory: ")
        self._brat_dir_entry     = Entry(self, bd=5, width=ENTRY_W)
        fastq_label              = Label(self, padx=PADX, pady=PADY, text="fastq directory: ")
        self._fastq_entry        = Entry(self, bd=5, width=ENTRY_W)
        analyzed_res_label       = Label(self, padx=PADX, pady=PADY, text="results directory: ")
        self._analyzed_res_entry = Entry(self, bd=5, width=ENTRY_W)
        mistmatch_label          = Label(self, padx=2, pady=PADY, text="non-BS mismatches: ")
        self._mismatch_entry     = Entry(self, bd=5, width=10)
        self._mismatch_entry.insert(END, '2')
        quality_label            = Label(self, padx=2, pady=PADY, text="quality score: ")
        self._quality_entry      = Entry(self, width=10, bd=5)
        self._quality_entry.insert(END, '20')
        self._build_check_var    = IntVar()
        build_check              = Checkbutton(self, text="build genome", variable=self._build_check_var,
                                              onvalue=1, offvalue=0, height=5, width=20)
        self._clean_check_var    = IntVar()
        self._clean_check_var.set(1)
        clean_check              = Checkbutton(self, text="remove extra output", variable=self._clean_check_var,
                                              onvalue=1, offvalue=0, height=5, width=20)
        start                    = Button(self, text='RUN PIPELINE', font=cur_font, command=self.run_pipeline)
        self._email_entry.focus_set()
       
        #GUI structure
        email_label.grid(row=0, column=0, sticky=W, padx=PADX+30)
        self._email_entry.grid(row=0, column=1, sticky=W, padx=PADX+30)
        usr_name_label.grid(row=1, column=0, sticky=W, padx=PADX+30)
        self._usr_name_entry.grid(row=1, column=1, sticky=W, padx=PADX+30)
        pswd_label.grid(row=2, column=0, stick=W, padx=PADX+30)
        self._pswd_entry.grid(row=2, column=1, sticky=W, padx=PADX+30)
        brat_dir_label.grid(row=3, column=0, sticky=W, padx=PADX+30)
        self._brat_dir_entry.grid(row=3, column=1, sticky=W, padx=PADX+30)
        fastq_label.grid(row=4, column=0, sticky=W, padx=PADX+30)
        self._fastq_entry.grid(row=4, column=1, sticky=W, padx=PADX+30)
        analyzed_res_label.grid(row=5, column=0, sticky=W, padx=PADX+30)
        self._analyzed_res_entry.grid(row=5, column=1, sticky=W, padx=PADX+30)
        mistmatch_label.grid(row=6, column=0, sticky=W, padx=PADX+30)
        self._mismatch_entry.grid(row=6, column=1, sticky=W, padx=PADX+30)
        quality_label.grid(row=7, column=0, sticky=W, padx=PADX+30)
        self._quality_entry.grid(row=7, column=1, sticky=W, padx=PADX+30)
        build_check.grid(row=8, column=0, sticky=W)
        clean_check.grid(row=8, column=1)
        progress_box.grid(row=9, column=0, sticky=N+E+S+W, padx=PADX+5, pady=PADY,columnspan=2)
        start.grid(row=10, column=1, sticky=E, pady=PADY)
    
    
    def run_pipeline(self):
        '''
        Retrieve entries from the GUI, create the ACISS
        command, and call aciss_connect().
        '''
        #Retrieve entries
        passed = True
        email           = self._email_entry.get()
        pswrd           = self._pswd_entry.get()
        BRAT_genome_dir = self._brat_dir_entry.get()
        fastq_dir       = self._fastq_entry.get()
        results_dir     = self._analyzed_res_entry.get()
        usrname         = self._usr_name_entry.get()
        quality_score   = self._quality_entry.get()
        mismatches      = self._mismatch_entry.get()    
        if self._build_check_var.get():
            build_genome = True 
        else:
            build_genome = False
        if self._clean_check_var.get():
            clean = True
        else:
            clean = False
         
        vars = [usrname, fastq_dir, results_dir, BRAT_genome_dir,
                mismatches, quality_score, build_genome, clean]
        
        for var in vars:
            if var == '':
                passed = False
                               
        if passed:
            command = ("(cd /research/CIS454/vince/pipeline; qsub -M {} -v brat={},fastq={},"
            "build={},mismatch={},score={},res={},clean={},map='mapResults' bratPipe.pbs)".format(email, 
            BRAT_genome_dir, fastq_dir, build_genome, mismatches, quality_score, 
            results_dir, clean))
     
            self.aciss_connect(command, usrname, pswrd)
        else:
            self._message_txt.insert(INSERT, "All entry windows must be filled (excluding email and password)\n") 
       
       
 
        
        
        
        
      

