from app.app import app, db

with app.app_context():
    # 检查is_admin字段是否存在
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns('user')]
    print('is_admin' in columns)
