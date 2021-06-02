# bitcoin-address-update-value-from-excel-list

Tool designed to be run scheduled once a day to get the latest balances on a list of bitcoin addresses.

The input list is an excel file column, and the output is to stdout suitable for redirect to a csv.

The idea is that you can then have a get data link in excel to the csv, and vlookup the balances against those addresses.

Reads data from mempool.spaces and allows self adjusting delaying to avoid hiting usage limits.
