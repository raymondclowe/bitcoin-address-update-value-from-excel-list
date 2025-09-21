# Electrum Commands Reference

## add_hold_invoice

Create a lightning hold invoice for the given payment hash

### Arguments

- `payment_hash` (str): Hex encoded payment hash to be used for the invoice
- `amount` (decimal): Optional requested amount (in btc)
- `memo` (str): Optional description of the invoice
- `expiry` (int): Optional expiry in seconds (default: 3600s)
- `min_final_cltv_expiry_delta` (int): Optional min final cltv expiry delta (default: 294 blocks)

### Description

Create a lightning hold invoice for the given payment hash. Hold invoices have to get settled manually later.
HTLCs will get failed automatically if block_height + 144 > htlc.cltv_abs.

## add_peer

Connect to a lightning node

### Arguments

- `connection_string` (str): Lightning network node ID or network address
- `gossip` (bool): Apply command to your gossip node instead of wallet node
- `timeout` (int): Timeout in seconds (default=20)

## add_request

Create a payment request, using the first unused address of the wallet

### Arguments

- `amount` (decimal): Requested amount (in btc)
- `memo` (str): Description of the request
- `force` (bool): Create new address beyond gap limit, if no more addresses are available.
- `lightning` (bool): Create lightning request.
- `expiry` (int): Time in seconds.

### Description

Create a payment request, using the first unused address of the wallet.
The address will be considered as used after this operation.
If no payment is received, the address will be considered as unused if the payment request is deleted from the wallet.

## addtransaction

Add a transaction to the wallet history, without broadcasting it

### Arguments

- `tx` (tx): Transaction, in hexadecimal format.

### Description

Add a transaction to the wallet history, without broadcasting it.

## broadcast

Broadcast a transaction to the network

### Arguments

- `tx` (str): Serialized transaction (must be hexadecimal)

### Description

Broadcast a transaction to the network.

## bumpfee

Bump the fee for an unconfirmed transaction

### Arguments

- `tx` (str): Serialized transaction (hexadecimal)
- `new_fee_rate` (str):  The Updated/Increased Transaction fee rate (in sats/vbyte)
- `decrease_payment` (bool): Whether payment amount will be decreased (true/false)
- `unsigned` (bool): Do not sign transaction
- `from_coins` (json): Coins that may be used to inncrease the fee (must be in wallet)

### Description

Bump the fee for an unconfirmed transaction.
'tx' can be either a raw hex tx or a txid. If txid, the corresponding tx must already be part of the wallet history.

## cancel_hold_invoice

Cancels lightning hold invoice 'payment_hash'

### Arguments

- `payment_hash` (str): Payment hash in hex of the hold invoice

### Description

Cancels lightning hold invoice 'payment_hash'.

## changegaplimit

Change the gap limit of the wallet

### Arguments

- `new_limit` (int): new gap limit
- `iknowwhatimdoing` (bool): Acknowledge that I understand the full implications of what I am about to do

### Description

Change the gap limit of the wallet.

## check_hold_invoice

Checks the status of a lightning hold invoice 'payment_hash'

### Arguments

- `payment_hash` (str): Payment hash in hex of the hold invoice

### Description

Checks the status of a lightning hold invoice 'payment_hash'.
Returns: {
"status": unpaid | paid | settled | unknown (cancelled or not found),
"received_amount_sat": currently received amount (pending htlcs or final after settling),
"invoice_amount_sat": Invoice amount, Optional (only if invoice is found),
"closest_htlc_expiry_height": Closest absolute expiry height of all received htlcs
(Note: HTLCs will get failed automatically if block_height + 144 > htlc_expiry_height)
}

## clear_invoices

Remove all invoices
wallet

### Description

Remove all invoices
wallet.clear_invoices()
return True
@command('n')
async def notify(self, address: str, URL: Optional[str]):

## clear_ln_blacklist

Close a lightning channel

### Arguments

- `channel_point` (str): channel point
- `force` (bool): Force closes (broadcast local commitment transaction)

### Description

Close a lightning channel.
Returns txid of closing tx.

## clear_requests

Remove all payment requests
wallet

### Description

Remove all payment requests
wallet.clear_requests()
return True
@command('w')
async def clear_invoices(self, wallet: Abstract_Wallet = None):
Remove all invoices

## close_channel

Close a lightning channel

### Arguments

- `channel_point` (str): channel point
- `force` (bool): Force closes (broadcast local commitment transaction)

