import os
from subprocess import check_output
from os import path

'''
The purpose of this script is to automate the management of windows backups on a local drive. The script will
get a list of the backups, create a copy of the newest one, set it's contents to read-only, then delete the oldest
backup if the maximum threshhold has been exceeded. Refer to the read me for more details.

TODO: figure oout how to incorporate multithreading to speed up compression
'''

max_backups = 4
backups_dir = "C:\\Users\\cftbr\\Desktop\\test_folder\\"
backup_folder_name = "WindowsImageBackup"
compress_archive = True

#Create and remove a temp file to update the backup's [parent folder] last modified time
try:
    tmp_file = backups_dir + backup_folder_name + "\\tmp.txt"
    print("Updating " + backup_folder_name + "'s last modified time", end='')
    file = open(tmp_file, "x")
    file.close()
    os.system("del " + tmp_file)
    print("...COMPLETE")
except:
    os.system("del " + tmp_file)
    
#Get a list of all the archived backups (old to new)
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

#Get the date and format it MM-DD-YYYY
current_date = check_output("date /T", shell=True).decode()
new_backup_name = backups_dir + str(current_date[4:current_date.find("\n") -2 ]).replace("/","-")

#Create and compress archived copy, set it to read-only
if compress_archive:
    try:      
        print("Creating backup...", end="")
        os.system("tar -czvf " + new_backup_name + ".tar.gz " + backups_dir + backup_list[-1])
        os.system("attrib /S /D +R " + new_backup_name + ".tar.gz")
        print("...COMPLETE")
    except:
        print("ERROR: Unable to create backup!")
        
#Create an uncompredded backup 
else:
    try:
        print("Creating backup", end='')
        os.system("mkdir " + new_backup_name)
        
        os.system("xcopy /E /I /H /V /K /Y " + backups_dir + '"' + backup_list[-1] + '" ' + new_backup_name)
        print("...COMPLETE")
        
        print("Setting all sub-directories and files to read-only", end='')
        os.system("attrib /S /D +R " + backups_dir + backup_list[-1] + "\\*") 
        print("...COMPLETE")
    except:
        print("ERROR: Unable to create backup!")
        
 

#Update the backups list to include the new archived backup (old to new)
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
    print("Maximum backups exceeded, deleting the oldest archive [" + backup_list[0] + "]", end="")
    os.system("attrib -R " + backups_dir + backup_list[0])
    os.system("del /S /Q " + backups_dir + backup_list[0])
    if path.exists(backups_dir + backup_list[0]):
        print("\nERROR: Unable to remove archive!")
    else:
        print("...COMPLETE")
    