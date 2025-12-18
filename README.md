# CampusMarket - 校园二手交易平台

## 1. 项目概述

CampusMarket是一个基于Flask框架开发的校园二手交易平台，旨在为在校学生提供便捷的二手商品交易、求购信息发布以及交流互动功能。平台支持商品发布、搜索、关注、购买，以及用户间的私信交流和公共交流广场等核心功能。

## 2. 技术栈清单

### 2.1 后端技术
| 技术/框架 | 版本 | 用途 | 文件位置 |
|-----------|------|------|----------|
| Python | 3.11+ | 开发语言 | - |
| Flask | 3.0.3 | Web框架 | `requirements.txt` |
| Flask-SQLAlchemy | 3.1.1 | ORM框架 | `requirements.txt` |
| Flask-Login | 0.6.3 | 用户认证 | `requirements.txt` |
| Flask-WTF | 1.2.1 | 表单处理 | `requirements.txt` |
| SQLAlchemy | 2.0.32 | 数据库操作 | `requirements.txt` |
| Werkzeug | 3.0.4 | WSGI工具库 | `requirements.txt` |
| Jinja2 | 3.1.4 | 模板引擎 | `requirements.txt` |
| Pillow | 10.4.0 | 图片处理 | `requirements.txt` |
| pyodbc | 5.1.0 | SQL Server驱动 | `requirements.txt` |
| pymssql | 2.2.5 | SQL Server驱动 | `requirements.txt` |

### 2.2 前端技术
| 技术/框架 | 用途 |
|-----------|------|
| HTML5 | 页面结构 |
| CSS3 | 样式设计 |
| JavaScript | 交互逻辑 |
| Bootstrap | 响应式布局框架 |
| jQuery | JavaScript库 |

### 2.3 数据库
| 数据库 | 用途 |
|--------|------|
| SQL Server | 主数据库 |

### 2.4 其他工具
| 工具 | 用途 |
|------|------|
| Git | 版本控制 |
| VS Code | 开发环境 |

## 3. 项目框架结构

### 3.1 目录结构

```
CampusMarket/
├── app/                    # 应用核心目录
│   ├── __init__.py         # 应用初始化
│   ├── models.py           # 数据库模型定义
│   ├── routes.py           # 路由和视图函数
│   ├── forms.py            # 表单定义
│   ├── utils.py            # 工具函数
│   └── __pycache__/        # Python编译缓存
├── static/                 # 静态资源
│   └── uploads/            # 上传文件存储
│       └── avatars/        # 用户头像存储
├── templates/              # HTML模板文件
├── __pycache__/            # Python编译缓存
├── .vs/                    # VS Code配置
├── CampusMarket_backup.bak # 数据库备份
├── add_admin_column.py     # 数据库迁移脚本
├── add_views_column.py     # 数据库迁移脚本
├── app.py                  # 应用入口（旧版）
├── check_admin_column.py   # 数据库检查脚本
├── check_db.py             # 数据库检查脚本
├── check_tables.py         # 数据库表检查脚本
├── config.py               # 应用配置
├── create_admin.py         # 创建管理员脚本
├── create_tables.py        # 创建数据库表脚本
├── database_migration_report.md # 数据库迁移报告
├── delete_user_data.sql    # 删除用户数据SQL脚本
├── delete_users.py         # 删除用户脚本
├── migrate_db.py           # 数据库迁移脚本
├── output.html             # 输出文件
├── requirements.txt        # 项目依赖
├── run.py                  # 应用启动脚本
├── sqlserver_migration_script.sql # SQL Server迁移脚本
├── sqlserver_schema.sql    # SQL Server schema
├── sqlserver_validation_script.sql # SQL Server验证脚本
├── test_login.py           # 登录测试脚本
├── test_login_fix.py       # 登录测试修复脚本
├── test_login_json.py      # JSON登录测试脚本
├── test_login_simple.py    # 简单登录测试脚本
├── update_db.py            # 数据库更新脚本
└── verify_delete.py        # 删除验证脚本
```

