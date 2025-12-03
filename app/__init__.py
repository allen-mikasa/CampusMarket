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
    
    # 覆盖数据库路径以保持兼容性
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../market.db')
    # 确保上传文件夹路径正确
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, '../static/uploads')
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(main)
    
    # 上下文处理器
    from .utils import format_content
    
    @app.context_processor
    def utility_processor():
        """
        添加模板上下文处理器
        """
        def get_format_content(content):
            return format_content(content)
        
        return dict(format_content=get_format_content)
    
    @app.context_processor
    def notifications_processor():
        """
        添加未读通知数量到模板上下文
        """
        from flask_login import current_user
        from .models import Notification
        if current_user.is_authenticated:
            # 获取当前用户的未读通知数量
            unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
            return dict(unread_notifications_count=unread_count)
        return dict(unread_notifications_count=0)
    
    return app


# 创建应用实例
app = create_app()

# 导出必要的对象
__all__ = ['app', 'db', 'User']
