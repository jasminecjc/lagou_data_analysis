import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config
import pandas as pd
import numpy as np

databaseurl =  'mysql://%s:%s@%s:%s/%s' % (config.USER, config.PASSWORD, config.HOST, config.PORT, config.DATABASE)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl

db = SQLAlchemy(app)

class lagou_lan(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    lan = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    aver_salary = db.Column(db.Integer, nullable=False)
    years = db.Column(db.String(20), nullable=False)
    finance_stage = db.Column(db.String(20), nullable=False)
    education = db.Column(db.String(20), nullable=False)
    fields = db.Column(db.String(20), nullable=False)

    def __init__(self, id, lan, city):
        self.id = id
        self.lan = lan
        self.city = city
        self.aver_salary = aver_salary
        self.years = years
        self.finance_stage = finance_stage
        self.education = education
        self.fields = fields

    def __repr__(self):
        return '<Id %r User %r>' % (self.id, self.name)

@app.route('/lan/get-by-city', methods=['GET'])
def get_by_city():
    #得到表中所有的数据
    ids = mytable.query.all()
    #使用filter找到指定项目
    get = mytable.query.filter_by(id = get_id).first()
    #获取表成员属性
    ret = 'id=%d,name=%s,age=%d' % (get.id, get.name, get.age)
    return ret
    
app.run(debug = True)