SELECT IF(
(
    SELECT SUM(num_transactions)
    FROM `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.tx_blocks`
    WHERE DATE(timestamp) <= '{{ds}}'
) =
(
    SELECT COUNT(*)
    FROM `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.transactions`
    WHERE DATE(timestamp) <= '{{ds}}'
), 1,
CAST((SELECT 'Total number of transactions is not equal to sum of num_transactions in tx_blocks table') AS INT64))
