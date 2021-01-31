# Crypto scanning scripts

- I had a stack of old hard drives, and wanted to try to find any crypto wallets.
    - 99% sure I've kept track of them all, but oh geeze I don't want to reformat or get rid of the drives because WHAT IF
- this project is pretty hacky and specific to the old project laptop I'm working on, I'm not responsible if anything explodes and you lose all your crypto. However it should be entirely read-only and non destructive of the mounted drives.
    - you should update the `ignore_drives` var in mount-drives.py and byte-scan.py to reflect your machine
    - these scripts do multiple passes on the drive because I'm lazy. If your drives are flakey and failing, you should stop whatever you're doing and do a full disk backup first.
- This project is V1 feature complete for the purposes of dealing with my stack of old drives

## mount-drives.py

This script attempts to list and mount drives by UUID. it script includes a blocklist of drive IDs to skip (update for your system!)

## folder-scan.py

This script naively scans all the folders for files that is named like a wallet (possibly encrypted?)

- filenames I knew about:
    - `wallet.dat` which is the default name
    - `*wallet*.*dat*` any backup wallets with alternate names
    - `electrum_default_wallet` default electrum wallet name
    - `*.wallet` armory wallets

- so, looking for any filename with wallet in the name.
    - this results in a -lot- of false postives (eg: windows .dll's)
    - added a 'likelyWallet' flag that checks if the file starts with the bytes I've seen on my wallets

## byte-scan.py

this script scans the bytes of the drive, looking for forgotten bitcoin wallets that may exist in unformatted space.

- implementation:
    - read in ./wallet/meta.json
    - count # of likely wallets on drive
    - scan drive for likelyWallet header
    - compare count of likely headers with meta.json from scanning folders
    
- if wallet headers are found and don't match the # found on partitioned space:
    - may be duplicates? currently folder-scan.py dedupes on md5sum (not path) and doesn't keep track of # of duplicates (PRs welcome)
    - may be wallets in unused space on the partition
    - may be a false positive in an unrelated file

example on an empty wallet on a USB drive:
```
monofuel@twist:~/btc-scan$ sudo python3 ./mount-drives.py 
drives to mount:  ['47ad0d2e-0470-434c-ba65-fc6c24990aba']
./mount exists
cleaning up mounts folder
unmounted 47ad0d2e-0470-434c-ba65-fc6c24990aba
mounting disks
mounted: 47ad0d2e-0470-434c-ba65-fc6c24990aba

monofuel@twist:~/btc-scan$ sudo python3 ./folder-scan.py 

loaded existing ./wallets/meta.json
./wallets exists
likely wallet: 120bccde9fa4eed1a161b1890f07f622 at ./47ad0d2e-0470-434c-ba65-fc6c24990aba/wallet.dat
wrote out ./wallets/meta.json

monofuel@twist:~/btc-scan$ sudo python3 ./byte-scan.py 
loaded existing ./wallets/meta.json
drives to scan:  ['47ad0d2e-0470-434c-ba65-fc6c24990aba']
scanning: /dev/disk/by-uuid/47ad0d2e-0470-434c-ba65-fc6c24990aba
fileno 3

results

found matches: 1
matching indices: {} [136323072]

meta matches: 1
all likely wallets found
```
