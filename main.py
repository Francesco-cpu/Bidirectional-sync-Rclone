import sys
import multiprocessing
import argparse

from functions import run_command, getFilesFromFolder
from objects import MyFile

def listLocalFiles(queue, excludePatterns=None, verbose=False):
    if verbose:
        print("Listing local files...")
    files = getFilesFromFolder(baseFolderLocal, excludePatterns, verbose)
    queue.put(files)
    if verbose:
        print("Local files listed.")

def listRemoteFiles(queue, excludePatterns=None, verbose=False):
    if verbose:
        print("Listing remote files...")
    files = getFilesFromFolder(baseFolderRemote, excludePatterns, verbose)
    queue.put(files)
    if verbose:
        print("Remote files listed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List files in local and remote folders.')
    parser.add_argument('local_folder', help='Path to local folder')
    parser.add_argument('remote_folder', help='Path to remote folder')
    parser.add_argument('--exclude-from-local', nargs='*',help='Exclude patterns for local folder as a list of strings separated by spaces')
    parser.add_argument('--exclude-from-remote', nargs='*',help='Exclude patterns for remote folder as a list of strings separated by spaces')
    parser.add_argument('-v','--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    baseFolderLocal = args.local_folder
    baseFolderRemote = args.remote_folder
    excludeFileLocal = args.exclude_from_local
    excludeFileRemote = args.exclude_from_remote
    verbose = args.verbose

    local_queue = multiprocessing.Queue()
    remote_queue = multiprocessing.Queue()

    x = multiprocessing.Process(target=listLocalFiles, args=(local_queue, excludeFileLocal, verbose))
    y = multiprocessing.Process(target=listRemoteFiles, args=(remote_queue, excludeFileRemote, verbose))

    x.start()
    y.start()

    listLocal = local_queue.get()
    listRemote = remote_queue.get()

    x.join()
    y.join()

    if verbose:
        print("Local files:")
        for file in listLocal:
            print(file)
        print("Remote files:")
        for file in listRemote:
            print(file)

    print(len(listLocal))
    print(len(listRemote))

    listLocalPurged = listLocal - listRemote
    listRemote -= listLocal
    listLocal = listLocalPurged

    print(len(listLocal))
    print(len(listRemote))