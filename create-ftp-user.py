#!/bin/python3

import argparse
import getpass
import os
import pwd
import subprocess
import sys


def check_dir(directory):
    # Check if user's home directory exists. 
    print(directory)
    dir_exists = os.path.isdir(directory)

    if dir_exists:
        return True
    else:
        return False


def create_dir(username, write):
    # Create user's home directory.
    home_dir = "/srv/ftp/" + username
    upload_dir = home_dir + "/upload"
    dir_exists = check_dir(home_dir)
    
    if dir_exists:
        print("Directory already exists.")
    else:
        print("Creating directory.")
        subprocess.run(['mkdir', '-p', home_dir])
        subprocess.run(['chown', '-R', username + ':sftpusers', home_dir])
    
    if write:
        upload_exists = check_dir(upload_dir)

        if upload_exists:
            print("Upload directory exists.")
        else:
            print("Creating upload directory")
            subprocess.run(['mkdir', '-p', upload_dir])
            subprocess.run(['chown', '-R', username + ':sftpusers', upload_dir])


def check_user(username):
    # Check if username already exists.
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def create_user(username, write):
    # Create new user.
    user_exists = check_user(username)

    if user_exists:
        print("User " + username + " already exists.")
    else:
        print("Creating user " + username + "...")        
        password = getpass.getpass()

        if write:
            create_dir(username, write)
        else:
            create_dir(username, write)
            subprocess.run(['useradd', '-g', 'sftpusers', '-s', '/sbin/nologin', '-m', '-d', '/srv/ftp/' + username, username, '-p', password])


def main():
    # Create parser and parse arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username")
    parser.add_argument("-w", "--write", action="store_true", help="Grants write access.")
    args = parser.parse_args()

    create_user(args.username, args.write)


if __name__ == "__main__":
    main()
    sys.exit()
