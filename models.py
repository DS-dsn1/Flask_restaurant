from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database

DB_USER = 'postgres'
DB_PASSWORD = ''
DB_NAME = 'restaurant-samusenko'
DB_ECHO = True

restaurant = Flask(__name__)
restaurant.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
restaurant.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'
db = SQLAlchemy(restaurant)


dishes = db.Table('dishes',
    db.Column('ChefId', db.Integer, db.ForeignKey('chef.ChefId'), primary_key=True),
    db.Column('DishId', db.Integer, db.ForeignKey('dish.DishId'), primary_key=True)
)


class Chef(db.Model):
    id = db.Column('ChefId', db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(30))
    experience = db.Column(db.String(100))
    salary = db.Column(db.Float(30))
    dishes = db.relationship('Dish', secondary=dishes, lazy='subquery',
                             backref=db.backref('dishes', lazy=True))

    def __init__(self, first_name, last_name, phone, experience, salary):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.experience = experience
        self.salary = salary

    def __repr__(self):
        return f'Chef {self.id}'


class Dish(db.Model):
    id = db.Column('DishId', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    recipe = db.Column(db.Text)
    ingredients = db.Column(db.String(250))
    cost = db.Column(db.Float(30))

    def __init__(self, name, recipe, ingredients, cost):
        self.name = name
        self.recipe = recipe
        self.ingredients = ingredients
        self.cost = cost

    def __repr__(self):
        return f'{self.name}'


orders_dish = db.Table('orders_dish',
    db.Column('OrderId', db.Integer, db.ForeignKey('orders.OrderId'), primary_key=True),
    db.Column('DishId', db.Integer, db.ForeignKey('dish.DishId'), primary_key=True)
)


class Orders(db.Model):
    id = db.Column('OrderId', db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.CustomerId'),
                            nullable=False)
    payments = db.relationship('Payment', backref='orders', lazy=True)
    orders_dish = db.relationship('Dish', secondary=orders_dish, lazy='subquery',
                             backref=db.backref('orders_dish', lazy=True))

    def __init__(self, order_date, customer_id):
        self.order_date = order_date
        self.customer_id = customer_id


class Customer(db.Model):
    id = db.Column('CustomerId', db.Integer, primary_key=True)
    all_orders = db.relationship('Orders', backref='customer', lazy=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(30))

    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class Payment(db.Model):
    id = db.Column('PaymentId', db.Integer, primary_key=True)
    payment_method = db.Column(db.String(30))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.OrderId'),
                            nullable=False)

    def __init__(self, payment_method):
        self.payment_method = payment_method

    def __repr__(self):
        return f'Payment with {self.payment_method}'


# create_database(db.engine.url)
# db.init_app(restaurant)
# db.create_all()
