### ds_blocks

```
hash: STRING
number: INTEGER
timestamp: TIMESTAMP
difficulty: INTEGER
difficulty_ds: INTEGER
gas_price: NUMERIC
leader_pub_key: STRING
prev_hash: STRING
signature: STRING
```

### tx_blocks

```
hash: STRING
number: INTEGER
ds_block_number: INTEGER
timestamp: TIMESTAMP
version: INTEGER
gas_limit: NUMERIC
gas_used: NUMERIC
mb_info_hash: STRING
miner_pub_key: STRING
num_micro_blocks: INTEGER
num_transactions: INTEGER
prev_block_hash: STRING
rewards: INTEGER
state_delta_hash: STRING
state_root_hash: STRING
header_signature: STRING
```

### transactions

```
id: STRING
block_number: INTEGER
timestamp: TIMESTAMP
amount: NUMERIC
data: STRING
gas_limit: NUMERIC
gas_price: NUMERIC
nonce: INTEGER
sender_pub_key: STRING
signature: STRING
to_addr: STRING
version: INTEGER
accepted: INTEGER
success: INTEGER
cumulative_gas: NUMERIC
epoch_num: INTEGER
```

### event_logs

```
block_number: INTEGER
timestamp: TIMESTAMP
transaction_id: STRING
index: INTEGER
address: STRING
event_name: STRING
params: STRUCT (REPEATED)
├── type: STRING
├── value: STRING
├── vname: STRING
```

### transitions

```
block_number: INTEGER
timestamp: TIMESTAMP
transaction_id: STRING
addr: STRING
depth: INTEGER
amount: NUMERIC
recipient: STRING
tag: STRING
```
