-- Create tables for the MES Engine

-- Table: counttype
-- This table stores valid count types for the MES Engine.
CREATE TABLE `mes_core`.`counttype` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `CountType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `CountType_UNIQUE` (`CountType` ASC) VISIBLE
);

-- Table: counttag
-- This table stores tag paths for counts in the MES Engine.
CREATE TABLE `mes_core`.`counttag` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `TagPath` VARCHAR(100) NOT NULL,
  `ParentID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `TagPath_UNIQUE` (`TagPath` ASC) VISIBLE
);

-- Table: counthistory
-- This table stores historical count data in the MES Engine.
CREATE TABLE `mes_core`.`counthistory` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `TagID` INT NOT NULL,
  `CountTypeID` INT NOT NULL,
  `Count` INT NOT NULL,
  `TimeStamp` DATETIME NOT NULL,
  `RunID` INT NULL,
  PRIMARY KEY (`ID`)
);
