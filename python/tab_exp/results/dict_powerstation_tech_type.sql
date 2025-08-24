-- MySQL 表完整导出文件
-- 包含表结构和数据

SET FOREIGN_KEY_CHECKS=0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- 表结构导出
DROP TABLE IF EXISTS `dict_powerstation_tech_type`;
CREATE TABLE `dict_powerstation_tech_type` (
  `tech_type_id` int NOT NULL AUTO_INCREMENT,
  `tech_type_code` varchar(50) NOT NULL,
  `tech_type_name` varchar(100) NOT NULL,
  `tech_type_name_cn` varchar(100) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL COMMENT '技术分类',
  `efficiency` decimal(5,2) DEFAULT NULL COMMENT '效率(%)',
  `description` varchar(500) DEFAULT NULL COMMENT '技术描述',
  `sortOrder` int DEFAULT '0' COMMENT '排序顺序',
  `is_active` tinyint(1) DEFAULT '1',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updatedAt` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`tech_type_id`),
  UNIQUE KEY `techTypeCode` (`tech_type_code`),
  KEY `idx_tech_code` (`tech_type_code`),
  KEY `idx_tech_category` (`category`),
  KEY `idx_tech_active` (`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='电站技术类型字典表';

-- 数据导出
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (1, 'SUBCRITICAL', 'Subcritical', '亚临界', 'Traditional', '35.00', NULL, 1, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (2, 'SUPERCRITICAL', 'Supercritical', '超临界', 'Advanced', '40.00', NULL, 2, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (3, 'ULTRA_SUPER', 'Ultra-supercritical', '超超临界', 'Advanced', '45.00', NULL, 3, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (4, 'IGCC', 'IGCC', '整体煤气化联合循环', 'Clean Coal', '43.00', NULL, 4, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (5, 'CFB', 'CFB', '循环流化床', 'Traditional', '37.00', NULL, 5, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (6, 'CCS', 'CCS', '碳捕获与封存', 'Clean Coal', '35.00', NULL, 6, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (7, 'SUBCRITICAL_CCS', 'Subcritical/CCS', '亚临界+碳捕获', 'Clean Coal', '33.00', NULL, 7, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (8, 'IGCC_CCS', 'IGCC/CCS', 'IGCC+碳捕获', 'Clean Coal', '40.00', NULL, 8, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (9, 'UNKNOWN', 'Unknown', '未知', 'Unknown', NULL, NULL, 99, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (10, 'SUBCRITICAL___SUPERCRITICAL', 'Subcritical / Supercritical', 'Subcritical / Supercritical', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (11, 'SUBCRITICAL___ULTRA_SUPER', 'Subcritical / Ultra-super', 'Subcritical / Ultra-super', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (12, 'SUBCRITICAL___UNKNOWN', 'Subcritical / Unknown', 'Subcritical / Unknown', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (13, 'SUBCRITICAL_CCS___SUBCRITICAL', 'Subcritical/CCS / Subcritical', 'Subcritical/CCS / Subcritical', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (14, 'SUPERCRITICAL___SUBCRITICAL', 'Supercritical / Subcritical', 'Supercritical / Subcritical', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (15, 'ULTRA_SUPER___SUBCRITICAL', 'Ultra-super / Subcritical', 'Ultra-super / Subcritical', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (16, 'ULTRA_SUPER___UNKNOWN', 'Ultra-super / Unknown', 'Ultra-super / Unknown', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (17, 'UNKNOWN___CFB', 'Unknown / CFB', 'Unknown / CFB', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_tech_type` (`tech_type_id`, `tech_type_code`, `tech_type_name`, `tech_type_name_cn`, `category`, `efficiency`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (18, 'UNKNOWN___SUBCRITICAL', 'Unknown / Subcritical', 'Unknown / Subcritical', 'Mixed', NULL, NULL, 50, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');

SET FOREIGN_KEY_CHECKS=1;
