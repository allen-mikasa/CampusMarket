import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_picture, is_avatar=False):
    """
    保存上传的图片到服务器
    
    Args:
        form_picture: Flask-WTF文件字段对象
        is_avatar: 是否为头像图片
        
    Returns:
        str: 保存后的图片文件名
    """
    try:
        # 生成随机文件名
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        
        # 确保上传主目录存在
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])
        
        if is_avatar:
            # 确保avatars子目录存在
            avatars_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars')
            if not os.path.exists(avatars_folder):
                os.makedirs(avatars_folder)
            picture_path = os.path.join(avatars_folder, picture_fn)
            # 头像图片保持125x125像素
            output_size = (125, 125)
        else:
            picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)
            # 商品图片使用更大的尺寸，保持宽高比
            output_size = (800, 800)
        
        # 调整图片大小
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        # 保存图片，对于JPEG格式设置质量参数
        if f_ext.lower() in ['.jpg', '.jpeg']:
            i.save(picture_path, quality=85, optimize=True)
        else:
            i.save(picture_path)
        
        return picture_fn
    except Exception as e:
        # 记录错误并返回默认图片
        print(f"Error saving picture: {e}")
        return 'default_avatar.png' if is_avatar else 'default.jpg'



def format_content(content):
    """
    格式化内容，处理@用户等特殊格式
    
    Args:
        content: 原始内容
        
    Returns:
        str: 格式化后的内容
    """
    import re
    # 简单的@用户处理，实际应用中可能需要更复杂的正则表达式
    def replace_mention(match):
        username = match.group(1)
        return f'<a href="#" class="text-primary">@{username}</a>'
    
    return re.sub(r'@(\w+)', replace_mention, content)



def get_pagination_data(query, page, per_page=10):
    """
    获取分页数据
    
    Args:
        query: SQLAlchemy查询对象
        page: 当前页码
        per_page: 每页数据量
        
    Returns:
        tuple: (分页对象, 数据列表)
    """
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination, pagination.items
