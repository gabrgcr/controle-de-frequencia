-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema controle_de_frequencia_db
-- -----------------------------------------------------
-- Banco de dados de controle de frequencia para o PI I Eixo Computação da UNIVESP, turma 2021.2
-- 
-- Turma 010, UniCEU Vila Atlantica

-- -----------------------------------------------------
-- Schema controle_de_frequencia_db
--
-- Banco de dados de controle de frequencia para o PI I Eixo Computação da UNIVESP, turma 2021.2
-- 
-- Turma 010, UniCEU Vila Atlantica
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `controle_de_frequencia_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `controle_de_frequencia_db` ;

-- -----------------------------------------------------
-- Table `controle_de_frequencia_db`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `controle_de_frequencia_db`.`usuario` (
  `username` VARCHAR(100) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tipo_usuario` VARCHAR(45) NOT NULL,
  `nome` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`username`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `controle_de_frequencia_db`.`dia_letivo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `controle_de_frequencia_db`.`dia_letivo` (
  `id` INT AUTO_INCREMENT,
  `dia` INT NOT NULL,
  `mes` INT NOT NULL,
  `ano` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `LETIVO_UNICO` (`dia` ASC, `mes` ASC, `ano` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `controle_de_frequencia_db`.`turma`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `controle_de_frequencia_db`.`turma` (
  `turma` VARCHAR(2) NOT NULL,
  `ano_letivo` VARCHAR(4) NOT NULL,
  `id` INT AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `turma_unico` (`ano_letivo` ASC, `turma` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `controle_de_frequencia_db`.`aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `controle_de_frequencia_db`.`aluno` (
  `id` INT AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  `fk_turma` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_aluno_turma_idx` (`fk_turma` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `fk_aluno_turma`
    FOREIGN KEY (`fk_turma`)
    REFERENCES `controle_de_frequencia_db`.`turma` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `controle_de_frequencia_db`.`responsavel_aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `controle_de_frequencia_db`.`responsavel_aluno` (
  `nome` VARCHAR(45) NULL,
  `relacao` VARCHAR(45) NULL,
  `telefone` VARCHAR(45) NULL,
  `endereco` VARCHAR(45) NULL,
  `id` INT AUTO_INCREMENT,
  `fk_aluno` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_responsavel_aluno_aluno1_idx` (`fk_aluno` ASC) VISIBLE,
  CONSTRAINT `fk_responsavel_aluno_aluno1`
    FOREIGN KEY (`fk_aluno`)
    REFERENCES `controle_de_frequencia_db`.`aluno` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `controle_de_frequencia_db`.`lista_presenca`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `controle_de_frequencia_db`.`lista_presenca` (
  `fk_aluno` INT NOT NULL,
  `fk_dia_letivo` INT NOT NULL,
  `presente` TINYINT NOT NULL,
  `fk_usuario` VARCHAR(16) NOT NULL,
  INDEX `fk_lista_presenca_aluno1_idx` (`fk_aluno` ASC) VISIBLE,
  INDEX `fk_lista_presenca_dia_letivo1_idx` (`fk_dia_letivo` ASC) VISIBLE,
  PRIMARY KEY (`fk_dia_letivo`, `fk_aluno`),
  INDEX `fk_lista_presenca_usuario1_idx` (`fk_usuario` ASC) VISIBLE,
  CONSTRAINT `fk_lista_presenca_aluno1`
    FOREIGN KEY (`fk_aluno`)
    REFERENCES `controle_de_frequencia_db`.`aluno` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lista_presenca_dia_letivo1`
    FOREIGN KEY (`fk_dia_letivo`)
    REFERENCES `controle_de_frequencia_db`.`dia_letivo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lista_presenca_usuario1`
    FOREIGN KEY (`fk_usuario`)
    REFERENCES `controle_de_frequencia_db`.`usuario` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `controle_de_frequencia_db`.`alertas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `controle_de_frequencia_db`.`alertas` (
  `fk_dia_letivo` INT NOT NULL,
  `fk_aluno` INT NOT NULL,
  `feito_aviso` TINYINT NOT NULL DEFAULT 0,
  `fk_usuario_aviso` VARCHAR(100) NULL,
  INDEX `fk_alertas_lista_presenca1_idx` (`fk_dia_letivo` ASC, `fk_aluno` ASC) VISIBLE,
  PRIMARY KEY (`fk_aluno`, `fk_dia_letivo`),
  INDEX `fk_alertas_usuario1_idx` (`fk_usuario_aviso` ASC) VISIBLE,
  CONSTRAINT `fk_alertas_lista_presenca1`
    FOREIGN KEY (`fk_dia_letivo` , `fk_aluno`)
    REFERENCES `controle_de_frequencia_db`.`lista_presenca` (`fk_dia_letivo` , `fk_aluno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_alertas_usuario1`
    FOREIGN KEY (`fk_usuario_aviso`)
    REFERENCES `controle_de_frequencia_db`.`usuario` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
