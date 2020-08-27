# Zilliqa ETL CLI

[![Build Status](https://travis-ci.org/blockchain-etl/zilliqa-etl.svg?branch=master)](https://travis-ci.org/blockchain-etl/zilliqa-etl)

Zilliqa ETL CLI lets you convert Zilliqa data into JSON newline-delimited format.

[Full documentation available here](http://zilliqa-etl.readthedocs.io/).

## Quickstart

Install Zilliqa ETL CLI:

```bash
pip3 install zilliqa-etl
```

Export directory service blocks ([Schema](../docs/schema.md), [Reference](../docs/commands.md)):

```bash
> zilliqaetl export_ds_blocks --start-block 1 --end-block 500000 \
--output-dir output --provider-uri https://api.zilliqa.com
```

Find other commands [here](https://zilliqa-etl.readthedocs.io/en/latest/commands/).

For the latest version, check out the repo and call 
```bash
> pip3 install -e . 
> python3 zilliqaetl.py
```

## Useful Links

- [Schema](https://zilliqa-etl.readthedocs.io/en/latest/schema/)
- [Command Reference](https://zilliqa-etl.readthedocs.io/en/latest/commands/)
- [Documentation](https://zilliqa-etl.readthedocs.io/)

## Running Tests

```bash
> pip3 install -e .[dev]
> export ZILLIQAETL_PROVIDER_URI=https://api.zilliqa.com
> pytest -vv
```

### Running Tox Tests

```bash
> pip3 install tox
> tox
```

## Running in Docker

1. Install Docker https://docs.docker.com/install/

2. Build a docker image
        
        > docker build -t zilliqa-etl:latest .
        > docker image ls
        
3. Run a container out of the image

        > docker run -v $HOME/output:/zilliqa-etl/output zilliqa-etl:latest export_ds_blocks -s 1 -e 500000 -o output
        