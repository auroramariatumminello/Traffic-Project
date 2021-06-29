CREATE TRIGGER bluetoothstations.update_station_sum
AFTER INSERT ON `measurement`   
FOR EACH ROW 
UPDATE 		bluetoothstations.station_traffic_per_hour AS t 
SET 		t.sum = t.sum+ new.count   
WHERE 		t.station = NEW.station AND 
			t.hour = HOUR(NEW.timestamp);