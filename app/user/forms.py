from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email
from wtforms import ValidationError
from ..models import User
from flask_pagedown.fields import PageDownField


class LoginForm(FlaskForm):
    account = StringField('学号/帐号', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("密码", validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    # email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    account = StringField('学号', validators=[DataRequired(), Length(2, 30)])
    username = StringField('真名', validators=[
        DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册.')

    def validate_account(self, field):
        if User.query.filter_by(account=field.data).first():
            raise ValidationError('学号/账户已被使用.')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    body = PageDownField('正文', validators=[DataRequired()])
    group = SelectField('组名', choices=[('Python', 'Python组'), ('Linux', 'Linux组')],
                        validators=[DataRequired()])
    submit = SubmitField('提交')


class HomeworkForm(FlaskForm):
    body = PageDownField('作业', validators=[DataRequired()])
    submit = SubmitField('提交')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='两次密码必须相同')])
    password2 = PasswordField('重复密码', validators=[DataRequired()])
    submit = SubmitField('更新密码')
