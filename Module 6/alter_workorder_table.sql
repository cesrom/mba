
-- allow the product code ID to be null
-- run this code against your mes_core database
ALTER TABLE `mes_core`.`workorder` 
CHANGE COLUMN `ProductCodeID` `ProductCodeID` INT NULL ;
