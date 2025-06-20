-- PostgreSQL schema for bananaairlines

-- Table: aircraft
CREATE TABLE IF NOT EXISTS aircraft (
  "AircraftID" VARCHAR(50) PRIMARY KEY,
  "AircraftName" VARCHAR(50) NOT NULL,
  "Capacity" INTEGER NOT NULL,
  "Capacity_Economy" INTEGER,
  "Capacity_Business" INTEGER,
  "Capacity_FirstClass" INTEGER NOT NULL DEFAULT 0
);

INSERT INTO aircraft ("AircraftID", "AircraftName", "Capacity", "Capacity_Economy", "Capacity_Business", "Capacity_FirstClass") VALUES
  ('BN1001', 'Boeing 737', 400, 346, 30, 0),
  ('BN1002', 'Airbus A350', 330, 296, 13, 0),
  ('BN1003', 'Boeing 777', 400, 349, 46, 0),
  ('BN1004', 'Airbus A330', 300, 269, 26, 0),
  ('BN1005', 'Beoing 747', 300, 249, 30, 20),
  ('BN1006', 'Boeing 787', 500, 396, 30, 50),
  ('BN1007', 'Boeing 777', 300, 250, 27, 20),
  ('BN1008', 'Beoing 737', 300, 249, 50, 0),
  ('BN1009', 'Airbus A350', 400, 299, 45, 50),
  ('BN1010', 'Airbus A321', 330, 299, 27, 0),
  ('BN1011', 'Airbus A321', 250, 199, 45, 2),
  ('BN1012', 'Airbus A350', 350, 300, 27, 21),
  ('BN1013', 'Airbus A380', 400, 299, 45, 50),
  ('BN1014', 'Boeing 737', 400, 346, 30, 0),
  ('BN1015', 'Airbus A350', 330, 296, 13, 0),
  ('BN1016', 'Boeing 777', 400, 349, 46, 0);

-- Table: cities
CREATE TABLE IF NOT EXISTS cities (
  "City" VARCHAR(50) NOT NULL,
  "Code" VARCHAR(50) PRIMARY KEY
);

INSERT INTO cities ("City", "Code") VALUES
  ('Barcelona', 'BCN'),
  ('Frankfurt', 'FRA'),
  ('Berlin', 'BER'),
  ('Paris', 'CDG'),
  ('Hanoi', 'HAN'),
  ('Tokyo', 'HND'),
  ('Seoul', 'ICN'),
  ('New York', 'JFK'),
  ('Shanghai', 'PVG'),
  ('Istanbul', 'IST'),
  ('Moscow', 'SVO'),
  ('Hawaii', 'HNL'),
  ('Athens', 'ATH');

-- Table: offer
CREATE TABLE IF NOT EXISTS offer (
  "Tier" VARCHAR(50) PRIMARY KEY,
  "Offers" VARCHAR(10000)
);

INSERT INTO offer ("Tier", "Offers") VALUES
  ('Bronze', 'BR2024'),
  ('Gold', 'GD2024'),
  ('Silver', 'SV2024');

-- Table: user
CREATE TABLE IF NOT EXISTS "user" (
  "username" VARCHAR(50) NOT NULL,
  "UserID" VARCHAR(10) PRIMARY KEY,
  "password" VARCHAR(50) NOT NULL,
  "UserType" VARCHAR(50) NOT NULL
);

INSERT INTO "user" ("username", "UserID", "password", "UserType") VALUES
  ('admin_boss', 'BOSS', '123', 'Employee');

-- Table: employee
CREATE TABLE IF NOT EXISTS employee (
  "EmployeeID" VARCHAR(10) PRIMARY KEY,
  "FirstName" VARCHAR(50),
  "LastName" VARCHAR(50),
  "Email" VARCHAR(50),
  CONSTRAINT fk_employee_user FOREIGN KEY ("EmployeeID") REFERENCES "user" ("UserID")
);

INSERT INTO employee ("EmployeeID", "FirstName", "LastName", "Email") VALUES
  ('BOSS', 'Viet', 'Ngo', 'viet@banana.airlines');

