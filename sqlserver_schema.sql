-- SQL Server 数据库架构创建脚本
-- 创建数据库（如果不存在）
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'CampusMarket')
BEGIN
    CREATE DATABASE CampusMarket;
END
GO

USE CampusMarket;
GO

-- 创建用户表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[user]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[user] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [username] VARCHAR(20) NOT NULL UNIQUE,
        [email] VARCHAR(120) NOT NULL UNIQUE,
        [password] VARCHAR(255) NOT NULL,
        [contact] VARCHAR(60) NOT NULL,
        [avatar] VARCHAR(20) NOT NULL DEFAULT 'default_avatar.png',
        [is_admin] BIT NOT NULL DEFAULT 0
    );
    -- 创建索引
    CREATE INDEX [IX_user_username] ON [dbo].[user] ([username]);
    CREATE INDEX [IX_user_email] ON [dbo].[user] ([email]);
END
GO

-- 创建商品表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[item]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[item] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [title] VARCHAR(100) NOT NULL,
        [price] FLOAT NOT NULL,
        [description] TEXT NOT NULL,
        [image_file] VARCHAR(20) NOT NULL DEFAULT 'default.jpg',
        [date_posted] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [user_id] INT NOT NULL,
        [views] INT NOT NULL DEFAULT 0,
        [stock] INT NOT NULL DEFAULT 1,
        CONSTRAINT [FK_item_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
    );
    -- 创建索引
    CREATE INDEX [IX_item_title] ON [dbo].[item] ([title]);
    CREATE INDEX [IX_item_date_posted] ON [dbo].[item] ([date_posted]);
    CREATE INDEX [IX_item_user_id] ON [dbo].[item] ([user_id]);
    CREATE INDEX [IX_item_views] ON [dbo].[item] ([views]);
END
GO

-- 创建求购表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[request]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[request] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [title] VARCHAR(100) NOT NULL,
        [description] TEXT NOT NULL,
        [price] FLOAT NOT NULL,
        [image_file] VARCHAR(20) NOT NULL DEFAULT 'default.jpg',
        [date_posted] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [user_id] INT NOT NULL,
        CONSTRAINT [FK_request_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
    );
    -- 创建索引
    CREATE INDEX [IX_request_title] ON [dbo].[request] ([title]);
    CREATE INDEX [IX_request_date_posted] ON [dbo].[request] ([date_posted]);
    CREATE INDEX [IX_request_user_id] ON [dbo].[request] ([user_id]);
END
GO

-- 创建帖子表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[post]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[post] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [content] TEXT NOT NULL,
        [image_file] VARCHAR(20) NULL,
        [date_posted] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [user_id] INT NOT NULL,
        CONSTRAINT [FK_post_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
    );
    -- 创建索引
    CREATE INDEX [IX_post_date_posted] ON [dbo].[post] ([date_posted]);
    CREATE INDEX [IX_post_user_id] ON [dbo].[post] ([user_id]);
END
GO

-- 创建回复表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[reply]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[reply] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [content] TEXT NOT NULL,
        [date_posted] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [user_id] INT NOT NULL,
        [post_id] INT NOT NULL,
        [quoted_post_id] INT NULL,
        [quoted_reply_id] INT NULL,
        CONSTRAINT [FK_reply_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE,
        CONSTRAINT [FK_reply_post_id] FOREIGN KEY ([post_id]) REFERENCES [dbo].[post] ([id]) ON DELETE NO ACTION,
        CONSTRAINT [FK_reply_quoted_post_id] FOREIGN KEY ([quoted_post_id]) REFERENCES [dbo].[post] ([id]) ON DELETE NO ACTION,
        CONSTRAINT [FK_reply_quoted_reply_id] FOREIGN KEY ([quoted_reply_id]) REFERENCES [dbo].[reply] ([id]) ON DELETE NO ACTION
    );
    -- 创建索引
    CREATE INDEX [IX_reply_user_id] ON [dbo].[reply] ([user_id]);
    CREATE INDEX [IX_reply_post_id] ON [dbo].[reply] ([post_id]);
END
GO

-- 创建关注商品表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[follow]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[follow] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [user_id] INT NOT NULL,
        [item_id] INT NOT NULL,
        [date_followed] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        CONSTRAINT [FK_follow_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE,
        CONSTRAINT [FK_follow_item_id] FOREIGN KEY ([item_id]) REFERENCES [dbo].[item] ([id]) ON DELETE NO ACTION
    );
    -- 创建索引
    CREATE INDEX [IX_follow_user_id] ON [dbo].[follow] ([user_id]);
    CREATE INDEX [IX_follow_item_id] ON [dbo].[follow] ([item_id]);
    CREATE INDEX [IX_follow_date_followed] ON [dbo].[follow] ([date_followed]);
END
GO

