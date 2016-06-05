__author__ = 'Hiranmayi Duvvuri, Alister Maguire'
__date__ = '05/31/2016'
__description__ = """
GUI for part of methylation pipeline.
"""

from tkinter import *
from tkinter.ttk import *
from paramiko import *

class MethInterface(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, padding = '0.2i')

        # Style
        style = Style()
        pad = '0.2i'
        #style.configure('TFrame', padding = pad)

        userlabel = Label(self, text = 'ACISS Username: ')
        userlabel.grid(row = 0, column = 0)

        self._username = Entry(self)
        self._username.grid(row = 0, column = 1)

        emaillabel = Label(self, text = 'email: ')
        emaillabel.grid(row = 1, column = 0)

        self._email = Entry(self)
        self._email.grid(row = 1, column = 1)

        progress_box = Frame(self)
        scroll = Scrollbar(progress_box)
        scroll.pack(side = RIGHT, fill = Y)
        self._message_txt = Text(progress_box, height = 8)
        self._message_txt.pack()


        # Create notebook style Frames for GUI
        meth_nb = Notebook(self)
        meth_convert = Frame(meth_nb, padding = pad)
        meth_comp = Frame(meth_nb, padding = pad)

        # conversion frame
        conv_input_label = Label(meth_convert, text = 'Converted BRAT-BW Files Directory: ')
        conv_input_label.grid(row = 0, column = 0)

        self._conv_input_entry = Entry(meth_convert)
        self._conv_input_entry.grid(row = 0, column = 1)

        conv_output_label = Label(meth_convert, text = 'Results Directory: ')
        conv_output_label.grid(row = 1, column = 0)

        self._conv_output_entry = Entry(meth_convert)
        self._conv_output_entry.grid(row = 1, column = 1)

        conv_pipe = Button(meth_convert, text = 'Convert to .meth files', command = self.run_pipeline)
        conv_pipe.grid(row = 3, column = 0, columnspan = 2)

        # methylome comparison Frame
        comp_input_label = Label(meth_comp, text = 'Files to Compare directory: ')
        comp_input_label.grid(row = 0, column = 0)

        self._comp_input_entry = Entry(meth_comp)
        self._comp_input_entry.grid(row = 0, column = 1)

        comp_output_label = Label(meth_comp, text = 'Results Directory: ')
        comp_output_label.grid(row = 1, column = 0)

        self._comp_output_entry = Entry(meth_comp)
        self._comp_output_entry.grid(row = 1, column = 1)

        wt_meth_label = Label(meth_comp, text = '.meth of WT Sample: ')
        wt_meth_label.grid(row = 2, column = 0)

        self._wt_meth_entry = Entry(meth_comp)
        self._wt_meth_entry.grid(row = 2, column = 1)

        wt_hmr_label = Label(meth_comp, text = '.hmr of WT Sample: ')
        wt_hmr_label.grid(row = 3, column = 0)

        self._wt_hmr_entry = Entry(meth_comp)
        self._wt_hmr_entry.grid(row = 3, column = 1)

        comp_pipe = Button(meth_comp, text = 'Start Sample Comparisons', command = self.run_pipeline)
        comp_pipe.grid(row = 5, column = 0, columnspan = 2)

        # Pack notebook
        meth_nb.add(meth_convert, text = 'convert to .meth files')
        meth_nb.add(meth_comp, text = 'methylome comparison')
        meth_nb.grid(row = 2, column = 0, columnspan = 2)
        progress_box.grid(row = 3, column = 0, columnspan = 2)

    def run_pipeline(self):

        # methylation file conversion variables
        convert_input = self._conv_input_entry.get()
        convert_output = self._conv_output_entry.get()
    
        # methylome comparison variables
        comp_input = self._comp_input_entry.get()
        comp_output = self._comp_output_entry.get()
        wt_meth = self._wt_meth_entry.get()
        wt_hmr = self._wt_hmr_entry.get()

        username = self._username.get()
        email = self._email.get()

        command = ''
        vars = [username, email]
        passed = True

        if not (convert_input or convert_output) and (comp_output and comp_input and wt_meth and wt_hmr):
            command = "(cd pipeline; qsub -M {} -v input={}, output={}, wt_meth={}, wt_hmr={} meth_compare.pbs)".format(
                            email, comp_input, comp_output, wt_meth, wt_hmr)
            vars.extend([comp_output, comp_input, wt_meth, wt_hmr])
        elif not (comp_input or comp_output or wt_meth or wt_hmr) and (convert_input and convert_output):
            command = "(cd pipeline; qsub -M {} -v input={}, output={} meth_convert.pbs)".format(
                            email, convert_input, convert_output)
            vars.extend([convert_input, convert_output])
        else:
            self._message_txt.insert(INSERT, 'please enter values for one pipeline! \n')

        for var in vars:
            if var == '':
                passed = False

        if passed:
            try:
                client = SSHClient()
                client.set_missing_host_key_policy(AutoAddPolicy())
                client.load_system_host_keys()
                client.connect('aciss.uoregon.edu', username=self._usrname)
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
        
        else:
            self._message_txt.insert(INSERT, "All entry windows must be filled\n") 

if __name__ == '__main__':
    tk = Tk()
    tk.wm_title('Methylation Pipeline')
    MethInterface(tk).pack()
    tk.mainloop()