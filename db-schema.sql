-- MySQL Workbench Forward Engineering
SET
    @OLD_UNIQUE_CHECKS = @ @UNIQUE_CHECKS,
    UNIQUE_CHECKS = 0;

SET
    @OLD_FOREIGN_KEY_CHECKS = @ @FOREIGN_KEY_CHECKS,
    FOREIGN_KEY_CHECKS = 0;

SET
    @OLD_SQL_MODE = @ @SQL_MODE,
    SQL_MODE = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema b9sglba6s5iczo7pb6zf
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema b9sglba6s5iczo7pb6zf
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `b9sglba6s5iczo7pb6zf` DEFAULT CHARACTER SET utf8;

USE `b9sglba6s5iczo7pb6zf`;

-- -----------------------------------------------------
-- Table `b9sglba6s5iczo7pb6zf`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `b9sglba6s5iczo7pb6zf`.`users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) UNIQUE NOT NULL,
    `email` VARCHAR(255) UNIQUE NOT NULL,
    `photo` VARCHAR(255) NULL,
    `password` VARCHAR(255) NOT NULL,
    `password_changed_at` TIMESTAMP NULL,
    `password_reset_token` VARCHAR(255) NULL,
    `password_reset_expires` VARCHAR(255) NULL,
    PRIMARY KEY (`id`)
);

-- -----------------------------------------------------
-- Table `b9sglba6s5iczo7pb6zf`.`roses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `b9sglba6s5iczo7pb6zf`.`roses` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `photo` VARCHAR(255) NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;

SET
    SQL_MODE = @OLD_SQL_MODE;

SET
    FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;

SET
    UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;