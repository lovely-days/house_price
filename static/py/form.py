# -*- encoding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    name = StringField('name',
                       validators=[DataRequired(message="用户名不能为空"), Length(6, 16, message='长度位于6~16之间')],
                       render_kw={'Placeholder': '输入用户名'})

    password = PasswordField('password',
                             validators=[DataRequired(message="密码不能为空"), Length(6, 16, message='长度位于6~16位之间')],
                             render_kw={'placeholder': '输入密码'})


class EnrollForm(Form):
    name = StringField('name',
                       validators=[DataRequired(message="用户名不能为空"), Length(6, 16, message='长度位于6~16之间')],
                       render_kw={'Placeholder': '输入用户名'})

    password = PasswordField('password',
                             validators=[DataRequired(message="密码不能为空"), Length(6, 16, message='长度位于6~16位之间')],
                             render_kw={'placeholder': '输入密码'})
