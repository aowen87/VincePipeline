import argparse
import clean
import os
import sys
import subprocess
import fileinput
import io
try:
    from paramiko import *
except ImportError: 
    os.system('pip3 install paramiko')
    os.system('pip install paramiko')
    from paramiko import *


class Installer:

    def __init__(self, os):
        self._os = os
        valid_os = ['win32', 'darwin', 'linux']
        if self._os not in valid_os:
            print('ERROR: Invalid os...')
            sys.exit()
        if os == 'win32':
            self._divider = '\\'
        else:
            self._divider = '/'

    def addPath(self, ACISS_path):
        '''
           Insert the aciss path into all appropriate files.
           param: ACISS_path -> a destination path on ACISS. 
        '''
        print("Inserting paths")
        path_dirs = ['..{}PBS'.format(self._divider), '..{}GUI'.format(self._divider)]
        for path_dir in path_dirs:
            for root, dirs, files in os.walk(path_dir):
                for f in files:
                    file_path = os.path.join(root, f)
                    with fileinput.FileInput(file_path, inplace=True) as file:
                        for line in file:
                            print(line.replace('_PATH_INSERT_', ACISS_path), end='') 
 
    def buildACISSRepo(self, usrname, pswd, ACISS_path, genome_path):
        '''
           Build a repository on ACISS where all computations can take place. 
           param:
                 usrname: ACISS user name.
                 pswd: ACISS password.
                 ACISS_path: The destination path located on ACISS.
                 genome_path: The local path to a genome that will be
                 uploaded into the repository. 
        '''
        try:
            print("Attempting to connect to ACISS...")
            host = "aciss.uoregon.edu"
            port = 22
            transport = Transport((host, port))
            transport.connect(username=usrname, password=pswd)
            sftp = SFTPClient.from_transport(transport)
            print("Connected to ACISS!")
            try:
                sftp.chdir(ACISS_path)
            except IOError:
                sftp.mkdir(ACISS_path)
                sftp.chdir(ACISS_path)
            print("Transfering directries")
            self.dirTransfer(sftp, '..{}pipeline'.format(self._divider), './')
            self.dirTransfer(sftp, '..{}PBS'.format(self._divider), './')
            self.dirTransfer(sftp, '.{}'.format(self._divider), './',
                             ['install.py', 'installer.py', 'clean.py', 'install_gui.py'])
            print("Directoires transfered")
            sftp.mkdir('BRAT_BW')
            if genome_path != "":
                print("Transfering genome (this may take a while)")
                self.genomeTransfer(sftp, genome_path, './')
                print("Genome transfered\nOrganizing repo")
            sftp.mkdir('mapChip')
            sftp.mkdir('MethylationPipe')
            self.organize(sftp)
            sftp.close()
            transport.close()
            print("Successfully installed!")
        except Exception as e:
            print("ERROR BUILDING REPO: ", e)
            clean.removeRemote(usrname, pswd, ACISS_path)
            clean.removePaths(ACISS_path, self._os)
            sys.exit()

    def genomeTransfer(self, trans_sftp, genome_path, sink_dir):
        '''
            Transfer a local genome to ACISS. 
            param:
                  trans_sftp: A paramiko sftp client.
                  genome_path: Local path to a genome.
                  sink_dir: The ACISS directory/ path 
                  for installation. 
        '''

        if self._divider == '/':
            offset = -1
        else:
            offset = -2
        if genome_path[offset] == self._divider:
            genome_path = genome_path[:offset]
        if sink_dir[offset] == self._divider:
            sink_dir = sink_dir[:offset]
        genome_dir = genome_path.split(self._divider)[-1] 
        sink_dir   = sink_dir + '/' + genome_dir 
        trans_sftp.mkdir(sink_dir)
        for root, dirs, files in os.walk(genome_path):
            for dr in dirs:                             
                dir_path  = os.path.join(root, dr)
                sink_path = dir_path.replace(genome_path, sink_dir) 
                if self._os == 'win32':
                    sink_path = sink_path.replace('\\', '/')
                trans_sftp.mkdir(sink_path)
            for f in files:
                file_path = os.path.join(root, f)
                sink_path = file_path.replace(genome_path, sink_dir) 
                if self._os == 'win32':
                    sink_path = sink_path.replace('\\', '/')
                trans_sftp.put(file_path, sink_path)

    def dirTransfer(self, trans_sftp, src_dir, sink_dir, file_excludes=[]):
        '''
           Transfer a directory and all of it's contents to ACISS.
           param: 
                 trans_sftp: A paramiko sftp client.
                 src_dir: The local target path/directory.
                 sink_dir: The ACISS target path/directory.
                 file_excludes: A list of files that shouldn't be 
                 transfered to ACISS. 
        '''
        if self._divider == '/':
            offset = -1
        else:
            offset = -2
        if src_dir[offset] == self._divider:
            src_dir = src_dir[:offset]
        if sink_dir[offset] == self._divider:
            sink_dir = sink_dir[:offset]
        
        for root, dirs, files in os.walk(src_dir):
            for dr in dirs:
                if dr != '__pycache__':
                    src_path  = os.path.join(root, dr)  
                    sink_path = src_path.replace(src_dir, sink_dir) 
                    trans_sftp.mkdir(sink_path)
            if file_excludes:
                for f in files:
                    if f not in file_excludes:
                        src_path  = os.path.join(root, f)
                        if src_path.split(self._divider)[1] != '__pycache__':
                            sink_path = src_path.replace(src_dir, sink_dir) 
                            if self._os == 'win32':
                                sink_path = sink_path.replace('\\', '/')
                            trans_sftp.put(src_path, sink_path)
            else:
                for f in files:
                    src_path  = os.path.join(root, f)
                    sink_path = src_path.replace(src_dir, sink_dir) 
                    if self._os == 'win32':
                        sink_path = sink_path.replace('\\', '/')
                    trans_sftp.put(src_path, sink_path)

    def linuxShortcut(self, sink_path):
        '''
           Create a shortcut to Main.pyw within the given destination path.
           param: sink_path -> the path to create a shortcut in. 
        '''
        if sink_path[-1] == '/':
            sink_path = sink_path[:-1]
        sink_path = sink_path + '/pipeline'
        if os.path.exists(sink_path):
            print("ERROR: {} already exists...".format(sink_path))
            print("shorcut not created")
            sys.exit()    
        proc = subprocess.Popen(["which python3"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        pypath = str(out)[2:-3]
        if not pypath:
            print("ERROR: unable to find python3 path...")
            print("Make sure you have python3.x installed")
            sys.exit()                                 #FIXME: raise error instead?
        pypath = '#!' + pypath
        src_path = os.path.dirname(os.getcwd()) + '/GUI/Main.pyw'
        os.system('chmod +x {}'.format(src_path))
        with open(src_path, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(pypath.rstrip('\r\n') + '\n' + content)
        os.symlink(src_path, '{}'.format(sink_path))

    def unixShortcut(self, sink_path):
        '''
           Create a bash script that calls Main.pyw within the given destination path.
           param: sink_path -> the path to create a shortcut in. 
        '''
        if sink_path[-1] == '/':
            sink_path = sink_path[:-1]
        sink_path = sink_path + '/pipeline'
        if os.path.exists(sink_path):
            print("ERROR: {} already exists...".format(sink_path))
            sys.exit()    


        #FIXME: testing block begin
        proc = subprocess.Popen(["which python3"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        pypath = str(out)[2:-3]
        if not pypath:
            print("ERROR: unable to find python3 path...")
            print("Make sure you have python3.x installed")
            sys.exit()                                 #FIXME: raise error instead?
        py_call = pypath.split('/')[-1]
        #FIXME: testing block end 

        src_path = os.path.dirname(os.getcwd()) + '/GUI/Main.pyw'
        text = "#!/bin/bash\n{} {}".format(py_call, src_path)
        exe_file = open(sink_path, 'w')
        exe_file.write(text)
        exe_file.close()
        os.system("chmod 755 {}".format(sink_path))
    
    def win32Shortcut(self, sink_path):
        '''
           Create a shortcut that runs Main.pyw. 
           param: sink_path -> where the shortcut should
                  be installed. 
        '''
        if sink_path[-1] == '\\':
            sink_path = sink_path[:-1]
        sink_path = sink_path + '\\pipeline.cmd'
        if os.path.exists(sink_path):
            print("ERROR: {} already exists...".format(sink_path))
            sys.exit()    
        os.system('touch {}'.format(sink_path)) 
        src_path = os.path.dirname(os.getcwd()) + '\\GUI\\Main.pyw'
        cmd_text = "python3 {}\nIF %ERRORLEVEL% NEQ 0 GOTO TryPython\n:TryPython\npython {}".format(src_path, src_path)
        with open(sink_path, 'r+') as f:
            f.write(cmd_text)

    def organize(self, sftp): 
        sftp.rename('chip_map_reads.py', 'mapChip/chip_map_reads.py')
        sftp.rename('chip_pipe.pbs', 'mapChip/chip_pipe.pbs')
        sftp.rename('analyzing.py', 'BRAT_BW/analyzing.py')
        sftp.rename('bisulfiteMap.py', 'BRAT_BW/bisulfiteMap.py')
        sftp.rename('mappedDupl', 'BRAT_BW/mappedDupl')
        sftp.rename('mappedNoDupl', 'BRAT_BW/mappedNoDupl')
        sftp.rename('bratPipe.pbs', 'BRAT_BW/bratPipe.pbs')
        sftp.rename('Nc12genome', 'BRAT_BW/Nc12genome')
        sftp.rename('BS_genome_fasta', 'BRAT_BW/BS_genome_fasta')
        sftp.rename('ave_meth.pbs', 'MethylationPipe/ave_meth.pbs')
        sftp.rename('average_meth.py', 'MethylationPipe/average_meth.py')
        sftp.rename('comp_avg.pbs', 'MethylationPipe/comp_avg.pbs')
        sftp.rename('conv_avg.pbs', 'MethylationPipe/conv_avg.pbs')
        sftp.rename('conv_comp.pbs', 'MethylationPipe/conv_comp.pbs')
        sftp.rename('meth_compare.pbs', 'MethylationPipe/meth_compare.pbs')
        sftp.rename('meth_convert.pbs', 'MethylationPipe/meth_convert.pbs')
        sftp.rename('meth_convert.py', 'MethylationPipe/meth_convert.py')
        sftp.rename('meth_pipe.pbs', 'MethylationPipe/meth_pipe.pbs')
        sftp.rename('methylome_comp.py', 'MethylationPipe/methylome_comp.py')

    def install(self, usrname, pswd, ACISS_path, shortcut_path, genome_path):
        '''
           Auto-Install install the pipeline. 
           param:
                 usrname: ACISS user name.
                 pswd: ACISS password.
                 ACISS_path: Target path/directory for installation
                 on ACISS. 
                 shorcut_path: Target path/directory for local 
                 shortcut. 
                 genome_path: Local path/directory containing the
                 genome to be transfered to ACISS. 
        '''
        try:
            self.addPath(ACISS_path)
            self.buildACISSRepo(usrname, pswd, ACISS_path, genome_path)
        except Exception:
            sys.exit()
        if self._os == 'darwin':
            self.unixShortcut(shortcut_path)
        elif self._os == 'linux':
            self.linuxShortcut(shortcut_path)
        else:
            self.win32Shortcut(shortcut_path)

