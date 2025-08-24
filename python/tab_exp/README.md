# MySQL 数据库表完整导出工具

一个功能强大的Python工具，用于完整导出MySQL数据库表的结构和数据，包括字符集、索引、约束等所有信息。

## 功能特性

- ✅ **完整表结构导出**：包括字符集、存储引擎、索引、约束、触发器等
- ✅ **数据完整导出**：生成标准的INSERT语句，保持数据完整性
- ✅ **灵活连接方式**：支持多种数据库连接参数格式
- ✅ **异常处理**：完善的错误处理和用户友好提示
- ✅ **智能覆盖策略**：目标表存在时提供多种处理选项
- ✅ **双重输出模式**：可保存为SQL文件或直接导入目标数据库

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# 方式1：使用连接字符串
python tab_exp.py \\
    --source root:password@localhost:3306/sourcedb \\
    --source-table users \\
    --target admin:secret@192.168.1.100:3306/targetdb \\
    --target-table new_users \\
    --output users_export.sql

# 方式2：使用分离的参数
python tab_exp.py \\
    --source-host localhost \\
    --source-port 3306 \\
    --source-user root \\
    --source-password password \\
    --source-db sourcedb \\
    --source-table users \\
    --target-host 192.168.1.100 \\
    --target-port 3306 \\
    --target-user admin \\
    --target-password secret \\
    --target-db targetdb \\
    --target-table new_users \\
    --output users_export.sql
```

### 常用场景

#### 1. 仅导出为SQL文件

```bash
python tab_exp.py \\
    --source root:123456@localhost:3306/mydb \\
    --source-table orders \\
    --output orders_backup.sql
```

#### 2. 直接导入到目标数据库

```bash
python tab_exp.py \\
    --source root:123456@localhost:3306/mydb \\
    --source-table users \\
    --target admin:secret@remote:3306/newdb \\
    --target-table users \\
    --execute
```

#### 3. 强制覆盖目标表

```bash
python tab_exp.py \\
    --source root:123456@localhost:3306/mydb \\
    --source-table products \\
    --target admin:secret@remote:3306/newdb \\
    --target-table products \\
    --execute \\
    --force
```

## 命令行参数

### 源数据库配置
- `--source`: 源数据库连接字符串 (格式: user:password@host:port/database)
- `--source-host`: 源数据库主机
- `--source-port`: 源数据库端口 (默认: 3306)
- `--source-user`: 源数据库用户名
- `--source-password`: 源数据库密码
- `--source-db`: 源数据库名
- `--source-table`: 源表名 (必需)

### 目标数据库配置
- `--target`: 目标数据库连接字符串
- `--target-host`: 目标数据库主机
- `--target-port`: 目标数据库端口 (默认: 3306)
- `--target-user`: 目标数据库用户名
- `--target-password`: 目标数据库密码
- `--target-db`: 目标数据库名
- `--target-table`: 目标表名 (默认与源表名相同)

### 其他选项
- `--output`, `-o`: 输出SQL文件路径
- `--execute`, `-e`: 直接在目标数据库执行
- `--force`, `-f`: 强制执行，不询问用户确认
- `--verbose`, `-v`: 详细输出

## 异常处理

工具会处理以下常见异常情况：

1. **数据库连接失败**：提供清晰的错误信息和连接参数检查
2. **源表不存在**：验证源表存在性
3. **权限不足**：检查数据库用户权限
4. **目标表已存在**：提供三种处理选项：
   - 删除现有表并重新创建
   - 跳过表创建，只插入数据
   - 取消操作
5. **数据类型转换**：安全处理各种MySQL数据类型

## 生成的SQL文件格式

```sql
-- MySQL 表完整导出文件
-- 包含表结构和数据

SET FOREIGN_KEY_CHECKS=0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- 表结构导出
DROP TABLE IF EXISTS `target_table`;
CREATE TABLE `target_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 数据导出
INSERT INTO `target_table` (`id`, `name`, `email`, `created_at`) VALUES (1, 'John Doe', 'john@example.com', '2024-01-01 10:00:00');
INSERT INTO `target_table` (`id`, `name`, `email`, `created_at`) VALUES (2, 'Jane Smith', 'jane@example.com', '2024-01-02 11:00:00');

SET FOREIGN_KEY_CHECKS=1;
```

## 注意事项

1. **权限要求**：
   - 源数据库需要 SELECT 权限
   - 目标数据库需要 CREATE, DROP, INSERT 权限

2. **大表处理**：
   - 对于大表，建议先使用 `--output` 生成文件，再手动导入
   - 考虑分批处理或使用专业的数据迁移工具

3. **字符集兼容性**：
   - 工具使用 utf8mb4 字符集连接，确保最大兼容性
   - 源表和目标表的字符集会保持一致

4. **数据安全**：
   - 敏感数据导出前请确保安全措施
   - 建议在测试环境先验证导出结果

## 许可证

MIT License