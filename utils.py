from ftplib import FTP, FTP_TLS

#parse ftp command
def parseCommand(command: str, ftp: FTP or FTP_TLS) -> None:
    allCommands = ["help", "put", "get", "ls", "dir", "rm", "rmdir", "size", "cd", "pwd", "mkdir", "rename", "exit"]

    resp = ""
    x=1

    if command == "help":
        for cmd in allCommands:
            print(cmd, end="\t")

    elif command.startswith("put"):
        name = command[4:]
        file = open(name, "rb")
        resp = ftp.storbinary(f"STOR {name}", file)
        file.close()

    elif command.startswith("get"):
        name = command[4:]
        file = open(name, "wb")
        resp = ftp.retrbinary(f"RETR {name}", file.write, 1024)
        file.close()

    elif command == "ls" or command == "dir":
        ftp.dir()
        x=0

    elif command.startswith("ls") or command.startswith("dir"):
        ftp.dir(command.replace("ls ", "").replace("dir ", ""))
        x=0

    elif command.startswith("rm"):
        resp = ftp.delete(command[3:])

    elif command.startswith("rmdir"):
        resp = ftp.rmd(command[6:])

    elif command.startswith("size"):
        resp = ftp.size(command[5:])

    elif command.startswith("cd"):
        resp = ftp.cwd(command[3:])

    elif command == "pwd":
        resp = ftp.pwd()

    elif command.startswith("mkdir"):
        resp = ftp.mkd(command[6:])

    elif command.startswith("rename"):
        name = command.split(" ")
        if len(name) < 3:
            resp = "Rename needs two arguments"
        else:
            resp = ftp.rename(name[1], name[2])

    elif command == "exit":
        print(ftp.close())
        exit(0)

    else:
        resp = "Command not found"

    if x:
        print(resp)