### 3.2 核心模块划分

| 模块 | 主要职责 | 文件位置 |
|------|----------|----------|
| 认证模块 | 用户注册、登录、注销 | `app/routes.py` |
| 商品模块 | 商品发布、搜索、详情、购买 | `app/routes.py` |
| 求购模块 | 求购信息发布、搜索、详情 | `app/routes.py` |
| 个人中心 | 用户信息管理、库存管理 | `app/routes.py` |
| 交流广场 | 帖子发布、回复、点赞 | `app/routes.py` |
| 私信系统 | 用户间私信交流 | `app/routes.py` |
| 通知系统 | 关注、点赞、回复等通知 | `app/routes.py` |
| 数据库模型 | 数据结构定义 | `app/models.py` |
| 表单处理 | 表单验证和提交 | `app/forms.py` |
| 工具函数 | 图片处理、分页等辅助功能 | `app/utils.py` |

## 4. 核心功能实现

### 4.1 用户认证系统

**功能描述**：实现用户注册、登录、注销等基本认证功能。

**实现逻辑**：
- 使用Flask-Login管理用户会话
- 密码使用Werkzeug的`generate_password_hash`进行哈希存储
- 登录状态通过session管理
- 表单验证使用WTForms

**关键代码**：
```python
# 用户注册
@main.route("/register", methods=['GET', 'POST'])
def register():
    # 表单验证和用户创建逻辑
    # ...
    hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
    user = User(username=form.username.data, email=form.email.data, 
                contact=form.contact.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    # ...

# 用户登录
@main.route("/login", methods=['GET', 'POST'])
def login():
    # 表单验证和用户登录逻辑
    # ...
    if user and check_password_hash(user.password, form.password.data):
        login_user(user)
        return redirect(url_for('main.home'))
    # ...
```

**文件位置**：`app/routes.py`

### 4.2 商品管理系统

**功能描述**：实现商品的发布、搜索、浏览、购买等功能。

**实现逻辑**：
- 商品发布支持图片上传和库存管理
- 商品搜索支持按标题和描述搜索
- 商品排序支持最新、最热、最多关注、最多浏览、销量最高等多种方式
- 商品详情页记录浏览量
- 支持商品关注和取消关注

**关键代码**：
```python
# 商品发布
@main.route("/item/new", methods=['GET', 'POST'])
@login_required
def new_item():
    # 商品表单处理和图片上传逻辑
    # ...
    if form.picture.data:
        pic_file = save_picture(form.picture.data, is_avatar=False)
    item = Item(
        title=form.title.data, 
        description=form.description.data, 
        price=form.price.data, 
        stock=form.stock.data, 
        image_file=pic_file, 
        seller=current_user
    )
    db.session.add(item)
    db.session.commit()
    # ...

# 商品详情
@main.route("/item/<int:item_id>", methods=['GET', 'POST'])
def item_detail(item_id):
    # 商品详情展示和评论处理
    # ...
    item.views += 1
    db.session.commit()
    # ...
```

**文件位置**：`app/routes.py`

### 4.3 求购信息系统

**功能描述**：实现求购信息的发布、搜索和浏览功能。

**实现逻辑**：
- 求购信息发布支持图片上传
- 求购信息搜索支持按标题和描述搜索
- 求购信息按最新排序

**关键代码**：
```python
# 发布求购信息
@main.route("/request/new", methods=['GET', 'POST'])
@login_required
def new_request():
    # 求购信息表单处理和图片上传逻辑
    # ...
    pic_file = 'default.jpg'
    if form.picture.data:
        pic_file = save_picture(form.picture.data, is_avatar=False)
    request_item = Request(title=form.title.data, description=form.description.data, 
                      price=form.price.data, image_file=pic_file, user=current_user)
    db.session.add(request_item)
    db.session.commit()
    # ...
```

