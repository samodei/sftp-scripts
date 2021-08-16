#!/bin/bash
#Stefano Amodei
#Run with sudo
#This script can be seriously cleaned up but this will work.

if [ "$#" -eq 1 ] ; then
	user=$1

	#Create user, add to sftpusers group, set home, and deny shell access.
	if useradd -g sftpusers -s /sbin/nologin -m /srv/ftp/$user $user ; then
		#Set password.
		if passwd $user ; then
			#Create directories and set permissions.
			#Uncomment if allowing users to upload. Please only have one of the following mkdirs active at a time.
			#mkdir -p /srv/ftp/$user/upload
			#mkdir /srv/ftp/$user
			echo skipping
			#chown -R root:sftpusers /srv/ftp/$user
			#Uncomment if allowing users to upload.
			#chown -R $user:sftpusers /srv/ftp/$user/upload
		fi
	else
		echo "fail"
	fi

else
	echo "Error: Invalid arguments."
	echo -e "Usage: ./create-ftp-user.sh username\n"
fi
