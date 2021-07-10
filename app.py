from flask import Flask, flash, url_for, redirect
from flask import render_template

import src.static.py.form as form_template
import src.static.py.sql as db_helper

from src import config

app = Flask(__name__, static_folder="./static", template_folder="./templates")
app.config.from_object(config)


@app.route('/')
def begin():
    sql = "select * from webgis_design.houses"
    results = db_helper.select_all(sql)

    return render_template('data.html', results=results, t=type(results))


@app.route('/login', methods=('POST', 'GET'))
def login():
    form_login = form_template.BaseLogin()

    if form_login.validate_on_submit():
        flash(form_login.name.data + '|' + form_login.password.data)

        # sql
        sql = "select Password from users where UserName='{0}' ".format(form_login.name.data)
        result = db_helper.select_one(sql)

        # print(result[0])
        # print(form_login.name.data)

        if result[0] == form_login.password.data:
            url = url_for('index')
            return redirect(url)
        else:
            return '登陆失败! '
    else:
        return render_template('login.html', form=form_login)


# CSRFProtect(app)
@app.route('/enroll', methods=('POST', 'GET'))
def enroll():
    form_enroll = form_template.BaseEnroll()

    if form_enroll.validate_on_submit():
        flash(form_enroll.name.data + '|' + form_enroll.password.data)

        # enroll
        sql = "insert into webgis_design.users (UserName,Password,Permission) " \
              "values ('{0}','{1}','{2}')".format(form_enroll.name.data, form_enroll.password.data, 0)

        print(sql)
        status = db_helper.update_database(sql)

        if status != 0:
            url = url_for('begin')
            return redirect(url)
        else:
            return '注册失败，请重试'
    else:
        return render_template('enroll.html', form=form_enroll)


@app.route('/index')
def index():
    sql = "select * from webgis_design.houses"
    results = db_helper.select_all(sql)

    return render_template('index.html', results=results, t=type(results))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)
