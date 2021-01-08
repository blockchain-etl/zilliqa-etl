SELECT IF(
(
    SELECT MAX(number)
    FROM `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.ds_blocks`
    WHERE DATE(TIMESTAMP) <= '{{ds}}'
) + 1 =
(
    SELECT COUNT(*) FROM `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.ds_blocks`
    WHERE DATE(TIMESTAMP) <= '{{ds}}'
), 1,
CAST((SELECT 'Total number of ds blocks is not equal to last block number {{ds}}') AS INT64))
