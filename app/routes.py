from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from .models import db, User, Item, Follow, Request, Post, Like, ReplyLike, UserFollow, Reply, Message, Notification, Stock
from .forms import RegistrationForm, LoginForm, ItemForm, ProfileForm, RequestForm, PostForm, ReplyForm, StockForm
from .utils import save_picture, format_content, get_pagination_data

# 创建蓝图对象
main = Blueprint('main', __name__)


# --- 路由逻辑 --- 
@main.route("/")
def welcome():
    return render_template('welcome.html')


@main.route("/market")
def market():
    # 获取排序参数，默认按最新排序
    sort_by = request.args.get('sort_by', 'latest')
    # 获取搜索参数
    search_query = request.args.get('search', '')
    # 获取页码
    page = request.args.get('page', 1, type=int)
    
    # 基础查询
    query = Item.query
    
    # 应用搜索过滤
    if search_query:
        query = query.filter(Item.title.ilike(f'%{search_query}%') | Item.description.ilike(f'%{search_query}%'))
    
    # 根据排序参数选择排序方式
    if sort_by == 'latest':
        query = query.order_by(Item.date_posted.desc())
    elif sort_by == 'most_followed':
        # 按关注数排序，需要使用外连接和计数
        query = query.outerjoin(Follow).group_by(Item.id).order_by(db.func.count(Follow.id).desc())
    elif sort_by == 'most_viewed':
        query = query.order_by(Item.views.desc())
    elif sort_by == 'price_asc':
        query = query.order_by(Item.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Item.price.desc())
    else:
        query = query.order_by(Item.date_posted.desc())
    
    # 应用分页
    pagination, items = get_pagination_data(query, page, per_page=12)
    
    return render_template('index.html', items=items, current_sort=sort_by, search_query=search_query, pagination=pagination)


