import os
import hashlib

def CalculateChecksum(path, BlockSize = 1024):

    Fobj = open(path,"rb")

    Hobj = hashlib.md5()

    buffer = Fobj.read(BlockSize)
    while (len(buffer) > 0):
        Hobj.update(buffer)
        buffer = Fobj.read(BlockSize)

    Fobj.close()

    return Hobj.hexdigest()


def DirectoryWatcher(DirectoryName = "Demo"):

    flag = os.path.isabs(DirectoryName)
    if (flag == False):
        DirectoryName = os.path.abspath(DirectoryName)

    flag = os.path.exists(DirectoryName)
    if (flag == False):
        print("Invalid path")
        exit()

    flag = os.path.isdir(DirectoryName)
    if (flag == False):
        print("The path is valid but the target is not the directory")
        exit()

    for FolderName, SubFolders, FileNames in os.walk(DirectoryName):
        for fname in FileNames:
            fname = os.path.join(FolderName, fname)
            checksum = CalculateChecksum(fname)
            print("File Name is ",fname )
            print("Checksum is : ",checksum)

def main():

    DirectoryWatcher()

if __name__ == "__main__":
    main()