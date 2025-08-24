#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库表完整导出工具
支持MySQL表结构和数据的完整导出，包括字符集、索引、约束等所有信息
"""

import argparse
import sys
import pymysql
from pymysql.constants import CLIENT
import logging
import os
from typing import Optional, Dict, Any, List, Tuple


class DatabaseConnector:
    """数据库连接管理器"""
    
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection: Optional[pymysql.Connection] = None
    
    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                client_flag=CLIENT.MULTI_STATEMENTS
            )
            return True
        except pymysql.Error as e:
            logging.error(f"数据库连接失败: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        if not self.connect():
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return True
        except pymysql.Error as e:
            logging.error(f"连接测试失败: {e}")
            return False
        finally:
            self.close()
    
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema = %s AND table_name = %s",
                    (self.database, table_name)
                )
                result = cursor.fetchone()
                return result[0] > 0
        except pymysql.Error as e:
            logging.error(f"检查表存在性失败: {e}")
            return False


class TableExporter:
    """表导出器"""
    
    def __init__(self, source_db: DatabaseConnector, target_db: DatabaseConnector):
        self.source_db = source_db
        self.target_db = target_db
        self.sql_statements: List[str] = []
    
    def get_create_table_statement(self, table_name: str) -> Optional[str]:
        """获取完整的创建表SQL语句"""
        try:
            with self.source_db.connection.cursor() as cursor:
                cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                result = cursor.fetchone()
                if result:
                    return result[1]  # CREATE TABLE语句
                return None
        except pymysql.Error as e:
            logging.error(f"获取表结构失败: {e}")
            return None
    
    def get_table_data(self, table_name: str) -> List[Tuple]:
        """获取表中的所有数据"""
        try:
            with self.source_db.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM `{table_name}`")
                return cursor.fetchall()
        except pymysql.Error as e:
            logging.error(f"获取表数据失败: {e}")
            return []
    
    def get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表的列信息"""
        try:
            with self.source_db.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, "
                    "CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE "
                    "FROM information_schema.columns "
                    "WHERE table_schema = %s AND table_name = %s "
                    "ORDER BY ordinal_position",
                    (self.source_db.database, table_name)
                )
                return cursor.fetchall()
        except pymysql.Error as e:
            logging.error(f"获取列信息失败: {e}")
            return []
    
    def generate_insert_statements(self, table_name: str, target_table_name: str, data: List[Tuple]) -> List[str]:
        """生成INSERT语句"""
        if not data:
            return []
        
        columns = self.get_table_columns(table_name)
        if not columns:
            return []
        
        column_names = [col['COLUMN_NAME'] for col in columns]
        column_list = ', '.join([f"`{col}`" for col in column_names])
        
        insert_statements = []
        
        for row in data:
            values = []
            for i, value in enumerate(row):
                if value is None:
                    values.append('NULL')
                elif isinstance(value, str):
                    escaped_value = value.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r')
                    values.append(f"'{escaped_value}'")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    values.append(f"'{str(value)}'")
            
            values_str = ', '.join(values)
            insert_sql = f"INSERT INTO `{target_table_name}` ({column_list}) VALUES ({values_str});"
            insert_statements.append(insert_sql)
        
        return insert_statements
    
    def export_table(self, source_table: str, target_table: str) -> bool:
        """导出表结构和数据"""
        logging.info(f"开始导出表: {source_table} -> {target_table}")
        
        # 清空之前的SQL语句
        self.sql_statements = []
        
        # 连接源数据库
        if not self.source_db.connect():
            logging.error("无法连接到源数据库")
            return False
        
        try:
            # 检查源表是否存在
            if not self.source_db.table_exists(source_table):
                logging.error(f"源表 '{source_table}' 不存在")
                return False
            
            # 获取创建表语句
            create_sql = self.get_create_table_statement(source_table)
            if not create_sql:
                logging.error("无法获取表结构")
                return False
            
            # 替换表名为目标表名
            if source_table != target_table:
                create_sql = create_sql.replace(f"CREATE TABLE `{source_table}`", 
                                              f"CREATE TABLE `{target_table}`", 1)
            
            self.sql_statements.append("-- 表结构导出")
            self.sql_statements.append(f"DROP TABLE IF EXISTS `{target_table}`;")
            self.sql_statements.append(create_sql + ";")
            self.sql_statements.append("")
            
            # 获取表数据
            data = self.get_table_data(source_table)
            
            if data:
                logging.info(f"找到 {len(data)} 行数据")
                self.sql_statements.append("-- 数据导出")
                insert_statements = self.generate_insert_statements(source_table, target_table, data)
                self.sql_statements.extend(insert_statements)
            else:
                logging.info("表中没有数据")
                self.sql_statements.append("-- 表中没有数据")
            
            return True
            
        finally:
            self.source_db.close()
    
    def save_sql_file(self, filename: str) -> bool:
        """保存SQL文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("-- MySQL 表完整导出文件\n")
                f.write("-- 包含表结构和数据\n\n")
                f.write("SET FOREIGN_KEY_CHECKS=0;\n")
                f.write("SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';\n\n")
                
                for statement in self.sql_statements:
                    f.write(statement + '\n')
                
                f.write("\nSET FOREIGN_KEY_CHECKS=1;\n")
            
            logging.info(f"SQL文件已保存: {filename}")
            return True
        except IOError as e:
            logging.error(f"保存文件失败: {e}")
            return False
    
    def execute_on_target(self, ask_if_exists: bool = True) -> bool:
        """在目标数据库上执行SQL语句"""
        if not self.target_db.connect():
            logging.error("无法连接到目标数据库")
            return False
        
        try:
            # 检查目标表是否存在
            target_table_name = None
            for stmt in self.sql_statements:
                if stmt.strip().startswith("CREATE TABLE"):
                    # 提取表名
                    start = stmt.find("`") + 1
                    end = stmt.find("`", start)
                    if start > 0 and end > start:
                        target_table_name = stmt[start:end]
                        break
            
            if target_table_name and self.target_db.table_exists(target_table_name):
                if ask_if_exists:
                    print(f"\n⚠️  目标表 '{target_table_name}' 已存在！")
                    print("请选择处理方式:")
                    print("1. 删除现有表并重新创建")
                    print("2. 跳过表创建，只插入数据") 
                    print("3. 取消操作")
                    
                    while True:
                        choice = input("请输入选择 (1/2/3): ").strip()
                        if choice == '1':
                            break
                        elif choice == '2':
                            # 过滤掉DROP和CREATE语句
                            filtered_statements = []
                            for stmt in self.sql_statements:
                                stmt_upper = stmt.strip().upper()
                                if not (stmt_upper.startswith("DROP TABLE") or 
                                       stmt_upper.startswith("CREATE TABLE")):
                                    filtered_statements.append(stmt)
                            self.sql_statements = filtered_statements
                            break
                        elif choice == '3':
                            print("操作已取消")
                            return False
                        else:
                            print("无效选择，请重新输入")
            
            # 执行SQL语句
            with self.target_db.connection.cursor() as cursor:
                for statement in self.sql_statements:
                    stmt = statement.strip()
                    if stmt and not stmt.startswith('--'):
                        try:
                            cursor.execute(stmt)
                        except pymysql.Error as e:
                            logging.error(f"执行SQL失败: {stmt[:50]}... - {e}")
                            return False
                
                self.target_db.connection.commit()
            
            logging.info("目标数据库导入成功")
            return True
            
        except pymysql.Error as e:
            logging.error(f"目标数据库操作失败: {e}")
            return False
        finally:
            self.target_db.close()


def parse_connection_string(conn_str: str) -> Dict[str, Any]:
    """解析连接字符串格式: user:password@host:port/database"""
    try:
        # 分离用户信息和主机信息
        if '@' in conn_str:
            user_part, host_part = conn_str.split('@', 1)
            if ':' in user_part:
                user, password = user_part.split(':', 1)
            else:
                user = user_part
                password = ""
        else:
            raise ValueError("连接字符串格式错误")
        
        # 分离主机和数据库
        if '/' in host_part:
            host_port, database = host_part.rsplit('/', 1)
        else:
            raise ValueError("连接字符串格式错误")
        
        # 分离主机和端口
        if ':' in host_port:
            host, port_str = host_port.rsplit(':', 1)
            port = int(port_str)
        else:
            host = host_port
            port = 3306
        
        return {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
    except (ValueError, IndexError) as e:
        raise ValueError(f"连接字符串格式错误: {conn_str}。正确格式: user:password@host:port/database")


def main():
    parser = argparse.ArgumentParser(
        description="MySQL数据库表完整导出工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --source-host localhost --source-port 3306 --source-user root --source-password 123456 \\
           --source-db mydb --source-table users --target-host 192.168.1.100 --target-port 3306 \\
           --target-user admin --target-password secret --target-db newdb --target-table new_users

  %(prog)s --source root:123456@localhost:3306/mydb --source-table users \\
           --target admin:secret@192.168.1.100:3306/newdb --target-table new_users --output users.sql

连接字符串格式: user:password@host:port/database
        """
    )
    
    # 源数据库参数
    source_group = parser.add_argument_group('源数据库配置')
    source_group.add_argument('--source', type=str, help='源数据库连接字符串 (user:password@host:port/database)')
    source_group.add_argument('--source-host', type=str, help='源数据库主机')
    source_group.add_argument('--source-port', type=int, default=3306, help='源数据库端口 (默认: 3306)')
    source_group.add_argument('--source-user', type=str, help='源数据库用户名')
    source_group.add_argument('--source-password', type=str, help='源数据库密码')
    source_group.add_argument('--source-db', type=str, help='源数据库名')
    source_group.add_argument('--source-table', type=str, required=True, help='源表名')
    
    # 目标数据库参数  
    target_group = parser.add_argument_group('目标数据库配置')
    target_group.add_argument('--target', type=str, help='目标数据库连接字符串 (user:password@host:port/database)')
    target_group.add_argument('--target-host', type=str, help='目标数据库主机')
    target_group.add_argument('--target-port', type=int, default=3306, help='目标数据库端口 (默认: 3306)')
    target_group.add_argument('--target-user', type=str, help='目标数据库用户名')
    target_group.add_argument('--target-password', type=str, help='目标数据库密码')
    target_group.add_argument('--target-db', type=str, help='目标数据库名')
    target_group.add_argument('--target-table', type=str, help='目标表名 (默认与源表名相同)')
    
    # 其他选项
    parser.add_argument('--output', '-o', type=str, help='输出SQL文件路径')
    parser.add_argument('--execute', '-e', action='store_true', help='直接在目标数据库执行')
    parser.add_argument('--force', '-f', action='store_true', help='强制执行，不询问用户确认')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志级别
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        # 解析源数据库连接参数
        if args.source:
            source_config = parse_connection_string(args.source)
        else:
            if not all([args.source_host, args.source_user, args.source_db]):
                parser.error("必须提供 --source 或完整的源数据库连接参数")
            source_config = {
                'host': args.source_host,
                'port': args.source_port,
                'user': args.source_user,
                'password': args.source_password or "",
                'database': args.source_db
            }
        
        # 解析目标数据库连接参数
        target_config = None
        if args.execute:
            if args.target:
                target_config = parse_connection_string(args.target)
            else:
                if not all([args.target_host, args.target_user, args.target_db]):
                    parser.error("使用 --execute 时必须提供 --target 或完整的目标数据库连接参数")
                target_config = {
                    'host': args.target_host,
                    'port': args.target_port,
                    'user': args.target_user,
                    'password': args.target_password or "",
                    'database': args.target_db
                }
        
        # 确定目标表名
        target_table = args.target_table or args.source_table
        
        print("🔄 数据库表导出工具启动...")
        print(f"源数据库: {source_config['user']}@{source_config['host']}:{source_config['port']}/{source_config['database']}")
        print(f"源表: {args.source_table}")
        
        if args.execute:
            print(f"目标数据库: {target_config['user']}@{target_config['host']}:{target_config['port']}/{target_config['database']}")
            print(f"目标表: {target_table}")
        
        # 创建数据库连接器
        source_db = DatabaseConnector(**source_config)
        target_db = DatabaseConnector(**target_config) if target_config else None
        
        # 测试源数据库连接
        print("\n🔍 测试数据库连接...")
        if not source_db.test_connection():
            print("❌ 源数据库连接失败")
            return 1
        print("✅ 源数据库连接成功")
        
        # 测试目标数据库连接
        if target_db:
            if not target_db.test_connection():
                print("❌ 目标数据库连接失败")
                return 1
            print("✅ 目标数据库连接成功")
        
        # 创建导出器并执行导出
        exporter = TableExporter(source_db, target_db)
        
        if not exporter.export_table(args.source_table, target_table):
            print("❌ 表导出失败")
            return 1
        
        print("✅ 表导出成功")
        
        # 保存到文件
        if args.output:
            if not exporter.save_sql_file(args.output):
                print("❌ 保存SQL文件失败")
                return 1
            print(f"📁 SQL文件已保存到: {args.output}")
        
        # 直接执行到目标数据库
        if args.execute:
            if not exporter.execute_on_target(ask_if_exists=not args.force):
                print("❌ 目标数据库导入失败")
                return 1
            print("✅ 目标数据库导入成功")
        
        print("\n🎉 所有操作完成！")
        return 0
        
    except Exception as e:
        logging.error(f"程序执行失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())