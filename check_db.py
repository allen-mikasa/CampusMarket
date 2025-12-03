from app import app, db
from app.app import Notification

with app.app_context():
    # 打印所有模型类
    print("所有模型类:")
    for model in db.Model.__subclasses__():
        print(f"  - {model.__name__}")
    
    # 检查Notification模型是否在其中
    print(f"\nNotification模型是否存在: {Notification in db.Model.__subclasses__()}")
    
    # 创建所有表
    print("\n正在创建数据库表...")
    db.create_all()
    print("数据库表创建完成！")
    
    # 检查表是否存在
    print("\n检查表是否存在:")
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"  所有表: {tables}")
    print(f"  notification表是否存在: {'notification' in tables}")
