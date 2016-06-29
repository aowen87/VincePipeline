import argparse
import os
import sys
import subprocess
import fileinput 

try:
    from paramiko import *
except ImportError: 
    os.system('pip3 install paramiko')
    os.system('pip install paramiko')
    from paramiko import *


def addPath(ACISS_path):
    '''
       Add the ACISS path to all appropriate python and pbs files. 
       param: ACISS_path 
    '''
    path_dirs = ['..\\PBS', '..\\GUI']
    for path_dir in path_dirs:
        for root, dirs, files in os.walk(path_dir):
            for f in files:
                file_path = os.path.join(root, f)
                with fileinput.FileInput(file_path, inplace=True, mode='U') as file:
                    for line in file:
                        print(line.replace('_PATH_INSERT_', ACISS_path), end='') 


def createShortcut(sink_path):
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


def buildACISSRepo(usrname, pswd, ACISS_path, genome_path):
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
        host = "aciss.uoregon.edu"
        port = 22
        transport = Transport((host, port))
        transport.connect(username=usrname, password=pswd)
        sftp = SFTPClient.from_transport(transport)
        try:
            sftp.chdir(ACISS_path)
        except IOError:
            sftp.mkdir(ACISS_path)
            sftp.chdir(ACISS_path)
        dirTransfer(sftp, '..\\pipeline', './')
        dirTransfer(sftp, '..\\PBS', './')
        dirTransfer(sftp, '.\\', './', ['install.py', 'helper.py', 'windowsInstall.py', 'unixInstall.py', 'linuxInstall.py'])
        sftp.mkdir('BRAT_BW')
        genomeTransfer(sftp, genome_path, './BRAT_BW')
        sftp.mkdir('mapChip')
        sftp.mkdir('MethlyationPipe')
        helper.organize()
        sftp.close()
        transport.close()
    except Exception as e:
        print("ERROR BUILDING REPO: ", e)


def dirTransfer(trans_sftp, src_dir, sink_dir, file_excludes=[]):
    '''
       Transfer a directory and all of it's contents to ACISS.
           param: 
                 trans_sftp: A paramiko sftp client.
                 src_dir: The local target path/directory.
                 sink_dir: The ACISS target path/directory.
                 file_excludes: A list of files that shouldn't be 
                 transfered to ACISS. 
    
    '''
    for root, dirs, files in os.walk(src_dir):
        for dr in dirs:
            src_path  = os.path.join(root, dr)
            sink_path  = src_path.replace(src_dir, sink_dir) 
            trans_sftp.mkdir(sink_path)
        if file_excludes:
            for f in files:
                if f not in file_excludes:
                    src_path  = os.path.join(root, f)
                    sink_path = src_path.replace(src_dir, sink_dir) 
                    sink_path = sink_path.replace('\\', '/')
                    trans_sftp.put(src_path, sink_path)
        else:
            for f in files:
                src_path  = os.path.join(root, f)
                sink_path = src_path.replace(src_dir, sink_dir) 
                sink_path = sink_path.replace('\\', '/')
                trans_sftp.put(src_path, sink_path)


def genomeTransfer(trans_sftp, genome_path, sink_dir):
    '''
    Transfer a local genome to ACISS. 
        param:
              trans_sftp: A paramiko sftp client.
              genome_path: Local path to a genome.
              sink_dir: The ACISS directory/ path 
              for installation. 
    '
    '''
    genome_dir = genome_path.split('\\')[-1] 
    sink_dir   = sink_dir + genome_dir 
    trans_sftp.mkdir(sink_dir)
    for root, dirs, files in os.walk(genome_path):
        for dr in dirs:                             
            dir_path  = os.path.join(root, dr)
            sink_path = dir_path.replace(genome_path, sink_dir) 
            sink_path = sink_path.replace('\\', '/')
            trans_sftp.mkdir(sink_path)
        for f in files:
            file_path = os.path.join(root, f)
            sink_path = file_path.replace(genome_path, sink_dir) 
            sink_path = sink_path.replace('\\', '/')
            trans_sftp.put(file_path, sink_path)


def windowsInstall(usrname, pswd, ACISS_path, shortcut_path, genome_path):
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
    addPath(ACISS_path)
    buildACISSRepo(usrname, pswd, ACISS_path, genome_path)
    createShortcut(shortcut_path)


if __name__ == "__main__":
    '''
       Used for testing from the command line. 
    '''
    parser = argparse.ArgumentParser("Setup for Vince's pipeline")
    parser.add_argument('usrname', type=str)
    parser.add_argument('pswd', type=str, default='')
    args = parser.parse_args()
    usrname = args.usrname
    pswd = args.pswd 
    windowsInstall(usrname, pswd, "Win32Install", 'C:\\Users\\alister\\Desktop', 'C:\\Users\\alister\\Dropbox\\BioInf\\research\\fakeGenome')


