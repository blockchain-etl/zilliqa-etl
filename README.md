# Zilliqa ETL

[![Build Status](https://travis-ci.org/blockchain-etl/zilliqa-etl.svg?branch=master)](https://travis-ci.org/blockchain-etl/zilliqa-etl)
[![Telegram](https://img.shields.io/badge/telegram-join%20chat-blue.svg)](https://t.me/joinchat/GsMpbA3mv1OJ6YMp3T5ORQ)

## Overview

Zilliqa ETL allows you to setup an ETL pipeline in Google Cloud Platform for ingesting Zilliqa blockchain data 
into BigQuery. It comes with [CLI tools](/cli) for exporting Zilliqa data into JSON newline-delimited files
partitioned by day. 

Data is available for you to query right away in 
[Google BigQuery](https://console.cloud.google.com/bigquery?page=dataset&d=crypto_zilliqa&p=public-data-finance).

## Architecture

![zilliqa_etl_architecture.svg](zilliqa_etl_architecture.png)

[Google Slides version](https://docs.google.com/presentation/d/16h_JVok0dZmHQfnWeGAUJAsEzkwUh2DSHVdhTe5LC-E/edit?usp=sharing)

1. [Airflow DAGs](https://airflow.apache.org/) export and load Zilliqa data to BigQuery daily. 
    Refer to [Zilliqa ETL Airflow](/airflow) for deployment instructions.
