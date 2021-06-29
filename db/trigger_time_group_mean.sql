CREATE TRIGGER bluetoothstations.update_time_data_mean 
AFTER INSERT ON `measurement`   
FOR EACH ROW 
UPDATE 		bluetoothstations.time_group AS t 
SET 		t.mean = (t.mean+ new.count)/2    
WHERE 		t.month = MONTH(NEW.timestamp) AND 
			t.weekday = WEEKDAY(NEW.timestamp) AND 
			t.hour = HOUR(NEW.timestamp);
