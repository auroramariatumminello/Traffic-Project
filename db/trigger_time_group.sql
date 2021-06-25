CREATE TRIGGER bluetoothstations.update_time_data
AFTER INSERT ON `measurement` 
FOR EACH ROW
UPDATE 		bluetoothstations.time_group AS t
SET 		t.sum = t.sum + new.count  
WHERE 		t.month = MONTH(NEW.timestamp) AND
			t.weekday = WEEKDAY(NEW.timestamp) AND
			t.hour = HOUR(NEW.timestamp);