### Description

Close a lightning channel.
Returns txid of closing tx.

## close_wallet

Close wallet
return await self

### Arguments

- `passphrase` (str): Seed extension
- `seed_type` (str): The type of wallet to create, e.g. 'standard' or 'segwit'
- `encrypt_file` (bool): Whether the file on disk should be encrypted with the provided password

### Description

Close wallet
return await self.daemon._stop_wallet(wallet_path)
@command('')
async def create(self, passphrase=None, password=None, encrypt_file=True, seed_type=None, wallet_path=None):
Create a new wallet.
If you want to be prompted for an argument, type '?' or ':' (concealed)

## convert_currency

Converts the given amount of currency to another using the
configured exchange rate source

### Arguments

- `from_amount` (decimal): Amount to convert (default=1)
- `from_ccy` (str): Currency to convert from
- `to_ccy` (str): Currency to convert to

### Description

Converts the given amount of currency to another using the
configured exchange rate source.

## convert_xkey

Convert xtype of a master key

### Arguments

- `xkey` (str): the key
- `xtype` (str): the type, eg 'xpub'

### Description

Convert xtype of a master key. e.g. xpub -> ypub

## create

Create a new wallet

### Arguments

- `passphrase` (str): Seed extension
- `seed_type` (str): The type of wallet to create, e.g. 'standard' or 'segwit'
- `encrypt_file` (bool): Whether the file on disk should be encrypted with the provided password

### Description

Create a new wallet.
If you want to be prompted for an argument, type '?' or ':' (concealed)

## createmultisig

Create multisig 'n of m' address

### Arguments

- `num` (int): Number of cosigners required
- `pubkeys` (json): List of public keys

## createnewaddress

Create a new receiving address, beyond the gap limit of the wallet
return wallet

### Description

Create a new receiving address, beyond the gap limit of the wallet
return wallet.create_new_address(False)
@command('w')
async def changegaplimit(self, new_limit, iknowwhatimdoing=False, wallet: Abstract_Wallet = None):

## decode_invoice

Decode a lightning invoice

### Arguments

- `invoice` (str): Lightning invoice (bolt 11)

## decrypt

Decrypt a message encrypted with a public key

### Arguments

- `encrypted` (str): Encrypted message
- `pubkey` (str): Public key of one of your wallet addresses

### Description

Decrypt a message encrypted with a public key.

## delete_invoice

Remove an outgoing payment invoice

### Arguments

- `invoice_id` (str): The invoice ID, as returned in list_invoices

## delete_request

Remove an incoming payment request

### Arguments

- `request_id` (str): The request ID, as returned in list_invoices

## deserialize

Deserialize a transaction

### Arguments

- `tx` (str): Serialized transaction

## dumpprivkeys

Deprecated

### Arguments

- `address` (str): Bitcoin address

### Description

Deprecated.
return "This command is deprecated. Use a pipe instead: 'electrum listaddresses | electrum getprivatekeys - '"
@command('')
async def validateaddress(self, address):
Check that an address is valid.

## enable_htlc_settle

command used in regtests

### Arguments

- `b` (bool): boolean

## encrypt

Encrypt a message with a public key

### Arguments

- `pubkey` (str): Public key
- `message` (str): Clear text message. Use quotes if it contains spaces.

### Description

Encrypt a message with a public key. Use quotes if the message contains whitespaces.

## export_channel_backup

Returns an encrypted channel backup

### Arguments

- `channel_point` (str): Channel outpoint

## freeze

Freeze address

### Arguments

- `address` (str): Bitcoin address

### Description

Freeze address. Freeze the funds at one of your wallet\'s addresses

## freeze_utxo

Freeze a UTXO so that the wallet will not spend it

### Arguments

- `coin` (str): outpoint, in the <txid:index> format

### Description

Freeze a UTXO so that the wallet will not spend it.

## get

Return item from wallet storage

### Arguments

- `key` (str): storage key

## get_blinded_path_via

Create a blinded path with node_id as introduction point

### Arguments

- `node_id` (str): Node pubkey in hex format
- `dummy_hops` (int): Number of dummy hops to add

### Description

Create a blinded path with node_id as introduction point. Introduction point must be direct peer of me.

## get_channel_ctx

return the current commitment transaction of a channel

### Arguments

- `channel_point` (str): Channel outpoint
- `iknowwhatimdoing` (bool): Acknowledge that I understand the full implications of what I am about to do

