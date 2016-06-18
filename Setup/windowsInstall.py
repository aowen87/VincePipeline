from paramiko import *
import argparse
import os
import sys
import subprocess




def addPath(ACISS_path):
    '''
    '''
    os.system("(Get-Content ../PBS/*) | ForEach-Object {{ $_ -replace '_PATH_INSERT_', '{}' }} | Set-Content ./*".format(ACISS_path))
    os.system("(Get-Content ../GUI/*) | ForEach-Object {{ $_ -replace '_PATH_INSERT_', '{}' }} | Set-Content ./*".format(ACISS_path))
   
#FIXME: change for win32 
def createShortcut(sink_path):
    '''
    '''
    if sink_path[-1] == '/':
        sink_path = sink_path[:-1]
    sink_path = sink_path + '\Main.pyw'
    if os.path.exists(sink_path):
        print("ERROR: {} already exists...".format(sink_path))
        sys.exit()    

    proc = subprocess.Popen(["which python3"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    pypath = str(out)[2:-3]
    if not pypath:
        print("ERROR: unable to find python3 path...")
        print("Make sure you have python3.x installed")
        sys.exit()
    
    src_path = os.path.dirname(os.getcwd()) + '/GUI/Main.pyw'
    os.system('chmod +x {}'.format(src_path))
    os.system("sed -i -e '1i#! {}\' {}".format(pypath, src_path))
    os.symlink(src_path, '{}'.format(sink_path))
     


#FIXME: change for win32 
def buildACISSRepo(usrname, pswd, ACISS_path):
    '''
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
        dirTransfer(sftp, '../pipe', './')
        dirTransfer(sftp, '../PBS', './')
        dirTransfer(sftp, './', './', ['setup.py'])
        sftp.close()
    except Exception as e:
        print("UNABLE TO CONNECT TO ACISS: ", e)
    sftp.close()
    transport.close()




#FIXME: change for win32 
def dirTransfer(trans_sftp, src_dir, sink_dir, file_excludes=[]):
    '''
    '''
    if src_dir[-1] == '/':
        src_dir = src_dir[:-1]
    if sink_dir[-1] == '/':
        sink_dir = sink_dir[:-1]
    
    for root, dirs, files in os.walk(src_dir):
        for dr in dirs:
            src_path  = os.path.join(root, dr)
            sink_path  = src_path.replace(src_dir, sink_dir) 
            trans_sftp.mkdir(sink_path)
        if file_excludes:
            for f in files:
                if f not in file_excludes:
                    src_path  = os.path.join(root, f)
                    sink_path  = src_path.replace(src_dir, sink_dir) 
                    trans_sftp.put(src_path, sink_path)
        else:
            for f in files:
                src_path  = os.path.join(root, f)
                sink_path  = src_path.replace(src_dir, sink_dir) 
                trans_sftp.put(src_path, sink_path)


def windowsInstall(usrname, pswd, ACISS_path, local_path):
    '''
    '''
    addPath(ACISS_path)
    buildACISSRepo(usrname, pswd, ACISS_path)
    #createShortcut(local_path)

if __name__ == "__main__":
    '''
    '''
    parser = argparse.ArgumentParser("Setup for Vince's pipeline")
    #parser.add_argument('usrname', type=str)
    #parser.add_argument('pswd', type=str, default='')
    #args = parser.parse_args()
    #usrname = args.usrname
    #pswd = args.pswd 
    #buildACISSRepo(usrname, , 'myPipe')
    #createShortcut('/home/alister')
    #addPath("{/my/new/path/}")
    #install(usrname, pswd, "MyInstall", None)
    createShortcut('/home/alister/Desktop')


