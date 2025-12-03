# 简化的入口文件，避免与app/app.py冲突
# 所有应用逻辑已移至app/app.py中

# 导入主应用 - 直接从app文件夹中的app.py导入
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 直接从app文件夹导入
from app.app import app, db

# 当直接运行此文件时，启动应用
if __name__ == '__main__':
    with app.app_context():
        # 确保数据库已创建
        db.create_all()
    
    # 启动应用
    app.run(debug=True)