USE CampusMarket;
GO
-- 验证各表记录数
SELECT 'User' AS TableName, COUNT(*) AS RecordCount FROM [User];
SELECT 'Item' AS TableName, COUNT(*) AS RecordCount FROM [Item];
SELECT 'Follow' AS TableName, COUNT(*) AS RecordCount FROM [Follow];
SELECT 'Request' AS TableName, COUNT(*) AS RecordCount FROM [Request];
SELECT 'Post' AS TableName, COUNT(*) AS RecordCount FROM [Post];
SELECT 'Like' AS TableName, COUNT(*) AS RecordCount FROM [Like];
SELECT 'ReplyLike' AS TableName, COUNT(*) AS RecordCount FROM [ReplyLike];
SELECT 'UserFollow' AS TableName, COUNT(*) AS RecordCount FROM [UserFollow];
SELECT 'Reply' AS TableName, COUNT(*) AS RecordCount FROM [Reply];
SELECT 'Message' AS TableName, COUNT(*) AS RecordCount FROM [Message];
SELECT 'Notification' AS TableName, COUNT(*) AS RecordCount FROM [Notification];
SELECT 'Stock' AS TableName, COUNT(*) AS RecordCount FROM [Stock];
