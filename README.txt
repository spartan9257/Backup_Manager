Backup Manager for windows image backups

The goal of this script is to automate the management of windows server backups stored on a local drive. The script makes a copy of the most recent folder, which should be the WindowsImageBackup folder, created by a windows server. Then renames the copy to prevent the server from saving over it. Windows server 2016 (and below) doesn't offer many options in regards to how it can store its backups. In this case we are using a network drive on a PC that also has the google drive backup and sync application installed. When the server sends it's backup to the network drive it saves it to the folder "WindowsImageBackup",  if the folder already exists it's over written. This of course limits us to just a single backup. 

This script is responsible for creating a new directory (using the current date) and copying the contents of the most recent backup to it. This allows multiple backups to exist within the same network drive. additionally the new backup and all of its contents will be set to read-only to provide an extra layer of security. To prevent storage exhaustion the script also checks how many backups exist, if it exceeds the predefined threshold, the oldest backup will be deleted.

The script is run using windows task scheduler.

The script performs 4 tasks:
1. It gets the path to the backups directory, then gets a list of all of the folders (backups) within. The list is organized by oldest to newest and the last item (an empty string) is removed. Note that backups_dir="" (line 15) will need to be changed to match the path to the correct directory.

2. Gets the current date and formats it using MM-DD-YYYY, then creates a new folder within the backups directory using the date as the name. 

3. Using xcopy the entire contents of the most recent folder within the backups directory is copied to the folder created in task 2. The most recent folder should ALWAYS be WindowsImageBackups, to ensure that is true the server will need to be scheduled to backup more frequently than this script is run. Thus ensuring that WindowsImageBackup is always the most recently modified. Additionally the new backup and all of it's content (subdirectories and files) are set to read-only access for added security.

4. The backups list is updated to include the newly created backup. It's then determined whether or not the total backups exceed the predefined limit. You can define the limit by adjusting the value assigned to max_backups in line 14. NOTE: you will need to ensure that the total drive space is equal or greater than (max_backups + 1 * backupsize). This is to account for there being an additional backup, momentarily exceeding the max limit, just before it's deleted. If the limit is exceeded the oldest backup is deleted.
