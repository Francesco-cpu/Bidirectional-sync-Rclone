import datetime
import os # For datetime objects and os.path.basename()
import subprocess # For executing a shell command
from time import sleep # For sleep()
import sys # For sys.argv, sys.exit()

import fnmatch # For fnmatch.fnmatch()

from objects import MyFile # For MyFile objects

# Runs a shell command and returns the output line by line
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

# Returns a set of MyFile objects representing the files in the baseFolder
def getFilesFromFolder(baseFolder, excludePatterns=None, excludeIfPresent=None, verbose=False):
    if verbose:
        print(f"Listing files in {baseFolder}...")
    if excludeIfPresent is not None:
        excluding = ""
        for pattern in excludeIfPresent:
            excluding += f" --exclude-if-present \"{pattern}\""
        cmd = f"rclone lsl \"{baseFolder}\" {excluding}"
        # output = run_command(f"rclone lsl \"{baseFolder}\" --exclude-if-present \"{excludeIfPresent}\"")
    else:
        cmd = f"rclone lsl \"{baseFolder}\""
    print(cmd)
    output = run_command(cmd)
        # output = run_command(f"rclone lsl \"{baseFolder}\"")
    files = {MyFile(" ".join(parts[3:]), parts[0], datetime.datetime.strptime((parts[1]+" "+parts[2])[:-3], '%Y-%m-%d %H:%M:%S.%f'))
             for line in output if line.strip()
             for parts in [line.split()]
             if excludePatterns is None or shouldIncludeFile(baseFolder, MyFile(" ".join(parts[3:]), parts[0], datetime.datetime.strptime((parts[1]+" "+parts[2])[:-3], '%Y-%m-%d %H:%M:%S.%f')), excludePatterns, excludeIfPresent, verbose)}
    if verbose:
        print(f"{len(files)} files listed in {baseFolder}.")
    return files


# Returns True if the file should be included, False otherwise, based on the excludePatterns
def shouldIncludeFile(baseFolder, file, excludePatterns, excludeIfPresent=None, verbose=False):
    # Check if the file matches any of the excludePatterns
    for pattern in excludePatterns:
        if fnmatch.fnmatch(file.name, pattern):
            if verbose:
                print(f"Excluding file {file.name} because it matches pattern {pattern}")
            return False
    return True

