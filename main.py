#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Raymond Lowe"
__version__ = "0.1.0"
__license__ = "none"

import argparse
from logzero import logger
import requests
from pandas import read_excel
from tqdm import tqdm
import json
import time
from datetime import datetime
import sys
import subprocess

mempool_api = "https://mempool.space/api/address/"


def get_balance_mempool(address):
    """Query balance from Mempool API."""
    api_url = mempool_api + address
    response = requests.get(api_url)
    if response.ok:
        return json.loads(response.text)
    else:
        raise Exception(f"Failed to query Mempool: {response.status_code}")


def get_balance_electrum(address, server):
    """Query balance from Electrum server."""
    electrum_path = "/home/rcl/Applications/electrum-4.6.2-x86_64_86a6c3900159c0ac8c769d03b1472543.AppImage"
    cmd = [electrum_path, 'getaddressbalance', address, '--server', server]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        data = json.loads(result.stdout.strip())
        return data
    else:
        raise Exception(f"Electrum error: {result.stderr}")


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
        'N/A' + ',' +
        str(data['confirmed']) + ',' +
        'N/A' + ',' +
        'N/A' + ',' +
        'N/A' + ',' +
        now.strftime("%Y-%m-%d %H:%M:%S")
    )


def main(args):
    """ Main entry point of the app """
    # logger.info("Starting")
    # logger.info(args)

    shortdelay = int(args.delay)
    longdelay = int(args.error)

    df = read_excel(args.excel, sheet_name=args.sheet, engine='openpyxl')
    addresslist = df[args.column].to_list()
    # logger.info("Got excel file")
    # print(addresslist)
    print('address' + ',' +
          'chain_stats-funded_txo_count' + ',' +
          'chain_stats-funded_txo_sum' + ',' +
          'chain_stats-spent_txo_count' + ',' +
          'chain_stats-spent_tx_sum' + ',' +
          'chain_stats-tx_sum'  + ',' +
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
