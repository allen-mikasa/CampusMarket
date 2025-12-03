from app.app import app, db

with app.app_context():
    # 检查is_admin字段是否存在
    with db.engine.connect() as conn:
        result = conn.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in result]
        
        if 'is_admin' not in columns:
            # 添加is_admin字段
            conn.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0")
            print("Added is_admin column to user table")
        else:
            print("is_admin column already exists")