-- Table: client
CREATE TABLE IF NOT EXISTS client (
  "ClientID" VARCHAR(10) NOT NULL,
  "FirstName" VARCHAR(50) NOT NULL,
  "LastName" VARCHAR(50) NOT NULL,
  "Email" VARCHAR(50) PRIMARY KEY,
  "MilesEarned" INTEGER NOT NULL DEFAULT 0,
  "Tier" VARCHAR(50) NOT NULL DEFAULT 'Bronze',
  "Birthdate" DATE NOT NULL,
  "Gender" VARCHAR(50) NOT NULL,
  "MobileNumber" VARCHAR(50) NOT NULL,
  "Country" VARCHAR(50) NOT NULL,
  CONSTRAINT fk_client_offer FOREIGN KEY ("Tier") REFERENCES offer ("Tier"),
  CONSTRAINT fk_client_user FOREIGN KEY ("ClientID") REFERENCES "user" ("UserID") ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table: flight
CREATE TABLE IF NOT EXISTS flight (
  "FlightCode" VARCHAR(50) PRIMARY KEY,
  "SourceAirport" VARCHAR(50) NOT NULL,
  "DestinationAirport" VARCHAR(50) NOT NULL,
  "DepartureTime" TIMESTAMP NOT NULL,
  "ArrivalTime" TIMESTAMP NOT NULL,
  "Distance" INTEGER NOT NULL
);

INSERT INTO flight ("FlightCode", "SourceAirport", "DestinationAirport", "DepartureTime", "ArrivalTime", "Distance") VALUES
  ('BN1001', 'FRA', 'BCN', '2025-03-15 09:00:00', '2025-03-15 11:00:00', 1300),
  ('BN1002', 'BER', 'CDG', '2025-06-10 14:30:00', '2025-06-10 16:00:00', 1050),
  ('BN1003', 'HAN', 'HND', '2025-09-20 20:00:00', '2025-09-21 04:00:00', 3700),
  ('BN1004', 'JFK', 'IST', '2025-12-05 18:00:00', '2025-12-06 10:00:00', 8000),
  ('BN1005', 'PVG', 'SVO', '2026-02-22 07:00:00', '2026-02-22 13:00:00', 6500),
  ('BN1006', 'ICN', 'ATH', '2026-05-18 12:00:00', '2026-05-18 18:00:00', 8000),
  ('BN1007', 'CDG', 'HNL', '2026-08-30 23:00:00', '2026-08-31 09:00:00', 12000),
  ('BN1008', 'IST', 'BER', '2026-11-11 06:00:00', '2026-11-11 08:30:00', 1750),
  ('BN1009', 'BCN', 'FRA', '2027-01-25 15:00:00', '2027-01-25 17:00:00', 1300),
  ('BN1010', 'HND', 'HAN', '2027-04-14 21:00:00', '2027-04-15 01:00:00', 3700),
  ('BN1011', 'ATH', 'ICN', '2027-07-19 10:00:00', '2027-07-19 18:00:00', 8000),
  ('BN1012', 'SVO', 'PVG', '2027-10-03 08:00:00', '2027-10-03 14:00:00', 6500),
  ('BN1013', 'HNL', 'CDG', '2028-01-12 20:00:00', '2028-01-13 06:00:00', 12000),
  ('BN1014', 'FRA', 'JFK', '2028-04-22 13:00:00', '2028-04-22 19:00:00', 6200),
  ('BN1015', 'BCN', 'BER', '2028-07-08 09:30:00', '2028-07-08 11:30:00', 1500),
  ('BN1016', 'HAN', 'IST', '2028-10-17 22:00:00', '2028-10-18 04:00:00', 7500);

-- Table: class
CREATE TABLE IF NOT EXISTS class (
  "flightID" VARCHAR(50) NOT NULL,
  "Price_Economy" INTEGER NOT NULL DEFAULT 0,
  "Price_Business" INTEGER NOT NULL DEFAULT 0,
  "Price_FirstClass" INTEGER DEFAULT 0,
  CONSTRAINT fk_class_flight FOREIGN KEY ("flightID") REFERENCES flight ("FlightCode")
);

INSERT INTO class ("flightID", "Price_Economy", "Price_Business", "Price_FirstClass") VALUES
  ('BN1001', 120, 220, 320),
  ('BN1002', 340, 420, 500),
  ('BN1003', 220, 420, 620),
  ('BN1004', 620, 1020, 1520),
  ('BN1005', 220, 520, 720),
  ('BN1006', 220, 420, 620),
  ('BN1007', 370, 520, 720),
  ('BN1008', 820, 1320, 1620),
  ('BN1009', 120, 220, 320),
  ('BN1010', 320, 520, 720),
  ('BN1011', 420, 720, 1020),
  ('BN1012', 220, 420, 620),
  ('BN1013', 220, 520, 720),
  ('BN1014', 150, 250, 350),
  ('BN1015', 200, 300, 400),
  ('BN1016', 250, 350, 450);

-- Table: ticket
CREATE TABLE IF NOT EXISTS ticket (
  "TicketID" VARCHAR(50) PRIMARY KEY,
  "UserID" VARCHAR(50),
  "PurchaseDate" DATE NOT NULL,
  "FlightCode" VARCHAR(50) NOT NULL,
  "Class" VARCHAR(50) NOT NULL DEFAULT '0',
  "CheckIn" INTEGER NOT NULL DEFAULT 0,
  "Baggage" INTEGER NOT NULL DEFAULT 0,
  "Paid" FLOAT NOT NULL DEFAULT 0,
  "Status" VARCHAR(50) NOT NULL,
  "Request" INTEGER NOT NULL,
  "Reason" VARCHAR(1000),
  CONSTRAINT fk_ticket_flight FOREIGN KEY ("FlightCode") REFERENCES flight ("FlightCode")
);

-- Triggers and events are not included, as Supabase/PostgreSQL does not support MySQL-style triggers/events in the same way.