# 用于创建数据库表的脚本
from app.app import app, db, UserFollow

with app.app_context():
    db.create_all()
    print("数据库表创建完成！")