from app.app import app, db
from app.app import Request

with app.app_context():
    # 检查request表是否存在
    if db.engine.has_table('request'):
        # 检查image_file列是否存在
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('request')]
        
        if 'image_file' not in columns:
            # 添加image_file列
            db.engine.execute('ALTER TABLE request ADD COLUMN image_file VARCHAR(20) DEFAULT "default.jpg"')
            print('成功添加image_file列到request表')
        else:
            print('image_file列已经存在')
    else:
        print('request表不存在，正在创建所有表...')
        db.create_all()
        print('所有表创建完成')