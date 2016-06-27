import argparse
import os
import sys
import subprocess
import fileinput
import io
try:
    from paramiko import *
except ImportError: 
    os.system('pip3 install paramiko') #FIXME: this is sloppy
    os.system('pip install paramiko')            


def addPath(ACISS_path):
    '''
       Insert the aciss path into all appropriate files.
       param: ACISS_path -> a destination path on ACISS. 
       
    '''
    path_dirs = ['../PBS', '../GUI']
    for path_dir in path_dirs:
        for root, dirs, files in os.walk(path_dir):
            for f in files:
                file_path = os.path.join(root, f)
                with fileinput.FileInput(file_path, inplace=True) as file:
                    for line in file:
                        print(line.replace('_PATH_INSERT_', ACISS_path), end='') 
 
 
def createShortcut(sink_path):
    '''
       Create a shortcut to Main.pyw within the given destination path.
       param: sink_path -> the path to create a shortcut in. 
    '''
    if sink_path[-1] == '/':
        sink_path = sink_path[:-1]
    sink_path = sink_path + '/pipeline'
    if os.path.exists(sink_path):
        print("ERROR: {} already exists...".format(sink_path))
        sys.exit()    
    
    #os.system('touch {}'.format(sink_path))
    #src_path = os.path.dirname(os.getcwd()) + 'GUI/Main.pyw'
    #cmd_text = "#!/bin/bash\npython3 {}\nIF %ERRORLEVEL% NEQ 0 GOTO TryPython\n:TryPython\npython {}".format(src_path, src_path)
    #with open(sink_path, 'r+') as f:
        #f.write(cmd_text)

    #proc = subprocess.Popen(["which python3"], stdout=subprocess.PIPE, shell=True)
    #(out, err) = proc.communicate()
    #pypath = str(out)[2:-3]
    #if not pypath:
        #print("ERROR: unable to find python3 path...")
        #print("Make sure you have python3.x installed")
        #sys.exit()
        
    #pypath = '#!' + pypath
    #src_path = os.path.dirname(os.getcwd()) + '/GUI/Main.pyw'
    #os.system('chmod +x {}'.format(src_path))
    #with open(src_path, 'r+') as f:
        #content = f.read()
        #f.seek(0, 0)
        #f.write(pypath.rstrip('\r\n') + '\n' + content)
    #os.system("sed -i -e '1i#!{}\' {}".format(pypath, src_path))
    #os.symlink(src_path, '{}'.format(sink_path))
    
    src_path = os.path.dirname(os.getcwd()) + '/GUI/Main.pyw'
    text = "#!/bin/bash\npython3 {}".format(src_path)
    exe_file = open(sink_path, 'w')
    exe_file.write(text)
    exe_file.close()
    os.system("chmod 755 {}".format(sink_path))
     

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
        dirTransfer(sftp, '../pipeline', './')
        dirTransfer(sftp, '../PBS', './')
        dirTransfer(sftp, './', './', ['install.py', 'windowsInstall.py', 'unixInstall.py'])
        genomeTransfer(sftp, genome_path, './')
        sftp.mkdir('mapChip')
        sftp.rename('chip_map_reads.py', 'mapChip/chip_map_reads.py')
        sftp.rename('chip_pipe.pbs', 'mapChip/chip_pipe.pbs')
        sftp.close()
    except Exception as e:
        print("ERROR BUILDING REPO: ", e)
    sftp.close()
    transport.close()


def genomeTransfer(trans_sftp, genome_path, sink_dir):
    '''
        Transfer a local genome to ACISS. 
        param:
              trans_sftp: A paramiko sftp client.
              genome_path: Local path to a genome.
              sink_dir: The ACISS directory/ path 
              for installation. 
    '''
    if genome_path[-1] == '/':
        genome_path = genome_path[:-1]
    if sink_dir[-1] == '/':
        sink_dir = sink_dir[:-1]
    genome_dir = genome_path.split('/')[-1] 
    sink_dir   = sink_dir + '/' + genome_dir 
    trans_sftp.mkdir(sink_dir)
    for root, dirs, files in os.walk(genome_path):
        for dr in dirs:                             
            dir_path  = os.path.join(root, dr)
            sink_path = dir_path.replace(genome_path, sink_dir) 
            trans_sftp.mkdir(sink_path)
        for f in files:
            file_path = os.path.join(root, f)
            sink_path = file_path.replace(genome_path, sink_dir) 
            trans_sftp.put(file_path, sink_path)


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
    if src_dir[-1] == '/':
        src_dir = src_dir[:-1]
    if sink_dir[-1] == '/':
        sink_dir = sink_dir[:-1]
    
    for root, dirs, files in os.walk(src_dir):
        for dr in dirs:
            src_path  = os.path.join(root, dr)  
            sink_path = src_path.replace(src_dir, sink_dir) 
            trans_sftp.mkdir(sink_path)
        if file_excludes:
            for f in files:
                if f not in file_excludes:
                    src_path  = os.path.join(root, f)
                    sink_path = src_path.replace(src_dir, sink_dir) 
                    trans_sftp.put(src_path, sink_path)
        else:
            for f in files:
                src_path  = os.path.join(root, f)
                sink_path = src_path.replace(src_dir, sink_dir) 
                trans_sftp.put(src_path, sink_path)


def unixInstall(usrname, pswd, ACISS_path, shortcut_path, genome_path):
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
    unixInstall(usrname, pswd, 'UnixInstall', '/home/alister/Desktop', '/home/alister/Dropbox/BioInf/research/fakeGenome')


