import datetime # For datetime objects
import subprocess # For executing a shell command
from time import sleep # For sleep()
import sys # For sys.argv, sys.exit()

from objects import MyFile # For MyFile objects

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    # Read stdout from subprocess until the buffer is empty !
    for line in iter(p.stdout.readline, b''):
        line = line.decode('utf-8')[:-1]
        if line: # Don't print blank lines
            yield line
    # This ensures the process has completed, AND sets the 'returncode' attr
    while p.poll() is None:                                                                                                                                        
        sleep(.1) #Don't waste CPU-cycles
    # Empty STDERR buffer
    err = p.stderr.read()
    if p.returncode != 0:
       # The run_command() function is responsible for logging STDERR 
       print("Error: " + str(err))

def getFilesFromFolder(baseFolder):
    output = run_command("rclone lsl "+baseFolder)
    files = {MyFile(" ".join(parts[3:]), parts[0], datetime.datetime.strptime((parts[1]+" "+parts[2])[:-3], '%Y-%m-%d %H:%M:%S.%f'))
             for line in output if line.strip()
             for parts in [line.split()]}
    return files