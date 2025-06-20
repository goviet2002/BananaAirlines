import random
from datetime import datetime, timedelta

cities = [
    'BCN', 'FRA', 'BER', 'CDG', 'HAN', 'HND', 'ICN', 'JFK', 'PVG', 'IST', 'SVO', 'HNL', 'ATH',
    'LHR', 'DXB', 'SIN', 'SYD', 'LAX', 'YYZ', 'FCO', 'BKK', 'CPT', 'MEX'
]
aircrafts = [
    'BN1001', 'BN1002', 'BN1003', 'BN1004', 'BN1005', 'BN1006', 'BN1007', 'BN1008', 'BN1009', 'BN1010',
    'BN1011', 'BN1012', 'BN1013', 'BN1014', 'BN1015', 'BN1016',
    'BN2001', 'BN2002', 'BN2003', 'BN2004', 'BN2005', 'BN2006', 'BN2007', 'BN2008', 'BN2009', 'BN2010'
]

start_date = datetime(2025, 7, 1, 6, 0)
flight_sql = []
class_sql = []

for i in range(1000):
    src, dst = random.sample(cities, 2)
    aircraft = random.choice(aircrafts)
    dep_time = start_date + timedelta(days=random.randint(0, 550), hours=random.randint(0, 23), minutes=random.choice([0, 30]))
    arr_time = dep_time + timedelta(hours=random.randint(2, 14))
    distance = random.randint(800, 13000)
    flight_code = f'BN{3000+i:04d}'
    # Insert flight
    flight_sql.append(
        f'''INSERT INTO flight ("FlightCode", "SourceAirport", "DestinationAirport", "DepartureTime", "ArrivalTime", "Distance") VALUES
('{flight_code}', '{src}', '{dst}', '{dep_time.strftime('%Y-%m-%d %H:%M:%S')}', '{arr_time.strftime('%Y-%m-%d %H:%M:%S')}', {distance});'''
    )
    # Insert class
    price_economy = random.randint(100, 900)
    price_business = price_economy + random.randint(100, 500)
    price_first = price_business + random.randint(100, 500)
    class_sql.append(
        f'''INSERT INTO class ("flightID", "Price_Economy", "Price_Business", "Price_FirstClass") VALUES
('{flight_code}', {price_economy}, {price_business}, {price_first});'''
    )

# Write to files
with open('flights.sql', 'w', encoding='utf-8') as f:
    f.write('-- Flights\n')
    for s in flight_sql:
        f.write(s + '\n')

with open('classes.sql', 'w', encoding='utf-8') as f:
    f.write('-- Classes\n')
    for s in class_sql:
        f.write(s + '\n')

models = [
    'Boeing 737', 'Boeing 747', 'Boeing 757', 'Boeing 767', 'Boeing 777', 'Boeing 787',
    'Airbus A320', 'Airbus A321', 'Airbus A330', 'Airbus A340', 'Airbus A350', 'Airbus A380'
]

aircraft_sql = []
for i in range(1001, 4000):
    aircraft_id = f'BN{i:04d}'
    aircraft_name = random.choice(models)
    capacity = random.choice([180, 220, 240, 300, 330, 350, 370, 400, 410, 500])
    capacity_economy = int(capacity * random.uniform(0.6, 0.8))
    capacity_business = int(capacity * random.uniform(0.1, 0.2))
    capacity_first = capacity - capacity_economy - capacity_business
    aircraft_sql.append(
        f'''INSERT INTO aircraft ("AircraftID", "AircraftName", "Capacity", "Capacity_Economy", "Capacity_Business", "Capacity_FirstClass") VALUES
('{aircraft_id}', '{aircraft_name}', {capacity}, {capacity_economy}, {capacity_business}, {capacity_first});'''
    )

with open('aircrafts.sql', 'w', encoding='utf-8') as f:
    f.write('-- Aircrafts\n')
    for s in aircraft_sql:
        f.write(s + '\n')

print("SQL files 'flights.sql', 'classes.sql', and 'aircrafts.sql' have been created.")