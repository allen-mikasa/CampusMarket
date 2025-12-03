from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# 初始化数据库对象，由app/__init__.py统一配置
db = SQLAlchemy()

# 数据库模型定义
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(60), nullable=False)
    contact = db.Column(db.String(60), nullable=False)
    avatar = db.Column(db.String(20), nullable=False, default='default_avatar.png')
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    items = db.relationship('Item', backref='seller', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    views = db.Column(db.Integer, nullable=False, default=0, index=True)
    stock = db.Column(db.Integer, nullable=False, default=1)
    followers = db.relationship('Follow', backref='item', lazy=True)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, index=True)
    date_followed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    user = db.relationship('User', backref='follows', lazy=True)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref='requests', lazy=True)

# 交流广场模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref='posts', lazy=True)
    # 关联点赞和回复
    likes = db.relationship('Like', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    # 明确指定使用post_id外键
    replies = db.relationship('Reply', backref='post', foreign_keys='Reply.post_id', lazy='dynamic', cascade='all, delete-orphan')

# 点赞模型
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_liked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    user = db.relationship('User', backref='likes', lazy=True)

# 回复点赞模型
class ReplyLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_liked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', backref='reply_likes', lazy=True)
    # 建立与Reply模型的关系，通过backref创建反向引用
    reply = db.relationship('Reply', backref=db.backref('likes', lazy='dynamic', cascade='all, delete-orphan'), lazy=True)

# 用户关注模型
class UserFollow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    date_followed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 关系定义
    follower = db.relationship('User', foreign_keys=[follower_id], backref=db.backref('following', lazy='dynamic', cascade='all, delete-orphan'))
    followed = db.relationship('User', foreign_keys=[followed_id], backref=db.backref('followers', lazy='dynamic', cascade='all, delete-orphan'))

# 回复模型
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False, index=True)
    # 引用字段，关联到被回复的Post
    quoted_post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='SET NULL'), nullable=True)
    quoted_post = db.relationship('Post', foreign_keys=[quoted_post_id], backref='quoted_in_replies', lazy=True)
    # 引用字段，关联到被回复的Reply
    quoted_reply_id = db.Column(db.Integer, db.ForeignKey('reply.id', ondelete='SET NULL'), nullable=True)
    quoted_reply = db.relationship('Reply', remote_side=[id], backref='quoted_in_replies', lazy=True)
    user = db.relationship('User', backref='replies', lazy=True)

# 私信模型
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    is_read = db.Column(db.Boolean, nullable=False, default=False, index=True)
    # 关联发送者和接收者
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages', lazy=True)
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages', lazy=True)

# 通知模型
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    notification_type = db.Column(db.String(50), nullable=False, index=True)  # follow_user, follow_item, reply_post, reply_reply, like_post, like_reply
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False, index=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    related_id = db.Column(db.Integer, nullable=True)  # 关联的对象ID（商品ID、帖子ID、回复ID等）
    
    # 关联用户
    user = db.relationship('User', foreign_keys=[user_id], backref='notifications', lazy=True)
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_notifications', lazy=True)

# 库存模型
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    description = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref='stocks', lazy=True)
