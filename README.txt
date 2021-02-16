Backup Manager for windows image backups

The goal of this script is to automate the management of windows server backups stored on a local drive. The script makes a copy of the most recent the WindowsImageBackup folder and renames the copy to prevent the next backup from saving over it. Windows server 2016 (and below) doesn't offer many options in regards to how it can store its backups. In this case we have a network drive hosted on a PC that also has the google drive backup and sync application installed. When the server sends it's backup to the network drive it saves it to the folder "WindowsImageBackup",  if a backup was already created, it's over written. This of course limits us to just a single backup by default. 

The script is responsible for creating a new folder or compressed file and copying the contents of the most recent backup to it. This allows multiple backups to exist on the same local drive. Additionally the new backup and all of its contents will be set to read-only and optionally compressed using tar. To prevent storage exhaustion the script also checks how many backups exist, if it exceeds a predefined threshold the oldest backup will be deleted.

The script is ran using windows task scheduler.

The script performs 4 tasks:

1. It gets the path to the backups directory, then gets a list of all of the files, the compressed backups, within. The list is formated and organized into oldest to newest order. Note that the variable backups_dir will need to be changed to match the path to the correct directory. I plan on changing how this works in the future.

2. Gets the current date and formats it using MM-DD-YYYY, then creates a new folder within the backups directory using the date as the name. 

3. When creating the backup there's two options to choose from; uncompressed and compressed. Which option you choose will largely be dependant on the system that the script is ran on and the size of the backup. A system that's CPU limited will likely struggle with compressing large files. To choose one of the two options set compress_archive to True or False. The result of both options is set to read-only.
	-Uncompression: xcopy is used to create a one to one copy of the backup.
	-Compressed: tar gz is used to create a tarball off the entire backup.

4. The backups list is updated to include the newly created backup and the total number of backups is checked to see if the maximum backups threshold is being violated. You can define the limit by adjusting the value assigned to max_backups. NOTE: you will need to ensure that the total drive space is equal or greater than (max_backups + 1 * backupsize). This is to account for there being an additional backup momentarily exceeding the max limit, just before it's deleted. If the limit is exceeded the oldest backup is deleted.