-- 创建点赞表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[like]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[like] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [date_liked] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [user_id] INT NOT NULL,
        [post_id] INT NOT NULL,
        CONSTRAINT [FK_like_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE,
        CONSTRAINT [FK_like_post_id] FOREIGN KEY ([post_id]) REFERENCES [dbo].[post] ([id]) ON DELETE NO ACTION
    );
    -- 创建索引
    CREATE INDEX [IX_like_user_id] ON [dbo].[like] ([user_id]);
    CREATE INDEX [IX_like_post_id] ON [dbo].[like] ([post_id]);
END
GO

-- 创建回复点赞表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[reply_like]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[reply_like] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [date_liked] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [user_id] INT NOT NULL,
        [reply_id] INT NOT NULL,
        CONSTRAINT [FK_reply_like_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE,
        CONSTRAINT [FK_reply_like_reply_id] FOREIGN KEY ([reply_id]) REFERENCES [dbo].[reply] ([id]) ON DELETE NO ACTION
    );
    -- 创建索引
    CREATE INDEX [IX_reply_like_user_id] ON [dbo].[reply_like] ([user_id]);
    CREATE INDEX [IX_reply_like_reply_id] ON [dbo].[reply_like] ([reply_id]);
END
GO

-- 创建用户关注表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[user_follow]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[user_follow] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [follower_id] INT NOT NULL,
        [followed_id] INT NOT NULL,
        [date_followed] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        CONSTRAINT [FK_user_follow_follower_id] FOREIGN KEY ([follower_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE,
        CONSTRAINT [FK_user_follow_followed_id] FOREIGN KEY ([followed_id]) REFERENCES [dbo].[user] ([id]) ON DELETE NO ACTION
    );
    -- 创建索引
    CREATE INDEX [IX_user_follow_follower_id] ON [dbo].[user_follow] ([follower_id]);
    CREATE INDEX [IX_user_follow_followed_id] ON [dbo].[user_follow] ([followed_id]);
END
GO

-- 创建私信表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[message]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[message] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [sender_id] INT NOT NULL,
        [receiver_id] INT NOT NULL,
        [content] TEXT NOT NULL,
        [date_sent] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [is_read] BIT NOT NULL DEFAULT 0,
        CONSTRAINT [FK_message_sender_id] FOREIGN KEY ([sender_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE,
        CONSTRAINT [FK_message_receiver_id] FOREIGN KEY ([receiver_id]) REFERENCES [dbo].[user] ([id]) ON DELETE NO ACTION
    );
    -- 创建索引
    CREATE INDEX [IX_message_sender_id] ON [dbo].[message] ([sender_id]);
    CREATE INDEX [IX_message_receiver_id] ON [dbo].[message] ([receiver_id]);
    CREATE INDEX [IX_message_date_sent] ON [dbo].[message] ([date_sent]);
    CREATE INDEX [IX_message_is_read] ON [dbo].[message] ([is_read]);
END
GO

-- 创建通知表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[notification]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[notification] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [user_id] INT NOT NULL,
        [sender_id] INT NOT NULL,
        [notification_type] VARCHAR(50) NOT NULL,
        [content] TEXT NOT NULL,
        [is_read] BIT NOT NULL DEFAULT 0,
        [date_created] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [related_id] INT NULL,
        CONSTRAINT [FK_notification_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE,
        CONSTRAINT [FK_notification_sender_id] FOREIGN KEY ([sender_id]) REFERENCES [dbo].[user] ([id]) ON DELETE NO ACTION
    );
    -- 创建索引
    CREATE INDEX [IX_notification_user_id] ON [dbo].[notification] ([user_id]);
    CREATE INDEX [IX_notification_sender_id] ON [dbo].[notification] ([sender_id]);
    CREATE INDEX [IX_notification_notification_type] ON [dbo].[notification] ([notification_type]);
    CREATE INDEX [IX_notification_is_read] ON [dbo].[notification] ([is_read]);
    CREATE INDEX [IX_notification_date_created] ON [dbo].[notification] ([date_created]);
END
GO

-- 创建库存表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[stock]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[stock] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [name] VARCHAR(100) NOT NULL,
        [quantity] INT NOT NULL DEFAULT 1,
        [description] TEXT NULL,
        [image_file] VARCHAR(20) NOT NULL DEFAULT 'default.jpg',
        [date_added] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [user_id] INT NOT NULL,
        CONSTRAINT [FK_stock_user_id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
    );
    -- 创建索引
    CREATE INDEX [IX_stock_name] ON [dbo].[stock] ([name]);
    CREATE INDEX [IX_stock_date_added] ON [dbo].[stock] ([date_added]);
    CREATE INDEX [IX_stock_user_id] ON [dbo].[stock] ([user_id]);
END
GO

-- 显示创建的表
SELECT name FROM sys.tables;
GO