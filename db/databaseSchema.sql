CREATE DATABASE IF NOT EXISTS `api_database` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `api_database`;

CREATE TABLE `flights_reservations` (
  `id` int(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `reservation_id` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `flights_reservations` ADD INDEX `country_city_idx` (`country`, `city`) USING BTREE;