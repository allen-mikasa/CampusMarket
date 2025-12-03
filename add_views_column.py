from app.app import app, db, Item

with app.app_context():
    # 检查数据库中是否已经有views列
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns('item')]
    
    if 'views' not in columns:
        # 添加views列
        with db.engine.connect() as conn:
            conn.execute(db.text('ALTER TABLE item ADD COLUMN views INTEGER DEFAULT 0'))
        print("Successfully added views column to item table")
    else:
        print("views column already exists in item table")
    
    # 提交更改
    db.session.commit()