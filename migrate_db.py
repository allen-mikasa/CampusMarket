from app.app import app, db

with app.app_context():
    # 检查stock字段是否存在
    with db.engine.connect() as conn:
        result = conn.execute("PRAGMA table_info(item)")
        columns = [row[1] for row in result]
        
        if 'stock' not in columns:
            # 添加stock字段
            conn.execute("ALTER TABLE item ADD COLUMN stock INTEGER NOT NULL DEFAULT 1")
            print("Added stock column to item table")
        else:
            print("stock column already exists")
