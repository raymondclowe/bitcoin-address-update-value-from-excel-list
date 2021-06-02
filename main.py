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

mempool_api = "https://mempool.space/api/address/"


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
          'chain_stats][funded_txo_count' + ',' +
          'chain_stats][funded_txo_sum' + ',' +
          'chain_stats][spent_txo_sum' + ',' +
          'chain_stats][spent_txo_sum' + ',' +
          'chain_stats][txo_sum' +
          'datetime')
    # logger.info("Starting loop")
    i = 0
    while i < len (addresslist):
        sys.stderr.write(str(i) +'/' + str( len(addresslist)) + '\n')
        address = addresslist[i]
        api_url = mempool_api + address
        # logger.info(api_url)

        response = requests.request("GET", api_url)
        

        if response.ok:
            response_native = json.loads(response.text)
            now = datetime.now()
            print(
                response_native['address'] + ',' +
                str(response_native['chain_stats']['funded_txo_count']) + ',' +
                str(response_native['chain_stats']['funded_txo_sum']) + ',' +
                str(response_native['chain_stats']['spent_txo_sum']) + ',' +
                str(response_native['chain_stats']['spent_txo_sum']) + ',' +
                str(response_native['chain_stats']['tx_count']) +',' +
                now.strftime("%Y-%m-%d %H:%M:%S")
            )
            time.sleep(shortdelay) 
            i = i + 1
        else:
            # logger.error("No success on url: "+api_url)
            sys.stderr.write("No success on url: "+api_url)
            time.sleep(longdelay)  # long time in case we are blocked
            if shortdelay == 0:
                shortdelay = 1
            if longdelay == 0:
                longdelay = 30
            shortdelay = shortdelay * args.increment
            longdelay = longdelay * args.increment

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
