from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # 检查testuser用户是否存在
    testuser = User.query.filter_by(username='testuser').first()
    if testuser:
        print("testuser用户仍然存在")
    else:
        print("testuser用户已成功删除")
    
    # 检查admin用户是否存在
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print("admin用户仍然存在")
    else:
        print("admin用户已成功删除")