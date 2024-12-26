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
