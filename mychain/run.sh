#!/usr/bin/env sh

geth --datadir ./data/ --networkid 1235 --port 8545  --http --http.api 'admin,eth,miner,net,txpool,personal,web3'  --mine --allow-insecure-unlock --unlock '0x79dF0D3c23f22370881dC92aF524A1D5E52e3552' --password password.txt
