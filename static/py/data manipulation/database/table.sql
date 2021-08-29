# MySQL version 8.026

# drop database house_price;

# 建库
create database house_price;

# 设置默认数据库
use house_price;

# 添加数据表
CREATE TABLE `houses` (
  `HouseID` int unsigned NOT NULL,
  `HouseName` varchar(45) DEFAULT NULL,
  `Price` varchar(45) DEFAULT NULL,
  `UnitPrice` varchar(45) DEFAULT NULL,
  `RoomType` varchar(45) DEFAULT NULL,
  `Floor` varchar(45) DEFAULT NULL,
  `Direction` varchar(45) DEFAULT NULL,
  `HouseType` varchar(45) DEFAULT NULL,
  `Area` varchar(45) DEFAULT NULL,
  `Years` varchar(45) DEFAULT NULL,
  `Community` varchar(45) DEFAULT NULL,
  `Region` varchar(45) DEFAULT NULL,
  `Longitude` varchar(45) DEFAULT NULL,
  `Latitude` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`HouseID`),
  UNIQUE KEY `HouseID_UNIQUE` (`HouseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `infrastructures` (
  `PointID` int unsigned NOT NULL AUTO_INCREMENT,
  `PointName` varchar(45) DEFAULT NULL,
  `PointType` varchar(45) DEFAULT NULL,
  `Longitude` varchar(45) DEFAULT NULL,
  `Latitude` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`PointID`),
  UNIQUE KEY `PointID_UNIQUE` (`PointID`)
) ENGINE=InnoDB AUTO_INCREMENT=4468 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `records` (
  `RecordID` int unsigned NOT NULL AUTO_INCREMENT,
  `TrafficIndex` int unsigned DEFAULT NULL,
  `EducationIndex` int unsigned DEFAULT NULL,
  `EnvironmentIndex` int unsigned DEFAULT NULL,
  `DistrictIndex` int unsigned DEFAULT NULL,
  PRIMARY KEY (`RecordID`),
  UNIQUE KEY `HouseID_UNIQUE` (`RecordID`),
  CONSTRAINT `records_houses` FOREIGN KEY (`RecordID`) REFERENCES `houses` (`HouseID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19305 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `users` (
  `UserID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserName` varchar(45) DEFAULT NULL,
  `Password` varchar(45) DEFAULT NULL,
  `Permission` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `UserID_UNIQUE` (`UserID`),
  UNIQUE KEY `UserName_UNIQUE` (`UserName`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

# 创建新用户，设置用户权限
CREATE USER 'sys_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'user_password';
GRANT ALL PRIVILEGES ON house_price.* TO 'sys_user'@'localhost' WITH GRANT OPTION;

# 刷新权限
FLUSH PRIVILEGES;