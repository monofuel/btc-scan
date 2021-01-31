# Crypto scanning scripts

- I had a stack of old hard drives, and wanted to try to find any crypto wallets.
- in progress

## mount-drives.py

This script attempts to list and mount drives by UUID. This script includes a blocklist of drive IDs to skip (update for your system!)

## folder-scan.py

This script naively scans all the folders for files that might look like a wallet (possibly encrypted)

- filenames I knew about:
    - `wallet.dat` which is the default name
    - `*wallet*.*dat*` any backup wallets with alternate names
    - `electrum_default_wallet` default electrum wallet name
    - `*.wallet` armory wallets

- so, looking for any filename with wallet in the name.
    - this results in a -lot- of false postives (eg: windows .dll's)
    - added a 'likelyWallet' flag 


## byte-scan.py

this script scans the bytes of the drive, looking for forgotten bitcoin wallets that may exist in unformatted space.

- implementation:
    - read in ./wallet/meta.json
    - count # of likely wallets on drive
    - scan drive for likelyWallet header
    - compare count of likely headers with meta.json from scanning folders

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