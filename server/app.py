#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries: returns an array of JSON objects for all bakeries in the database.
@app.route('/bakeries')
def bakeries():

    all_bakeries = []
    bakeries = Bakery.query.all()
    for each in bakeries:
        bakery = each.to_dict()
        all_bakeries.append(bakery)

    response = make_response(
        jsonify(all_bakeries),
        200
    )
    # response.headers['Content-Type'] = 'application/json'
    return response 

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery = Bakery.query.filter_by(id=id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    # response.headers['Content-Type'] = 'application/json'
    return response

# GET /baked_goods/by_price: returns an array of baked goods as JSON, sorted by price in descending order. (HINT: how can you use SQLAlchemy to sort the baked goods in a particular order?)
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    all_baked_goods = []
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    for each in baked_goods:
        each_dict = each.to_dict()
        all_baked_goods.append(each_dict)
    response = make_response(
        jsonify(all_baked_goods),
        200
    )
    # response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).all()
    for each in most_expensive:
        most_expensive_dict = each.to_dict()
    response = make_response(
        jsonify(most_expensive_dict),
        200
    )
    # response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=555, debug=True)