## get_invoice

Returns an invoice (request for outgoing payment)

### Arguments

- `invoice_id` (str): The invoice ID, as seen in list_invoices

## get_request

Returns a payment request

### Arguments

- `request_id` (str): The request ID, as seen in list_requests or add_request

## get_submarine_swap_providers

Queries nostr relays for available submarine swap providers

### Arguments

- `query_time` (int): Optional timeout how long the relays should be queried for provider announcements. Default: 15 sec

### Description

Queries nostr relays for available submarine swap providers.
To configure one of the providers use:
setconfig swapserver_npub 'npub...'

## get_tx_status

Returns some information regarding the tx

### Arguments

- `txid` (txid): Transaction ID

### Description

Returns some information regarding the tx. For now, only confirmations.
The transaction must be related to the wallet.

## get_watchtower_ctn

Return the local watchtower's ctn of channel

### Arguments

- `channel_point` (str): Channel outpoint (txid:index)

### Description

Return the local watchtower's ctn of channel. used in regtests

## getaddressbalance

Return the balance of any address

### Arguments

- `address` (str): Bitcoin address

### Description

Return the balance of any address. Note: This is a walletless
server query, results are not checked by SPV.

## getaddresshistory

Return the transaction history of any address

### Arguments

- `address` (str): Bitcoin address

### Description

Return the transaction history of any address. Note: This is a
walletless server query, results are not checked by SPV.

## getaddressunspent

Returns the UTXO list of any address

### Arguments

- `address` (str): Bitcoin address

### Description

Returns the UTXO list of any address. Note: This
is a walletless server query, results are not checked by SPV.

## getbalance

Return the balance of your wallet

### Description

Return the balance of your wallet.
c, u, x = wallet.get_balance()
l = wallet.lnworker.get_balance() if wallet.lnworker else None
out = {"confirmed": format_satoshis(c)}
if u:
out["unconfirmed"] = format_satoshis(u)
if x:
out["unmatured"] = format_satoshis(x)
if l:
out["lightning"] = format_satoshis(l)
return out
@command('n')
async def getaddressbalance(self, address):

## getconfig

Return the current value of a configuration variable

### Arguments

- `key` (str): name of the configuration variable

### Description

Return the current value of a configuration variable.

## getfeerate

Return current fee estimate given network conditions (in sat/kvByte)

### Description

Return current fee estimate given network conditions (in sat/kvByte).
To change the fee policy, use 'getconfig/setconfig fee_policy'

## getinfo

network info
net_params = self

### Description

network info
net_params = self.network.get_parameters()
response = {
'network': constants.net.NET_NAME,
'path': self.network.config.path,
'server': net_params.server.host,
'blockchain_height': self.network.get_local_height(),
'server_height': self.network.get_server_height(),
'spv_nodes': len(self.network.get_interfaces()),
'connected': self.network.is_connected(),
'auto_connect': net_params.auto_connect,
'version': ELECTRUM_VERSION,
'fee_estimates': self.network.fee_estimates.get_data()
}
return response
@command('n')
async def stop(self):
Stop daemon

## getmasterprivate

Get master private key

### Arguments

- `xkey` (str): the key
- `xtype` (str): the type, eg 'xpub'

### Description

Get master private key. Return your wallet\'s master private key
return str(wallet.keystore.get_master_private_key(password))
@command('')
async def convert_xkey(self, xkey, xtype):
Convert xtype of a master key. e.g. xpub -> ypub

## getmerkle

Get Merkle branch of a transaction included in a block

### Arguments

- `txid` (txid): Transaction ID
- `height` (int): Block height

### Description

Get Merkle branch of a transaction included in a block. Electrum
uses this to verify transactions (Simple Payment Verification).

## getminacceptablegap

Returns the minimum value for gap limit that would be sufficient to discover all
known addresses in the wallet

### Description

Returns the minimum value for gap limit that would be sufficient to discover all
known addresses in the wallet.

## getmpk

Get master public key

### Description

Get master public key. Return your wallet\'s master public key
return wallet.get_master_public_key()
@command('wp')
async def getmasterprivate(self, password=None, wallet: Abstract_Wallet = None):
Get master private key. Return your wallet\'s master private key

## getopenalias

Retrieve alias

### Arguments

- `key` (str): the alias to be retrieved

### Description

Retrieve alias. Lookup in your list of contacts, and for an OpenAlias DNS record.

