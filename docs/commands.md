# Commands

All commands accept `-h` parameter for help, e.g.:

```bash
zilliqaetl export_ds_blocks -h

Usage: zilliqaetl export_ds_blocks [OPTIONS]

  Export directory service blocks.

Options:
  -s, --start-block INTEGER       Start block  [default: 0]
  -e, --end-block INTEGER         End block  [required]
  -p, --provider-uri TEXT         The URI of the remote Zilliqa node  [default:
                                  https://api.zilliqa.com]
  -w, --max-workers INTEGER       The maximum number of workers.  [default: 5]
  -o, --output-dir TEXT           The output directory for block data.
  -h, --help                      Show this message and exit.
```

#### export_ds_blocks

```bash
zilliqaetl export_ds_blocks --start-block 1 --end-block 100 \
--provider-uri https://api.zilliqa.com --output-dir output 
```

Exports ds_blocks to the folder specified in `--output-dir`.

```
Options:
  -s, --start-block INTEGER       Start block  [default: 0]
  -e, --end-block INTEGER         End block  [required]
  -p, --provider-uri TEXT         The URI of the remote Zilliqa node  [default:
                                  https://api.zilliqa.com]
  -w, --max-workers INTEGER       The maximum number of workers.  [default: 5]
  -o, --output-dir TEXT           The output directory for block data.
  -f, --output-format [json]      The output format.  [default: json]
  -h, --help                      Show this message and exit.
```

#### export_tx_blocks

```bash
zilliqaetl export_ts_blocks --start-block 1 --end-block 100 \
--provider-uri https://api.zilliqa.com --output-dir output 
```

Exports tx_blocks, transactions, event_logs, transitions and exceptions 
to individual files in the folder specified in `--output-dir`.

```
Options:
  -s, --start-block INTEGER       Start block  [default: 0]
  -e, --end-block INTEGER         End block  [required]
  -p, --provider-uri TEXT         The URI of the remote Zilliqa node  [default:
                                  https://api.zilliqa.com]
  -w, --max-workers INTEGER       The maximum number of workers.  [default: 5]
  -o, --output-dir TEXT           The output directory for block data.
  -f, --output-format [json]      The output format.  [default: json]
  -h, --help                      Show this message and exit.
```
