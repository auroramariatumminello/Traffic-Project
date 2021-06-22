from Database_Manager import *

db_mngt = MySQLStationManagerAWS()

def get_available_stations(db_mngt):
    query = "SELECT * FROM bluetoothstations.station"\
            "WHERE latitude IS NOT NULL and longitude IS NOT NULL;"
    return db_mngt.execute_query(query)

