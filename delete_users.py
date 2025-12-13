from app import create_app, db
from app.models import User, Item, Follow, Request, Post, Like, ReplyLike, UserFollow, Reply, Message, Notification, Stock

app = create_app()
with app.app_context():
    # 删除testuser用户
    testuser = User.query.filter_by(username='testuser').first()
    if testuser:
        print(f"找到用户: {testuser.username}, ID: {testuser.id}")
        
        # 删除关联数据
        # 删除用户的商品
        Item.query.filter_by(user_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的商品")
        
        # 删除用户的关注商品记录
        Follow.query.filter_by(user_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的关注商品记录")
        
        # 删除用户的求购信息
        Request.query.filter_by(user_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的求购信息")
        
        # 删除用户的帖子
        Post.query.filter_by(user_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的帖子")
        
        # 删除用户的点赞
        Like.query.filter_by(user_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的点赞")
        
        # 删除用户的回复点赞
        ReplyLike.query.filter_by(user_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的回复点赞")
        
        # 删除用户的关注关系
        UserFollow.query.filter_by(follower_id=testuser.id).delete()
        UserFollow.query.filter_by(followed_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的关注关系")
        
        # 删除用户的回复
        Reply.query.filter_by(user_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的回复")
        
        # 删除用户的私信
        Message.query.filter_by(sender_id=testuser.id).delete()
        Message.query.filter_by(receiver_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的私信")
        
        # 删除用户的通知
        Notification.query.filter_by(user_id=testuser.id).delete()
        Notification.query.filter_by(sender_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的通知")
        
        # 删除用户的库存
        Stock.query.filter_by(user_id=testuser.id).delete()
        print(f"已删除用户 {testuser.username} 的库存")
        
        # 删除用户本身
        db.session.delete(testuser)
        db.session.commit()
        print(f"已删除用户: {testuser.username}")
    else:
        print("未找到testuser用户")
    
    # 删除admin用户
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print(f"找到用户: {admin.username}, ID: {admin.id}")
        
        # 删除关联数据
        # 删除用户的商品
        Item.query.filter_by(user_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的商品")
        
        # 删除用户的关注商品记录
        Follow.query.filter_by(user_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的关注商品记录")
        
        # 删除用户的求购信息
        Request.query.filter_by(user_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的求购信息")
        
        # 删除用户的帖子
        Post.query.filter_by(user_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的帖子")
        
        # 删除用户的点赞
        Like.query.filter_by(user_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的点赞")
        
        # 删除用户的回复点赞
        ReplyLike.query.filter_by(user_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的回复点赞")
        
        # 删除用户的关注关系
        UserFollow.query.filter_by(follower_id=admin.id).delete()
        UserFollow.query.filter_by(followed_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的关注关系")
        
        # 删除用户的回复
        Reply.query.filter_by(user_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的回复")
        
        # 删除用户的私信
        Message.query.filter_by(sender_id=admin.id).delete()
        Message.query.filter_by(receiver_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的私信")
        
        # 删除用户的通知
        Notification.query.filter_by(user_id=admin.id).delete()
        Notification.query.filter_by(sender_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的通知")
        
        # 删除用户的库存
        Stock.query.filter_by(user_id=admin.id).delete()
        print(f"已删除用户 {admin.username} 的库存")
        
        # 删除用户本身
        db.session.delete(admin)
        db.session.commit()
        print(f"已删除用户: {admin.username}")
    else:
        print("未找到admin用户")
    
    print("用户删除操作完成")