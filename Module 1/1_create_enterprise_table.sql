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
