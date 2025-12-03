from app.app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # 检查是否已经存在管理员账号
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        # 创建管理员账号
        hashed_password = generate_password_hash('admin123')
        admin = User(
            username='admin',
            email='admin@example.com',
            contact='13800138000',
            password=hashed_password,
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('管理员账号创建成功！')
        print('邮箱：admin@example.com')
        print('密码：admin123')
    else:
        print('管理员账号已存在！')