## getprivatekeyforpath

Get private key corresponding to derivation path (address index)

### Arguments

- `path` (str): Derivation path. Can be either a str such as "m/0/50", or a list of ints such as [0, 50].

### Description

Get private key corresponding to derivation path (address index).

## getprivatekeys

Get private keys of addresses

### Arguments

- `address` (str): Bitcoin address

### Description

Get private keys of addresses. You may pass a single wallet address, or a list of wallet addresses.

## getpubkeys

Return the public keys for a wallet address

### Arguments

- `address` (str): Bitcoin address

### Description

Return the public keys for a wallet address.

## getseed

Get seed phrase

### Arguments

- `privkey` (str): Private key. Type \'?\' to get a prompt.

### Description

Get seed phrase. Print the generation seed of your wallet.
s = wallet.get_seed(password)
return s
@command('wp')
async def importprivkey(self, privkey, password=None, wallet: Abstract_Wallet = None):
Import a private key or a list of private keys.

## getservers

Return the list of known servers (candidates for connecting)

### Description

Return the list of known servers (candidates for connecting).
return self.network.get_servers()
@command('')
async def version(self):
Return the version of Electrum.

## gettransaction

Retrieve a transaction

### Arguments

- `txid` (txid): Transaction ID

### Description

Retrieve a transaction.

## getunusedaddress

Returns the first unused address of the wallet, or None if all addresses are used

### Description

Returns the first unused address of the wallet, or None if all addresses are used.
An address is considered as used if it has received a transaction, or if it is used in a payment request.

## gossip_info

Display statistics about lightninig gossip
lngossip = self

### Description

Display statistics about lightninig gossip
lngossip = self.network.lngossip
channel_db = lngossip.channel_db
forwarded = dict([(key.hex(), p._num_gossip_messages_forwarded) for key, p in wallet.lnworker.peers.items()]),
out = {
'received': {
'channel_announcements': lngossip._num_chan_ann,
'channel_updates': lngossip._num_chan_upd,
'channel_updates_good': lngossip._num_chan_upd_good,
'node_announcements': lngossip._num_node_ann,
},
'database': {
'nodes': channel_db.num_nodes,
'channels': channel_db.num_channels,
'channel_policies': channel_db.num_policies,
},
'forwarded': forwarded,
}
return out
@command('wnl')
async def list_peers(self, gossip=False, wallet: Abstract_Wallet = None):

## help

