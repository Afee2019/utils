#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL数据库完整导出工具
支持导出整个数据库的所有对象：表、视图、存储过程、函数、触发器、事件等
"""

import argparse
import sys
import os
import pymysql
from pymysql.constants import CLIENT
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
import json
from tqdm import tqdm


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
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                logging.info(f"MySQL版本: {version}")
            return True
        except pymysql.Error as e:
            logging.error(f"连接测试失败: {e}")
            return False
        finally:
            self.close()


class DatabaseObjectDiscovery:
    """数据库对象发现器"""
    
    def __init__(self, connection: pymysql.Connection, database: str):
        self.connection = connection
        self.database = database
    
    def get_tables(self) -> List[str]:
        """获取所有表"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT TABLE_NAME FROM information_schema.TABLES "
                    "WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE' "
                    "ORDER BY TABLE_NAME",
                    (self.database,)
                )
                return [row[0] for row in cursor.fetchall()]
        except pymysql.Error as e:
            logging.error(f"获取表列表失败: {e}")
            return []
    
    def get_views(self) -> List[str]:
        """获取所有视图"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT TABLE_NAME FROM information_schema.VIEWS "
                    "WHERE TABLE_SCHEMA = %s ORDER BY TABLE_NAME",
                    (self.database,)
                )
                return [row[0] for row in cursor.fetchall()]
        except pymysql.Error as e:
            logging.error(f"获取视图列表失败: {e}")
            return []
    
    def get_procedures(self) -> List[str]:
        """获取所有存储过程"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ROUTINE_NAME FROM information_schema.ROUTINES "
                    "WHERE ROUTINE_SCHEMA = %s AND ROUTINE_TYPE = 'PROCEDURE' "
                    "ORDER BY ROUTINE_NAME",
                    (self.database,)
                )
                return [row[0] for row in cursor.fetchall()]
        except pymysql.Error as e:
            logging.error(f"获取存储过程列表失败: {e}")
            return []
    
    def get_functions(self) -> List[str]:
        """获取所有函数"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ROUTINE_NAME FROM information_schema.ROUTINES "
                    "WHERE ROUTINE_SCHEMA = %s AND ROUTINE_TYPE = 'FUNCTION' "
                    "ORDER BY ROUTINE_NAME",
                    (self.database,)
                )
                return [row[0] for row in cursor.fetchall()]
        except pymysql.Error as e:
            logging.error(f"获取函数列表失败: {e}")
            return []
    
    def get_triggers(self) -> List[str]:
        """获取所有触发器"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT TRIGGER_NAME FROM information_schema.TRIGGERS "
                    "WHERE TRIGGER_SCHEMA = %s ORDER BY TRIGGER_NAME",
                    (self.database,)
                )
                return [row[0] for row in cursor.fetchall()]
        except pymysql.Error as e:
            logging.error(f"获取触发器列表失败: {e}")
            return []
    
    def get_events(self) -> List[str]:
        """获取所有事件"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT EVENT_NAME FROM information_schema.EVENTS "
                    "WHERE EVENT_SCHEMA = %s ORDER BY EVENT_NAME",
                    (self.database,)
                )
                return [row[0] for row in cursor.fetchall()]
        except pymysql.Error as e:
            logging.error(f"获取事件列表失败: {e}")
            return []
    
    def get_all_objects(self) -> Dict[str, List[str]]:
        """获取所有数据库对象"""
        return {
            'tables': self.get_tables(),
            'views': self.get_views(),
            'procedures': self.get_procedures(),
            'functions': self.get_functions(),
            'triggers': self.get_triggers(),
            'events': self.get_events()
        }


class DatabaseExporter:
    """数据库导出器"""
    
    def __init__(self, source_db: DatabaseConnector, include_data: bool = True,
                 include_users: bool = False, show_progress: bool = True):
        self.source_db = source_db
        self.include_data = include_data
        self.include_users = include_users
        self.show_progress = show_progress
        self.sql_statements: List[str] = []
        self.discovery: Optional[DatabaseObjectDiscovery] = None
        
    def export_table_structure(self, table_name: str) -> Optional[str]:
        """导出表结构"""
        try:
            with self.source_db.connection.cursor() as cursor:
                cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                result = cursor.fetchone()
                if result:
                    return result[1]
                return None
        except pymysql.Error as e:
            logging.error(f"导出表结构失败 ({table_name}): {e}")
            return None
    
    def export_table_data(self, table_name: str) -> List[str]:
        """导出表数据"""
        statements = []
        try:
            with self.source_db.connection.cursor() as cursor:
                # 获取表的列信息
                cursor.execute(
                    "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
                    "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s "
                    "ORDER BY ORDINAL_POSITION",
                    (self.source_db.database, table_name)
                )
                columns = [row[0] for row in cursor.fetchall()]
                
                if not columns:
                    return statements
                
                column_list = ', '.join([f"`{col}`" for col in columns])
                
                # 获取数据
                cursor.execute(f"SELECT * FROM `{table_name}`")
                rows = cursor.fetchall()
                
                # 批量生成INSERT语句
                batch_size = 1000
                for i in range(0, len(rows), batch_size):
                    batch = rows[i:i+batch_size]
                    values_list = []
                    
                    for row in batch:
                        values = []
                        for value in row:
                            if value is None:
                                values.append('NULL')
                            elif isinstance(value, str):
                                escaped = value.replace('\\', '\\\\').replace("'", "\\'")
                                escaped = escaped.replace('\n', '\\n').replace('\r', '\\r')
                                values.append(f"'{escaped}'")
                            elif isinstance(value, (datetime,)):
                                values.append(f"'{value}'")
                            elif isinstance(value, bytes):
                                hex_str = value.hex()
                                values.append(f"0x{hex_str}" if hex_str else "''")
                            else:
                                values.append(str(value))
                        values_list.append(f"({', '.join(values)})")
                    
                    if values_list:
                        insert_sql = f"INSERT INTO `{table_name}` ({column_list}) VALUES\n"
                        insert_sql += ',\n'.join(values_list) + ';'
                        statements.append(insert_sql)
                
        except pymysql.Error as e:
            logging.error(f"导出表数据失败 ({table_name}): {e}")
        
        return statements
    
    def export_view(self, view_name: str) -> Optional[str]:
        """导出视图"""
        try:
            with self.source_db.connection.cursor() as cursor:
                cursor.execute(f"SHOW CREATE VIEW `{view_name}`")
                result = cursor.fetchone()
                if result:
                    # 替换DEFINER
                    create_statement = result[1]
                    import re
                    create_statement = re.sub(
                        r'DEFINER=`[^`]+`@`[^`]+`\s+',
                        '',
                        create_statement
                    )
                    return create_statement
                return None
        except pymysql.Error as e:
            logging.error(f"导出视图失败 ({view_name}): {e}")
            return None
    
    def export_procedure(self, proc_name: str) -> Optional[str]:
        """导出存储过程"""
        try:
            with self.source_db.connection.cursor() as cursor:
                cursor.execute(f"SHOW CREATE PROCEDURE `{proc_name}`")
                result = cursor.fetchone()
                if result and len(result) > 2:
                    create_statement = result[2]
                    # 移除DEFINER
                    import re
                    create_statement = re.sub(
                        r'DEFINER=`[^`]+`@`[^`]+`\s+',
                        '',
                        create_statement
                    )
                    return create_statement
                return None
        except pymysql.Error as e:
            logging.error(f"导出存储过程失败 ({proc_name}): {e}")
            return None
    
    def export_function(self, func_name: str) -> Optional[str]:
        """导出函数"""
        try:
            with self.source_db.connection.cursor() as cursor:
                cursor.execute(f"SHOW CREATE FUNCTION `{func_name}`")
                result = cursor.fetchone()
                if result and len(result) > 2:
                    create_statement = result[2]
                    # 移除DEFINER
                    import re
                    create_statement = re.sub(
                        r'DEFINER=`[^`]+`@`[^`]+`\s+',
                        '',
                        create_statement
                    )
                    return create_statement
                return None
        except pymysql.Error as e:
            logging.error(f"导出函数失败 ({func_name}): {e}")
            return None
    
    def export_trigger(self, trigger_name: str) -> Optional[str]:
        """导出触发器"""
        try:
            with self.source_db.connection.cursor() as cursor:
                cursor.execute(f"SHOW CREATE TRIGGER `{trigger_name}`")
                result = cursor.fetchone()
                if result and len(result) > 2:
                    create_statement = result[2]
                    # 移除DEFINER
                    import re
                    create_statement = re.sub(
                        r'DEFINER=`[^`]+`@`[^`]+`\s+',
                        '',
                        create_statement
                    )
                    return create_statement
                return None
        except pymysql.Error as e:
            logging.error(f"导出触发器失败 ({trigger_name}): {e}")
            return None
    
    def export_event(self, event_name: str) -> Optional[str]:
        """导出事件"""
        try:
            with self.source_db.connection.cursor() as cursor:
                cursor.execute(f"SHOW CREATE EVENT `{event_name}`")
                result = cursor.fetchone()
                if result and len(result) > 3:
                    create_statement = result[3]
                    # 移除DEFINER
                    import re
                    create_statement = re.sub(
                        r'DEFINER=`[^`]+`@`[^`]+`\s+',
                        '',
                        create_statement
                    )
                    return create_statement
                return None
        except pymysql.Error as e:
            logging.error(f"导出事件失败 ({event_name}): {e}")
            return None
    
    def export_users_and_privileges(self) -> List[str]:
        """导出用户和权限"""
        statements = []
        try:
            with self.source_db.connection.cursor() as cursor:
                # 获取与当前数据库相关的用户
                cursor.execute(
                    "SELECT DISTINCT GRANTEE FROM information_schema.SCHEMA_PRIVILEGES "
                    "WHERE TABLE_SCHEMA = %s",
                    (self.source_db.database,)
                )
                users = cursor.fetchall()
                
                for user_row in users:
                    user = user_row[0]
                    # 获取用户的权限
                    try:
                        cursor.execute(f"SHOW GRANTS FOR {user}")
                        grants = cursor.fetchall()
                        for grant in grants:
                            statements.append(grant[0] + ';')
                    except pymysql.Error:
                        # 某些用户可能无法查看权限
                        pass
                        
        except pymysql.Error as e:
            logging.warning(f"导出用户权限失败: {e}")
        
        return statements
    
    def export_database(self) -> bool:
        """导出整个数据库"""
        if not self.source_db.connect():
            logging.error("无法连接到源数据库")
            return False
        
        try:
            # 初始化发现器
            self.discovery = DatabaseObjectDiscovery(
                self.source_db.connection,
                self.source_db.database
            )
            
            # 获取所有对象
            all_objects = self.discovery.get_all_objects()
            
            # 统计对象数量
            total_objects = sum(len(objs) for objs in all_objects.values())
            if self.include_data:
                total_objects += len(all_objects['tables'])  # 数据导出也算作任务
            
            logging.info(f"发现数据库对象:")
            logging.info(f"  表: {len(all_objects['tables'])}个")
            logging.info(f"  视图: {len(all_objects['views'])}个")
            logging.info(f"  存储过程: {len(all_objects['procedures'])}个")
            logging.info(f"  函数: {len(all_objects['functions'])}个")
            logging.info(f"  触发器: {len(all_objects['triggers'])}个")
            logging.info(f"  事件: {len(all_objects['events'])}个")
            
            # 创建进度条
            if self.show_progress:
                progress_bar = tqdm(total=total_objects, desc="导出进度", unit="对象")
            
            # 添加文件头
            self.sql_statements.append(f"-- MySQL数据库完整导出")
            self.sql_statements.append(f"-- 数据库: {self.source_db.database}")
            self.sql_statements.append(f"-- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.sql_statements.append("")
            self.sql_statements.append("SET FOREIGN_KEY_CHECKS=0;")
            self.sql_statements.append("SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';")
            self.sql_statements.append("SET AUTOCOMMIT=0;")
            self.sql_statements.append("START TRANSACTION;")
            self.sql_statements.append("")
            
            # 导出表结构
            if all_objects['tables']:
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("-- 表结构")
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("")
                
                for table in all_objects['tables']:
                    create_sql = self.export_table_structure(table)
                    if create_sql:
                        self.sql_statements.append(f"-- 表: {table}")
                        self.sql_statements.append(f"DROP TABLE IF EXISTS `{table}`;")
                        self.sql_statements.append(create_sql + ";")
                        self.sql_statements.append("")
                    
                    if self.show_progress:
                        progress_bar.update(1)
            
            # 导出表数据
            if self.include_data and all_objects['tables']:
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("-- 数据")
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("")
                
                for table in all_objects['tables']:
                    data_statements = self.export_table_data(table)
                    if data_statements:
                        self.sql_statements.append(f"-- 数据: {table}")
                        self.sql_statements.extend(data_statements)
                        self.sql_statements.append("")
                    
                    if self.show_progress:
                        progress_bar.update(1)
            
            # 导出视图
            if all_objects['views']:
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("-- 视图")
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("")
                
                for view in all_objects['views']:
                    create_sql = self.export_view(view)
                    if create_sql:
                        self.sql_statements.append(f"-- 视图: {view}")
                        self.sql_statements.append(f"DROP VIEW IF EXISTS `{view}`;")
                        self.sql_statements.append(create_sql + ";")
                        self.sql_statements.append("")
                    
                    if self.show_progress:
                        progress_bar.update(1)
            
            # 导出存储过程
            if all_objects['procedures']:
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("-- 存储过程")
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("DELIMITER $$")
                self.sql_statements.append("")
                
                for proc in all_objects['procedures']:
                    create_sql = self.export_procedure(proc)
                    if create_sql:
                        self.sql_statements.append(f"-- 存储过程: {proc}")
                        self.sql_statements.append(f"DROP PROCEDURE IF EXISTS `{proc}`$$")
                        self.sql_statements.append(create_sql + "$$")
                        self.sql_statements.append("")
                    
                    if self.show_progress:
                        progress_bar.update(1)
                
                self.sql_statements.append("DELIMITER ;")
                self.sql_statements.append("")
            
            # 导出函数
            if all_objects['functions']:
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("-- 函数")
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("DELIMITER $$")
                self.sql_statements.append("")
                
                for func in all_objects['functions']:
                    create_sql = self.export_function(func)
                    if create_sql:
                        self.sql_statements.append(f"-- 函数: {func}")
                        self.sql_statements.append(f"DROP FUNCTION IF EXISTS `{func}`$$")
                        self.sql_statements.append(create_sql + "$$")
                        self.sql_statements.append("")
                    
                    if self.show_progress:
                        progress_bar.update(1)
                
                self.sql_statements.append("DELIMITER ;")
                self.sql_statements.append("")
            
            # 导出触发器
            if all_objects['triggers']:
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("-- 触发器")
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("DELIMITER $$")
                self.sql_statements.append("")
                
                for trigger in all_objects['triggers']:
                    create_sql = self.export_trigger(trigger)
                    if create_sql:
                        self.sql_statements.append(f"-- 触发器: {trigger}")
                        self.sql_statements.append(f"DROP TRIGGER IF EXISTS `{trigger}`$$")
                        self.sql_statements.append(create_sql + "$$")
                        self.sql_statements.append("")
                    
                    if self.show_progress:
                        progress_bar.update(1)
                
                self.sql_statements.append("DELIMITER ;")
                self.sql_statements.append("")
            
            # 导出事件
            if all_objects['events']:
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("-- 事件")
                self.sql_statements.append("-- ----------------------------------------")
                self.sql_statements.append("DELIMITER $$")
                self.sql_statements.append("")
                
                for event in all_objects['events']:
                    create_sql = self.export_event(event)
                    if create_sql:
                        self.sql_statements.append(f"-- 事件: {event}")
                        self.sql_statements.append(f"DROP EVENT IF EXISTS `{event}`$$")
                        self.sql_statements.append(create_sql + "$$")
                        self.sql_statements.append("")
                    
                    if self.show_progress:
                        progress_bar.update(1)
                
                self.sql_statements.append("DELIMITER ;")
                self.sql_statements.append("")
            
            # 导出用户权限
            if self.include_users:
                user_statements = self.export_users_and_privileges()
                if user_statements:
                    self.sql_statements.append("-- ----------------------------------------")
                    self.sql_statements.append("-- 用户权限")
                    self.sql_statements.append("-- ----------------------------------------")
                    self.sql_statements.append("")
                    self.sql_statements.extend(user_statements)
                    self.sql_statements.append("")
            
            # 添加文件尾
            self.sql_statements.append("COMMIT;")
            self.sql_statements.append("SET FOREIGN_KEY_CHECKS=1;")
            
            if self.show_progress:
                progress_bar.close()
            
            return True
            
        except Exception as e:
            logging.error(f"导出过程中发生错误: {e}")
            return False
        finally:
            self.source_db.close()
    
    def save_sql_file(self, filename: str) -> bool:
        """保存SQL文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for statement in self.sql_statements:
                    f.write(statement + '\n')
            
            logging.info(f"SQL文件已保存: {filename}")
            return True
        except IOError as e:
            logging.error(f"保存文件失败: {e}")
            return False
    
    def save_metadata(self, filename: str) -> bool:
        """保存导出元数据"""
        try:
            if self.discovery:
                all_objects = self.discovery.get_all_objects()
                metadata = {
                    'database': self.source_db.database,
                    'export_time': datetime.now().isoformat(),
                    'statistics': {
                        'tables': len(all_objects['tables']),
                        'views': len(all_objects['views']),
                        'procedures': len(all_objects['procedures']),
                        'functions': len(all_objects['functions']),
                        'triggers': len(all_objects['triggers']),
                        'events': len(all_objects['events'])
                    },
                    'objects': all_objects
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                logging.info(f"元数据已保存: {filename}")
                return True
        except Exception as e:
            logging.error(f"保存元数据失败: {e}")
            return False


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
        description="MySQL数据库完整导出工具 - 导出所有数据库对象",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --source root:123456@localhost:3306/mydb --output mydb_backup.sql
  
  %(prog)s --source-host localhost --source-user root --source-password 123456 \\
           --source-db mydb --output mydb_full.sql --include-users
           
  %(prog)s --source root:123456@localhost:3306/mydb --no-data --output mydb_structure.sql

连接字符串格式: user:password@host:port/database
        """
    )
    
    # 源数据库参数
    source_group = parser.add_argument_group('数据库配置')
    source_group.add_argument('--source', type=str, help='数据库连接字符串')
    source_group.add_argument('--source-host', type=str, help='数据库主机')
    source_group.add_argument('--source-port', type=int, default=3306, help='数据库端口 (默认: 3306)')
    source_group.add_argument('--source-user', type=str, help='数据库用户名')
    source_group.add_argument('--source-password', type=str, help='数据库密码')
    source_group.add_argument('--source-db', type=str, help='数据库名')
    
    # 导出选项
    export_group = parser.add_argument_group('导出选项')
    export_group.add_argument('--output', '-o', type=str, required=True, help='输出SQL文件路径')
    export_group.add_argument('--no-data', action='store_true', help='只导出结构，不导出数据')
    export_group.add_argument('--include-users', action='store_true', help='包含用户和权限信息')
    export_group.add_argument('--metadata', type=str, help='保存导出元数据的JSON文件路径')
    
    # 其他选项
    parser.add_argument('--no-progress', action='store_true', help='不显示进度条')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.quiet:
        log_level = logging.ERROR
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    try:
        # 解析数据库连接参数
        if args.source:
            source_config = parse_connection_string(args.source)
        else:
            if not all([args.source_host, args.source_user, args.source_db]):
                parser.error("必须提供 --source 或完整的数据库连接参数")
            source_config = {
                'host': args.source_host,
                'port': args.source_port,
                'user': args.source_user,
                'password': args.source_password or "",
                'database': args.source_db
            }
        
        print("🔄 MySQL数据库完整导出工具")
        print(f"📍 数据库: {source_config['user']}@{source_config['host']}:{source_config['port']}/{source_config['database']}")
        
        # 创建数据库连接器
        source_db = DatabaseConnector(**source_config)
        
        # 测试连接
        print("\n🔍 测试数据库连接...")
        if not source_db.test_connection():
            print("❌ 数据库连接失败")
            return 1
        print("✅ 数据库连接成功")
        
        # 创建导出器
        exporter = DatabaseExporter(
            source_db,
            include_data=not args.no_data,
            include_users=args.include_users,
            show_progress=not args.no_progress
        )
        
        # 执行导出
        print("\n📦 开始导出数据库...")
        if not exporter.export_database():
            print("❌ 数据库导出失败")
            return 1
        
        # 保存SQL文件
        if not exporter.save_sql_file(args.output):
            print("❌ 保存SQL文件失败")
            return 1
        
        print(f"✅ SQL文件已保存: {args.output}")
        
        # 保存元数据
        if args.metadata:
            if not exporter.save_metadata(args.metadata):
                print("⚠️  保存元数据失败")
            else:
                print(f"📊 元数据已保存: {args.metadata}")
        
        # 显示统计信息
        file_size = os.path.getsize(args.output)
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        elif file_size > 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size} bytes"
        
        print(f"\n📈 导出统计:")
        print(f"   文件大小: {size_str}")
        print(f"   包含数据: {'是' if not args.no_data else '否'}")
        print(f"   包含用户权限: {'是' if args.include_users else '否'}")
        
        print("\n🎉 数据库导出完成！")
        return 0
        
    except Exception as e:
        logging.error(f"程序执行失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())