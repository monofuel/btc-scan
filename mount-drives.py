#!/usr/bin/python3
import os
import subprocess

# script assumes running as root

# list of system drives to not attempt to mount
ignore_drives = ("7a907b0c-4f8a-4350-b2b4-c804abca9622", "ed5b6085-40e0-463e-b2fa-438f6cb9ddcb", "6d406c55-5de8-4401-b2ee-92bd1046520c", "80b7f420-7699-476c-9db1-c0108bb661aa")

def main():
    
    check_disks = [f for f in os.listdir('/dev/disk/by-uuid') if f not in ignore_drives]
    print("drives to mount: ", check_disks)
    try:
        os.mkdir("./mounts")
    except FileExistsError:
        print('./mount exists')
        
    print("cleaning up mounts folder")
    clean_mounts = os.listdir("./mounts")
    for f in clean_mounts:
        subprocess.run('umount ./mounts/{}'.format(f), shell=True)
        subprocess.run("rmdir ./mounts/{}".format(f), shell=True)
        print('unmounted ' + f)

    mounts = subprocess.getoutput('mount')
    print("mounting disks")    
    for f in check_disks:
        try:
            os.mkdir("./mounts/" + f)
        except FileExistsError:
            print('folder exists: ' + f)

        if not  'mounts/{}'.format(f) in mounts:
            subprocess.run('mount -o ro /dev/disk/by-uuid/{} ./mounts/{}'.format(f, f), shell=True)
            print('mounted: ' + f)
        else:
            print('folder already mounted: ' + f)

main()