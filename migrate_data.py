import sqlite3
import pyodbc
import os
from datetime import datetime

# 连接到SQLite数据库
sqlite_conn = sqlite3.connect('market.db')
sqlite_cursor = sqlite_conn.cursor()

# 连接到SQL Server数据库
# 注意：需要根据实际情况修改连接字符串
sqlserver_conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};' \
    'SERVER=localhost;' \
    'DATABASE=CampusMarket;' \
    'Trusted_Connection=yes;'
)
sqlserver_cursor = sqlserver_conn.cursor()

# 迁移数据函数
def migrate_table(table_name, columns, primary_key):
    print(f"开始迁移表: {table_name}")
    
    # 清空SQL Server表
    sqlserver_cursor.execute(f"DELETE FROM [dbo].[{table_name}]")
    sqlserver_cursor.execute(f"DBCC CHECKIDENT('{table_name}', RESEED, 0)")
    sqlserver_conn.commit()
    
    # 从SQLite读取数据
    sqlite_cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    # 构建插入语句
    placeholders = '?, ' * len(columns)
    placeholders = placeholders.rstrip(', ')
    insert_sql = f"INSERT INTO [dbo].[{table_name}] ({', '.join(columns)}) VALUES ({placeholders})"
    
    # 批量插入数据
    count = 0
    for row in rows:
        try:
            # 处理日期时间类型
            processed_row = []
            for value in row:
                if isinstance(value, str):
                    # 尝试解析日期时间字符串
                    try:
                        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        processed_row.append(dt)
                    except:
                        processed_row.append(value)
                else:
                    processed_row.append(value)
            
            sqlserver_cursor.execute(insert_sql, processed_row)
            count += 1
            
            # 每100条提交一次
            if count % 100 == 0:
                sqlserver_conn.commit()
                print(f"  已迁移 {count} 条记录")
        except Exception as e:
            print(f"  插入记录失败: {row}")
            print(f"  错误信息: {e}")
            raise
    
    sqlserver_conn.commit()
    print(f"  完成迁移表 {table_name}，共迁移 {count} 条记录")

# 按照表的依赖顺序进行迁移
tables_to_migrate = [
    # 用户表（无外键依赖）
    {
        'name': 'user',
        'columns': ['username', 'email', 'password', 'contact', 'avatar', 'is_admin'],
        'primary_key': 'id'
    },
    # 商品表（依赖user表）
    {
        'name': 'item',
        'columns': ['title', 'price', 'description', 'image_file', 'date_posted', 'user_id', 'views', 'stock'],
        'primary_key': 'id'
    },
    # 求购表（依赖user表）
    {
        'name': 'request',
        'columns': ['title', 'description', 'price', 'image_file', 'date_posted', 'user_id'],
        'primary_key': 'id'
    },
    # 帖子表（依赖user表）
    {
        'name': 'post',
        'columns': ['content', 'image_file', 'date_posted', 'user_id'],
        'primary_key': 'id'
    },
    # 关注商品表（依赖user表和item表）
    {
        'name': 'follow',
        'columns': ['user_id', 'item_id', 'date_followed'],
        'primary_key': 'id'
    },
    # 点赞表（依赖user表和post表）
    {
        'name': 'like',
        'columns': ['date_liked', 'user_id', 'post_id'],
        'primary_key': 'id'
    },
    # 回复表（依赖user表和post表）
    {
        'name': 'reply',
        'columns': ['content', 'date_posted', 'user_id', 'post_id', 'quoted_post_id', 'quoted_reply_id'],
        'primary_key': 'id'
    },
    # 回复点赞表（依赖user表和reply表）
    {
        'name': 'reply_like',
        'columns': ['date_liked', 'user_id', 'reply_id'],
        'primary_key': 'id'
    },
    # 用户关注表（依赖user表）
    {
        'name': 'user_follow',
        'columns': ['follower_id', 'followed_id', 'date_followed'],
        'primary_key': 'id'
    },
    # 私信表（依赖user表）
    {
        'name': 'message',
        'columns': ['sender_id', 'receiver_id', 'content', 'date_sent', 'is_read'],
        'primary_key': 'id'
    },
    # 通知表（依赖user表）
    {
        'name': 'notification',
        'columns': ['user_id', 'sender_id', 'notification_type', 'content', 'is_read', 'date_created', 'related_id'],
        'primary_key': 'id'
    },
    # 库存表（依赖user表）
    {
        'name': 'stock',
        'columns': ['name', 'quantity', 'description', 'image_file', 'date_added', 'user_id'],
        'primary_key': 'id'
    }
]

try:
    for table in tables_to_migrate:
        migrate_table(table['name'], table['columns'], table['primary_key'])
    
    print("\n数据迁移完成！")
    
except Exception as e:
    print(f"迁移过程中发生错误: {e}")
    sqlserver_conn.rollback()
finally:
    # 关闭数据库连接
    sqlite_cursor.close()
    sqlite_conn.close()
    sqlserver_cursor.close()
    sqlserver_conn.close()