-- This table stores enterprise-level data for the MES system,
-- including a primary ID, name, timestamp, 
-- and a flag for active/disabled status.
CREATE TABLE `mes_core`.`enterprise` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `TimeStamp` DATETIME NOT NULL,
  `Disable` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `Name_UNIQUE` (`Name` ASC) VISIBLE
);

-- This table stores site-level data in the MES system.
-- The `ParentID` column references the enterprise table
-- (foreign key to be added later as homework).
CREATE TABLE `mes_core`.`site` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `TimeStamp` DATETIME NOT NULL,
  `Disable` TINYINT NULL DEFAULT 0,
  `ParentID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `Name_UNIQUE` (`Name` ASC) VISIBLE
);


-- This table stores area-level data in the MES system.
-- The `ParentID` column references the site table 
-- (foreign key to be added later as homework).
CREATE TABLE `mes_core`.`area` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `TimeStamp` DATETIME NOT NULL,
  `Disable` TINYINT NULL DEFAULT 0,
  `ParentID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `Name_UNIQUE` (`Name` ASC) VISIBLE
);

-- This table stores line-level data in the MES system.
-- The `ParentID` column references the area table
-- (foreign key to be added later as homework).
CREATE TABLE `mes_core`.`line` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `TimeStamp` DATETIME NOT NULL,
  `Disable` TINYINT NULL DEFAULT 0,
  `ParentID` INT NOT NULL,
  PRIMARY KEY (`ID`)
);


-- This table stores cell-level data in the MES system.
-- The `ParentID` column references the line table
-- (foreign key to be added later as homework).
CREATE TABLE `mes_core`.`cell` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `TimeStamp` DATETIME NOT NULL,
  `Disable` TINYINT DEFAULT '0',
  `ParentID` INT NOT NULL,
  PRIMARY KEY (`ID`)
);
