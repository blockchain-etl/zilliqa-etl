#standardSQL
SELECT
    DATE(TIMESTAMP_TRUNC(block_timestamp, MONTH, "UTC")) AS month,
    COUNT(DISTINCT sender) AS active_addresses
FROM `public-data-finance.crypto_zilliqa.transactions`
GROUP BY month
ORDER BY month DESC