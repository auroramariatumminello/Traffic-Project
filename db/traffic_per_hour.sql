CREATE TABLE bluetoothstations.station_traffic_per_hour AS
(
SELECT station, hour(timestamp), sum(count) as sum, avg(count) as mean
FROM bluetoothstations.measurement
GROUP BY station, hour(timestamp)
);