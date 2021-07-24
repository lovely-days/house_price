def validate(name="", password=""):
    if len(name) == 0:
        return "用户名不能为空值！！"
    if len(password) == 0:
        return "密码不能为空值！！"
    if len(password) < 6 or len(password) > 12:
        return "密码位数应该位于 6~12 位之间！！ "
    else:
        return "success validate"
