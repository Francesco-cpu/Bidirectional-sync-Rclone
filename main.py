import sys # For sys.argv, sys.exit()
import threading 

from functions import run_command, getFilesFromFolder
from objects import MyFile

listLocal =[]
listRemote =[]

def listLocalFiles():
    global listLocal
    listLocal = getFilesFromFolder(baseFolderLocal)

def listRemoteFiles():
    global listRemote
    listRemote = getFilesFromFolder(baseFolderRemote)


if len(sys.argv) > 2:
    baseFolderLocal = sys.argv[1]
    baseFolderRemote = sys.argv[2]
else:
    print("Usage: python main.py <local folder> <remote folder>")
    sys.exit(1)

x = threading.Thread(target=listLocalFiles)

y= threading.Thread(target=listRemoteFiles)
x.start()
y.start()

x.join()
y.join()

print(len(listLocal))

print(len(listRemote))

listLocal = [file for file in listLocal if file not in listRemote]
listRemote = [file for file in listRemote if file not in listLocal]

print(len(listLocal))

print(len(listRemote))