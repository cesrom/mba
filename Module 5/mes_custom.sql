DROP TABLE IF EXISTS `nav_tree`;

SET @saved_cs_client = @@character_set_client;
SET character_set_client = utf8mb4;

CREATE TABLE `nav_tree` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `path` VARCHAR(1536) DEFAULT NULL,
    `text` VARCHAR(765) DEFAULT NULL,
    `type` VARCHAR(135) DEFAULT NULL,
    `security` VARCHAR(765) DEFAULT NULL,
    `command` VARCHAR(765) DEFAULT NULL,
    `icon` VARCHAR(765) DEFAULT NULL,
    `order` INT(10) DEFAULT NULL,
    `mode` VARCHAR(135) DEFAULT '',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;

SET character_set_client = @saved_cs_client;


DROP TABLE IF EXISTS `nav_tree_vars`;

SET @saved_cs_client = @@character_set_client;
SET character_set_client = utf8mb4;

CREATE TABLE `nav_tree_vars` (
    `nav_tree_new_id` INT(11) NOT NULL AUTO_INCREMENT,
    `property` VARCHAR(765) DEFAULT NULL,
    `value` VARCHAR(765) DEFAULT NULL,
    PRIMARY KEY (`nav_tree_new_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET character_set_client = @saved_cs_client;
SET TIME_ZONE = @@TIME_ZONE;

/* Additional settings */
SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;
SET CHARACTER_SET_CLIENT = @OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS = @OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION = @OLD_COLLATION_CONNECTION;
SET SQL_NOTES = @OLD_SQL_NOTES;
