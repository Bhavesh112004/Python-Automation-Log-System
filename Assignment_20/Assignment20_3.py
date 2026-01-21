import os
import sys
import time
import hashlib

def CalculateChecksum(path, BlockSize=1024):
    fobj = open(path, 'rb')
    hobj = hashlib.md5()
    buffer = fobj.read(BlockSize)
    while len(buffer) > 0:
        hobj.update(buffer)
        buffer = fobj.read(BlockSize)
    fobj.close()
    return hobj.hexdigest()

def FindDuplicate(DirectoryName="Marvellous"):
    if not os.path.isabs(DirectoryName):
        DirectoryName = os.path.abspath(DirectoryName)

    if not os.path.exists(DirectoryName):
        print("The path is invalid")
        exit()

    if not os.path.isdir(DirectoryName):
        print("Path is valid but the target is not a directory")
        exit()

    Duplicate = {}
    for FolderName, SubFolderNames, FileNames in os.walk(DirectoryName):
        for fname in FileNames:
            fname = os.path.join(FolderName, fname)
            checksum = CalculateChecksum(fname)
            if checksum in Duplicate:
                Duplicate[checksum].append(fname)
            else:
                Duplicate[checksum] = [fname]

    return Duplicate

def DirectoryWatcher(DirectoryName="Demo"):
    if not os.path.isabs(DirectoryName):
        DirectoryName = os.path.abspath(DirectoryName)

    if not os.path.exists(DirectoryName):
        print("The path is invalid")
        exit()

    if not os.path.isdir(DirectoryName):
        print("Path is valid but the target is not a directory")
        exit()

    timestamp = time.ctime()
    filename = "MarvellousLog%s.log" % (timestamp)
    filename = filename.replace(" ", "_").replace(":", "_")

    
    fobj = open(filename, "w")

    Border = "-" * 54
    fobj.write(Border + "\n")
    fobj.write("This is a log file of Marvellous Automation Script\n")
    fobj.write("This is a Directory Cleaner Script\n")
    fobj.write(Border + "\n")
    fobj.write("Log created at: " + timestamp + "\n")
    fobj.write(Border + "\n\n")

    
    return fobj  
    

def DeleteDuplicate(MyDict, fobj):
    Result = list(filter(lambda x: len(x) > 1, MyDict.values()))

    Count = 0
    Cnt = 0

    fobj.write("Deleted Duplicate Files:\n")
    fobj.write("-" * 54 + "\n")

    for value in Result:
        for subvalue in value:
            Count += 1
            if Count > 1:
                try:
                    os.remove(subvalue)
                    fobj.write(f"{subvalue}\n")
                    print("Deleted file:", subvalue)
                    Cnt += 1
                except Exception as e:
                    fobj.write(f"Failed to delete {subvalue}: {e}\n")
        Count = 0

    fobj.write("-" * 54 + "\n")
    fobj.write(f"Total deleted files: {Cnt}\n")
    fobj.write("-" * 54 + "\n")

def main():
    Border = "-" * 54
    print(Border)
    print("--------------- Marvellous Automation ----------------")
    print(Border)

    if len(sys.argv) == 2:
        if sys.argv[1] in ("--h", "--H"):
            print("This application is used to perform directory cleaning")
            print("This is the directory automation script")

        elif sys.argv[1] in ("--u", "--U"):
            print("Use the given script as:")
            print("ScriptName.py NameOfDirectory")
            print("Please provide a valid absolute path")

        else:
            log_file = DirectoryWatcher(sys.argv[1])  
            Result = FindDuplicate(sys.argv[1])
            DeleteDuplicate(Result, log_file)
            log_file.close()  
    else:
        print("Invalid number of command line arguments")
        print("Use the given flags as:")
        print("--h : Used to display the help")
        print("--u : Used to display the usage")

    print(Border)
    print("----------- Thank you for using our script -----------")
    print("---------------- Marvellous Infosystems --------------")
    print(Border)

if __name__ == "__main__":
    main()
