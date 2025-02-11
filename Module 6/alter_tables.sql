
-- allow the product code ID to be null
-- run this code against your mes_core database
ALTER TABLE `mes_core`.`workorder` 
CHANGE COLUMN `ProductCodeID` `ProductCodeID` INT NULL ;



-- alter the schedule table ScheduleType datatype to VARCHAR(45)
ALTER TABLE `mes_core`.`schedule` 
CHANGE COLUMN `ScheduleType` `ScheduleType` VARCHAR(45) NOT NULL ;
