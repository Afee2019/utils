-- MySQL 表完整导出文件
-- 包含表结构和数据

SET FOREIGN_KEY_CHECKS=0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- 表结构导出
DROP TABLE IF EXISTS `agg_powerstation_by_tech`;
CREATE TABLE `agg_powerstation_by_tech` (
  `agg_id` int NOT NULL AUTO_INCREMENT,
  `tech_type_id` int NOT NULL,
  `status_id` int DEFAULT NULL,
  `total_plants` int DEFAULT '0',
  `total_capacity` decimal(15,2) DEFAULT '0.00',
  `total_carbon` decimal(15,2) DEFAULT '0.00',
  `avg_capacity` decimal(10,2) DEFAULT '0.00',
  `avg_carbon` decimal(10,2) DEFAULT '0.00',
  `lastUpdated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`agg_id`),
  UNIQUE KEY `uk_tech_status` (`tech_type_id`,`status_id`),
  KEY `idx_agg_tech` (`tech_type_id`),
  KEY `idx_agg_status` (`status_id`),
  CONSTRAINT `agg_powerstation_by_tech_ibfk_1` FOREIGN KEY (`tech_type_id`) REFERENCES `dict_powerstation_tech_type` (`tech_type_id`),
  CONSTRAINT `agg_powerstation_by_tech_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `dict_powerstation_status` (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='技术类型电站汇总表';

-- 数据导出
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (1, 1, 1, 3691, '2663077.00', '13619.91', '721.51', '3.69', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (2, 9, 5, 76, '87958.00', '358.79', '1157.34', '4.72', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (3, 4, 1, 10, '16602.00', '72.97', '1660.20', '7.30', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (4, 2, 1, 467, '622966.00', '2721.59', '1333.97', '5.83', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (5, 14, 1, 10, '28355.00', '143.67', '2835.50', '14.37', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (6, 9, 8, 75, '75695.00', '307.59', '1009.27', '4.10', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (7, 16, 1, 1, '4424.00', '21.16', '4424.00', '21.16', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (8, 9, 1, 399, '277086.00', '1170.11', '694.45', '2.93', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (9, 2, 3, 25, '32683.00', '131.18', '1307.32', '5.25', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (10, 2, 8, 33, '40801.00', '163.24', '1236.39', '4.95', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (11, 2, 5, 13, '18140.00', '72.81', '1395.38', '5.60', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (12, 2, 2, 85, '82993.00', '336.22', '976.39', '3.96', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (13, 9, 2, 127, '132969.00', '524.52', '1047.00', '4.13', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (14, 9, 3, 45, '38109.00', '154.62', '846.87', '3.44', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (15, 10, 1, 6, '8348.00', '39.74', '1391.33', '6.62', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (16, 15, 1, 6, '8471.00', '38.39', '1411.83', '6.40', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (17, 11, 1, 1, '2147.00', '9.73', '2147.00', '9.73', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (18, 18, 1, 5, '4148.00', '18.15', '829.60', '3.63', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (19, 1, 8, 36, '10270.00', '47.03', '285.28', '1.31', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (20, 1, 2, 48, '15494.00', '72.46', '322.79', '1.51', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (21, 13, 1, 1, '1650.00', '7.98', '1650.00', '7.98', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (22, 17, 5, 1, '1400.00', '6.15', '1400.00', '6.15', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (23, 4, 8, 2, '1820.00', '6.91', '910.00', '3.46', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (24, 1, 3, 29, '10166.00', '46.90', '350.55', '1.62', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (25, 1, 5, 36, '12110.00', '55.82', '336.39', '1.55', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (26, 8, 8, 1, '800.00', '0.43', '800.00', '0.43', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (27, 5, 3, 5, '2140.00', '9.28', '428.00', '1.86', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (28, 7, 1, 1, '703.00', '3.78', '703.00', '3.78', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (29, 5, 8, 10, '3729.00', '16.83', '372.90', '1.68', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (30, 5, 1, 27, '6644.00', '32.22', '246.07', '1.19', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (31, 5, 2, 11, '3097.00', '15.37', '281.55', '1.40', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (32, 12, 1, 6, '2670.00', '14.88', '445.00', '2.48', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (33, 4, 2, 2, '1080.00', '3.82', '540.00', '1.91', '2025-08-20 19:45:47');
INSERT INTO `agg_powerstation_by_tech` (`agg_id`, `tech_type_id`, `status_id`, `total_plants`, `total_capacity`, `total_carbon`, `avg_capacity`, `avg_carbon`, `lastUpdated`) VALUES (34, 5, 5, 3, '650.00', '3.18', '216.67', '1.06', '2025-08-20 19:45:47');

SET FOREIGN_KEY_CHECKS=1;