@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, 
                    contact=form.contact.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('账号创建成功，请登录！', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='注册', form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('登录成功！', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('登录失败，请检查邮箱或密码', 'danger')
    return render_template('login.html', title='登录', form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route("/item/new", methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    # 获取当前用户的库存物品列表
    user_stocks = Stock.query.filter_by(user_id=current_user.id).order_by(Stock.name.asc()).all()
    
    if form.validate_on_submit():
        # 手动输入商品信息
        pic_file = 'default.jpg'
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
        
        # 保存商品到数据库
        db.session.add(item)
        db.session.commit()
        flash('商品发布成功！', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('create_item.html', title='发布商品', form=form, stocks=user_stocks)


# 从库存添加商品路由
@main.route("/item/add_from_stock", methods=['POST'])
@login_required
def add_stock_item():
    # 获取表单数据
    stock_id = request.form.get('stock_id')
    stock_quantity = int(request.form.get('stock_quantity', 1))
    stock_price = float(request.form.get('stock_price', 0.01))
    use_stock_description = request.form.get('use_stock_description') == 'on'
    
    # 检查库存物品是否存在
    stock_item = Stock.query.get_or_404(stock_id)
    
    # 检查是否为当前用户的库存物品
    if stock_item.user_id != current_user.id:
        flash('您没有权限操作此库存物品！', 'danger')
        return redirect(url_for('main.new_item'))
    
    # 检查上货数量是否超过库存数量
    if stock_quantity > stock_item.quantity:
        flash('上货数量不能超过库存数量！', 'danger')
        return redirect(url_for('main.new_item'))
    
    # 创建新商品
    item = Item(
        title=stock_item.name,
        description=stock_item.description if use_stock_description else '',
        price=stock_price,
        stock=stock_quantity,
        image_file=stock_item.image_file,
        seller=current_user
    )
    
    # 更新库存数量
    stock_item.quantity -= stock_quantity
    
    # 如果库存数量为0，删除库存物品
    if stock_item.quantity == 0:
        # 删除库存物品的图片（如果不是默认图片）
        if stock_item.image_file != 'default.jpg':
            from flask import current_app
            picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], stock_item.image_file)
            if os.path.exists(picture_path):
                import os
                os.remove(picture_path)
        db.session.delete(stock_item)
    
    # 保存商品到数据库
    db.session.add(item)
    db.session.commit()
    flash('商品发布成功！', 'success')
    return redirect(url_for('main.home'))


@main.route("/item/<int:item_id>")
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    item.views += 1
    db.session.commit()
    return render_template('item_detail.html', title=item.title, item=item)


@main.route("/item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.seller != current_user and not current_user.is_admin:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('商品已删除', 'success')
    return redirect(url_for('main.profile'))


@main.route("/item/<int:item_id>/follow", methods=['POST'])
@login_required
def follow_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    # 检查是否是自己的商品
    if item.user_id == current_user.id:
        flash('您不能关注自己的商品！', 'danger')
        return redirect(url_for('main.item_detail', item_id=item.id))
    
    # 检查是否已经关注
    follow = Follow.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if not follow:
        try:
            follow = Follow(user_id=current_user.id, item_id=item.id)
            db.session.add(follow)
            
            # 添加关注商品通知
            notification = Notification(
                user_id=item.user_id,
                sender_id=current_user.id,
                notification_type='follow_item',
                content=f'{current_user.username} 关注了您的商品 "{item.title}"',
                related_id=item.id
            )
            db.session.add(notification)
            
            db.session.commit()
            flash('已成功关注该商品', 'success')
        except Exception as e:
            db.session.rollback()
            flash('关注商品失败，请稍后重试！', 'danger')
            print(f"关注商品错误: {e}")
    return redirect(url_for('main.item_detail', item_id=item.id))


@main.route("/item/<int:item_id>/unfollow", methods=['POST'])
@login_required
def unfollow_item(item_id):
    item = Item.query.get_or_404(item_id)
    follow = Follow.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        flash('已取消关注该商品', 'success')
    return redirect(url_for('main.item_detail', item_id=item.id))


@main.route("/profile")
@login_required
def profile():
    # 创建库存表单对象
    form = StockForm()
    # 获取当前用户发布的所有商品
    user_items = Item.query.filter_by(user_id=current_user.id).order_by(Item.date_posted.desc()).all()
    # 获取当前用户关注的所有商品
    followed_items = Item.query.join(Follow).filter(Follow.user_id == current_user.id).order_by(Follow.date_followed.desc()).all()
    # 获取当前用户发布的所有求购信息
    user_requests = Request.query.filter_by(user_id=current_user.id).order_by(Request.date_posted.desc()).all()
    # 获取当前用户发布的所有帖子
    user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).all()
    # 获取当前用户发布的所有回复
    user_replies = Reply.query.filter_by(user_id=current_user.id).order_by(Reply.date_posted.desc()).all()
    # 获取当前用户的所有库存物品
    user_stocks = Stock.query.filter_by(user_id=current_user.id).order_by(Stock.date_added.desc()).all()
    return render_template('profile.html', title='个人中心', user=current_user, items=user_items, followed_items=followed_items, requests=user_requests, posts=user_posts, replies=user_replies, stocks=user_stocks, form=form)


@main.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # 检查邮箱是否被其他用户使用
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user and existing_user.id != current_user.id:
            flash('该邮箱已被其他用户使用！', 'danger')
            return redirect(url_for('main.edit_profile'))
        
        # 处理头像上传
        if form.avatar.data:
            avatar_file = save_picture(form.avatar.data, is_avatar=True)
            # 删除旧头像（如果不是默认头像）
            if current_user.avatar != 'default_avatar.png':
                from flask import current_app
                old_avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', current_user.avatar)
                if os.path.exists(old_avatar_path):
                    import os
                    os.remove(old_avatar_path)
            current_user.avatar = avatar_file
        
        # 处理密码修改
        if form.current_password.data or form.new_password.data or form.confirm_new_password.data:
            # 检查当前密码是否正确
            if not check_password_hash(current_user.password, form.current_password.data):
                flash('当前密码错误！', 'danger')
                return redirect(url_for('main.edit_profile'))
            
            # 检查新密码是否为空
            if not form.new_password.data:
                flash('新密码不能为空！', 'danger')
                return redirect(url_for('main.edit_profile'))
            
            # 更新密码
            hashed_password = generate_password_hash(form.new_password.data)
            current_user.password = hashed_password
        
        # 更新用户信息
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.contact = form.contact.data
        db.session.commit()
        flash('个人信息已成功更新！', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        # 预填充表单
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.contact.data = current_user.contact
    return render_template('edit_profile.html', title='编辑资料', form=form)


@main.route("/item/<int:item_id>/update", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('您没有权限修改此商品！', 'danger')
        return redirect(url_for('main.profile'))
    
    form = ItemForm()
    if form.validate_on_submit():
        # 更新商品信息
        item.title = form.title.data
        item.price = form.price.data
        item.stock = form.stock.data
        item.description = form.description.data
        
        # 处理图片更新
        if form.picture.data:
            picture_file = save_picture(form.picture.data, is_avatar=False)
            # 删除旧图片（如果不是默认图片）
            if item.image_file != 'default.jpg':
                from flask import current_app
                old_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], item.image_file)
                if os.path.exists(old_picture_path):
                    import os
                    os.remove(old_picture_path)
            item.image_file = picture_file
        
        db.session.commit()
        flash('商品信息已成功更新！', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        # 预填充表单
        form.title.data = item.title
        form.price.data = item.price
        form.stock.data = item.stock
        form.description.data = item.description
    
    return render_template('update_item.html', title='编辑商品', form=form, item=item)


# --- 求购相关路由 ---
@main.route("/requests")
def requests():
    # 获取页码
    page = request.args.get('page', 1, type=int)
    # 获取搜索参数
    search_query = request.args.get('search', '')
    
    # 基础查询
    query = Request.query
    
    # 应用搜索过滤
    if search_query:
        query = query.filter(Request.title.ilike(f'%{search_query}%') | Request.description.ilike(f'%{search_query}%'))
    
    # 按最新排序
    query = query.order_by(Request.date_posted.desc())
    
    # 应用分页
    pagination, requests_list = get_pagination_data(query, page, per_page=12)
    
    return render_template('requests.html', title='求购信息', requests=requests_list, pagination=pagination, search_query=search_query)


@main.route("/request/new", methods=['GET', 'POST'])
@login_required
def new_request():
    form = RequestForm()
    if form.validate_on_submit():
        pic_file = 'default.jpg'
        if form.picture.data:
            pic_file = save_picture(form.picture.data, is_avatar=False)
        request_item = Request(title=form.title.data, description=form.description.data, 
                          price=form.price.data, image_file=pic_file, user=current_user)
        db.session.add(request_item)
        db.session.commit()
        flash('求购信息发布成功！', 'success')
        return redirect(url_for('main.requests'))
    return render_template('create_request.html', title='发布求购', form=form)


@main.route("/request/<int:request_id>")
def request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    return render_template('request_detail.html', title=req.title, request=req)


@main.route("/request/<int:request_id>/update", methods=['GET', 'POST'])
@login_required
def update_request(request_id):
    req = Request.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        flash('您没有权限修改此求购信息！', 'danger')
        return redirect(url_for('main.requests'))
    
    form = RequestForm()
    if form.validate_on_submit():
        # 更新求购信息
        req.title = form.title.data
        req.price = form.price.data
        req.description = form.description.data
        
        # 处理图片更新
        if form.picture.data:
            pic_file = save_picture(form.picture.data, is_avatar=False)
            # 删除旧图片（如果不是默认图片）
            if req.image_file != 'default.jpg':
                from flask import current_app
                old_pic_path = os.path.join(current_app.config['UPLOAD_FOLDER'], req.image_file)
                if os.path.exists(old_pic_path):
                    import os
                    os.remove(old_pic_path)
            req.image_file = pic_file
        
        db.session.commit()
        flash('求购信息已成功更新！', 'success')
        return redirect(url_for('main.requests'))
    elif request.method == 'GET':
        # 预填充表单
        form.title.data = req.title
        form.price.data = req.price
        form.description.data = req.description
    
    return render_template('update_request.html', title='编辑求购', form=form, request=req)


@main.route("/request/<int:request_id>/delete", methods=['POST'])
@login_required
def delete_request(request_id):
    req = Request.query.get_or_404(request_id)
    if req.user_id != current_user.id and not current_user.is_admin:
        flash('您没有权限删除此求购信息！', 'danger')
        return redirect(url_for('main.requests'))
    
    # 删除求购信息对应的图片（如果不是默认图片）
    if req.image_file != 'default.jpg':
        from flask import current_app
        pic_path = os.path.join(current_app.config['UPLOAD_FOLDER'], req.image_file)
        if os.path.exists(pic_path):
            import os
            os.remove(pic_path)
    
    db.session.delete(req)
    db.session.commit()
    flash('求购信息已删除', 'success')
    return redirect(url_for('main.requests'))


# 关注用户路由
@main.route("/user/<int:user_id>/follow", methods=['POST'])
@login_required
def follow_user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('您不能关注自己！', 'danger')
        return redirect(url_for('main.user_profile', user_id=user_id))
    
    # 检查是否已经关注
    follow = UserFollow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    if not follow:
        follow = UserFollow(follower_id=current_user.id, followed_id=user_id)
        db.session.add(follow)
        
        # 添加关注通知
        notification = Notification(
            user_id=user.id,
            sender_id=current_user.id,
            notification_type='follow_user',
            content=f'{current_user.username} 关注了您',
            related_id=current_user.id
        )
        db.session.add(notification)
        
        db.session.commit()
        flash(f'您已成功关注 {user.username}！', 'success')
    return redirect(request.referrer or url_for('main.user_profile', user_id=user_id))


# 取消关注用户路由
@main.route("/user/<int:user_id>/unfollow", methods=['POST'])
@login_required
def unfollow_user(user_id):
    user = User.query.get_or_404(user_id)
    follow = UserFollow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        flash(f'您已取消关注 {user.username}！', 'success')
    return redirect(request.referrer or url_for('main.user_profile', user_id=user_id))


# 交流广场路由
@main.route("/square", methods=['GET', 'POST'])
@login_required
def square():
    form = PostForm()
    reply_forms = {}
    
    # 获取搜索参数
    search_query = request.args.get('search', '')
    search_type = request.args.get('search_type', 'content')
    # 获取页码
    page = request.args.get('page', 1, type=int)
    
    # 根据搜索参数和类型过滤帖子
    if search_query:
        if search_type == 'user':
            # 搜索用户发言（根据用户名搜索）
            query = Post.query.join(User).filter(User.username.ilike(f'%{search_query}%'))
        else:
            # 搜索发言内容
            query = Post.query.filter(Post.content.ilike(f'%{search_query}%'))
    else:
        query = Post.query
    
    # 按时间升序排列
    query = query.order_by(Post.date_posted.asc())
    
    # 应用分页
    pagination, posts = get_pagination_data(query, page, per_page=20)
    
    # 为每条帖子创建一个回复表单
    for post in posts:
        reply_forms[post.id] = ReplyForm()
    
    if form.validate_on_submit():
        # 处理图片上传
        image_file = None
        if form.picture.data:
            image_file = save_picture(form.picture.data, is_avatar=False)
        
        # 创建新留言
        post = Post(content=form.content.data, image_file=image_file, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('留言发布成功！', 'success')
        return redirect(url_for('main.square', new_message='true'))
    
    # 将Reply模型和搜索参数传递给模板上下文
    return render_template('square.html', title='交流广场', form=form, posts=posts, reply_forms=reply_forms, Reply=Reply, search_query=search_query, search_type=search_type, pagination=pagination)


# 点赞路由
@main.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    # 检查是否已经点赞
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
        if post.user_id != current_user.id:
            notification = Notification(
                user_id=post.user_id,
                sender_id=current_user.id,
                notification_type='like_post',
                content=f'{current_user.username} 点赞了您的帖子',
                related_id=post.id
            )
            db.session.add(notification)
        
        flash('点赞成功！', 'success')
    
    db.session.commit()
    return redirect(url_for('main.square'))


# 回复点赞路由
@main.route("/reply/<int:reply_id>/like", methods=['POST'])
@login_required
def like_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    # 检查是否已经点赞
    like = ReplyLike.query.filter_by(user_id=current_user.id, reply_id=reply_id).first()
    
    if like:
        # 取消点赞
        db.session.delete(like)
        flash('已取消点赞！', 'success')
    else:
        # 添加点赞
        like = ReplyLike(user_id=current_user.id, reply_id=reply_id)
        db.session.add(like)
        
        # 添加回复点赞通知
        if reply.user_id != current_user.id:
            notification = Notification(
                user_id=reply.user_id,
                sender_id=current_user.id,
                notification_type='like_reply',
                content=f'{current_user.username} 点赞了您的回复',
                related_id=reply.id
            )
            db.session.add(notification)
        
        flash('点赞成功！', 'success')
    
    db.session.commit()
    return redirect(url_for('main.square'))


# 回复路由
@main.route("/post/<int:post_id>/reply", methods=['POST'])
@login_required
def reply_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = ReplyForm()
    
    if form.validate_on_submit():
        # 获取引用的ID和类型
        quoted_id = request.form.get('quoted_post_id')
        quoted_type = request.form.get('quoted_type')
        
        quoted_post_id = None
        quoted_reply_id = None
        
        # 根据类型设置相应的引用ID
        if quoted_id and quoted_type:
            if quoted_type == 'post':
                quoted_post_id = quoted_id
            elif quoted_type == 'reply':
                quoted_reply_id = quoted_id
        
        # 创建回复
        reply = Reply(
            content=form.content.data, 
            user_id=current_user.id, 
            post_id=post_id,
            quoted_post_id=quoted_post_id,
            quoted_reply_id=quoted_reply_id
        )
        db.session.add(reply)
        
        # 添加回复通知
        if post.user_id != current_user.id:
            notification = Notification(
                user_id=post.user_id,
                sender_id=current_user.id,
                notification_type='reply_post',
                content=f'{current_user.username} 回复了您的帖子',
                related_id=post.id
            )
            db.session.add(notification)
        
        # 如果是回复回复，给被回复的人也发通知
        if quoted_reply_id:
            quoted_reply = Reply.query.get_or_404(quoted_reply_id)
            if quoted_reply.user_id != current_user.id and quoted_reply.user_id != post.user_id:
                notification = Notification(
                    user_id=quoted_reply.user_id,
                    sender_id=current_user.id,
                    notification_type='reply_reply',
                    content=f'{current_user.username} 回复了您的评论',
                    related_id=quoted_reply.id
                )
                db.session.add(notification)
        
        db.session.commit()
        flash('回复成功！', 'success')
    
    return redirect(url_for('main.square'))


# 删除帖子路由
@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    # 删除帖子相关的图片（如果有）
    if post.image_file:
        from flask import current_app
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image_file)
        if os.path.exists(image_path):
            import os
            os.remove(image_path)
    
    # 删除帖子（级联删除会自动处理相关的点赞和回复）
    db.session.delete(post)
    db.session.commit()
    flash('留言已删除', 'success')
    return redirect(url_for('main.square'))


# 删除回复路由
@main.route("/reply/<int:reply_id>/delete", methods=['POST'])
@login_required
def delete_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    if reply.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    # 删除回复（级联删除会自动处理相关的点赞）
    db.session.delete(reply)
    db.session.commit()
    flash('回复已删除', 'success')
    return redirect(url_for('main.square'))


# 用户信息路由 - 用于弹出窗口显示用户信息
@main.route("/user/<int:user_id>/info")
@login_required
def user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_info.html', user=user)


# 其他用户的个人主页路由
@main.route("/user/<int:user_id>/profile")
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    # 获取该用户发布的所有商品
    user_items = Item.query.filter_by(user_id=user.id).order_by(Item.date_posted.desc()).all()
    # 获取该用户关注的所有商品
    followed_items = Item.query.join(Follow).filter(Follow.user_id == user.id).order_by(Follow.date_followed.desc()).all()
    # 获取该用户发布的所有求购信息
    user_requests = Request.query.filter_by(user_id=user.id).order_by(Request.date_posted.desc()).all()
    # 获取该用户发布的所有帖子
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).all()
    # 获取该用户发布的所有回复
    user_replies = Reply.query.filter_by(user_id=user.id).order_by(Reply.date_posted.desc()).all()
    
    # 只有当查看自己的个人主页时，才获取库存物品
    user_stocks = []
    form = None
    if user.id == current_user.id:
        # 创建库存表单对象
        form = StockForm()
        # 获取该用户的所有库存物品
        user_stocks = Stock.query.filter_by(user_id=user.id).order_by(Stock.date_added.desc()).all()
    
    return render_template('profile.html', title=f'{user.username}的个人主页', user=user, items=user_items, followed_items=followed_items, requests=user_requests, posts=user_posts, replies=user_replies, stocks=user_stocks, form=form)


# 添加库存路由
@main.route('/stock/new', methods=['GET', 'POST'])
@login_required
def add_stock():
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
        
        flash('库存物品添加成功！', 'success')
        return redirect(url_for('main.profile'))
    
    # 如果是GET请求，重定向到profile页面
    return redirect(url_for('main.profile'))


# 更新库存路由
@main.route('/stock/<int:stock_id>/update', methods=['GET', 'POST'])
@login_required
def update_stock(stock_id):
    # 获取库存物品
    stock = Stock.query.get_or_404(stock_id)
    
    # 检查用户是否有权限更新该库存物品
    if stock.user != current_user:
        abort(403)
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        picture = request.files.get('picture')
        
        # 更新库存物品信息
        stock.name = name
        stock.quantity = int(quantity)
        stock.description = description
        
        # 处理图片上传（如果有新图片）
        if picture:
            # 删除旧图片（如果不是默认图片）
            if stock.image_file != 'default.jpg':
                from flask import current_app
                old_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], stock.image_file)
                if os.path.exists(old_picture_path):
                    import os
                    os.remove(old_picture_path)
            # 保存新图片
            stock.image_file = save_picture(picture, is_avatar=False)
        
        # 保存到数据库
        db.session.commit()
        
        flash('库存物品更新成功！', 'success')
        return redirect(url_for('main.profile'))
    
    # 如果是GET请求，重定向到profile页面
    return redirect(url_for('main.profile'))


# 删除库存路由
@main.route('/stock/<int:stock_id>/delete', methods=['POST'])
@login_required
def delete_stock(stock_id):
    # 获取库存物品
    stock = Stock.query.get_or_404(stock_id)
    
    # 检查用户是否有权限删除该库存物品
    if stock.user != current_user:
        abort(403)
    
    # 删除库存物品的图片（如果不是默认图片）
    if stock.image_file != 'default.jpg':
        from flask import current_app
        picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], stock.image_file)
        if os.path.exists(picture_path):
            import os
            os.remove(picture_path)
    
    # 从数据库中删除库存物品
    db.session.delete(stock)
    db.session.commit()
    
    flash('库存物品已删除', 'success')
    return redirect(url_for('main.profile'))


