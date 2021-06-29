CREATE TABLE bluetoothstations.time_group AS
(
SELECT month(timestamp) as month,dayname(timestamp) as weekday, hour(timestamp) as hour, sum(count) as sum, avg(count) as mean
FROM bluetoothstations.measurement
GROUP BY month(timestamp),dayname(timestamp), hour(timestamp)
);