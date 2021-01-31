#!/usr/bin/python3
import os
import subprocess
import hashlib
import json
import mmap

# script assumes running as root

likely_header = bytearray.fromhex("000000000100000000000000623105000900")

# list of system drives to not attempt to mount
ignore_drives = ("7a907b0c-4f8a-4350-b2b4-c804abca9622", "ed5b6085-40e0-463e-b2fa-438f6cb9ddcb", "6d406c55-5de8-4401-b2ee-92bd1046520c", "80b7f420-7699-476c-9db1-c0108bb661aa")


def main():
    meta_file = open("./wallets/meta.json", 'r')
    contents = meta_file.read()
    meta_file.close()
    wallet_meta = json.loads(contents)
    print('loaded existing ./wallets/meta.json')

    check_disks = [f for f in os.listdir('/dev/disk/by-uuid') if f not in ignore_drives]
    print("drives to scan: ", check_disks)

    matches = {}

    for disk in check_disks:
        matches[disk] = []
        diskMatches = matches[disk]
        diskname = '/dev/disk/by-uuid/{}'.format(disk)
        # diskpath = os.path.realpath(diskname)
        print('scanning: ' + diskname)
        with open(diskname, 'r+b') as file:
            print("fileno {}".format(file.fileno()))
            file.seek(0, 2) # move to end of file
            size = file.tell() # get size
            file.seek(0,0) # move back to start (is this needed?)

            with mmap.mmap(file.fileno(), length=size, access=mmap.ACCESS_READ) as s:
                idx = 0
                while True:
                    index = s.find(likely_header, idx)
                    if index == -1:
                        break
                    # print('found match: {}'.format(index))
                    diskMatches.append(index)
                    idx = index + 1

    # compare results of disk scan with results of meta.json
    print()
    print('results')
    print()
    for disk in matches:
        diskMatches=matches[disk]
        print('found matches: {}'.format(len(diskMatches)))
        print('matching indices: {}', diskMatches)
        print()

        metaMatches = []
        for meta in wallet_meta.values():
            if disk == meta["drive"] and meta["likelyWallet"] == True:
                metaMatches.append(meta["fulldir"])

        print('meta matches: {}'.format(len(metaMatches)))
        
        if len(metaMatches) == len(diskMatches):
            print('all likely wallets found')





main()