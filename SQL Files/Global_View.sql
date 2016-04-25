-- MySQL Script generated by MySQL Workbench
-- Mon Apr 25 12:50:52 2016
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Model`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Model` (
  `model_id` INT NOT NULL,
  `price` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `gas_mileage` INT NOT NULL,
  `seat` INT NOT NULL,
  `engine` INT NOT NULL,
  PRIMARY KEY (`model_id`),
  UNIQUE INDEX `model_id_UNIQUE` (`model_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Add-on`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Add-on` (
  `package_id` INT NOT NULL,
  `price` VARCHAR(45) NOT NULL,
  `Add-oncol` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`package_id`),
  UNIQUE INDEX `package_id_UNIQUE` (`package_id` ASC),
  CONSTRAINT `model_id`
    FOREIGN KEY ()
    REFERENCES `mydb`.`Model` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Potential_Buyer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Potential_Buyer` (
  `buyer_no` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`buyer_no`),
  UNIQUE INDEX `buyer_no_UNIQUE` (`buyer_no` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Available_Auto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Available_Auto` (
  `serial_no` INT NOT NULL,
  `color` VARCHAR(45) NOT NULL,
  `dealer` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`serial_no`),
  UNIQUE INDEX `serial_no_UNIQUE` (`serial_no` ASC),
  CONSTRAINT `model_id`
    FOREIGN KEY ()
    REFERENCES `mydb`.`Model` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Employee` (
  `emp_no` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NOT NULL,
  `position` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`emp_no`),
  UNIQUE INDEX `emp_no_UNIQUE` (`emp_no` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Sales_Rep`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Sales_Rep` (
  `rep_no` INT NOT NULL,
  `base_salary` VARCHAR(45) NOT NULL,
  `ytd_sales` INT NOT NULL,
  `comm` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`rep_no`),
  UNIQUE INDEX `rep_no_UNIQUE` (`rep_no` ASC),
  CONSTRAINT `emp_no`
    FOREIGN KEY ()
    REFERENCES `mydb`.`Employee` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Customer_Global`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Customer_Global` (
  `customer_no` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`customer_no`),
  UNIQUE INDEX `customer_no_UNIQUE` (`customer_no` ASC),
  CONSTRAINT `buyer_no`
    FOREIGN KEY ()
    REFERENCES `mydb`.`Potential_Buyer` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Transaction` (
  `transaction_no` INT NOT NULL,
  `date` DATETIME NOT NULL,
  PRIMARY KEY (`transaction_no`),
  UNIQUE INDEX `transaction_no_UNIQUE` (`transaction_no` ASC),
  CONSTRAINT `rep_no`
    FOREIGN KEY ()
    REFERENCES `mydb`.`Sales_Rep` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `customer_no`
    FOREIGN KEY ()
    REFERENCES `mydb`.`Customer_Global` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `model_id`
    FOREIGN KEY ()
    REFERENCES `mydb`.`Model` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Rebate_Global`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Rebate_Global` (
  `rebate_no` INT NOT NULL,
  `amount` VARCHAR(45) NOT NULL,
  `dealer` VARCHAR(45) NOT NULL,
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  PRIMARY KEY (`rebate_no`),
  UNIQUE INDEX `rebate_no_UNIQUE` (`rebate_no` ASC),
  CONSTRAINT `model_id`
    FOREIGN KEY ()
    REFERENCES `mydb`.`Model` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
