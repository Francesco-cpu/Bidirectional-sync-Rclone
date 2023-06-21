import sys # For sys.argv, sys.exit()

from functions import run_command, getFilesFromFolder
from objects import MyFile





if len(sys.argv) > 2:
    baseFolderLocal = sys.argv[1]
    baseFolderRemote = sys.argv[2]
else:
    print("Usage: python main.py <local folder> <remote folder>")
    sys.exit(1)


listLocal = getFilesFromFolder(baseFolderLocal)
print(len(listLocal))

listRemote = getFilesFromFolder(baseFolderRemote)
print(len(listRemote))
