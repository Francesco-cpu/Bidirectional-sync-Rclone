import sys
import multiprocessing
import argparse

from functions import run_command, getFilesFromFolder
from objects import MyFile

def listLocalFiles(queue, excludePatterns=None):
    files = getFilesFromFolder(baseFolderLocal, excludePatterns)
    queue.put(files)

def listRemoteFiles(queue, excludePatterns=None):
    files = getFilesFromFolder(baseFolderRemote, excludePatterns)
    queue.put(files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List files in local and remote folders.')
    parser.add_argument('local_folder', help='Path to local folder')
    parser.add_argument('remote_folder', help='Path to remote folder')
    parser.add_argument('--exclude-from-local', nargs='*',help='Path to file containing exclude patterns for local folder')
    parser.add_argument('--exclude-from-remote', nargs='*',help='Path to file containing exclude patterns for remote folder')
    args = parser.parse_args()

    baseFolderLocal = args.local_folder
    baseFolderRemote = args.remote_folder
    excludeFileLocal = args.exclude_from_local
    excludeFileRemote = args.exclude_from_remote

    local_queue = multiprocessing.Queue()
    remote_queue = multiprocessing.Queue()

    x = multiprocessing.Process(target=listLocalFiles, args=(local_queue, excludeFileLocal))
    y = multiprocessing.Process(target=listRemoteFiles, args=(remote_queue, excludeFileRemote))

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