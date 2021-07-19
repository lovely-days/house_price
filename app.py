# encoding:utf-8
from flask import Flask, url_for, redirect, request
from flask import render_template

import src.static.py.sql as db_helper
import folium

from src.static.py import config

app = Flask(__name__, static_folder="./static", template_folder="./templates")
app.config.from_object(config)


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        # flash(form_login.name.data + '|' + form_login.password.data)
        name = request.form["name"]
        password = request.form["password"]

        print(type(name))
        print(name)
        print(type(password))
        print(password)

        # sql
        sql = "select Password from users where UserName='{0}' ".format(name)
        result = db_helper.select_one(sql)

        print(result[0])
        print(name)
        print(name == result[0])

        if result[0] == password:
            url = url_for('index')
            return redirect(url)
        else:

            url = url_for('login')
            return redirect(url)
    else:
        return render_template('login.html')


@app.route('/enroll', methods=('POST', 'GET'))
def enroll():

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        print(type(name))
        print(name)
        print(type(password))
        print(password)

        # flash(form_enroll.name.data + '|' + form_enroll.password.data)

        # enroll
        sql = "insert into webgis_design.users (UserName,Password,Permission) " \
              "values ('{0}','{1}','{2}')".format(name, password, 0)

        print(sql)
        status = db_helper.update_database(sql)

        if status != 0:
            url = url_for('login')
            return redirect(url)
        else:
            return '注册失败，请重试'
    else:
        return render_template('login.html')


@app.route('/map/init_map')
def init_map():
    maps = folium.Map(location=[35.3, 100.6], zoom_start=4)
    maps.save("./templates/map/init_map.html")
    return render_template("map/init_map.html")


@app.route('/index')
def index():
    return render_template('index.html', init_map=url_for('init_map'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)
