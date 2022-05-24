import ftplib
import sys
import argparse
from ftplib import FTP, FTP_TLS
from utils import *


def main() -> None:
    #get flags
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--anon-login",
        action="store_true",
        dest="anonLogin",
        help="connecting to the server using anonymous login",
    )
    parser.add_argument(
        "--ftps",
        action="store_true",
        dest="ftps",
        help="connecting to the server using FTPS",
    )
    parser.add_argument(
        "-s", "--server",
        dest="server",
        help="set server",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-t", "--timeout",
        dest="timeout",
        help="set timeout connection in seconds",
        type=float,
    )
    parser.add_argument(
        "-p", "--port",
        dest="port",
        help="set ftp server port, default 21",
        default=21,
        type=int,
    )

    args = parser.parse_args()

    #get ftp
    ftp = 0
    if args.ftps:
        ftp = FTP_TLS()
    else:
        ftp = FTP()

    #connect to the server
    try:
        resp = ftp.connect(host=args.server, port=args.port, timeout=args.timeout)
        print(resp)
    except Exception as err:
        print(f"ERROR: {err}")
        exit(1)


    #login to ftp server
    try:
        if args.anonLogin:
            resp = ftp.login()
        else:
            username = input("Enter username: ")
            password = input("Enter password: ")
            resp = ftp.login(username, password)
    except ftplib.all_errors as err:
        print(err)
        exit(0)

    while 1:
        cmd = input("ftp> ")
        try:
            parseCommand(cmd, ftp)
        except ftplib.all_errors as err:
            print(err)
        except KeyboardInterrupt:
            ftp.close()
            exit(0)


if __name__ == "__main__":
    main()