**文件位置**：`app/routes.py`

### 4.4 交流广场系统

**功能描述**：实现用户间的公共交流功能，包括帖子发布、回复、点赞等。

**实现逻辑**：
- 支持帖子发布和图片上传
- 支持回复帖子和回复他人的回复
- 支持帖子和回复点赞
- 支持帖子和回复删除
- 支持搜索帖子内容和用户

**关键代码**：
```python
# 交流广场
@main.route("/square", methods=['GET', 'POST'])
@login_required
def square():
    # 帖子发布、搜索和展示逻辑
    # ...
    if form.validate_on_submit():
        # 处理图片上传
        image_file = None
        if form.picture.data:
            image_file = save_picture(form.picture.data, is_avatar=False)
        # 创建新留言
        post = Post(content=form.content.data, image_file=image_file, user=current_user)
        db.session.add(post)
        db.session.commit()
        # ...

# 帖子点赞
@main.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    # 帖子点赞逻辑
    # ...
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if like:
        # 取消点赞
        db.session.delete(like)
        flash('已取消点赞！', 'success')
    else:
        # 添加点赞
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        # 添加点赞通知
        # ...
        flash('点赞成功！', 'success')
    db.session.commit()
    # ...
```

**文件位置**：`app/routes.py`

### 4.5 私信系统

**功能描述**：实现用户间的一对一私信交流功能。

**实现逻辑**：
- 支持用户搜索和选择聊天对象
- 支持发送和接收私信
- 支持查看聊天记录
- 支持未读消息计数

**关键代码**：
```python
# 私信页面
@main.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    # 私信列表和聊天记录展示逻辑
    # ...
    # 处理发送消息
    if request.method == 'POST' and selected_user:
        content = request.form.get('content')
        if content:
            message = Message(sender_id=current_user.id, receiver_id=selected_user.id, content=content)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('main.messages', user_id=selected_user.id))
    # ...
```

**文件位置**：`app/routes.py`

### 4.6 通知系统

**功能描述**：实现用户关注、点赞、回复等行为的通知功能。

**实现逻辑**：
- 支持多种类型通知：关注用户、关注商品、回复帖子、回复回复、点赞帖子、点赞回复、购买商品
- 支持通知标记已读和全部已读
- 支持点击通知跳转到对应页面

**关键代码**：
```python
# 通知列表
@main.route('/notifications')
@login_required
def notifications():
    # 通知列表展示逻辑
    # ...
    # 获取当前用户的所有通知，按时间倒序排列
    query = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date_created.desc())
    # 应用分页
    pagination, notifications_list = get_pagination_data(query, page, per_page=20)
    # ...

# 标记所有通知为已读
@main.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    # 标记所有通知为已读逻辑
    # ...
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    # ...
```

**文件位置**：`app/routes.py`

### 4.7 库存管理系统

**功能描述**：实现用户库存物品的管理功能，支持从库存快速发布商品。

**实现逻辑**：
- 支持库存物品的添加、编辑和删除
- 支持从库存直接发布商品
- 支持库存物品图片上传

**关键代码**：
```python
# 添加库存物品
@main.route('/stock/new', methods=['GET', 'POST'])
@login_required
def add_stock():
    # 添加库存物品逻辑
    # ...
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        picture = request.files.get('picture')
        # 处理图片上传
        image_file = 'default.jpg'
        if picture:
            image_file = save_picture(picture, is_avatar=False)
        # 创建新库存物品
        stock = Stock(
            name=name,
            quantity=int(quantity),
            description=description,
            image_file=image_file,
            user=current_user
        )
        # 保存到数据库
        db.session.add(stock)
        db.session.commit()
        # ...
```

**文件位置**：`app/routes.py`

## 5. 数据库设计

### 5.1 核心数据模型