# 私信功能路由
@main.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    # 获取搜索参数
    search_query = request.args.get('search', '')
    
    # 获取所有用户（用于搜索）
    if search_query:
        users = User.query.filter(User.username.ilike(f'%{search_query}%'), User.id != current_user.id).all()
    else:
        users = []
    
    # 获取当前用户的所有对话对象
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(receiver_id=current_user.id).all()
    
    # 合并对话对象
    conversation_users = set()
    for msg in sent_messages:
        conversation_users.add(msg.receiver)
    for msg in received_messages:
        conversation_users.add(msg.sender)
    
    # 按最近消息时间排序
    def get_latest_message(user):
        # 获取与该用户的最新消息
        latest_sent = Message.query.filter_by(sender_id=current_user.id, receiver_id=user.id).order_by(Message.date_sent.desc()).first()
        latest_received = Message.query.filter_by(sender_id=user.id, receiver_id=current_user.id).order_by(Message.date_sent.desc()).first()
        
        if latest_sent and latest_received:
            return max(latest_sent, latest_received, key=lambda x: x.date_sent)
        elif latest_sent:
            return latest_sent
        elif latest_received:
            return latest_received
        return None
    
    # 计算未读消息数量
    def get_unread_count(user):
        return Message.query.filter_by(sender_id=user.id, receiver_id=current_user.id, is_read=False).count()
    
    conversation_users = sorted(conversation_users, key=lambda x: get_latest_message(x).date_sent if get_latest_message(x) else datetime.min, reverse=True)
    
    # 为每个对话用户添加未读消息数量
    conversation_data = []
    for user in conversation_users:
        conversation_data.append({
            'user': user,
            'latest_message': get_latest_message(user),
            'unread_count': get_unread_count(user)
        })
    
    # 获取当前选中的对话用户
    selected_user_id = request.args.get('user_id')
    selected_user = User.query.get(selected_user_id) if selected_user_id else None
    
    # 获取聊天记录
    messages_list = []
    if selected_user:
        messages_list = Message.query.filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == selected_user.id)) |
            ((Message.sender_id == selected_user.id) & (Message.receiver_id == current_user.id))
        ).order_by(Message.date_sent.asc()).all()
        
        # 将未读消息标记为已读
        for msg in messages_list:
            if msg.receiver_id == current_user.id and not msg.is_read:
                msg.is_read = True
        db.session.commit()
    
    # 处理发送消息
    if request.method == 'POST' and selected_user:
        content = request.form.get('content')
        if content:
            message = Message(sender_id=current_user.id, receiver_id=selected_user.id, content=content)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('main.messages', user_id=selected_user.id))
    
    return render_template('messages.html', title='私信', users=users, conversation_data=conversation_data, selected_user=selected_user, messages=messages_list, search_query=search_query)


