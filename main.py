#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Raymond Lowe"
__version__ = "0.1.0"
__license__ = "none"

import argparse
# from logzero import logger
import requests
from pandas import read_excel
# from tqdm import tqdm
import json
import time
from datetime import datetime
import sys

mempool_api = "https://mempool.space/api/address/"

# Electrum RPC configuration
ELECTRUM_RPC_URL = "http://127.0.0.1:7777"
ELECTRUM_RPC_USER = "user"
ELECTRUM_RPC_PASSWORD = "--Y-2Ben-VJppSmBn1Yedg=="


def get_balance_mempool(address):
    """Query balance from Mempool API."""
    api_url = mempool_api + address
    response = requests.get(api_url)
    if response.ok:
        return json.loads(response.text)
    else:
        raise Exception(f"Failed to query Mempool: {response.status_code}")


def get_balance_electrum(address, server=None):
    """Query balance and tx count from Electrum server via RPC."""
    # Prepare authentication
    auth = (ELECTRUM_RPC_USER, ELECTRUM_RPC_PASSWORD)
    headers = {'content-type': 'application/json'}
    
    # Get balance
    balance_payload = {
        "jsonrpc": "2.0",
        "id": "balance",
        "method": "getaddressbalance",
        "params": [address]
    }
    
    balance_response = requests.post(ELECTRUM_RPC_URL, 
                                   data=json.dumps(balance_payload),
                                   headers=headers,
                                   auth=auth)
    
    if not balance_response.ok:
        raise Exception(f"Electrum RPC balance error: {balance_response.status_code}")
    
    balance_result = balance_response.json()
    if 'error' in balance_result:
        raise Exception(f"Electrum balance error: {balance_result['error']}")
    
    balance_data = balance_result['result']
    
    # Get transaction history for tx count
    history_payload = {
        "jsonrpc": "2.0", 
        "id": "history",
        "method": "getaddresshistory",
        "params": [address]
    }
    
    history_response = requests.post(ELECTRUM_RPC_URL,
                                   data=json.dumps(history_payload),
                                   headers=headers,
                                   auth=auth)
    
    if not history_response.ok:
        raise Exception(f"Electrum RPC history error: {history_response.status_code}")
    
    history_result = history_response.json()
    if 'error' in history_result:
        raise Exception(f"Electrum history error: {history_result['error']}")
    
    history_data = history_result['result']
    tx_count = len(history_data)
    
    # Combine data
    combined = balance_data.copy()
    combined['tx_count'] = tx_count
    return combined


def print_mempool_data(data, now):
    """Print CSV line for Mempool data."""
    print(
        data['address'] + ',' +
        str(data['chain_stats']['funded_txo_count']) + ',' +
        str(data['chain_stats']['funded_txo_sum']) + ',' +
        str(data['chain_stats']['spent_txo_count']) + ',' +
        str(data['chain_stats']['spent_txo_sum']) + ',' +
        str(data['chain_stats']['tx_count']) + ',' +
        now.strftime("%Y-%m-%d %H:%M:%S")
    )


def print_electrum_data(address, data, now):
    """Print CSV line for Electrum data."""
    print(
        address + ',' +
        str(data.get('tx_count', 'N/A')) + ',' +
        str(data.get('confirmed', 'N/A')) + ',' +
        str(data.get('unconfirmed', '0')) + ',' +
        now.strftime("%Y-%m-%d %H:%M:%S")
    )


def main(args):
    """ Main entry point of the app """
    # logger.info("Starting")
    # logger.info(args)

    shortdelay = float(args.delay)
    longdelay = float(args.error)

    df = read_excel(args.excel, sheet_name=args.sheet, engine='openpyxl')
    addresslist = df[args.column].to_list()
    # logger.info("Got excel file")
    # print(addresslist)
    # Set header based on mode
    if args.mode == 'mempool':
        print('address' + ',' +
              'chain_stats-funded_txo_count' + ',' +
              'chain_stats-funded_txo_sum' + ',' +
              'chain_stats-spent_txo_count' + ',' +
              'chain_stats-spent_txo_sum' + ',' +
              'chain_stats-tx_count'  + ',' +
              'datetime')
    else:  # electrum modes
        print('address' + ',' +
              'tx_count' + ',' +
              'confirmed_balance' + ',' +
              'unconfirmed_balance' + ',' +
              'datetime')
    # logger.info("Starting loop")
    for i, address in enumerate(addresslist):
        sys.stderr.write(f"{i}/{len(addresslist)}\n")
        now = datetime.now()
        try:
            if args.mode == 'mempool':
                data = get_balance_mempool(address)
                print_mempool_data(data, now)
            elif args.mode == 'electrum':
                data = get_balance_electrum(address, args.electrum_server)
                print_electrum_data(address, data, now)
            elif args.mode == 'both':
                # Try Electrum first for speed, fallback to Mempool
                try:
                    data = get_balance_electrum(address, args.electrum_server)
                    print_electrum_data(address, data, now)
                except Exception as e:
                    sys.stderr.write(f"Electrum failed for {address}, trying Mempool: {e}\n")
                    data = get_balance_mempool(address)
                    print_mempool_data(data, now)
            elif args.mode == 'fallback':
                # Same as both for now
                try:
                    data = get_balance_electrum(address, args.electrum_server)
                    print_electrum_data(address, data, now)
                except Exception as e:
                    sys.stderr.write(f"Electrum failed for {address}, trying Mempool: {e}\n")
                    data = get_balance_mempool(address)
                    print_mempool_data(data, now)
            time.sleep(shortdelay)
        except Exception as e:
            sys.stderr.write(f"Error for {address}: {e}\n")
            time.sleep(longdelay)
            shortdelay = max(shortdelay * args.increment, 1)
            longdelay = max(longdelay * args.increment, 30)

    # logger.info('-done-')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument(
        "excel", help="Path/name to excel file of which the first sheet, column called add")

    # Optional argument flag which defaults to False
    parser.add_argument("-s", "--sheet", action="store",
                        default=0, help="Sheet defautls to first one '0'")
    parser.add_argument("-c", "--column", action="store",
                        default="add", help="Column defautls to 'add''")
    parser.add_argument("-d", "--delay", action="store",
                        default=1, help="Delay in seconds between api default 1")
    parser.add_argument("-e", "--error", action="store",
                        default=30, help="Delay on error in seconds between api default 30")
    parser.add_argument("-i", "--increment", action="store",
                        default=2, help="incremeting multiplier for delays default 2")                        
    parser.add_argument("--mode", action="store",
                        default="fallback", choices=["mempool", "electrum", "both", "fallback"],
                        help="Query mode: mempool, electrum, both, or fallback (default: fallback)")
    parser.add_argument("--electrum-server", action="store",
                        default="localhost:50002", help="Electrum server address:port (default: localhost:50002)")

    # Optional argument which requires a parameter (eg. -d test)
    # parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    # parser.add_argument(
    # "--version",
    # action="version",
    # version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
