CREATE TEMPORARY TABLE bluetoothstations.traffic_per_month
SELECT MONTH(timestamp) as month, SUM(count)
FROM bluetoothstations.measurement
GROUP BY month(timestamp)
ORDER BY month;