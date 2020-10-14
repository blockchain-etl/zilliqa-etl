#standardSQL
SELECT tx_leader_address, COUNT(*) AS block_count
FROM `public-data-finance.crypto_zilliqa.tx_blocks`
GROUP BY tx_leader_address
ORDER BY block_count DESC
LIMIT 1000