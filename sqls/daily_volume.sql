#standardSQL
WITH all_transactions AS (
  SELECT block_timestamp, amount
  FROM `public-data-finance.crypto_zilliqa.transactions`
  UNION ALL
  SELECT block_timestamp, amount
  FROM `public-data-finance.crypto_zilliqa.transitions`
)
SELECT
  DATE(block_timestamp) AS date,
  SUM(amount) / 1e12 AS volume
FROM all_transactions
GROUP BY date
ORDER BY date DESC
LIMIT 1000