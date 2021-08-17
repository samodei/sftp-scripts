#!/bin/python3

import argparse
import getpass
import os
import pwd
import subprocess
import sys


def check_dir(directory):
    # Check if directory exists.
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
    
    if not dir_exists:
        # This will probably never run since useradd will create the home directory.
        print("Creating " + home_dir + "...\n")
        subprocess.run(['mkdir', '-p', home_dir])
        
    # Change home_dir owner to root.
    subprocess.run(['chown', '-R', 'root:sftpusers', home_dir])
    
    # Create upload directory if granting write access.
    if write:
        upload_exists = check_dir(upload_dir)

        if upload_exists:
            print(upload_dir + " already exists...\n")
            subprocess.run(['chown', '-R', username + ':sftpusers', upload_dir])
        else:
            # Create upload_dir and change owner to that user.
            print("Creating " + upload_dir + "...\n")
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
        print("User " + username + " already exists.\n")
    else:
        print("Creating user " + username + "...\n")        
        password = getpass.getpass()

        dir_exists = check_dir("/srv/ftp/" + username)

        if dir_exists:
            print("Directory /srv/ftp/" + username + " already exists.\n")
        else:
            # Create user.
            subprocess.run(['useradd', '-g', 'sftpusers', '-s', '/sbin/nologin', 
                '-m', '-d', '/srv/ftp/' + username, username, '-p', password])

            # Create necessary directories.
            create_dir(username, write)

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
