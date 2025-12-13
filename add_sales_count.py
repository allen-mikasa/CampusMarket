import sqlite3
import os

# 获取数据库路径
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'market.db')

# 连接到数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查user表是否存在sales_count列
try:
    cursor.execute("PRAGMA table_info(user)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'sales_count' not in columns:
        # 添加sales_count列
        cursor.execute("ALTER TABLE user ADD COLUMN sales_count INTEGER DEFAULT 0")
        print("已成功添加sales_count列")
    else:
        print("sales_count列已存在")
        
    # 提交更改
    conn.commit()
except Exception as e:
    print(f"执行SQL命令时出错: {e}")
finally:
    # 关闭连接
    conn.close()