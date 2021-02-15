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

max_backups = 4
backups_dir = "C:\\Users\\cftbr\\Desktop\\test_folder\\"
backup_new_backup_name = "WindowsImageBackup"

#Create and remove a temp file to update the original backup's parent folder last modified time
try:
    tmp_file = backups_dir + backup_new_backup_name + "\\tmp.txt"
    print("Updating " + backup_new_backup_name + "'s last modified time", end='')
    file = open(tmp_file, "x")
    file.close()
    os.system("del " + tmp_file)
    print("...COMPLETE")
except:
    os.system("del " + tmp_file)
    
#Switch to the backups directory and get a list of all the backups in newest to oldest order.
try:
    print("Getting list of backups", end="")
    backup_list = check_output("dir /OD /B " + backups_dir, shell=True).decode().replace("\r", "", 999).split("\n")
    backup_list.pop()
    print("...COMPLETE")
    
    print("\nBackups found: ")
    for name in backup_list:
        print(name)
    print("")
except:
    print("ERROR: Unable to get list of backups!")

#Use date to create archive folder for the backup
try:
    current_date = check_output("date /T", shell=True).decode()
    new_backup_name = backups_dir + str(current_date[4:current_date.find("\n") -2 ]).replace("/","-")
    print("Creating new backup folder", end='')
    os.system("mkdir " + new_backup_name)
    print("...COMPLETE")
except:
    print("ERROR: Unable to create new backup folder!")

#Create the new backup copy and set it to ready only
try:
    print("Creating backup", end='')
    os.system("xcopy /E /I /H /V /K /Y " + backups_dir + '"' + backup_list[-1] + '" ' + new_backup_name)
    print("...COMPLETE")
    
    print("Setting all sub-directories and files to read-only", end='')
    os.system("attrib /S /D +R " + backups_dir + backup_list[-1] + "\\*") 
    print("...COMPLETE")
except:
    print("ERROR: Unable to create backup!")
 
#Create a compressed copy of the new backup 
try:
    print("Compressing backup...", end="")
    os.system("tar -czvf " + new_backup_name + ".tar.gz " + new_backup_name)
    print("...COMPLETE")
    
    print("Removing uncompressed backup...", end="")
    os.system("rmdir /S /Q " + new_backup_name)
    print("...COMPLETE")
    
    print("Setting compressed backup to read-only", end='')
    os.system("attrib /S /D +R " + new_backup_name + ".tar.gz")
    print("...COMPLETE")
except:
    print("ERROR: compression unsuccessful!")

#Update the backups list with with the new backup
print("Updating the backups list", end='')
backup_list = check_output("dir /OD /B " + backups_dir, shell=True).decode().replace("\r", "", 999).split("\n")
backup_list.pop()
print("...COMPLETE")
print("\nBackups found: ")
for name in backup_list:
    print(name)
print("")

#If the backups exceed max limit, delete the oldest one
if len(backup_list) >= max_backups and backup_list[0] != "WindowsImageBackup":
    print("Maximum backups exceeded, deleting the oldest archive [" + backup_list[0] + "]", end='')
    os.system("del /S /Q " + backups_dir + backup_list[0])
    print("...COMPLETE")
    