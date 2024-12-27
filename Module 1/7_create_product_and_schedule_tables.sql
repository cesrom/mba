-- =====================================================================
-- MES Work Order Tables
-- =====================================================================
-- This script creates tables related to work orders and their management
-- in the MES system. These tables are used to track work order details,
-- production quantities, product codes, and timestamps.
-- =====================================================================

-- =====================================================================
-- Table: workorder
-- Stores work order information, including quantity, status, and product details.
-- =====================================================================
CREATE TABLE `mes_core`.`workorder` (
  `ID` INT NOT NULL AUTO_INCREMENT,          -- Primary Key
  `WorkOrder` VARCHAR(100) NOT NULL,         -- Unique identifier for the work order
  `Quantity` INT NOT NULL,                   -- Total quantity associated with the work order
  `Closed` TINYINT NULL,                     -- Indicates if the work order is closed (1 = closed, 0 = open)
  `Hide` TINYINT NULL DEFAULT 0,             -- Determines if the work order should be hidden in the UI
  `TimeStamp` DATETIME NOT NULL,             -- Timestamp when the work order was created or updated
  `ProductCodeID` INT NOT NULL,              -- References the product associated with this work order (foreign key can be added later)
  `ProductCode` VARCHAR(100) NOT NULL,       -- Code representing the product for the work order
  PRIMARY KEY (`ID`),                        -- Ensures unique identification for each record
  UNIQUE INDEX `WorkOrder_UNIQUE` (`WorkOrder` ASC) VISIBLE -- Prevents duplicate work orders
);

-- =====================================================================
-- Table: productcode
-- Stores product code information, including descriptions and status.
-- =====================================================================
CREATE TABLE `mes_core`.`productcode` (
  `ID` INT NOT NULL AUTO_INCREMENT,          -- Primary Key
  `ProductCode` VARCHAR(100) NOT NULL,       -- Unique identifier for the product
  `Description` VARCHAR(255) NULL,           -- Description of the product
  `Disable` TINYINT NULL DEFAULT 0,          -- Determines if the product code is disabled (1 = disabled, 0 = enabled)
  `TimeStamp` DATETIME NOT NULL,             -- Timestamp when the product code was created or updated
  PRIMARY KEY (`ID`)                         -- Ensures unique identification for each record
);

-- =====================================================================
-- Table: productcodeline
-- Links product codes to specific production lines and tracks their
-- enablement status and timestamps.
-- =====================================================================
CREATE TABLE `mes_core`.`productcodeline` (
  `ID` INT NOT NULL AUTO_INCREMENT,          -- Primary Key
  `ProductCodeID` INT NOT NULL,              -- Foreign key to the productcode table (to be defined later)
  `LineID` INT NOT NULL,                     -- Foreign key to the line table (to be defined later)
  `Enable` TINYINT NOT NULL DEFAULT 1,       -- Indicates if the product is enabled on the line (1 = enabled, 0 = disabled)
  `TimeStamp` DATETIME NOT NULL,             -- Timestamp for when the record was created or updated
  PRIMARY KEY (`ID`)                         -- Ensures unique identification for each record
);

-- =====================================================================
-- Table: schedule
-- Stores scheduling information for production lines, including details
-- about work orders, planned schedules, actual outcomes, and timestamps.
-- =====================================================================
CREATE TABLE `mes_core`.`schedule` (
  `ID` INT NOT NULL AUTO_INCREMENT,                 -- Primary Key
  `LineID` INT NOT NULL,                            -- Foreign key to the line table (to be defined later)
  `WorkOrderID` INT NOT NULL,                       -- Foreign key to the workorder table (to be defined later)
  `ScheduleType` INT NOT NULL,                      -- Type of schedule (e.g., planned, maintenance)
  `Note` VARCHAR(255) NULL,                         -- Optional notes related to the schedule
  `ScheduleStartDateTime` DATETIME NOT NULL,        -- Planned start date and time for the schedule
  `ScheduleFinishDateTime` DATETIME NOT NULL,       -- Planned finish date and time for the schedule
  `Quantity` INT NOT NULL,                          -- Quantity planned for the schedule
  `EnteredBy` VARCHAR(45) NULL,                     -- User who entered the schedule
  `TimeStamp` DATETIME NULL,                        -- Timestamp for when the record was created or updated
  `RunID` INT NULL,                                 -- Identifier for the associated production run
  `ActualStartDateTime` DATETIME NULL,              -- Actual start date and time for the schedule
  `ActualFinishDateTime` DATETIME NULL,             -- Actual finish date and time for the schedule
  `ActualQuantity` INT NULL,                        -- Actual quantity achieved during the schedule
  `RunStartDateTime` DATETIME NULL,                 -- Start time of the associated production run
  PRIMARY KEY (`ID`)                                -- Ensures unique identification for each record
);

-- This table stores detailed information about production runs
-- and their associated metrics within the MES system.

CREATE TABLE `mes_core`.`run` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `ScheduleID` INT NOT NULL,
  `RunStartDateTime` DATETIME NULL,
  `RunStopDateTime` DATETIME NULL,
  `StartInfeed` INT NULL,
  `CurrentInfeed` INT NULL,
  `StartOutfeed` INT NULL,
  `CurrentOutfeed` INT NULL,
  `StartWaste` INT NULL,
  `CurrentWaste` INT NULL,
  `TotalCount` INT NULL,
  `WasteCount` INT NULL,
  `GoodCount` INT NULL,
  `Availability` REAL NULL,
  `Performance` REAL NULL,
  `Quality` REAL NULL,
  `OEE` REAL NULL,
  `SetupStartDateTime` DATETIME NULL,
  `SetupEndDateTime` DATETIME NULL,
  `RunTime` INT NULL,
  `UnplannedDowntime` INT NULL,
  `PlannedDowntime` INT NULL,
  `TotalTime` INT NULL,
  `TimeStamp` DATETIME NULL,
  `Closed` TINYINT NULL DEFAULT 0,
  `EstimatedFinishedTime` DATETIME NULL,
  PRIMARY KEY (`ID`)
);
