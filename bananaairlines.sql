-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.11.3-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for bananaairlines
CREATE DATABASE IF NOT EXISTS `bananaairlines` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `bananaairlines`;

-- Dumping structure for table bananaairlines.aircraft
CREATE TABLE IF NOT EXISTS `aircraft` (
  `AircraftID` varchar(50) NOT NULL DEFAULT '',
  `AircraftName` varchar(50) NOT NULL,
  `Capacity` int(11) NOT NULL,
  `Capacity_Economy` int(11) DEFAULT NULL,
  `Capacity_Business` int(11) DEFAULT NULL,
  `Capacity_FirstClass` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`AircraftID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table bananaairlines.aircraft: ~13 rows (approximately)
INSERT INTO `aircraft` (`AircraftID`, `AircraftName`, `Capacity`, `Capacity_Economy`, `Capacity_Business`, `Capacity_FirstClass`) VALUES
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

-- Dumping structure for table bananaairlines.cities
CREATE TABLE IF NOT EXISTS `cities` (
  `City` varchar(50) NOT NULL,
  `Code` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table bananaairlines.cities: ~12 rows (approximately)
INSERT INTO `cities` (`City`, `Code`) VALUES
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

-- Dumping structure for table bananaairlines.class
CREATE TABLE IF NOT EXISTS `class` (
  `flightID` varchar(50) NOT NULL,
  `Price_Economy` int(11) NOT NULL DEFAULT 0,
  `Price_Business` int(11) NOT NULL DEFAULT 0,
  `Price_FirstClass` int(11) DEFAULT 0,
  KEY `FK_class_flight` (`flightID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table bananaairlines.class: ~12 rows (approximately)
INSERT INTO `class` (`flightID`, `Price_Economy`, `Price_Business`, `Price_FirstClass`) VALUES
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

-- Dumping structure for table bananaairlines.client
CREATE TABLE IF NOT EXISTS `client` (
  `ClientID` varchar(10) NOT NULL DEFAULT '',
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `MilesEarned` int(11) NOT NULL DEFAULT 0,
  `Tier` varchar(50) NOT NULL DEFAULT 'Bronze',
  `Birthdate` date NOT NULL,
  `Gender` varchar(50) NOT NULL,
  `MobileNumber` varchar(50) NOT NULL,
  `Country` varchar(50) NOT NULL,
  PRIMARY KEY (`Email`),
  KEY `FK_client_offer` (`Tier`),
  KEY `FK_client_user` (`ClientID`),
  CONSTRAINT `FK_client_offer` FOREIGN KEY (`Tier`) REFERENCES `offer` (`Tier`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_client_user` FOREIGN KEY (`ClientID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping structure for table bananaairlines.employee
CREATE TABLE IF NOT EXISTS `employee` (
  `EmployeeID` varchar(10) NOT NULL DEFAULT '',
  `FirstName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`EmployeeID`),
  CONSTRAINT `FK_employee_user` FOREIGN KEY (`EmployeeID`) REFERENCES `user` (`UserID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table bananaairlines.employee: ~0 rows (approximately)
INSERT INTO `employee` (`EmployeeID`, `FirstName`, `LastName`, `Email`) VALUES
	('BOSS', 'Viet', 'Ngo', 'viet@banana.airlines');

-- Dumping structure for table bananaairlines.flight
CREATE TABLE IF NOT EXISTS `flight` (
  `FlightCode` varchar(50) NOT NULL,
  `SourceAirport` varchar(50) NOT NULL,
  `DestinationAirport` varchar(50) NOT NULL,
  `DepartureTime` timestamp NOT NULL,
  `ArrivalTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `Distance` int(11) NOT NULL,
  PRIMARY KEY (`FlightCode`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table bananaairlines.flight: ~13 rows (approximately)
INSERT INTO `flight` (`FlightCode`, `SourceAirport`, `DestinationAirport`, `DepartureTime`, `ArrivalTime`, `Distance`) VALUES
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

-- Dumping structure for table bananaairlines.offer
CREATE TABLE IF NOT EXISTS `offer` (
  `Tier` varchar(50) NOT NULL DEFAULT '',
  `Offers` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`Tier`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table bananaairlines.offer: ~3 rows (approximately)
INSERT INTO `offer` (`Tier`, `Offers`) VALUES
	('Bronze', 'BR2024'),
	('Gold', 'GD2024'),
	('Silver', 'SV2024');

-- Dumping structure for table bananaairlines.ticket
CREATE TABLE IF NOT EXISTS `ticket` (
  `TicketID` varchar(50) NOT NULL DEFAULT '',
  `UserID` varchar(50) DEFAULT NULL,
  `PurchaseDate` date NOT NULL,
  `FlightCode` varchar(50) NOT NULL,
  `Class` varchar(50) NOT NULL DEFAULT '0',
  `CheckIn` int(11) NOT NULL DEFAULT 0,
  `Baggage` int(11) NOT NULL DEFAULT 0,
  `Paid` float NOT NULL DEFAULT 0,
  `Status` varchar(50) NOT NULL,
  `Request` int(11) NOT NULL,
  `Reason` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`TicketID`),
  KEY `FK_ticket_flight` (`FlightCode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping structure for event bananaairlines.update_ticket_status
DELIMITER //
CREATE EVENT `update_ticket_status` ON SCHEDULE EVERY 1 MINUTE STARTS '2023-09-27 22:27:02' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE ticket
  INNER JOIN flight ON ticket.FlightCode = flight.FlightCode
  SET ticket.Status = 'Finished'
  WHERE flight.DepartureTime < NOW()//
DELIMITER ;

-- Dumping structure for table bananaairlines.user
CREATE TABLE IF NOT EXISTS `user` (
  `username` varchar(50) NOT NULL,
  `UserID` varchar(10) NOT NULL DEFAULT '',
  `password` varchar(50) NOT NULL,
  `UserType` varchar(50) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table bananaairlines.user: ~8 rows (approximately)
INSERT INTO `user` (`username`, `UserID`, `password`, `UserType`) VALUES
	('admin_boss', 'BOSS', '123', 'Employee'),

-- Dumping structure for trigger bananaairlines.check_times
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER check_times
BEFORE UPDATE ON flight
FOR EACH ROW
BEGIN
  IF NEW.DepartureTime > NEW.ArrivalTime THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Departure time cannot be later than arrival time';
  END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger bananaairlines.clear_reason
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER clear_reason
BEFORE UPDATE ON ticket
FOR EACH ROW
BEGIN
    IF NEW.Request = 0 THEN
        SET NEW.Reason = NULL;
    END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger bananaairlines.FlightCancellation
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER FlightCancellation
AFTER DELETE ON flight
FOR EACH ROW
BEGIN
    UPDATE ticket
    SET Status = 'Flight Cancelled'
    WHERE FlightCode = OLD.FlightCode;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger bananaairlines.FlightInsertion
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER FlightInsertion
AFTER INSERT ON flight
FOR EACH ROW
BEGIN
    UPDATE ticket
    SET Status = 'Operating'
    WHERE FlightCode = NEW.FlightCode;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger bananaairlines.update_tier
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER update_tier
BEFORE UPDATE ON client
FOR EACH ROW
BEGIN
    IF NEW.MilesEarned < 10000 THEN
        SET NEW.Tier = 'Bronze';
    ELSEIF NEW.MilesEarned >= 10000 AND NEW.MilesEarned < 20000 THEN
        SET NEW.Tier = 'Silver';
    ELSEIF NEW.MilesEarned >= 20000 THEN
        SET NEW.Tier = 'Gold';
    END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger bananaairlines.update__insert_tier
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER update__insert_tier
	BEFORE INSERT ON client 
	FOR EACH ROW
	BEGIN
	    IF NEW.MilesEarned < 10000 THEN
	        SET NEW.Tier = 'Bronze';
	    ELSEIF NEW.MilesEarned >= 10000 AND NEW.MilesEarned < 20000 THEN
	        SET NEW.Tier = 'Silver';
	    ELSE
	        SET NEW.Tier = 'Gold';
	    END IF;
	END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