Show help about a command
# for the python console
return sorted(known_commands

### Description

Show help about a command
# for the python console
return sorted(known_commands.keys())
# lightning network commands
@command('wnl')
async def add_peer(self, connection_string, timeout=20, gossip=False, wallet: Abstract_Wallet = None):

## helpconfig

Returns help about a configuration variable

### Arguments

- `key` (str): name of the configuration variable

### Description

Returns help about a configuration variable.

## import_channel_backup

## importprivkey

Import a private key or a list of private keys

### Arguments

- `privkey` (str): Private key. Type \'?\' to get a prompt.

### Description

Import a private key or a list of private keys.

## is_synchronized

return wallet synchronization status
return wallet

### Description

return wallet synchronization status
return wallet.is_up_to_date()
@command('wn')
async def wait_for_sync(self, wallet: Abstract_Wallet = None):
Block until the wallet synchronization finishes.

## ismine

Check if address is in wallet

### Arguments

- `address` (str): Bitcoin address

### Description

Check if address is in wallet. Return true if and only address is in wallet

## lightning_history

lightning history

### Description

lightning history.
lightning_history = wallet.lnworker.get_lightning_history() if wallet.lnworker else {}
sorted_hist= sorted(lightning_history.values(), key=lambda x: x.timestamp)
return json_normalize([x.to_dict() for x in sorted_hist])
@command('w')
async def setlabel(self, key, label, wallet: Abstract_Wallet = None):

## list_channels

Return the list of Lightning channels in a wallet
# FIXME: we need to be online to display capacity of backups
from 

### Description

Return the list of Lightning channels in a wallet
# FIXME: we need to be online to display capacity of backups
from .lnutil import LOCAL, REMOTE, format_short_channel_id
channels = list(wallet.lnworker.channels.items())
backups = list(wallet.lnworker.channel_backups.items())
return [
{
'type': 'CHANNEL',
'short_channel_id': format_short_channel_id(chan.short_channel_id) if chan.short_channel_id else None,
'channel_id': chan.channel_id.hex(),
'channel_point': chan.funding_outpoint.to_str(),
'closing_txid': chan.get_closing_height()[0] if chan.get_closing_height() else None,
'state': chan.get_state().name,
'peer_state': chan.peer_state.name,
'remote_pubkey': chan.node_id.hex(),
'local_balance': chan.balance(LOCAL)//1000,
'remote_balance': chan.balance(REMOTE)//1000,
'local_ctn': chan.get_latest_ctn(LOCAL),
'remote_ctn': chan.get_latest_ctn(REMOTE),
'local_reserve': chan.config[REMOTE].reserve_sat,  # their config has our reserve
'remote_reserve': chan.config[LOCAL].reserve_sat,
'local_unsettled_sent': chan.balance_tied_up_in_htlcs_by_direction(LOCAL, direction=SENT) // 1000,
'remote_unsettled_sent': chan.balance_tied_up_in_htlcs_by_direction(REMOTE, direction=SENT) // 1000,
} for channel_id, chan in channels
] + [
{
'type': 'BACKUP',
'short_channel_id': format_short_channel_id(chan.short_channel_id) if chan.short_channel_id else None,
'channel_id': chan.channel_id.hex(),
'channel_point': chan.funding_outpoint.to_str(),
'closing_txid': chan.get_closing_height()[0] if chan.get_closing_height() else None,
'state': chan.get_state().name,
} for channel_id, chan in backups
]
@command('wnl')
async def enable_htlc_settle(self, b: bool, wallet: Abstract_Wallet = None):

## list_invoices

Returns the list of invoices (requests for outgoing payments) saved in the wallet

### Arguments

- `paid` (bool): Show only paid invoices
- `pending` (bool): Show only pending invoices
- `expired` (bool): Show only expired invoices

### Description

Returns the list of invoices (requests for outgoing payments) saved in the wallet.

## list_peers

List lightning peers of your node

### Arguments

- `gossip` (bool): Apply command to your gossip node instead of wallet node

## list_requests

Returns the list of incoming payment requests saved in the wallet

### Arguments

- `paid` (bool): Show only paid requests
- `pending` (bool): Show only pending requests
- `expired` (bool): Show only expired requests

### Description

Returns the list of incoming payment requests saved in the wallet.

## list_wallets

List wallets open in daemon
return [
{
'path': w

### Description

List wallets open in daemon
return [
{
'path': w.db.storage.path,
'synchronized': w.is_up_to_date(),
'unlocked': not w.has_password() or (w.get_unlocked_password() is not None),
}
for w in self.daemon.get_wallets().values()
]
@command('n')
async def load_wallet(self, wallet_path=None, password=None):

## listaddresses

List wallet addresses

### Arguments

- `receiving` (bool): Show only receiving addresses
- `change` (bool): Show only change addresses
- `frozen` (bool): Show only frozen addresses
- `unused` (bool): Show only unused addresses
- `funded` (bool): Show only funded addresses
- `balance` (bool): Show the balances of listed addresses
- `labels` (bool): Show the labels of listed addresses

### Description

List wallet addresses. Returns the list of all addresses in your wallet. Use optional arguments to filter the results.

## listconfig

Returns the list of all configuration variables

### Arguments

- `key` (str): name of the configuration variable

### Description

Returns the list of all configuration variables.
return self.config.list_config_vars()
@command('')
async def helpconfig(self, key):
Returns help about a configuration variable.

## listcontacts

Show your list of contacts
return wallet

### Description

Show your list of contacts
return wallet.contacts
@command('w')
async def getopenalias(self, key, wallet: Abstract_Wallet = None):

## listunspent

List unspent outputs

### Description

List unspent outputs. Returns the list of unspent transaction
outputs in your wallet.

## lnpay

Pay a lightning invoice
Note: it is *not* safe to try paying the same invoice multiple times with a timeout

### Arguments

- `invoice` (str): Lightning invoice (bolt 11)
- `timeout` (int): Timeout in seconds (default=120)
- `max_cltv` (int): Maximum total time lock for the route (default=4032+invoice_final_cltv_delta)
- `max_fee_msat` (int): Maximum absolute fee budget for the payment (if unset, the default is a percentage fee based on config.LIGHTNING_PAYMENT_FEE_MAX_MILLIONTHS)

### Description

Pay a lightning invoice
Note: it is *not* safe to try paying the same invoice multiple times with a timeout.
It is only safe to retry paying the same invoice if there are no more pending HTLCs
with the same payment_hash.  # FIXME should there even be a default timeout? just block forever.

## load_wallet

Load the wallet in memory

## make_seed

Create a seed

### Arguments

- `nbits` (int): Number of bits of entropy
- `seed_type` (str): The type of seed to create, e.g. 'standard' or 'segwit'
- `language` (str): Default language for wordlist

## nodeid

Return the Lightning Node ID of a wallet
listen_addr = self

### Description

Return the Lightning Node ID of a wallet
listen_addr = self.config.LIGHTNING_LISTEN
return wallet.lnworker.node_keypair.pubkey.hex() + (('@' + listen_addr) if listen_addr else '')
@command('wl')
async def list_channels(self, wallet: Abstract_Wallet = None):
Return the list of Lightning channels in a wallet

## normal_swap

Normal submarine swap: send on-chain BTC, receive on Lightning

### Arguments

- `lightning_amount` (decimal_or_dryrun): Amount to be received, in BTC. Set it to 'dryrun' to receive a value
- `onchain_amount` (decimal_or_dryrun): Amount to be sent, in BTC. Set it to 'dryrun' to receive a value

## notify

Watch an address

### Arguments

- `address` (str): Bitcoin address
- `URL` (str): The callback URL

### Description

Watch an address. Every time the address changes, a http POST is sent to the URL.
Call with an empty URL to stop watching an address.

## onchain_capital_gains

Capital gains, using utxo pricing

### Arguments

- `year` (int): Show cap gains for a given year

### Description

Capital gains, using utxo pricing.
This cannot be used with lightning.

## onchain_history

Wallet onchain history

### Arguments

- `show_addresses` (bool): Show input and output addresses
- `show_fiat` (bool): Show fiat value of transactions
- `year` (int): Show history for a given year
- `from_height` (int): Only show transactions that confirmed after(inclusive) given block height
- `to_height` (int): Only show transactions that confirmed before(exclusive) given block height

### Description

Wallet onchain history. Returns the transaction history of your wallet.

## open_channel

Open a lightning channel with a peer

### Arguments

- `connection_string` (str): Lightning network node ID or network address
- `amount` (decimal_or_max): funding amount (in BTC)
- `push_amount` (decimal): Push initial amount (in BTC)
- `public` (bool): The channel will be announced
- `zeroconf` (bool): request zeroconf channel

## password

Change wallet password

### Arguments

- `encrypt_file` (bool): Whether the file on disk should be encrypted with the provided password (default=true)
- `new_password` (str): New Password

### Description

Change wallet password.

## payto

Create an on-chain transaction

### Arguments

- `destination` (str): Bitcoin address, contact or alias
- `amount` (decimal_or_max): Amount to be sent (in BTC). Type '!' to send the maximum available.
- `fee` (decimal): Transaction fee (absolute, in BTC)
- `feerate` (float): Transaction fee rate (in sat/vbyte)
- `from_addr` (str): Source address (must be a wallet address; use sweep to spend from non-wallet address)
- `change_addr` (str): Change address. Default is a spare address, or the source address if it's not in the wallet
- `rbf` (bool): Whether to signal opt-in Replace-By-Fee in the transaction (true/false)
- `addtransaction` (bool): Whether transaction is to be used for broadcasting afterwards. Adds transaction to the wallet
- `locktime` (int): Set locktime block number
- `unsigned` (bool): Do not sign transaction
- `nocheck` (bool): Do not verify aliases
- `from_coins` (json): Source coins (must be in wallet; use sweep to spend from non-wallet address)

### Description

Create an on-chain transaction.

## paytomany

Create a multi-output transaction

### Arguments

- `outputs` (json): json list of ["address", "amount in BTC"]
- `rbf` (bool): Whether to signal opt-in Replace-By-Fee in the transaction (true/false)
- `fee` (str): Transaction fee (absolute, in BTC)
- `feerate` (str): Transaction fee rate (in sat/vbyte)
- `from_addr` (str): Source address (must be a wallet address; use sweep to spend from non-wallet address)
- `change_addr` (str): Change address. Default is a spare address, or the source address if it's not in the wallet
- `addtransaction` (bool): Whether transaction is to be used for broadcasting afterwards. Adds transaction to the wallet
- `locktime` (int): Set locktime block number
- `unsigned` (bool): Do not sign transaction
- `nocheck` (bool): Do not verify aliases
- `from_coins` (json): Source coins (must be in wallet; use sweep to spend from non-wallet address)

### Description

Create a multi-output transaction.

## rebalance_channels

Rebalance channels

### Arguments

- `from_scid` (str): Short channel ID
- `dest_scid` (str): Short channel ID
- `amount` (decimal): Amount (in BTC)

### Description

Rebalance channels.
If trampoline is used, channels must be with different trampolines.

## removelocaltx

Remove a 'local' transaction from the wallet, and its dependent
transactions

### Arguments

- `txid` (txid): Transaction ID

### Description

Remove a 'local' transaction from the wallet, and its dependent
transactions.

## request_force_close

Requests the remote to force close a channel

### Arguments

- `connection_string` (str): Lightning network node ID or network address
- `channel_point` (str): channel point

### Description

Requests the remote to force close a channel.
If a connection string is passed, can be used without having state or any backup for the channel.
Assumes that channel was originally opened with the same local peer (node_keypair).

## reset_liquidity_hints

Close a lightning channel

### Arguments

- `channel_point` (str): channel point
- `force` (bool): Force closes (broadcast local commitment transaction)

### Description

Close a lightning channel.
Returns txid of closing tx.

## restore

Restore a wallet from text

### Arguments

- `text` (str): seed phrase
- `passphrase` (str): Seed extension
- `encrypt_file` (bool): Whether the file on disk should be encrypted with the provided password

### Description

Restore a wallet from text. Text can be a seed phrase, a master
public key, a master private key, a list of bitcoin addresses
or bitcoin private keys.
If you want to be prompted for an argument, type '?' or ':' (concealed)

## reverse_swap

Reverse submarine swap: send on Lightning, receive on-chain

### Arguments

- `lightning_amount` (decimal_or_dryrun): Amount to be sent, in BTC. Set it to 'dryrun' to receive a value
- `onchain_amount` (decimal_or_dryrun): Amount to be received, in BTC. Set it to 'dryrun' to receive a value
- `prepayment` (decimal_or_dryrun): Lightning payment required by the swap provider in order to cover their mining fees. This is included in lightning_amount. However, this part of the operation is not trustless; the provider is trusted to fail this payment if the swap fails.

## searchcontacts

Search through your wallet contacts, return matching entries

### Arguments

- `query` (str): Search query

### Description

Search through your wallet contacts, return matching entries.

## send_onion_message

Send an onion message with onionmsg_tlv

### Arguments

- `node_id_or_blinded_path_hex` (str): node id or blinded path
- `message` (str): Message to send

### Description

Send an onion message with onionmsg_tlv.message payload to node_id.

## serialize

Create a signed raw transaction from a json tx template

### Arguments

- `jsontx` (json): Transaction in json

### Description

Create a signed raw transaction from a json tx template.
Example value for "jsontx" arg: {
"inputs": [
{"prevout_hash": "9d221a69ca3997cbeaf5624d723e7dc5f829b1023078c177d37bdae95f37c539", "prevout_n": 1,
"value_sats": 1000000, "privkey": "p2wpkh:cVDXzzQg6RoCTfiKpe8MBvmm5d5cJc6JLuFApsFDKwWa6F5TVHpD"}
],
"outputs": [
{"address": "tb1q4s8z6g5jqzllkgt8a4har94wl8tg0k9m8kv5zd", "value_sats": 990000}
]
}

## setconfig

Set a configuration variable

### Arguments

- `key` (str): name of the configuration variable
- `value` (str): value. may be a string or a Python expression.

### Description

Set a configuration variable.

## setlabel

Assign a label to an item

### Arguments

- `key` (str): Key
- `label` (str): Label

### Description

Assign a label to an item. Item may be a bitcoin address or a
transaction ID

## settle_hold_invoice

Settles lightning hold invoice with the given preimage

### Arguments

- `preimage` (str): Hex encoded preimage of the invoice to be settled

### Description

Settles lightning hold invoice with the given preimage.
Doesn't block until actual settlement of the HTLCs.

## signmessage

Sign a message with a key

### Arguments

- `address` (str): Bitcoin address
- `message` (str): Clear text message. Use quotes if it contains spaces.

### Description

Sign a message with a key. Use quotes if your message contains
whitespaces

## signtransaction

Sign a transaction with the current wallet

### Arguments

- `tx` (tx): transaction
- `ignore_warnings` (bool): ignore warnings

### Description

Sign a transaction with the current wallet.

## signtransaction_with_privkey

Sign a transaction with private keys passed as parameter

### Arguments

- `tx` (tx): Transaction to sign
- `privkey` (str): private key or list of private keys

### Description

Sign a transaction with private keys passed as parameter.

## stop

Stop daemon
await self

### Description

Stop daemon
await self.daemon.stop()
return "Daemon stopped"
@command('n')
async def list_wallets(self):
List wallets open in daemon

## sweep

Sweep private keys

### Arguments

- `privkey` (str): Private key. Type \'?\' to get a prompt.
- `destination` (str): Bitcoin address, contact or alias
- `fee` (str): Transaction fee (absolute, in BTC)
- `feerate` (str): Transaction fee rate (in sat/vbyte)
- `imax` (int): Maximum number of inputs
- `nocheck` (bool): Do not verify aliases

### Description

Sweep private keys. Returns a transaction that spends UTXOs from
privkey to a destination address. The transaction will not be broadcast.

## test_inject_fee_etas

Inject fee estimates into the network object, as if they were coming from connected servers

### Arguments

- `fee_est` (str): dict of ETA-based fee estimates, encoded as str

### Description

Inject fee estimates into the network object, as if they were coming from connected servers.
Useful on regtest.

## unfreeze

Unfreeze address

### Arguments

- `address` (str): Bitcoin address

### Description

Unfreeze address. Unfreeze the funds at one of your wallet\'s address

## unfreeze_utxo

Unfreeze a UTXO so that the wallet might spend it

### Arguments

- `coin` (str): outpoint

### Description

Unfreeze a UTXO so that the wallet might spend it.

## unlock

Unlock the wallet (store the password in memory)

### Description

Unlock the wallet (store the password in memory).
wallet.unlock(password)
@command('w')
async def listunspent(self, wallet: Abstract_Wallet = None):
List unspent outputs. Returns the list of unspent transaction
outputs in your wallet.

## unsetconfig

Clear a configuration variable

### Arguments

- `key` (str): name of the configuration variable

### Description

Clear a configuration variable.
The variable will be reset to its default value.

## validateaddress

Check that an address is valid

### Arguments

- `address` (str): Bitcoin address

### Description

Check that an address is valid.

## verifymessage

Verify a signature

### Arguments

- `address` (str): Bitcoin address
- `message` (str): Clear text message. Use quotes if it contains spaces.
- `signature` (str): The signature, base64-encoded.

### Description

Verify a signature.

## version

Return the version of Electrum

### Description

Return the version of Electrum.
return ELECTRUM_VERSION
@command('')
async def version_info(self):
Return information about dependencies, such as their version and path.

## version_info

Return information about dependencies, such as their version and path

### Description

Return information about dependencies, such as their version and path.
ret = {
"electrum.version": ELECTRUM_VERSION,
"electrum.path": os.path.dirname(os.path.realpath(__file__)),
"python.version": sys.version,
"python.path": sys.executable,
}
# add currently running GUI
if self.daemon and self.daemon.gui_object:
ret.update(self.daemon.gui_object.version_info())
# always add Qt GUI, so we get info even when running this from CLI
try:
from .gui.qt import ElectrumGui as QtElectrumGui
ret.update(QtElectrumGui.version_info())
except GuiImportError:
pass
# Add shared libs (.so/.dll), and non-pure-python dependencies.
# Such deps can be installed in various ways - often via the Linux distro's pkg manager,
# instead of using pip, hence it is useful to list them for debugging.
from electrum_ecc import ecc_fast
ret.update(ecc_fast.version_info())
from . import qrscanner
ret.update(qrscanner.version_info())
ret.update(DeviceMgr.version_info())
ret.update(crypto.version_info())
# add some special cases
import aiohttp
ret["aiohttp.version"] = aiohttp.__version__
import aiorpcx
ret["aiorpcx.version"] = aiorpcx._version_str
import certifi
ret["certifi.version"] = certifi.__version__
import dns
ret["dnspython.version"] = dns.__version__
return ret
@command('w')
async def getmpk(self, wallet: Abstract_Wallet = None):
Get master public key. Return your wallet\'s master public key

## wait_for_sync

Block until the wallet synchronization finishes

### Description

Block until the wallet synchronization finishes.
while True:
if wallet.is_up_to_date():
return True
await wallet.up_to_date_changed_event.wait()
@command('n')
async def getfeerate(self):

