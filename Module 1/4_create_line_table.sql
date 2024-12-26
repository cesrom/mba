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
