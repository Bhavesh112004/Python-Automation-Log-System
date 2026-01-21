import hashlib
import os
import sys
import time

def CalculateChecksum(path, Blocksize=1024):
    Fobj = open(path, "rb")
    Hobj = hashlib.md5()

    buffer = Fobj.read(Blocksize)
    while len(buffer) > 0:
        Hobj.update(buffer)
        buffer = Fobj.read(Blocksize)

    Fobj.close()
    return Hobj.hexdigest()

def FindDuplicate(DirectoryName="Demo"):
    flag = os.path.isabs(DirectoryName)
    if flag == False:
        DirectoryName = os.path.abspath(DirectoryName)

    flag = os.path.exists(DirectoryName)
    if flag == False:
        print("Invalid path")
        exit()

    flag = os.path.isdir(DirectoryName)
    if flag == False:
        print("Path is valid but the target is not the directory")
        exit()

    Duplicate = {}

    for FolderName, SubFolders, FileNames in os.walk(DirectoryName):
        for fname in FileNames:
            fname = os.path.join(FolderName, fname)
            checksum = CalculateChecksum(fname)

            if checksum in Duplicate:
                Duplicate[checksum].append(fname)
            else:
                Duplicate[checksum] = [fname]

    return Duplicate

def DirectoryWatcher(DirectoryName="Demo"):
    flag = os.path.isabs(DirectoryName)
    if flag == False:
        DirectoryName = os.path.abspath(DirectoryName)

    flag = os.path.exists(DirectoryName)
    if flag == False:
        print("The path is invalid")
        exit()

    flag = os.path.isdir(DirectoryName)
    if flag == False:
        print("Path is valid but the target is not a directory")
        exit()

    timestamp = time.ctime()
    filename = "Log%s.txt" % timestamp
    filename = filename.replace(" ", "_").replace(":", "_")

    fobj = open(filename, "w")
    Border = "-" * 60

    fobj.write(Border + "\n")
    fobj.write("This is the log file for the finding duplicate script\n")
    fobj.write("Directory scanned: " + DirectoryName + "\n")
    fobj.write("Created at: " + timestamp + "\n")
    fobj.write(Border + "\n\n")

    for FolderName, SubFolderNames, FileNames in os.walk(DirectoryName):
        for fname in FileNames:
            full_path = os.path.join(FolderName, fname)
            checksum = CalculateChecksum(full_path)
            #fobj.write(f"File: {full_path}\nChecksum: {checksum}\n\n")

    # Find and write duplicate files
    fobj.write(Border + "\n")
    fobj.write("Duplicate Files:\n")
    fobj.write(Border + "\n")

    duplicates = FindDuplicate(DirectoryName)
    found = False
    for checksum, files in duplicates.items():
        if len(files) > 1:
            found = True
            fobj.write(f"\nChecksum: {checksum}\n")
            for file in files:
                fobj.write(f"  {file}\n")

    if not found:
        fobj.write("No duplicate files found.\n")

    fobj.write("\n" + Border + "\n")
    fobj.close()
    print(f"Log file created: {filename}")

def main():
    Border = "-" * 90
    print(Border)
    print("-----------------------------------Marvellous Infosysytem--------------------------------------")
    print(Border)

    if len(sys.argv) == 2:
        if sys.argv[1] == "--h" or sys.argv[1] == "--H":
            print("This script is to find the duplicate files in a directory")
            print("This is the FindDuplicate Automation Script")

        elif sys.argv[1] == "--u" or sys.argv[1] == "--U":
            print("Use the given script as: ")
            print("Script_Name.py NameofDirectory")
            print("Please provide valid absolute path")

        else:
            DirectoryWatcher(sys.argv[1])

    else:
        print("Invalid number of command line arguments")
        print("use --h or --H to display help")
        print("use --u or --U to display usage")

    print(Border)
    print("----------------------Thank you for using our script---------------------")
    print("-------------------------Marvellous Infosysytem-------------------------")
    print(Border)

if __name__ == "__main__":
    main()