#### 5.1.1 用户模型 (User)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | Integer | 主键 |
| username | String(20) | 用户名 |
| email | String(120) | 邮箱 |
| password | String(60) | 密码（哈希值） |
| contact | String(60) | 联系方式 |
| avatar | String(20) | 头像文件名 |
| is_admin | Boolean | 是否为管理员 |
| sales_count | Integer | 成交量统计 |
| views | Integer | 主页访问量统计 |

#### 5.1.2 商品模型 (Item)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | Integer | 主键 |
| title | String(100) | 商品标题 |
| price | Float | 商品价格 |
| description | Text | 商品描述 |
| image_file | String(20) | 商品图片文件名 |
| date_posted | DateTime | 发布时间 |
| user_id | Integer | 外键，关联User表 |
| views | Integer | 浏览量 |
| stock | Integer | 库存数量 |
| sales_count | Integer | 已售数量 |

#### 5.1.3 求购模型 (Request)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | Integer | 主键 |
| title | String(100) | 求购标题 |
| description | Text | 求购描述 |
| price | Float | 期望价格 |
| image_file | String(20) | 求购图片文件名 |
| date_posted | DateTime | 发布时间 |
| user_id | Integer | 外键，关联User表 |

#### 5.1.4 帖子模型 (Post)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | Integer | 主键 |
| content | Text | 帖子内容 |
| image_file | String(20) | 帖子图片文件名 |
| date_posted | DateTime | 发布时间 |
| user_id | Integer | 外键，关联User表 |

#### 5.1.5 回复模型 (Reply)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | Integer | 主键 |
| content | Text | 回复内容 |
| date_posted | DateTime | 发布时间 |
| user_id | Integer | 外键，关联User表 |
| post_id | Integer | 外键，关联Post表 |
| quoted_post_id | Integer | 外键，关联被引用的Post表 |
| quoted_reply_id | Integer | 外键，关联被引用的Reply表 |

#### 5.1.6 私信模型 (Message)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | Integer | 主键 |
| sender_id | Integer | 外键，关联发送者User表 |
| receiver_id | Integer | 外键，关联接收者User表 |
| content | Text | 私信内容 |
| date_sent | DateTime | 发送时间 |
| is_read | Boolean | 是否已读 |

#### 5.1.7 通知模型 (Notification)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 外键，关联接收通知的User表 |
| sender_id | Integer | 外键，关联发送通知的User表 |
| notification_type | String(50) | 通知类型 |
| content | Text | 通知内容 |
| is_read | Boolean | 是否已读 |
| date_created | DateTime | 创建时间 |
| related_id | Integer | 关联的对象ID |

### 5.2 模型关系

- User与Item：一对多关系，一个用户可以发布多个商品
- User与Request：一对多关系，一个用户可以发布多个求购信息
- User与Post：一对多关系，一个用户可以发布多个帖子
- User与Reply：一对多关系，一个用户可以发布多个回复
- Item与Comment：一对多关系，一个商品可以有多个评论
- Post与Reply：一对多关系，一个帖子可以有多个回复
- User与Message：一对多关系，一个用户可以发送和接收多个私信
- User与Notification：一对多关系，一个用户可以接收多个通知

## 6. 核心功能流程

### 6.1 商品发布流程

1. 用户登录系统
2. 点击"发布商品"按钮
3. 填写商品信息（标题、价格、描述、库存等）
4. 上传商品图片
5. 提交表单
6. 系统保存商品信息到数据库
7. 跳转到商品列表页，显示发布成功消息

### 6.2 商品购买流程

1. 用户浏览商品列表或搜索商品
2. 点击商品进入详情页
3. 选择购买数量
4. 点击"立即购买"按钮
5. 跳转到支付页面
6. 完成支付（模拟）
7. 跳转到支付成功页面
8. 系统更新商品库存和销量
9. 发送购买通知给卖家

### 6.3 帖子发布和回复流程

