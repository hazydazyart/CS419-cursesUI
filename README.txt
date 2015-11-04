README.txt

Instructions for VM install and usage.

CS419 Curses Database Project in Python

1.	Download "CS419-cursesUI" from https://github.com/megaconle/CS419-cursesUI.
2.	Unzip "CS419-cursesUI-master.zip" to desired Directory.
3.	Download and install Oracle VirtualBox then Vagrant
4.	Open Terminal or command line.
5.	Navigate to directory (CS419-cursesUI-master) in Terminal or command line that contains the Vagrantfile and bootstrap.sh
6.	Type, "vagrant up" will boot up the VM and install dependencies
		Dependencies: 
			Vagrantfile
			bootstrap.sh
7.	Setup takes about 5 mins if it is the first time.
8.	After install completes, ssh into the VM from Terminal or open VirtualBox.

*Opening in VirtualBox*

9.	In VirtualBox, select the VM from the panel on the left, then click the "Show" button above.
10.	From there you can log into the VM and interact with it.

*Closing session*

11.	To end the session, type "vagrant destroy" to free up the RAM being used by the VM