# Quickstart

Install Zilliqa ETL CLI:

```bash
pip install zilliqa-etl
```

Export ds_blocks ([Schema](schema.md), [Reference](commands.md#export_ds_blocks)):

```bash
zilliqaetl export_ds_blocks --start-block 1 --end-block 100 \
--provider-uri https://api.zilliqa.com --output-dir output
```

Find all commands [here](commands.md).
