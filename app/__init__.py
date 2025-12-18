import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from .models import db, User
from .routes import main

# 初始化登录管理器
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

# 初始化CSRF保护
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    """
    用户加载器，用于从数据库中加载用户
    """
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    """
    应用工厂函数，用于创建和配置Flask应用
    
    Args:
        config_class: 配置类
        
    Returns:
        Flask: 配置好的Flask应用实例
    """
    # 创建Flask应用实例
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # 配置应用
    app.config.from_object(config_class)
    
    # 确保上传文件夹路径正确
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, '../static/uploads')
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(main)
    
    # 添加全局上下文处理器，用于传递未读通知和消息数量
    @app.context_processor
    def inject_unread_counts():
        from .models import Notification, Message
        from flask_login import current_user
        if current_user.is_authenticated:
            # 获取未读通知数量
            unread_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
            # 获取未读消息数量
            unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
            return {
                'unread_notifications': unread_notifications,
                'unread_messages': unread_messages
            }
        return {
            'unread_notifications': 0,
            'unread_messages': 0
        }
    
    return app


# 创建应用实例
app = create_app()

# 导出必要的对象
__all__ = ['app', 'db', 'User']
