# Crypto scanning scripts

- I had a stack of old hard drives, and wanted to try to find any crypto wallets.
- in progress

## mount-drives.py

This script attempts to list and mount drives by UUID. This script includes a blocklist of drive IDs to skip (update for your system!)

## folder-scan.py

This script naively scans all the folders for files that might look like a wallet (possibly encrypted)

- filenames I knew about:
    - `wallet.dat` which is the default name
    - *wallet*.*dat*` any backup wallets with alternate names
    - `electrum_default_wallet` default electrum wallet name
    - `*.wallet` armory wallets

- so, looking for any filename with wallet in the name.
    - this results in a -lot- of false postives (eg: windows .dll's)
    - added a 'likelyWallet' flag 


## byte-scan.py

TODO
this script scans the bytes of the drive, looking for forgotten bitcoin wallets that may exist in unformatted space.