1. 用户登录系统
2. 进入交流广场
3. 填写帖子内容
4. 上传图片（可选）
5. 发布帖子
6. 其他用户可以浏览帖子
7. 用户可以回复帖子或回复他人的回复
8. 用户可以点赞帖子和回复

### 6.4 私信交流流程

1. 用户登录系统
2. 进入私信页面
3. 搜索或选择聊天对象
4. 查看聊天记录
5. 输入消息内容
6. 发送消息
7. 接收方会收到新消息提醒
8. 接收方可以查看和回复消息

## 7. 关键代码片段说明

### 7.1 图片上传和处理

**功能**：处理用户上传的图片，包括头像和商品图片

**实现**：
```python
def save_picture(form_picture, is_avatar=True):
    # 生成随机文件名
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # 根据是否为头像选择存储路径
    if is_avatar:
        picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', picture_fn)
    else:
        picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)
    
    # 调整图片大小
    output_size = (125, 125) if is_avatar else (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn
```

**文件位置**：`app/utils.py`

### 7.2 分页功能

**功能**：实现数据分页展示

**实现**：
```python
def get_pagination_data(query, page, per_page=10):
    # 使用SQLAlchemy的paginate方法进行分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    return pagination, items
```

**文件位置**：`app/utils.py`

### 7.3 表单验证

**功能**：实现用户注册表单验证

**实现**：
```python
class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    contact = StringField('联系方式', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')
    
    # 自定义验证：用户名是否已存在
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请选择其他用户名。')
    
    # 自定义验证：邮箱是否已存在
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被注册，请选择其他邮箱。')
```

**文件位置**：`app/forms.py`

## 8. 开发和部署

### 8.1 开发环境搭建

1. 安装Python 3.11+
2. 克隆项目代码：`git clone <repository-url>`
3. 安装依赖：`pip install -r requirements.txt`
4. 配置数据库连接：修改`config.py`中的数据库配置
5. 创建数据库表：`python create_tables.py`
6. 启动开发服务器：`python run.py`
7. 访问：`http://localhost:5000`

### 8.2 部署说明

1. 安装生产环境依赖
2. 配置生产环境配置文件
3. 设置环境变量
4. 使用WSGI服务器（如Gunicorn）启动应用
5. 配置反向代理（如Nginx）
6. 设置定时任务和日志管理

## 9. 项目特点和优势

1. **用户友好的界面设计**：简洁、直观的界面，易于使用
2. **完整的功能体系**：涵盖商品交易、求购信息、交流互动等核心功能
3. **良好的扩展性**：模块化设计，便于添加新功能
4. **安全可靠**：使用Flask-Login和密码哈希保护用户数据
5. **响应式设计**：支持不同设备访问
6. **高效的数据库操作**：使用SQLAlchemy ORM，优化数据库查询
7. **完善的通知系统**：及时通知用户相关活动
8. **丰富的交互功能**：支持点赞、回复、关注等社交功能

## 10. 未来改进方向

1. 实现真正的在线支付功能
2. 添加商品分类和标签系统
3. 实现商品推荐功能
4. 添加用户评价和信用体系
5. 优化移动端体验
6. 添加消息推送功能
7. 实现数据统计和分析功能
8. 添加管理员后台管理系统
9. 支持多语言
10. 优化性能和安全性

## 11. 总结

CampusMarket是一个功能完整、设计合理的校园二手交易平台，基于Flask框架开发，采用了现代化的Web开发技术栈。平台实现了商品交易、求购信息、交流互动等核心功能，具有良好的用户体验和扩展性。

本项目的设计和实现遵循了软件工程的最佳实践，包括模块化设计、数据库优化、安全防护等。通过学习和参考本项目，新开发者可以快速了解Flask框架的使用、数据库设计、Web应用开发流程等核心概念和技术。

---

**项目维护者**：校园市场开发团队
**联系方式**：
**更新时间**：2025-12-15