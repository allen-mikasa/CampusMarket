import os
import sys
print("Starting application...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# 添加调试输
print("Importing app from app package...")
from app import app, db
print(f"App imported successfully: {app}")

# 确保上传目录存在
with app.app_context():
    # 首次运行时创建数据库
    print("Creating database tables...")
    db.create_all()
    
    # 确保上传主目录存在
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        print(f"Creating upload folder: {app.config['UPLOAD_FOLDER']}")
        os.makedirs(app.config['UPLOAD_FOLDER'])
        # 确保avatars子目录存在
        avatars_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'avatars')
        if not os.path.exists(avatars_folder):
            os.makedirs(avatars_folder)

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Debug mode: {app.debug}")
    print(f"Templates folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")
    # 在生产环境中应将debug设置为False
    app.run(debug=True, host='127.0.0.1', port=5000)
