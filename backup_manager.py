import os
from subprocess import check_output

'''
The purpose of this script is to automate the management of windows backups on a local drive. The script will
get a list of the backups, create a copy of the newest one, set it's contents to read-only, then delete the oldest
backup if the maximum threshhold has been exceeded. Refer to the read me for more details.

TODO: Compress the backups
    tar -cf uncompressed compressed.gzip #Compress dir
    tar -xvf compressed.gzip             #Uncompress dir
'''

max_backups = 12
backups_dir = "backup_manager\\"

#Switch to the backups directory and get a list of all the backups in newest to oldest order.
backup_list = check_output("dir /OD /B " + backups_dir, shell=True).decode().replace("\r", "", 999).split("\n")
backup_list.pop()

#Get the current date and use it to create a new folder that will be used to store the copy 
#of the most recent backup.
current_date = check_output("date /T", shell=True).decode()
folder_name = str(current_date[4:current_date.find("\n") -2 ]).replace("/","-")
os.system("mkdir " + backups_dir + folder_name)

#Create the new backup copy and set it to ready only
os.system("xcopy /E /I /H /V /K /Y " + backups_dir + '"' + backup_list[-1] + '" ' + backups_dir + folder_name)
os.system("attrib /S /D +R " + backups_dir + backup_list[-1] + "\\*") 

#Update the backups list with to include the newly created backup. If the backups exceed a 
#predefined threshhold, delete the oldest one.
backup_list = check_output("dir /OD /B " + backups_dir, shell=True).decode().replace("\r", "", 999).split("\n")
backup_list.pop()
if len(backup_list) >= max_backups and backup_list[0] != "WindowsImageBackup":
    os.system("rmdir /S /Q " + backups_dir + backup_list[0])
    