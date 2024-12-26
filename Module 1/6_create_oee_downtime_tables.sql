-- =====================================================================
-- MES Core Tables for Bootcamp Accelerator
-- =====================================================================
-- This script creates all the necessary tables for the MES Bootcamp
-- Accelerator. These tables support the core MES functionality, 
-- including count tracking, state reasons, and state history.
-- Foreign keys are omitted for now and will be added later.

-- =====================================================================
-- Table: counttype
-- Defines different types of counts for the MES Engine.
-- =====================================================================
CREATE TABLE `mes_core`.`counttype` (
  `ID` INT NOT NULL AUTO_INCREMENT,         -- Primary Key
  `CountType` VARCHAR(45) NOT NULL,         -- Name of the count type (e.g., Good, Reject)
  PRIMARY KEY (`ID`),                       -- Ensures unique identification for each record
  UNIQUE INDEX `CountType_UNIQUE` (`CountType` ASC) VISIBLE -- Prevents duplicate count types
);

-- =====================================================================
-- Table: counttag
-- Stores tag paths associated with counts in the MES Engine.
-- =====================================================================
CREATE TABLE `mes_core`.`counttag` (
  `ID` INT NOT NULL AUTO_INCREMENT,         -- Primary Key
  `TagPath` VARCHAR(100) NOT NULL,          -- Tag path for the count
  `ParentID` INT NOT NULL,                  -- References the count type (foreign key to be added later)
  PRIMARY KEY (`ID`),                       -- Ensures unique identification for each record
  UNIQUE INDEX `TagPath_UNIQUE` (`TagPath` ASC) VISIBLE -- Prevents duplicate tag paths
);

-- =====================================================================
-- Table: counthistory
-- Records the count history, including metadata such as timestamps.
-- =====================================================================
CREATE TABLE `mes_core`.`counthistory` (
  `ID` INT NOT NULL AUTO_INCREMENT,         -- Primary Key
  `TagID` INT NOT NULL,                     -- References the tag associated with this count (foreign key to be added later)
  `CountTypeID` INT NOT NULL,               -- References the count type (foreign key to be added later)
  `Count` INT NOT NULL,                     -- Numeric count value
  `TimeStamp` DATETIME NOT NULL,            -- Timestamp when the count occurred
  `RunID` INT NULL,                         -- References the production run (foreign key to be added later)
  PRIMARY KEY (`ID`)                        -- Ensures unique identification for each record
);

-- =====================================================================
-- Table: statereason
-- Defines state reasons for the MES Engine, including downtime reasons.
-- =====================================================================
CREATE TABLE `mes_core`.`statereason` (
  `ID` INT NOT NULL AUTO_INCREMENT,         -- Primary Key
  `ParentID` INT NOT NULL,                  -- References a parent state or category
  `ReasonName` VARCHAR(45) NOT NULL,        -- Name of the state reason
  `ReasonCode` INT NOT NULL,                -- Unique code for the reason
  `RecordDowntime` TINYINT NOT NULL DEFAULT 0, -- Indicates whether downtime is recorded
  `PlannedDowntime` TINYINT NOT NULL DEFAULT 0, -- Indicates planned downtime
  `OperatorSelectable` TINYINT NOT NULL DEFAULT 0, -- Indicates if the reason is operator-selectable
  `SubReasonOf` INT NULL,                   -- References a parent reason if this is a sub-reason
  PRIMARY KEY (`ID`)                        -- Ensures unique identification for each record
);

-- =====================================================================
-- Table: statehistory
-- Records state history events, referencing state reasons.
-- =====================================================================
CREATE TABLE `mes_core`.`statehistory` (
  `ID` INT NOT NULL AUTO_INCREMENT,         -- Primary Key, unique identifier for each record
  `StateReasonID` INT NOT NULL,             -- References the state reason associated with this history (foreign key can be added later)
  `StartDateTime` DATETIME NOT NULL,        -- Start timestamp of the state
  `EndDateTime` DATETIME NOT NULL,          -- End timestamp of the state
  `Note` VARCHAR(100) NULL,                 -- Optional notes or comments about the state
  `LineID` INT NOT NULL,                    -- References the line where the state occurred (foreign key can be added later)
  `RunID` INT NOT NULL,                     -- References the production run (foreign key can be added later)
  PRIMARY KEY (`ID`)                        -- Ensures unique identification for each record
);