# 搜索用户路由
@main.route('/search_users')
@login_required
def search_users():
    search_query = request.args.get('q', '')
    if search_query:
        users = User.query.filter(
            User.username.ilike(f'%{search_query}%'),
            User.id != current_user.id
        ).all()
    else:
        users = User.query.filter(User.id != current_user.id).all()
    
    # 返回JSON格式的用户列表
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'avatar': user.avatar,
            'avatar_url': url_for('static', filename=f'uploads/avatars/{user.avatar}', _external=True)
        })
    
    return jsonify(users_data)


# 通知列表路由
@main.route('/notifications')
@login_required
def notifications():
    # 获取页码
    page = request.args.get('page', 1, type=int)
    
    # 获取当前用户的所有通知，按时间倒序排列
    query = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date_created.desc())
    
    # 应用分页
    pagination, notifications_list = get_pagination_data(query, page, per_page=20)
    
    return render_template('notifications.html', title='通知', notifications=notifications_list, pagination=pagination)


# 通知重定向路由（点击通知跳转）
@main.route('/notification/<int:notification_id>/redirect')
@login_required
def notification_redirect(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    
    # 确保通知属于当前用户
    if notification.user_id != current_user.id:
        abort(403)
    
    # 标记通知为已读
    if not notification.is_read:
        notification.is_read = True
        db.session.commit()
    
    # 根据通知类型跳转到相应页面
    if notification.notification_type == 'follow_user':
        # 跳转到关注者的个人主页
        return redirect(url_for('main.user_profile', user_id=notification.related_id))
    elif notification.notification_type == 'follow_item':
        # 跳转到被关注的商品页面
        return redirect(url_for('main.item_detail', item_id=notification.related_id))
    elif notification.notification_type == 'reply_post' or notification.notification_type == 'like_post':
        # 跳转到被回复或点赞的帖子页面
        return redirect(url_for('main.square') + f'#post-{notification.related_id}')
    elif notification.notification_type == 'reply_reply' or notification.notification_type == 'like_reply':
        # 跳转到被回复或点赞的回复所在的帖子页面
        reply = Reply.query.get_or_404(notification.related_id)
        return redirect(url_for('main.square') + f'#post-{reply.post_id}')
    else:
        # 默认跳转到通知列表
        return redirect(url_for('main.notifications'))


# 转发商品到私信路由
@main.route('/item/<int:item_id>/forward/message', methods=['POST'])
@login_required
def forward_to_message(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    
    if not receiver_id:
        return jsonify({'success': False, 'message': '请选择转发对象'})
    
    receiver = User.query.get_or_404(receiver_id)
    
    # 构建转发消息内容
    message_content = f"【商品转发】\n商品名称：{item.title}\n商品价格：¥{item.price}\n商品链接：{request.host_url}item/{item.id}\n卖家：{item.seller.username}\n库存：{item.stock}\n浏览：{item.views}\n关注：{len(item.followers)}\n\n{item.description}"
    
    # 创建消息
    message = Message(sender_id=current_user.id, receiver_id=receiver.id, content=message_content)
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '转发成功'})


# 上下文处理器
@main.app_context_processor
def utility_processors():
    def format_content(content):
        return format_content(content)
    
    def notifications_processor():
        if current_user.is_authenticated:
            # 获取当前用户的未读通知数量
            unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
            return unread_count
        return 0
    
    return dict(format_content=format_content, unread_notifications_count=notifications_processor)
