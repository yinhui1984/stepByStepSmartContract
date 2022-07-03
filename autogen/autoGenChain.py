#!/usr/bin/env python3

# 一键创建ETH私有链，共识算法POW，如果要使用POA请修改createGenesisFile()中的配置文件
# 这只是练习使用，更好的做法是使用 ganache-cli

import os
import subprocess
import re
from typing import List

ROOT_FOLDER = os.getcwd()
DATA_FOLDER = "./data/"
ACCOUNT_FILE = "accounts.txt"
PASSWORD_FILE = "password.txt"
GENESIS_FILE = "genesis.json"
CHAIN_ID = ""


def run_command(cmd: List):
    sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    out = out.decode('utf-8').rstrip()
    err = err.decode('utf-8').rstrip()
    rtn = sp.returncode
    if out:
        # print("[output]"+out)
        return out
    if err:
        print("return code:" + str(rtn) + " : " + err)
        return err


def ask_root_folder():
    i = input("the folder path of output:")
    p = os.path.abspath(i)
    if not os.path.exists(p):
        os.mkdir(p)
    global ROOT_FOLDER
    ROOT_FOLDER = p
    print(ROOT_FOLDER)
    os.chdir(ROOT_FOLDER)


def create_account():
    # geth account new --password <(echo $mypassword)
    account = ""
    password = input("password of new account:")
    with open(PASSWORD_FILE, "w+") as f:
        f.write(password)
    out = run_command(["geth", "--datadir", DATA_FOLDER, "account",
                       "new", "--password", "./password.txt"])
    m = re.search('0x.+', out)
    if m:
        account = m.group(0)
        with open(ACCOUNT_FILE, "w+") as f:
            f.write(account)
        print("account: " + account + " with password:" + password)
    else:
        print("creat account error!")
        quit()
    return account


def create_genesis(coinbase):
    # use os.system("puppeth") is another option

    global CHAIN_ID
    CHAIN_ID = input("id of chain (numbers):")

    g = '''
{{
    "nonce": "0x0000000000000042",
    "timestamp": "0x00",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "extraData": "0x00",
    "gasLimit": "0x8000000",
    "difficulty": "0x0400",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "coinbase": "{}",
    "alloc": {{
        "{}": {{ "balance": "1000000000000000000000"}}
    }},
    "config": {{
        "chainId": {},
        "homesteadBlock": 0,
        "byzantiumBlock": 0,
        "constantinopleBlock": 0,
        "eip150Block": 0,
        "eip155Block": 0,
        "eip158Block": 0
    }}
}}
    '''.format(coinbase, coinbase, CHAIN_ID)
    print(g)
    with open(GENESIS_FILE, "w+") as f:
        f.write(g)


def init_chain():
    run_command(["geth", "--datadir", DATA_FOLDER, "init", GENESIS_FILE])


def create_run_script(account):
    #  do not add   --http.corsdomain '*'  , it's not safe for private chain
    cmd = '''
    geth --datadir {} --networkid {} --port 8545  --http --http.api 'admin,eth,miner,net,txpool,personal,web3'  --mine --allow-insecure-unlock --unlock '{}' --password password.txt
    '''.format(DATA_FOLDER, CHAIN_ID, account)
    with open("run.sh", "w+") as f:
        f.write(cmd)
    run_command(["chmod", "+x", "run.sh"])
    # runCommand(["sh", "run.sh"])


def create_attach_script():
    cmd = '''
    geth attach {}geth.ipc
    '''.format(DATA_FOLDER)
    with open("attach.sh", "w+") as f:
        f.write(cmd)
    run_command(["chmod", "+x", "attach.sh"])


def main():
    ask_root_folder()
    account = create_account()
    create_genesis(account)
    init_chain()
    create_run_script(account)
    create_attach_script()
    print("DONE")


if __name__ == "__main__":
    main()
