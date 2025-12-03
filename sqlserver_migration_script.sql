IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'CampusMarket') CREATE DATABASE CampusMarket;
USE CampusMarket;
GO
CREATE TABLE [User] (
    id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL,
    contact VARCHAR(60) NOT NULL,
    avatar VARCHAR(20) NOT NULL DEFAULT 'default_avatar.png',
    is_admin BIT NOT NULL DEFAULT 0
);
CREATE INDEX IX_User_username ON [User](username);
CREATE INDEX IX_User_email ON [User](email);
CREATE TABLE [Item] (
    id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    description TEXT NOT NULL,
    image_file VARCHAR(20) NOT NULL DEFAULT 'default.jpg',
    date_posted DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    user_id INT NOT NULL,
    views INT NOT NULL DEFAULT 0,
    stock INT NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES [User](id)
);
CREATE INDEX IX_Item_title ON [Item](title);
CREATE INDEX IX_Item_date_posted ON [Item](date_posted);
CREATE INDEX IX_Item_user_id ON [Item](user_id);
CREATE INDEX IX_Item_views ON [Item](views);
CREATE TABLE [Follow] (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    date_followed DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (user_id) REFERENCES [User](id),
    FOREIGN KEY (item_id) REFERENCES [Item](id)
);
CREATE INDEX IX_Follow_user_id ON [Follow](user_id);
CREATE INDEX IX_Follow_item_id ON [Follow](item_id);
CREATE INDEX IX_Follow_date_followed ON [Follow](date_followed);
CREATE TABLE [Request] (
    id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price FLOAT NOT NULL,
    image_file VARCHAR(20) NOT NULL DEFAULT 'default.jpg',
    date_posted DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES [User](id)
);
CREATE INDEX IX_Request_title ON [Request](title);
CREATE INDEX IX_Request_date_posted ON [Request](date_posted);
CREATE INDEX IX_Request_user_id ON [Request](user_id);
CREATE TABLE [Post] (
    id INT PRIMARY KEY IDENTITY(1,1),
    content TEXT NOT NULL,
    image_file VARCHAR(20) NULL,
    date_posted DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES [User](id)
);
CREATE INDEX IX_Post_date_posted ON [Post](date_posted);
CREATE INDEX IX_Post_user_id ON [Post](user_id);
CREATE TABLE [Like] (
    id INT PRIMARY KEY IDENTITY(1,1),
    date_liked DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES [User](id),
    FOREIGN KEY (post_id) REFERENCES [Post](id)
);
CREATE INDEX IX_Like_user_id ON [Like](user_id);
CREATE INDEX IX_Like_post_id ON [Like](post_id);
CREATE TABLE [UserFollow] (
    id INT PRIMARY KEY IDENTITY(1,1),
    follower_id INT NOT NULL,
    followed_id INT NOT NULL,
    date_followed DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (follower_id) REFERENCES [User](id),
    FOREIGN KEY (followed_id) REFERENCES [User](id)
);
CREATE INDEX IX_UserFollow_follower_id ON [UserFollow](follower_id);
CREATE INDEX IX_UserFollow_followed_id ON [UserFollow](followed_id);
CREATE TABLE [Reply] (
    id INT PRIMARY KEY IDENTITY(1,1),
    content TEXT NOT NULL,
    date_posted DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    quoted_post_id INT NULL,
    quoted_reply_id INT NULL,
    FOREIGN KEY (user_id) REFERENCES [User](id),
    FOREIGN KEY (post_id) REFERENCES [Post](id) ON DELETE CASCADE,
    FOREIGN KEY (quoted_post_id) REFERENCES [Post](id) ON DELETE SET NULL,
    FOREIGN KEY (quoted_reply_id) REFERENCES [Reply](id) ON DELETE SET NULL
);
CREATE INDEX IX_Reply_user_id ON [Reply](user_id);
CREATE INDEX IX_Reply_post_id ON [Reply](post_id);
CREATE INDEX IX_Reply_quoted_post_id ON [Reply](quoted_post_id);
CREATE INDEX IX_Reply_quoted_reply_id ON [Reply](quoted_reply_id);
CREATE TABLE [ReplyLike] (
    id INT PRIMARY KEY IDENTITY(1,1),
    date_liked DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    user_id INT NOT NULL,
    reply_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES [User](id),
    FOREIGN KEY (reply_id) REFERENCES [Reply](id) ON DELETE CASCADE
);
CREATE INDEX IX_ReplyLike_user_id ON [ReplyLike](user_id);
CREATE INDEX IX_ReplyLike_reply_id ON [ReplyLike](reply_id);
CREATE TABLE [Message] (
    id INT PRIMARY KEY IDENTITY(1,1),
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    content TEXT NOT NULL,
    date_sent DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    is_read BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (sender_id) REFERENCES [User](id),
    FOREIGN KEY (receiver_id) REFERENCES [User](id)
);
CREATE INDEX IX_Message_sender_id ON [Message](sender_id);
CREATE INDEX IX_Message_receiver_id ON [Message](receiver_id);
CREATE INDEX IX_Message_date_sent ON [Message](date_sent);
CREATE INDEX IX_Message_is_read ON [Message](is_read);
CREATE TABLE [Notification] (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    sender_id INT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    is_read BIT NOT NULL DEFAULT 0,
    date_created DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    related_id INT NULL,
    FOREIGN KEY (user_id) REFERENCES [User](id),
    FOREIGN KEY (sender_id) REFERENCES [User](id)
);
CREATE INDEX IX_Notification_user_id ON [Notification](user_id);
CREATE INDEX IX_Notification_sender_id ON [Notification](sender_id);
CREATE INDEX IX_Notification_notification_type ON [Notification](notification_type);
CREATE INDEX IX_Notification_is_read ON [Notification](is_read);
CREATE INDEX IX_Notification_date_created ON [Notification](date_created);
CREATE TABLE [Stock] (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    description TEXT NULL,
    image_file VARCHAR(20) NOT NULL DEFAULT 'default.jpg',
    date_added DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES [User](id)
);
CREATE INDEX IX_Stock_name ON [Stock](name);
CREATE INDEX IX_Stock_date_added ON [Stock](date_added);
CREATE INDEX IX_Stock_user_id ON [Stock](user_id);
GO
INSERT INTO [User] (username, email, password, contact, avatar, is_admin) VALUES ('琅琊老仙', '1812653271@qq.com', 'pbkdf2:sha256:260000$EM2B29Rc3oilgb17$82e5cc64b49f4f119b164ea06e44b7c8b7d961d281908be3c0d31583ac370bda', '1', '9d8fcd863f0ac2b0.png', 0);
INSERT INTO [User] (username, email, password, contact, avatar, is_admin) VALUES ('何春秋', '123456@qq.com', 'pbkdf2:sha256:260000$bcrTTkC6eNrleehn$f4e22b4e510dd3e226b9978f3e0bb5a29156dd2a84c7426456fb9f2564032700', '1', '15a6d2ab2edc3d66.jpg', 0);
INSERT INTO [User] (username, email, password, contact, avatar, is_admin) VALUES ('多宝真人', '1234567@qq.com', 'pbkdf2:sha256:260000$3eRxlZmR4LLhWYYt$ba7b47d8685e4e03824bb3a26fe53781b52818c236840f237e2b53e6f76493f6', '1', '0a570dc718fa67c9.png', 0);
INSERT INTO [User] (username, email, password, contact, avatar, is_admin) VALUES ('白狐仙子', '111111@qq.com', 'pbkdf2:sha256:260000$fbNaLqyY5Llms8y9$523dbadcded5fec2a9b0525e32b21083d3f904e6e958a59c502c51bbee4c9bfc', '1', '40bc12ac5ff407b9.png', 0);
INSERT INTO [User] (username, email, password, contact, avatar, is_admin) VALUES ('admin', 'admin@example.com', 'pbkdf2:sha256:260000$O8ads16w3Qhd2GiS$0ea4d9f6ad13692446eb2a7b1e30d1f6661d0526d6b5e50adf8877e5547a44c1', '13800138000', 'default_avatar.png', 1);
INSERT INTO [User] (username, email, password, contact, avatar, is_admin) VALUES ('testuser', 'test@example.com', 'password', '1234567890', 'default_avatar.png', 0);
GO
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('雷电蛊', 17.0, '难以反应，瞬间麻痹对手，给予对手强力一击！', '94473b544b0e4026.png', '2025-11-25 07:28:20', 1, 27, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('回旋风', 17.0, '远程遥击，并利用强劲的风力将对手带到面前，以便继续进攻！', 'a7d071101c2621e6.png', '2025-11-25 07:33:19', 1, 0, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('洁身自好', 3500.0, '对自身的道痕进行筛选和清理冲刷，精准分离并剥离对蛊仙不利的坏道痕，清除一切负面效果！', 'b78e83e2853d58b0.png', '2025-11-25 07:35:04', 1, 8, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('鬼灯蛊', 15.0, '在原地留下一只鬼灯笼蛊，敌人触碰引发爆炸，将敌人击飞！若十秒内敌人未接触，则鬼灯自动引爆，在周围的小范围内造成影响！', '64dc9051cf3ea5a1.png', '2025-11-25 07:38:33', 1, 0, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('火龙蛊', 15.0, '向前方喷吐出一只火龙，火龙来势汹汹，但是似乎是个死脑筋，不会拐弯！沿途撞到敌人则直接自爆！对敌人造成大量伤害！', 'dcd0eb1ff6db82d8.png', '2025-11-25 07:42:35', 1, 1, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('粘土鸟蛊', 1.0, '小巧灵活，适合用于干扰对手，拉扯游击。小鸟自动追踪敌人，接触敌人爆炸，如果追不上敌人，则飞行一段路程后自爆。', '6629b64ab08985ca.png', '2025-11-25 07:48:36', 2, 0, 999);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('粘土鸟仙蛊', 1000.0, '一只得力的坐骑！坐上大鸟，在高空飞行！增加移速，但是飞行一段时间后粘土大鸟必须休息，过段时间方可继续使用。', '7e11c69a11714771.png', '2025-11-25 07:51:43', 2, 0, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('起死回生蛊', 5000.0, '极其珍贵的治疗类蛊虫，能让人自动免疫一次致命的伤害，该效果一旦触发则仙蛊自毁，再没有任何效果！若在触发起死回生前使用，则可小幅度提升体质，小幅度加强自身大部分属性。', '5a8e768cd50ee26b.png', '2025-11-25 07:59:09', 2, 0, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('残招·逆流护身印', 2500.0, '反弹对手造成的伤害，但是仙蛊残缺，每次使用时反弹效果只能触发一次，无论反弹成功与否，之后的短时间内无法再催动。（对残招进行过改良，反弹成功后可以选择逃跑或者潜伏到对方身后进行偷袭！）', '72b020f7807157c0.png', '2025-11-25 08:03:13', 2, 0, 9999);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('名声蛊', 5000.0, '《人祖传》中的传奇蛊虫，太日阳莽曾经使用此蛊，但是收获的全是坏名声，不知你若使用。。。？', '77df04fa8a6de8ac.png', '2025-11-25 08:12:55', 3, 27, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('杀招雾隐', 20.0, '阴阴阴！隐形匿迹！', '076b73cd7da5b54d.png', '2025-11-25 08:14:47', 3, 2, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('木龙蛊', 12.0, '向前方释放一只巨大的木龙，之后使用者骑在木龙头上横冲直撞，一飞冲天，使用者可选择时机落下地面。', 'a735aeb42031a22a.png', '2025-11-25 08:16:50', 3, 0, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('木人蛊', 12.0, '木道蛊虫，人道效果，制造一个木人分身。', '716513ef34f13cd1.png', '2025-11-25 08:17:47', 3, 0, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('摸头蛊', 0.01, '没有实质性伤害，但是异常好用！挑衅对手，给他精神上的打击！零成本，大回报！', '4cbe6e566f871b26.png', '2025-11-25 08:19:50', 3, 47, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('神秘的宙道真传。。。', 1000.0, '极其珍贵，极其神秘的宙道真传，似乎是某位尊者的手笔。。。', 'd85496afae1380f2.png', '2025-11-25 11:22:56', 2, 59, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('红莲真传', 9999.0, '尊者真传，珍贵无比！', '4596eb52d9f44067.png', '2025-12-01 03:51:11', 2, 55, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('红莲真传', 8888.0, '尊者真传，珍贵无比！', '4596eb52d9f44067.png', '2025-12-01 14:10:23', 2, 13, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('红莲真传', 6666.0, '尊者真传，珍贵无比！', '4596eb52d9f44067.png', '2025-12-02 05:38:59', 2, 6, 1);
INSERT INTO [Item] (title, price, description, image_file, date_posted, user_id, views, stock) VALUES ('失败蛊', 1.0, '失败乃是成功之母。。。。。。', '287ee83868de5664.png', '2025-12-02 06:18:46', 4, 4, 1);
GO
INSERT INTO [Request] (title, description, price, image_file, date_posted, user_id) VALUES ('食道传承', '蛊仙传承，完整度不低于三成，至少姚有一套完整的仙道杀招。', 1000.0, 'default.jpg', '2025-11-26 17:00:38', 1);
INSERT INTO [Request] (title, description, price, image_file, date_posted, user_id) VALUES ('魔丸蛊', '转数越高价格越高！有多少要多少！', 500.0, '5af67c659c577374.jpg', '2025-11-30 13:27:06', 2);
GO
INSERT INTO [Post] (content, image_file, date_posted, user_id) VALUES ('小渡小渡！', NULL, '2025-11-27 10:03:24', 2);
INSERT INTO [Post] (content, image_file, date_posted, user_id) VALUES ('小渡开麦！', NULL, '2025-11-27 10:03:48', 2);
INSERT INTO [Post] (content, image_file, date_posted, user_id) VALUES ('今天炼出来一只六转书虫，要的私聊我！', 'bd57042af5aca9e7.png', '2025-11-27 10:07:05', 1);
INSERT INTO [Post] (content, image_file, date_posted, user_id) VALUES ('在我宝黄天内，任何人不得发布不良信息，不实信息，如若发现，将永久禁止进入宝黄天！！！', NULL, '2025-11-27 10:26:16', 3);
GO
INSERT INTO [Stock] (name, quantity, description, image_file, date_added, user_id) VALUES ('失败蛊', 9998, '失败乃是成功之母。。。。。。', '287ee83868de5664.png', '2025-12-01 02:53:24', 4);
INSERT INTO [Stock] (name, quantity, description, image_file, date_added, user_id) VALUES ('红莲真传', 9997, '尊者真传，珍贵无比！', '4596eb52d9f44067.png', '2025-12-01 03:42:21', 2);
GO
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (1, 11, '2025-11-26 15:26:24');
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (1, 16, '2025-11-26 15:30:27');
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (3, 16, '2025-11-30 08:50:57');
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (4, 16, '2025-11-30 10:23:26');
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (2, 15, '2025-12-01 06:06:32');
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (3, 17, '2025-12-01 06:15:39');
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (4, 11, '2025-12-01 06:35:12');
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (2, 11, '2025-12-01 08:21:03');
INSERT INTO [Follow] (user_id, item_id, date_followed) VALUES (4, 18, '2025-12-01 14:20:45');
GO
INSERT INTO [Like] (date_liked, user_id, post_id) VALUES ('2025-11-27 11:35:09', 1, 3);
INSERT INTO [Like] (date_liked, user_id, post_id) VALUES ('2025-11-27 11:35:24', 1, 4);
INSERT INTO [Like] (date_liked, user_id, post_id) VALUES ('2025-11-27 11:37:09', 3, 4);
INSERT INTO [Like] (date_liked, user_id, post_id) VALUES ('2025-11-27 13:26:23', 2, 4);
INSERT INTO [Like] (date_liked, user_id, post_id) VALUES ('2025-11-27 13:44:03', 2, 3);
INSERT INTO [Like] (date_liked, user_id, post_id) VALUES ('2025-11-27 13:48:33', 3, 3);
INSERT INTO [Like] (date_liked, user_id, post_id) VALUES ('2025-11-27 16:38:45', 4, 4);
INSERT INTO [Like] (date_liked, user_id, post_id) VALUES ('2025-11-27 16:38:47', 4, 3);
GO
INSERT INTO [UserFollow] (follower_id, followed_id, date_followed) VALUES (2, 4, '2025-12-01 17:12:07');
INSERT INTO [UserFollow] (follower_id, followed_id, date_followed) VALUES (2, 1, '2025-12-01 17:19:21');
INSERT INTO [UserFollow] (follower_id, followed_id, date_followed) VALUES (4, 2, '2025-12-02 07:59:07');
GO
INSERT INTO [Reply] (content, date_posted, user_id, post_id, quoted_post_id, quoted_reply_id) VALUES ('我看你是老糊涂了，把这玩意炼到六转有什么用？吃饱了撑的？', '2025-11-27 10:57:06', 2, 3, 3, NULL);
INSERT INTO [Reply] (content, date_posted, user_id, post_id, quoted_post_id, quoted_reply_id) VALUES ('乐子', '2025-11-27 11:27:32', 2, 3, 3, NULL);
INSERT INTO [Reply] (content, date_posted, user_id, post_id, quoted_post_id, quoted_reply_id) VALUES ('你小子什么意思？你不要就快滚！有的是人想要！', '2025-11-27 11:47:32', 1, 3, 1, NULL);
INSERT INTO [Reply] (content, date_posted, user_id, post_id, quoted_post_id, quoted_reply_id) VALUES ('小老头别急嘛，我愿意出十块元石，卖给我吧！不然这货要烂在你手里了！', '2025-11-27 15:26:01', 2, 3, NULL, NULL);
INSERT INTO [Reply] (content, date_posted, user_id, post_id, quoted_post_id, quoted_reply_id) VALUES ('支持！', '2025-11-27 15:55:45', 2, 4, NULL, NULL);
GO
INSERT INTO [ReplyLike] (date_liked, user_id, reply_id) VALUES ('2025-11-27 11:37:13', 3, 1);
INSERT INTO [ReplyLike] (date_liked, user_id, reply_id) VALUES ('2025-11-27 13:43:58', 2, 1);
INSERT INTO [ReplyLike] (date_liked, user_id, reply_id) VALUES ('2025-11-27 16:38:49', 4, 1);
GO
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '地灵何在？', '2025-11-29 17:34:22', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '主人！！！你什么时候回来啊？', '2025-11-29 17:37:55', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '> 主人！！！你什么时候回来啊？

放心，乖乖呆在福地，我会回来的', '2025-11-30 07:00:17', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '> : 放心，乖乖呆在福地，我会回来的

好的！！！主人！', '2025-11-30 07:07:59', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '
', '2025-11-30 07:09:37', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, ' ', '2025-11-30 07:09:48', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, ' ', '2025-11-30 07:09:49', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (3, 1, '【商品转发】
商品名称：红莲真传
商品价格：¥9999.0
商品链接：http://127.0.0.1:5000/item/17

尊者真传，珍贵无比！', '2025-12-01 06:15:55', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '【商品转发】
商品名称：名声蛊
商品价格：¥5000.0
商品链接：http://127.0.0.1:5000/item/11

《人祖传》中的传奇蛊虫，太日阳莽曾经使用此蛊，但是收获的全是坏名声，不知你若使用。。。？', '2025-12-01 06:30:18', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '地灵何在？', '2025-12-01 06:33:53', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '帮我盯着这个名声蛊，降价了提醒我', '2025-12-01 06:34:13', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '好的！！！收到！主人！', '2025-12-01 06:35:41', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 1, '【商品转发】
商品名称：洁身自好
商品价格：¥3500.0
商品链接：http://127.0.0.1:5000/item/3

对自身的道痕进行筛选和清理冲刷，精准分离并剥离对蛊仙不利的坏道痕，清除一切负面效果！', '2025-12-01 08:40:57', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 1, '老头，这个杀招有配套的蛊虫吗？', '2025-12-01 08:41:23', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '【商品转发】
商品名称：名声蛊
商品价格：¥5000.0
商品链接：http://127.0.0.1:5000/item/11
卖家：多宝真人
库存：1
浏览：20
关注：3

《人祖传》中的传奇蛊虫，太日阳莽曾经使用此蛊，但是收获的全是坏名声，不知你若使用。。。？', '2025-12-01 08:50:56', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '主人，这个名声蛊一直都这么贵啊！', '2025-12-01 08:51:42', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '没事，你继续盯着，贵我们就不买了', '2025-12-01 08:54:36', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '【商品转发】
商品名称：红莲真传
商品价格：¥8888.0
商品链接：http://127.0.0.1:5000/item/18
卖家：何春秋
库存：1
浏览：4
关注：0

尊者真传，珍贵无比！', '2025-12-01 14:19:37', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '关注一下，给我当托', '2025-12-01 14:19:58', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '> : 没事，你继续盯着，贵我们就不买了

好的主人！', '2025-12-01 14:20:40', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '> : 关注一下，给我当托

已关注，主人！', '2025-12-01 14:21:02', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (1, 2, '有，但是我只卖杀招，你想要配套的蛊虫，那就得加价另买！用其他蛊虫虽然也可以模拟出来，但是效果嘛。。。当然是不如原版的杀招了！', '2025-12-01 17:11:15', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 1, '死老头，那这杀招你还买这么贵？！', '2025-12-01 17:12:59', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (1, 2, '哼，不要就快走！我这杀招稀罕的很，效果也不是一般的！五域两天还有谁有这样的杀招？', '2025-12-01 17:14:19', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '【商品转发】
商品名称：失败蛊
商品价格：¥1.0
商品链接：http://127.0.0.1:5000/item/20
卖家：白狐仙子
库存：1
浏览：1
关注：0

失败乃是成功之母。。。。。。', '2025-12-02 06:18:59', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (4, 2, '主人,失败蛊太多了，我拿出来卖掉一些！', '2025-12-02 06:19:33', 1);
INSERT INTO [Message] (sender_id, receiver_id, content, date_sent, is_read) VALUES (2, 4, '嗯', '2025-12-02 06:20:09', 1);
GO
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (3, 2, 'follow_item', '何春秋 关注了您的商品 "摸头蛊"', 1, '2025-12-01 06:06:32', 15);
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (2, 3, 'follow_item', '多宝真人 关注了您的商品 "红莲真传"', 1, '2025-12-01 06:15:39', 17);
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (3, 4, 'follow_item', '白狐仙子 关注了您的商品 "名声蛊"', 1, '2025-12-01 06:35:12', 11);
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (3, 2, 'follow_item', '何春秋 关注了您的商品 "名声蛊"', 1, '2025-12-01 08:21:03', 11);
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (2, 4, 'follow_item', '白狐仙子 关注了您的商品 "红莲真传"', 1, '2025-12-01 14:20:45', 18);
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (4, 2, 'follow_user', '何春秋 关注了您', 1, '2025-12-01 17:12:07', 2);
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (1, 2, 'follow_user', '何春秋 关注了您', 1, '2025-12-01 17:19:21', 2);
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (1, 4, 'follow_user', '白狐仙子 关注了您', 1, '2025-12-02 07:48:31', 4);
INSERT INTO [Notification] (user_id, sender_id, notification_type, content, is_read, date_created, related_id) VALUES (2, 4, 'follow_user', '白狐仙子 关注了您', 1, '2025-12-02 07:59:07', 4);
GO
