# 数据库访问规范

## 1. 文档目的

本文档旨在规范CampusMarket项目中数据库访问的开发实践，确保所有开发人员按照统一的标准进行数据库操作，提高代码质量、可维护性和安全性。

## 2. 数据库选择

- **唯一数据库**：项目统一使用SQL Server作为唯一数据库，禁止使用其他数据库系统（如SQLite、MySQL等）。
- **版本要求**：SQL Server 2017或更高版本。

## 3. 配置管理

### 3.1 数据库连接

- 数据库连接字符串必须通过环境变量`DATABASE_URL`配置。
- 本地开发环境可使用默认连接字符串作为备选。
- 禁止在代码中硬编码数据库连接信息。

### 3.2 配置示例

```python
# config.py
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mssql+pyodbc://localhost/CampusMarket?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
```

## 4. 模型定义规范

### 4.1 模型继承

- 所有数据库模型必须继承自`db.Model`。
- 禁止直接操作数据库表结构。

```python
# 正确示例
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
```

### 4.2 字段定义

- 合理选择字段类型和长度。
- 为常用查询字段添加索引。
- 使用合适的默认值。

```python
# 正确示例
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
```

### 4.3 关系定义

- 使用SQLAlchemy的关系函数定义表之间的关系。
- 合理设置`backref`和`lazy`参数。

```python
# 正确示例
class User(db.Model):
    items = db.relationship('Item', backref='seller', lazy=True)

class Item(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
```

## 5. 数据库操作规范

### 5.1 数据访问层

- 所有数据库操作必须通过SQLAlchemy ORM进行。
- 禁止直接使用`pyodbc`或`pymssql`等原生库进行数据库连接和操作。

### 5.2 增删改查

- 使用ORM提供的方法进行数据操作。
- 优先使用`db.session`进行事务管理。

```python
# 正确示例 - 添加数据
user = User(username='test', email='test@example.com')
db.session.add(user)
db.session.commit()

# 正确示例 - 查询数据
user = User.query.filter_by(username='test').first()

# 正确示例 - 更新数据
user.email = 'new@example.com'
db.session.commit()

# 正确示例 - 删除数据
db.session.delete(user)
db.session.commit()
```

## 6. 查询编写规范

### 6.1 使用查询构建器

- 优先使用SQLAlchemy的查询构建器（Query Builder）编写查询。
- 减少直接编写原生SQL的机会。

```python
# 正确示例 - 使用查询构建器
items = Item.query.filter(Item.price > 100).order_by(Item.date_posted.desc()).all()

# 正确示例 - 使用关系查询
seller_items = User.query.get(1).items
```

### 6.2 原生SQL使用

- 如必须使用原生SQL，确保SQL语句兼容SQL Server语法。
- 使用参数化查询，避免SQL注入。

```python
# 正确示例 - 使用参数化原生SQL
items = db.session.execute(db.text("SELECT * FROM item WHERE price > :price"), {"price": 100}).fetchall()
```

## 7. 事务处理

- 使用`db.session`进行事务管理。
- 对于复杂操作，显式使用事务。

```python
# 正确示例 - 显式事务
try:
    with db.session.begin():
        # 执行多个数据库操作
        db.session.add(item1)
        db.session.add(item2)
        # 自动提交
    return True
except Exception as e:
    # 自动回滚
    return False
```

## 8. 性能优化

### 8.1 查询优化

- 只查询需要的字段。
- 使用`lazy='joined'`或`lazy='subquery'`优化关联查询。
- 合理使用分页。

```python
# 正确示例 - 只查询需要的字段
users = User.query.with_entities(User.id, User.username).all()

# 正确示例 - 分页查询
items = Item.query.paginate(page=1, per_page=10)
```

### 8.2 索引优化

- 为常用查询字段添加索引。
- 避免过度索引。

```python
# 正确示例 - 添加索引
class User(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    views = db.Column(db.Integer, nullable=False, default=0, index=True)
```

## 9. 安全考虑

- 使用参数化查询，避免SQL注入。
- 限制数据库用户权限，遵循最小权限原则。
- 禁止在日志中记录敏感数据。
- 加密存储敏感信息。

## 10. 开发流程

### 10.1 模型变更

- 模型变更必须通过修改Python代码实现，禁止直接修改数据库表结构。
- 确保模型变更与数据库表结构保持同步。

### 10.2 测试

- 所有数据库操作必须编写测试用例。
- 测试环境必须使用独立的数据库实例。

### 10.3 代码审查

- 数据库相关代码必须经过代码审查。
- 审查重点包括：查询效率、安全性、事务处理等。

## 11. 最佳实践

- 遵循DRY（Don't Repeat Yourself）原则，将常用查询封装为方法。
- 使用`db.relationship`定义表之间的关系，减少JOIN查询的编写。
- 定期清理无用数据，优化数据库性能。
- 监控数据库性能，及时发现和解决问题。

## 12. 违反规范的处理

- 对于违反本规范的代码，将要求开发人员进行修改。
- 多次违反规范的开发人员将进行团队内培训。

## 13. 规范更新

本规范将根据项目需求和技术发展进行定期更新，更新后的规范将通过团队会议传达给所有开发人员。

---

**生效日期**：2025-12-14
**版本**：1.0