-- MySQL 表完整导出文件
-- 包含表结构和数据

SET FOREIGN_KEY_CHECKS=0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- 表结构导出
DROP TABLE IF EXISTS `dim_region`;
CREATE TABLE `dim_region` (
  `region_id` int NOT NULL AUTO_INCREMENT,
  `region_code` varchar(50) NOT NULL,
  `region_name` varchar(100) NOT NULL,
  `region_name_cn` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL COMMENT '区域描述',
  `sortOrder` int DEFAULT '0' COMMENT '排序顺序',
  `is_active` tinyint(1) DEFAULT '1',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updatedAt` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`region_id`),
  UNIQUE KEY `regionCode` (`region_code`),
  KEY `idx_region_code` (`region_code`),
  KEY `idx_region_active` (`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='区域维度表';

-- 数据导出
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (1, 'CN', 'China', '中国', NULL, 1, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (2, 'IN', 'India', '印度', NULL, 2, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (3, 'US', 'United States', '美国', NULL, 3, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (4, 'OTHER_ASIA', 'Other Asia', '其他亚洲', NULL, 4, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (5, 'EU28', 'EU28', '欧盟28国', NULL, 5, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (6, 'FORMER_USSR', 'Former USSR', '前苏联地区', NULL, 6, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (7, 'NON_EU_EUROPE', 'Non-EU Europe', '非欧盟欧洲', NULL, 7, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (8, 'AFRICA_MIDEAST', 'Africa and Middle East', '非洲和中东', NULL, 8, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (9, 'LATIN_AMERICA', 'Latin America', '拉丁美洲', NULL, 9, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');
INSERT INTO `dim_region` (`region_id`, `region_code`, `region_name`, `region_name_cn`, `description`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (10, 'OTHER', 'Other', '其他地区', NULL, 10, 1, '2025-08-20 19:45:41', '2025-08-20 19:45:41');

SET FOREIGN_KEY_CHECKS=1;
