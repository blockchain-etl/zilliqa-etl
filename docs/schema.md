### ds_blocks

```
hash: STRING
number: INTEGER
timestamp: TIMESTAMP
difficulty: INTEGER
difficulty_ds: INTEGER
gas_price: NUMERIC
ds_leader_pub_key: STRING
ds_leader_address: STRING
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
tx_leader_pub_key: STRING
tx_leader_address: STRING
num_micro_blocks: INTEGER
num_transactions: INTEGER
num_present_transactions: INTEGER
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
block_timestamp: TIMESTAMP
amount: NUMERIC
code: STRING
data: STRING
gas_limit: NUMERIC
gas_price: NUMERIC
nonce: INTEGER
sender_pub_key: STRING
signature: STRING
to_addr: STRING
version: INTEGER
accepted: BOOL
success: BOOL
cumulative_gas: NUMERIC
epoch_num: INTEGER
```

### event_logs

```
block_number: INTEGER
block_timestamp: TIMESTAMP
transaction_id: STRING
index: INTEGER
address: STRING
event_name: STRING
params: STRING (REPEATED)
```

### exceptions

```
block_number: INTEGER
block_timestamp: TIMESTAMP
transaction_id: STRING
index: INTEGER
line: INTEGER
message: STRING
```

### transitions

```
block_number: INTEGER
block_timestamp: TIMESTAMP
transaction_id: STRING
index: INTEGER
accepted: BOOL
addr: STRING
depth: INTEGER
amount: NUMERIC
recipient: STRING
tag: STRING
params: STRING (REPEATED)
```
