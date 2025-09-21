# bitcoin address update value from excel list

Tool designed to be run scheduled once a day to get the latest balances on a list of bitcoin addresses.

The input list is an excel file column, and the output is to stdout suitable for redirect to a csv.

The idea is that you can then have a get data link in excel to the csv, and vlookup the balances against those addresses.

Reads data from mempool.spaces and allows self adjusting delaying to avoid hiting usage limits.

Retries on error loading api and never gives up.


## Usage

For fastest performance with your personal Electrum server (recommended for 700+ addresses):

```
python3 main.py addresses.xlsx -c B --mode electrum --electrum-server your_server:50002 -d 0.1 > balances.csv
```

This will:
- Read addresses from column B of `addresses.xlsx`
- Query each address via your local Electrum server (much faster than public APIs)
- Output CSV format: address, confirmed_balance, datetime
- Use minimal delay (0.1s) between queries since it's your local server

For Mempool API (if no local server):
```
python3 main.py addresses.xlsx -c B --mode mempool > balances.csv
```

### Options

- `-c B`: Specify column B (default is "add")
- `--mode electrum`: Use local Electrum server (fastest)
- `--electrum-server your_server:50002`: Your personal Electrum server address
- `-d 0.1`: Minimal delay between queries (adjust based on server capacity)
- `-e 30`: Delay on errors (seconds)
- `--mode mempool`: Fallback to Mempool API

### Performance Comparison

- **Mempool API**: ~1-2 seconds per address (rate limited, 700 addresses = ~20+ minutes)
- **Personal Electrum Server**: ~0.1-0.5 seconds per address (local, no limits, 700 addresses = ~1-5 minutes)

### Output Formats

- **Mempool mode**: address, funded_txo_count, funded_txo_sum, spent_txo_count, spent_txo_sum, tx_count, datetime
- **Electrum mode**: address, tx_count, confirmed_balance, unconfirmed_balance, datetime

### Adding/Changing Addresses

Simply edit `addresses.xlsx` column B. The tool processes the current Excel file each run.

### Wallet Management Workflow Examples

#### Check if a wallet exists
```
uv run electrum list_wallets
```

#### Create a new wallet
```
uv run electrum -w mywallet create --password mypassword
```

#### Load a wallet
```
uv run electrum -w mywallet load_wallet --password mypassword
```

#### Check balance of a specific address
```
uv run electrum -w mywallet getaddressbalance 12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S
```

#### Check balance of the entire wallet
```
uv run electrum -w mywallet getbalance
```

#### Close a wallet
```
uv run electrum -w mywallet close_wallet
```

#### Check if wallet is synchronized
```
uv run electrum -w mywallet is_synchronized
```

#### Wait for wallet to sync
```
uv run electrum -w mywallet wait_for_sync
```

#### Get wallet synchronization status
```
uv run electrum -w mywallet getinfo
```

#### Create a watch-only wallet from a list of addresses
For a large number of addresses (like your 700+ from Excel), create a text file with one address per line:

```
echo "address1" > addresses.txt
echo "address2" >> addresses.txt
# ... or extract from your Excel file
```

Then use:
```
addresses=$(cat addresses.txt | tr '\n' ' ')
uv run electrum -w watchonly_wallet restore "$addresses" --password mypassword
```

Alternatively, if the command supports it, you can pipe the addresses:
```
cat addresses.txt | tr '\n' ' ' | xargs uv run electrum -w watchonly_wallet restore --password mypassword
```

Note: You can pass a space-separated list of addresses to the `restore` command to create a watch-only wallet containing those addresses. This allows you to monitor balances for specific addresses from your Excel list.

### Creating Watch-Only Wallet from Excel Addresses

This section documents the complete process of extracting Bitcoin addresses from an Excel file and creating a watch-only wallet for balance monitoring. The process was tested with 485 addresses and completed in under 10 seconds total.

#### Step 1: Extract Addresses from Excel (Python Script)

Create a Python script `extract_addresses.py`:

```python
#!/usr/bin/env python3
from openpyxl import load_workbook

wb = load_workbook('addresses.xlsx')
ws = wb.active

addresses = []
for row in range(2, ws.max_row + 1):  # skip header
    cell = ws.cell(row=row, column=2)
    if cell.value:
        addresses.append(str(cell.value))

# Write to file
with open('extracted_addresses.txt', 'w') as f:
    for addr in addresses:
        f.write(addr + '\n')

print(f"Extracted {len(addresses)} addresses to extracted_addresses.txt")
```

Run the script:
```
python3 extract_addresses.py
```

**Timing**: Instantaneous for 485 addresses.

#### Step 2: Create Watch-Only Wallet

Concatenate addresses and restore wallet:
```
addresses=$(cat extracted_addresses.txt | tr '\n' ' ')
uv run electrum -w excel_wallet restore "$addresses" --password your_password
```

**Expected Output**:
```json
{
    "msg": "This wallet was restored offline. It may contain more addresses than displayed. Start a daemon and use load_wallet to sync its history.",
    "path": "/home/user/.electrum/wallets/excel_wallet"
}
```

**Timing**: ~3 seconds for 485 addresses.

#### Step 3: Load and Sync Wallet

Load the wallet:
```
uv run electrum -w excel_wallet load_wallet --password your_password
```

**Expected Output**: `/home/user/.electrum/wallets/excel_wallet`

**Timing**: ~2 seconds.

Check sync status:
```
uv run electrum -w excel_wallet is_synchronized
```

**Expected Output**: `false` (initially)

Wait for synchronization:
```
uv run electrum -w excel_wallet wait_for_sync
```

**Expected Output**: `true`

**Timing**: ~3 seconds.

#### Step 4: Check Balances

Get total wallet balance:
```
uv run electrum -w excel_wallet getbalance
```

**Example Output**:
```json
{
    "confirmed": "4.31877186"
}
```

Check individual address balance:
```
uv run electrum -w excel_wallet getaddressbalance bc1qexampleaddress
```

**Example Output**:
```json
{
    "confirmed": "0.44277942",
    "unconfirmed": "0"
}
```

#### Important Notes

- **Security**: Use strong passwords and keep them secure. The wallet files are encrypted.
- **Performance**: The process scales well - 485 addresses processed in ~8 seconds total.
- **Shell Limitations**: The `addresses=$(cat file.txt | tr '\n' ' ')` method handles large address lists efficiently without command-line length issues.
- **Wallet Management**: Use `uv run electrum list_wallets` to see available wallets, and `uv run electrum -w wallet_name close_wallet` to unload when done.
- **Address Format**: Ensure addresses in Excel column B are valid Bitcoin addresses. The script extracts them as strings.
- **Dependencies**: Requires `openpyxl` for Excel reading (already in project dependencies).

This workflow enables efficient monitoring of balances across hundreds of addresses from your Excel spreadsheet.

rcl@AspireE1:~/bitcoin-address-update-value-from-excel-list$ 