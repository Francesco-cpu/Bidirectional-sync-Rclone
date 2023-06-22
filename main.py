import sys
import multiprocessing

from functions import run_command, getFilesFromFolder
from objects import MyFile

def listLocalFiles(queue):
    files = getFilesFromFolder(baseFolderLocal)
    queue.put(files)

def listRemoteFiles(queue):
    files = getFilesFromFolder(baseFolderRemote)
    queue.put(files)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        baseFolderLocal = sys.argv[1]
        baseFolderRemote = sys.argv[2]
    else:
        print("Usage: python main.py <local folder> <remote folder>")
        sys.exit(1)

    local_queue = multiprocessing.Queue()
    remote_queue = multiprocessing.Queue()

    x = multiprocessing.Process(target=listLocalFiles, args=(local_queue,))
    y = multiprocessing.Process(target=listRemoteFiles, args=(remote_queue,))

    x.start()
    y.start()

    listLocal = local_queue.get()
    listRemote = remote_queue.get()

    x.join()
    y.join()

    print(len(listLocal))
    print(len(listRemote))

    listLocalPurged = listLocal - listRemote
    listRemote -= listLocal
    listLocal = listLocalPurged

    print(len(listLocal))
    print(len(listRemote))