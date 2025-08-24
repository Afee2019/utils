-- MySQL 表完整导出文件
-- 包含表结构和数据

SET FOREIGN_KEY_CHECKS=0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- 表结构导出
DROP TABLE IF EXISTS `dq_powerstation_metrics`;
CREATE TABLE `dq_powerstation_metrics` (
  `metric_id` int NOT NULL AUTO_INCREMENT,
  `check_date` date NOT NULL,
  `total_records` int DEFAULT NULL,
  `records_with_location` int DEFAULT NULL,
  `records_with_capacity` int DEFAULT NULL,
  `records_with_carbon` int DEFAULT NULL,
  `records_with_tech_type` int DEFAULT NULL,
  `records_with_coal_type` int DEFAULT NULL,
  `duplicate_plants` int DEFAULT NULL,
  `data_completeness` decimal(5,2) DEFAULT NULL,
  `carbon_content` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`metric_id`),
  KEY `idx_dq_date` (`check_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='电站数据质量指标表';

-- 表中没有数据

SET FOREIGN_KEY_CHECKS=1;
