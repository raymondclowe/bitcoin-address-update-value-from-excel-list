# Bitcoin Address Update Value from Excel List - ROADMAP

## Project Overview

This project updates an Excel file with current Bitcoin address balances by querying either Mempool.space API or a personal Electrum server.

## Features

- Read addresses from Excel file
- Query balances from Mempool or Electrum
- Support multiple modes: mempool only, electrum only, both, fallback
- Output CSV with balance data

## Roadmap

### Phase 1: Basic Functionality (Current)

- [x] Read Excel file
- [x] Query Mempool API
- [x] Output CSV

### Phase 2: Electrum Integration

- [x] Add Electrum query function
- [ ] Test Electrum CLI/RPC with personal server
- [ ] Integrate with personal Electrum server

### Phase 3: Mode Support

- [x] Add command-line modes
- [ ] Test all modes with real data

### Phase 4: UV Project Setup

- [x] Initialize uv
- [x] Add dependencies (pandas, requests, openpyxl)

### Phase 5: Testing and Refinement

- [ ] Manual testing with real data
- [ ] Error handling improvements
- [ ] Performance optimizations

## Usage

```bash
python main.py addresses.xlsx --mode fallback --electrum-server <server>:<port>
```

Modes:
- `mempool`: Use only Mempool API
- `electrum`: Use only Electrum server
- `both`: Try Electrum first, fallback to Mempool
- `fallback`: Same as both

## Dependencies

- pandas
- requests
- openpyxl
- Electrum client (AppImage or installed)

## Notes

- Electrum integration uses subprocess to call the AppImage CLI.
- Tested with public Electrum server (electrum.blockstream.info:50002), but needs testing with personal server.
- RPC setup attempted but CLI method used instead.
- Output format uses N/A for missing fields in Electrum data.

## Manual Test Results

- Electrum CLI getaddressbalance command attempted, but failed with "unrecognized arguments" for --server.
- Daemon RPC tested, but connection refused on port 7777.
- Need to verify personal Electrum server address and connection method.