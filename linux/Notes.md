# Linux for Absolute Beginners!
## Get started with Linux, app development, server configuration, networking, and become a system administrator!
## https://www.udemy.com/course/linux-system-admin/

# Section 1 - Introduction to Linux
GNU libary/Linux OS
	-> debian (one of first major distros) - stable, sporadic release
		-> ubuntu - stable, often releases

*tutorial suggests using ubuntu + virtualbox, but will run on docker instead*
- docker run -t -i ubuntu

# Section 2 - Distributions explained
... Ubuntu Linux Installation (skipped)

# Secion 3 - Linux Command Line Interface (CLI) Essentials
- print working dir: pwd
- change directory: cd
- cd into absolute directory (i.e. from root, /): cd /path
- cd into relative directory (i.e. from folder in): cd path
- 	or from current directory: cd ./path
- cd to home: cd ~
- 	can use cd ~/path
- cd up one level: cd ../

- list contents of folder: ls
- list contents long: ls -l
-	left colum are the persmissions of the file, owner user account and their group
-	-drwxrwxr 1 user group
- list contents in reverse: ls -r
- list file/folders by types: ls -p
- list files in path: ls /path

# change permissions

install nano on docker:
- apt-get update
- apt-get install nano
- export TERM=xterm

if persmission denied for file, use
- sudo nano file
which will run command with elevated privileges
- run previous command: sudo !!
if want to use sudo many times, can switch user
- su (user)
- sudo su / su (user)

# package manager

linux package manager
- apt-get

to search:
- apt-cache search package*
is it installed?
- apt-get policy package
to install:
- apt-get install package
to remove:
- apt-get remove package
to install packages NOT from apt
- download file (.deb) from the web
- cd to dir where downloaded
- sudo dpkg -i package_name
to update all installed packages (get newer versions)
- sudo apt-get upgrade

# File permissions and ownership
-rw-r--r--   1 root root    2 Oct 21 14:32 file.txt
				^	 ^
				user group

*change ownsership*
- sudo chown user:group

*change permissions*
*6 readable/writable*
*4 readable*
*7 dir*

- sudo chmod 646 file.txt
-rw-r--rw-   1 ron  root    2 Oct 21 14:32 file.txt

### Remove file
- rm file

### Make dir
- mkdir dir

### remove files in dir from upper folder (keeping dir)
- upper$ rm mydir/*

### remove dir from upper folder
- upper$ rm -rf mydir

### remove specific file types from dir
- rm dir/\*.txt

### remove specific file types from dir
- rm ./dir/*


# Change permissions on folder
- chown -R user:group ./dir (use -R for recursive - also changes permissions on files)

$ ls -l
drwxr-xr-x   2 root root 4096 Oct 21 15:13 mydir
$ chown...
drwxr-xr-x   2 ron  ron  4096 Oct 21 15:13 mydir
$ ls -l mydir/
-rw-r--r-- 1 ron ron 0 Oct 21 15:11 file.txt
-rw-r--r-- 1 ron ron 0 Oct 21 15:13 file2.txt

### more utility commans
utility commands - cd, pwd, sudo, chmod, chown, su

### move file
- $ mv file dir/file

### rename dir
mv mydir mydirnewname

### copy file
- $ cp dir/file dir/file

### copy whilst renaming file
cp./dir1/file1 ./dir2/file1newname

### find (recursively)
$ find . -type f -name "\*.php"
find in this folder type of file (d for dirs) with name wildcard.php

$ find . -type f iname "\*.php"
find in this folder type of file with case-insensitive name wildcard.php

$ find . -type f -iname "file\*"
find in this folder type of file with case-insensitive name name.wildcard

### find (non-recursively)
$ find . -maxdepth 1 (other args)

### find files with certain permission
$ find . -type f -perm 0664

### by size
$ find . -size -1M
$ find . -size +1M

### not operator
$ find . -type f -not -iname "\*.php"

# Find things in files with grep
$ grep "string" file
$ grep -i "string" ./\*/\* <- all folders (./dir/ for specific)
       ^case-insensitive
$ grep -n "string" ./\*/\*
       ^ gives line number

$ find . -type f -iname "\*.php" -exec grep -i -n "function" {} +
  ^ for what this finds			 ^ grep this                 ^ end

# re-direct output of command
$ ls > outfile.txt
$ find . -type f -size -10k -exec grep -i -n "\*" {} + > something.txt
$ find . -type f -size -10k -exec grep -i -n "\*" {} + | tee of something.txt 	<- allows you to see what's being outputted in real time

# View processes/applications in real time
$ top
$ ps aux
$ ps aux | grep something 	<- gets all the info of processes specified by grep
$ pgrep 	<- gets the process ids of processes

$ kill -9 (process_id) 	<- kills process
$ killall (process_name)	<- kill multiple

# services
service - special type of linux process

- start service
$ service service_name start
$ service service_name stop
$ service service_name restart
- if using systemctl
$ systemctl start service_name
$ systemctl stop service_name

## scheduled tasks
- install cron

m h dom mon dow		command
^ minute, hour, day-of-month, month-num, day-of-week, command-to-perform

- usage:
15 14 \* \* \* 		ls > home/cronres.txt
	  ^ means not set

- useful jobs:
0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
^ 5am every week   ^ here 				 ^ backup this

*** Keep in mind that cronjobs are user specific - so root cronjobs have different context to a user ***

# Section 5: Linux Development Tools

## GitHub setup
$ apt-get install -y git git-extras

$ git init *initialise*
*create repo on github*
$ git remote origin https://github.com/username/repo.git
$ git config --global user.name "Name"
$ git config --global user.email email
$ git pull
... etc.

## Remove and Ignore dirs in repo

$ git rm -r .directory *remove directory*
$ git-ignore .directory/* *ignore directory and everything inside*

## Resolving merge conflicts

$ git merge
- tells you where the conflict is and add comments to conflicting areas, e.g.

	<<<<<<<<< HEAD
		// This is different
	=========
	    // To this
	>>>>>>>>> refs/remotes/origin/master

- make changes

$ git add .
$ git commit -m "some message that conflict resolved"
$ git push

## Setup and manage branches
...

# Section 6: Web server setup, host configuration and app development

## Apache 2, PHP, MySQL setup

$ apt-get install -y apache2 php5 mysql-server php5-common

