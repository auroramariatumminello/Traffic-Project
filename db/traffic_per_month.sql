CREATE TEMPORARY TABLE bluetoothstations.month_traffic
SELECT MONTH(timestamp) as month,SUM(count)
FROM bluetoothstations.measurement
GROUP BY month(timestamp);