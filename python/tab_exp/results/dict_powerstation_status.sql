-- MySQL 表完整导出文件
-- 包含表结构和数据

SET FOREIGN_KEY_CHECKS=0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- 表结构导出
DROP TABLE IF EXISTS `dict_powerstation_status`;
CREATE TABLE `dict_powerstation_status` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `status_code` varchar(50) NOT NULL,
  `status_name` varchar(100) NOT NULL,
  `status_name_cn` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL COMMENT '状态描述',
  `color_code` varchar(7) DEFAULT NULL,
  `sortOrder` int DEFAULT '0' COMMENT '排序顺序',
  `is_active` tinyint(1) DEFAULT '1',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updatedAt` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`status_id`),
  UNIQUE KEY `statusCode` (`status_code`),
  KEY `idx_status_code` (`status_code`),
  KEY `idx_status_active` (`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='电站状态字典表';

-- 数据导出
INSERT INTO `dict_powerstation_status` (`status_id`, `status_code`, `status_name`, `status_name_cn`, `description`, `color_code`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (1, 'OPERATING', 'Operating', '运营中', '电站正常运营发电', '#52c41a', 1, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_status` (`status_id`, `status_code`, `status_name`, `status_name_cn`, `description`, `color_code`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (2, 'CONSTRUCTION', 'Construction', '建设中', '电站正在建设施工', '#1890ff', 2, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_status` (`status_id`, `status_code`, `status_name`, `status_name_cn`, `description`, `color_code`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (3, 'PERMITTED', 'Permitted', '已许可', '已获得建设许可但尚未开工', '#fa8c16', 3, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_status` (`status_id`, `status_code`, `status_name`, `status_name_cn`, `description`, `color_code`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (4, 'PRE_PERMIT', 'Pre-permit', '预许可', '正在申请建设许可', '#faad14', 4, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_status` (`status_id`, `status_code`, `status_name`, `status_name_cn`, `description`, `color_code`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (5, 'ANNOUNCED', 'Announced', '已宣布', '项目已公布但尚未获得许可', '#722ed1', 5, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_status` (`status_id`, `status_code`, `status_name`, `status_name_cn`, `description`, `color_code`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (6, 'RETIRED', 'Retired', '已退役', '电站已停止运营', '#8c8c8c', 6, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_status` (`status_id`, `status_code`, `status_name`, `status_name_cn`, `description`, `color_code`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (7, 'SUSPENDED', 'Suspended', '暂停', '项目暂时中止', '#f5222d', 7, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');
INSERT INTO `dict_powerstation_status` (`status_id`, `status_code`, `status_name`, `status_name_cn`, `description`, `color_code`, `sortOrder`, `is_active`, `createdAt`, `updatedAt`) VALUES (8, 'UNKNOWN', 'Unknown', '未知', '状态未知', '#d9d9d9', 99, 1, '2025-08-20 19:45:42', '2025-08-20 19:45:42');

SET FOREIGN_KEY_CHECKS=1;
