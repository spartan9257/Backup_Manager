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
#"C:\\Users\\cftbr\\Desktop\\test_folder\\"
max_backups = 13
backups_dir = "B:\\DC-Backup\\" 
backup_folder_name = "WindowsImageBackup"

#Create and remove a temp file to update the original backup's parent folder last modified time
tmp_file = backups_dir + backup_folder_name + "\\tmp.txt"
print("Updating " + backup_folder_name + "'s last modified time", end='')
try:
    file = open(tmp_file, "x")
    file.close()
    os.system("del " + tmp_file)
except:
    os.system("del " + tmp_file)
print("...COMPLETE")
    
#Switch to the backups directory and get a list of all the backups in newest to oldest order.
print("Getting list of backups", end="")
backup_list = check_output("dir /OD /AD /B " + backups_dir, shell=True).decode().replace("\r", "", 999).split("\n")
backup_list.pop()
print("...COMPLETE")
print("\nBackups found: ")
for name in backup_list:
    print(name)
print("")

#Use date to create archive folder for the backup
current_date = check_output("date /T", shell=True).decode()
folder_name = str(current_date[4:current_date.find("\n") -2 ]).replace("/","-")
print("Creating backup archive folder", end='')
os.system("mkdir " + backups_dir + folder_name)
print("...COMPLETE")

#Create the new backup copy and set it to ready only
print("Creating backup", end='')
os.system("xcopy /E /I /H /V /K /Y " + backups_dir + '"' + backup_list[-1] + '" ' + backups_dir + folder_name)
print("...COMPLETE")
print("Setting all sub-directories and files to read-only", end='')
os.system("attrib /S /D +R " + backups_dir + backup_list[-1] + "\\*") 
print("...COMPLETE")

#Update the backups list with with the new backup. If the backups exceed max limit, delete the oldest one.
print("Updating the backups list", end='')
backup_list = check_output("dir /OD /B " + backups_dir, shell=True).decode().replace("\r", "", 999).split("\n")
backup_list.pop()
print("...COMPLETE")
if len(backup_list) >= max_backups and backup_list[0] != "WindowsImageBackup":
    #delete_count = len(backup_list) - max_backups
    print("Maximum backups exceeded, deleting the oldest archive [" + backup_list[0] + "]", end='')
    os.system("rmdir /S /Q " + backups_dir + backup_list[0])
    print("...COMPLETE")
    