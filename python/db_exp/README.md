# MySQL 数据库完整导出工具

一个功能强大的Python工具，用于导出MySQL数据库的所有对象，包括表、视图、存储过程、函数、触发器、事件等。

## 功能特性

- 🗄️ **完整数据库导出**：一次导出数据库中的所有对象
- 📊 **支持多种对象类型**：
  - 表（结构和数据）
  - 视图
  - 存储过程
  - 函数
  - 触发器
  - 事件
  - 用户权限（可选）
- 📈 **实时进度显示**：使用进度条展示导出进度
- 📝 **元数据导出**：可生成JSON格式的导出元数据
- 🔧 **灵活配置**：
  - 可选择只导出结构不导出数据
  - 可选择包含用户权限信息
  - 支持静默模式和详细模式
- 🎯 **智能处理**：
  - 自动移除DEFINER语句避免权限问题
  - 批量INSERT提高导入效率
  - 正确处理各种数据类型包括二进制数据

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# 导出整个数据库（包含数据）
python db_exp.py --source root:password@localhost:3306/mydb --output mydb_full.sql

# 使用分离参数方式
python db_exp.py \
    --source-host localhost \
    --source-port 3306 \
    --source-user root \
    --source-password password \
    --source-db mydb \
    --output mydb_backup.sql
```

### 高级选项

```bash
# 只导出结构，不导出数据
python db_exp.py --source root:pass@localhost:3306/mydb \
    --output mydb_structure.sql \
    --no-data

# 包含用户权限信息
python db_exp.py --source root:pass@localhost:3306/mydb \
    --output mydb_with_users.sql \
    --include-users

# 同时导出元数据JSON文件
python db_exp.py --source root:pass@localhost:3306/mydb \
    --output mydb.sql \
    --metadata mydb_metadata.json

# 静默模式（只显示错误）
python db_exp.py --source root:pass@localhost:3306/mydb \
    --output mydb.sql \
    --quiet

# 详细模式（显示调试信息）
python db_exp.py --source root:pass@localhost:3306/mydb \
    --output mydb.sql \
    --verbose

# 不显示进度条
python db_exp.py --source root:pass@localhost:3306/mydb \
    --output mydb.sql \
    --no-progress
```

## 命令行参数

### 数据库配置
- `--source`: 数据库连接字符串 (格式: user:password@host:port/database)
- `--source-host`: 数据库主机
- `--source-port`: 数据库端口 (默认: 3306)
- `--source-user`: 数据库用户名
- `--source-password`: 数据库密码
- `--source-db`: 数据库名

### 导出选项
- `--output`, `-o`: 输出SQL文件路径 (必需)
- `--no-data`: 只导出结构，不导出数据
- `--include-users`: 包含用户和权限信息
- `--metadata`: 保存导出元数据的JSON文件路径

### 其他选项
- `--no-progress`: 不显示进度条
- `--verbose`, `-v`: 详细输出
- `--quiet`, `-q`: 静默模式

## 导出的SQL文件结构

生成的SQL文件按以下顺序组织：

1. **文件头**：包含数据库信息和导出时间
2. **表结构**：所有表的CREATE TABLE语句
3. **数据**：表数据的INSERT语句（如果包含数据）
4. **视图**：所有视图的CREATE VIEW语句
5. **存储过程**：所有存储过程
6. **函数**：所有函数
7. **触发器**：所有触发器
8. **事件**：所有事件
9. **用户权限**：用户和权限信息（如果选择包含）

## 元数据JSON格式

使用`--metadata`选项时，会生成包含以下信息的JSON文件：

```json
{
  "database": "mydb",
  "export_time": "2024-01-01T10:00:00",
  "statistics": {
    "tables": 10,
    "views": 3,
    "procedures": 5,
    "functions": 2,
    "triggers": 4,
    "events": 1
  },
  "objects": {
    "tables": ["table1", "table2", ...],
    "views": ["view1", ...],
    "procedures": ["proc1", ...],
    "functions": ["func1", ...],
    "triggers": ["trigger1", ...],
    "events": ["event1", ...]
  }
}
```

## 导入导出的数据库

```bash
# 导入到新数据库
mysql -u root -p newdb < mydb_full.sql

# 或使用mysql命令行
mysql> CREATE DATABASE newdb;
mysql> USE newdb;
mysql> SOURCE mydb_full.sql;
```

## 注意事项

1. **权限要求**：
   - 需要对源数据库的SELECT权限
   - 导出用户权限需要额外的权限
   - 查看存储过程/函数需要相应权限

2. **DEFINER处理**：
   - 工具会自动移除DEFINER语句
   - 避免在不同服务器间导入时的权限问题

3. **大数据库处理**：
   - 对于大型数据库，导出可能需要较长时间
   - 建议使用`--no-data`先测试结构导出
   - 考虑分批导出或使用专业备份工具

4. **字符集**：
   - 使用utf8mb4确保最大兼容性
   - 支持emoji等特殊字符

5. **二进制数据**：
   - 正确处理BLOB等二进制字段
   - 使用十六进制格式导出

## 与tab_exp工具的区别

| 特性 | db_exp（本工具） | tab_exp |
|------|-----------------|---------|
| 导出范围 | 整个数据库 | 单个表 |
| 支持对象 | 表、视图、存储过程、函数、触发器、事件 | 仅表 |
| 目标数据库 | 需手动导入 | 支持直接导入目标库 |
| 元数据 | 支持JSON元数据 | 不支持 |
| 进度显示 | 有进度条 | 无 |
| 用途 | 完整数据库备份/迁移 | 单表迁移 |

## 故障排除

### 连接失败
- 检查数据库服务是否运行
- 验证连接参数是否正确
- 确认防火墙设置

### 权限不足
- 确保用户有足够权限查看所有对象
- 使用root或具有相应权限的用户

### 导出不完整
- 检查日志中的错误信息
- 使用`--verbose`查看详细信息
- 确认是否有对象访问权限

## 许可证

MIT License