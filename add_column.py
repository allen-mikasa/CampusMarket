import sqlite3
import os

# 获取数据库路径
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'app', '../market.db')

# 连接到数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查reply表是否存在quoted_reply_id列
try:
    cursor.execute("PRAGMA table_info(reply)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'quoted_reply_id' not in columns:
        # 添加quoted_reply_id列
        cursor.execute("ALTER TABLE reply ADD COLUMN quoted_reply_id INTEGER")
        print("已成功添加quoted_reply_id列")
    else:
        print("quoted_reply_id列已存在")
        
    # 提交更改
    conn.commit()
except Exception as e:
    print(f"执行SQL命令时出错: {e}")
finally:
    # 关闭连接
    conn.close()