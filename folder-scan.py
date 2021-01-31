#!/usr/bin/python3
import os
import subprocess
import hashlib
import json

# script assumes running as root

wallet_dict = {}

# NB. this script indexes wallets based on md5sum. if multiple wallets share the same sum, only one is tracked
# TODO should track multiple dirs

# NB. I have no clue what the wallet format is, but they generally seem to start with this
# btc wallets have '0000 0010' after this, dogecoin has '0000 0020'
likely_header = bytearray.fromhex("000000000100000000000000623105000900")

class Wallet:
    dir = ""
    def __init__(self, dir):
        self.dir = dir

    def contents(self):
        f = open('./mounts/{}'.format(self.dir), mode='rb')
        contents = f.read()
        f.close()
        return contents

    def likelyWallet(self):
        contents = self.contents()
        return contents.startswith(likely_header)

    def md5hash(self):
        return hashlib.md5(self.contents()).hexdigest()

def main():
    find_output = subprocess.getoutput('cd ./mounts && find . -type f -iname "*wallet*"')
    lines = find_output.splitlines()
    for l in lines:
        wallet = Wallet(l)
        wallet_dict[wallet.md5hash()] = wallet

    print()
    wallet_meta  = {}
    try:
        meta_file = open("./wallets/meta.json", 'r')
        contents = meta_file.read()
        meta_file.close()
        wallet_meta = json.loads(contents)
        print('loaded existing ./wallets/meta.json')
    except:
        print("failed to load wallets/meta.json")
        wallet_meta = {}
        
    try:
        os.mkdir("./wallets")
    except FileExistsError:
        print('./wallets exists')
    for wallet in wallet_dict.values():
        md5hash = wallet.md5hash()
        wallet_name = "./wallets/{}.wallet.dat".format(md5hash)
        f_wallet = open(wallet_name, 'wb')
        f_wallet.write(wallet.contents())
        f_wallet.close()
        # print("wrote out " + wallet_name)

        meta = {
            'hash': md5hash,
            'fulldir': wallet.dir,
            'drive': os.path.split(os.path.dirname(wallet.dir))[0],
            'filename': os.path.basename(wallet.dir),
            'likelyWallet': wallet.likelyWallet()
        }
        wallet_meta[md5hash] = meta
        if meta["likelyWallet"]:
            print("likely wallet: {} at {}".format(meta["hash"], meta["fulldir"]))

    # handle metadata file for tracking wallets
    wallet_meta_f = open('./wallets/meta.json', 'w')
    wallet_meta_f.write(json.dumps(wallet_meta, indent=4, sort_keys=True))
    wallet_meta_f.close()
    print('wrote out ./wallets/meta.json')


main()