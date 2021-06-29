CREATE TRIGGER bluetoothstations.update_station_mean
AFTER INSERT ON `measurement`   
FOR EACH ROW 
UPDATE 		bluetoothstations.station_traffic_per_hour AS t 
SET 		t.mean = (t.mean+ new.count)/2    
WHERE 		t.station = NEW.station AND 
			t.hour = HOUR(NEW.timestamp);
