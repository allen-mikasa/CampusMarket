from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

# 表单定义
class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('校园邮箱', validators=[DataRequired(), Email()])
    contact = StringField('联系方式 (微信/手机)', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class ItemForm(FlaskForm):
    title = StringField('商品标题', validators=[DataRequired()])
    price = FloatField('价格 (元)', validators=[DataRequired()])
    stock = IntegerField('上架数量', validators=[DataRequired()])
    description = TextAreaField('商品描述', validators=[DataRequired()])
    picture = FileField('商品图片', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('发布商品')

class ProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('校园邮箱', validators=[DataRequired(), Email()])
    contact = StringField('联系方式 (微信/手机)', validators=[DataRequired()])
    avatar = FileField('头像上传', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    # 密码修改字段
    current_password = PasswordField('当前密码')
    new_password = PasswordField('新密码')
    confirm_new_password = PasswordField('确认新密码')
    
    submit = SubmitField('保存修改')
    
    def validate_current_password(self, current_password):
        # 只有当new_password有值时，才验证current_password是否提供
        if self.new_password.data and not current_password.data:
            raise ValidationError('修改密码时必须提供当前密码')
    
    def validate_new_password(self, new_password):
        # 只有当current_password或new_password有值时，才验证new_password的长度
        if self.current_password.data or new_password.data:
            if len(new_password.data) < 6:
                raise ValidationError('新密码长度必须至少为6个字符')
    
    def validate_confirm_new_password(self, confirm_new_password):
        # 只有当new_password有值时，才验证confirm_new_password是否与new_password一致
        if self.new_password.data:
            if confirm_new_password.data != self.new_password.data:
                raise ValidationError('两次输入的密码必须一致')

class RequestForm(FlaskForm):
    title = StringField('求购标题', validators=[DataRequired()])
    price = FloatField('期望价格 (元)', validators=[DataRequired()])
    description = TextAreaField('求购描述', validators=[DataRequired()])
    picture = FileField('求购图片', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('发布求购')

# 交流广场表单
class PostForm(FlaskForm):
    content = TextAreaField('留言内容', validators=[DataRequired()])
    picture = FileField('上传图片', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('发布留言')

# 回复表单
class ReplyForm(FlaskForm):
    content = TextAreaField('回复内容', validators=[DataRequired()])
    submit = SubmitField('发送回复')

# 库存表单
class StockForm(FlaskForm):
    name = StringField('物品名称', validators=[DataRequired()])
    quantity = IntegerField('数量', validators=[DataRequired()])
    description = TextAreaField('物品描述')
    picture = FileField('物品图片', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('保存库存')
