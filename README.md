# recover-deleted-files
A python script to recover deleted files from an image disk


==============Please read this guide before using the script=============

Tried with Windows system but it is harder to work with so I changed to OS X.


===Before using the script===

1. Install Sleuthkit on Mac OSX:
	a. Press Command+Space and type Terminal and press enter/return key.
		Run in Terminal app:

			ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null
		
		and press enter/return key. 

	b. If the screen prompts you to enter a password, please enter your Mac's user password to continue. When you type the password, 	it won't be displayed on screen, but the system would accept it. So just type your password and press ENTER/RETURN key. Then wait 	for the command to finish.

	c. Run:
		brew install sleuthkit

2. Use Disk Utility to create a disk image for an internal or external drive (for example. SHARED)

3. Execute the script with the disk image (SHARED.dmg):
	usage: recover.py [-h] [-o [OUTPUT]] [-v] image

	Recover files from a disk image file

	positional arguments:
	  image                 path to disk image or mount point (generally a ".dmg" file)

	optional arguments:
	  -h, --help            show this help message and exit
	  -o [OUTPUT], --output [OUTPUT] recover files to this directory [default=./recovered_files/]
	  -v, --verbose         print progress message while recovering


===Executing the script===

4. Example usage:

MAC: Desktop user$ python recover_deleted_files.py -o -v SHARED.dmg



5. Then the script will be executed and try to recover the deleted files in the disk image. 
Then put them in the "recovered_files" folder on Desktop


6. Results will also be printed out on the Terminal.app, stating which file is successfully recovered/skipped/failed to recover.
