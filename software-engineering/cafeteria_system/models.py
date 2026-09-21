import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    student_id = db.Column(db.String(50), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # 'student', 'staff', 'manager'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='Meals', nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)

    def __repr__(self):
        return f'<MenuItem {self.name} - ${self.price}>'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(30), unique=True, nullable=False)  # e.g. ORD-XXXXXX
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pickup_time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Pending, Preparing, Ready, Completed
    payment_method = db.Column(db.String(30), default='Cash', nullable=False)  # Cash, JazzCash, EasyPaisa, Card
    total = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<Order {self.order_number} - {self.status} - {self.payment_method}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Historical snapshot price

    @property
    def subtotal(self):
        return round(self.quantity * self.price, 2)

    def __repr__(self):
        return f'<OrderItem {self.id}: Menu {self.menu_item_id} x {self.quantity}>'
