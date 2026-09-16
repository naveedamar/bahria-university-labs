import uuid
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from models import db, User, MenuItem, Order, OrderItem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uni-cafeteria-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafeteria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user_role = str(session.get('user_role', '')).strip().lower()
            allowed = [str(r).strip().lower() for r in allowed_roles]
            if user_role not in allowed:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@app.route('/')
def index():
    if 'user_id' in session:
        role = str(session.get('user_role', '')).strip().lower()
        if role == 'manager':
            return redirect(url_for('manager_dashboard'))
        elif role == 'staff':
            return redirect(url_for('staff_dashboard'))
        return redirect(url_for('student_menu'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role.lower()
            session['cart'] = {}
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        student_id = request.form.get('student_id', '').strip()
        password = request.form.get('password', '').strip()

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, student_id=student_id, role='student')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/student/menu')
@role_required('student')
def student_menu():
    items = MenuItem.query.all()
    return render_template('student_menu.html', items=items)


@app.route('/student/cart')
@role_required('student')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0.0
    for item_id_str, qty in cart.items():
        item = MenuItem.query.get(int(item_id_str))
        if item:
            subtotal = item.price * qty
            total += subtotal
            cart_items.append({'item': item, 'quantity': qty, 'subtotal': subtotal})
    return render_template('student_cart.html', cart_items=cart_items, total=total)


@app.route('/student/cart/add', methods=['GET', 'POST'])
@app.route('/student/cart/add/', methods=['GET', 'POST'])
@app.route('/student/cart/add/', methods=['GET', 'POST'])
@role_required('student')
def add_to_cart(item_id=None):
    if item_id is None:
        raw_id = request.form.get('item_id') or request.args.get('item_id')
        if not raw_id:
            flash('Invalid item selected.', 'warning')
            return redirect(url_for('student_menu'))
        item_id = int(raw_id)

    item = MenuItem.query.get_or_404(item_id)
    if not item.is_available:
        flash('This item is currently unavailable.', 'warning')
        return redirect(url_for('student_menu'))

    cart = session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session['cart'] = cart
    flash(f'{item.name} added to cart.', 'success')
    return redirect(url_for('student_menu'))


@app.route('/student/cart/update/', methods=['POST'])
@role_required('student')
def update_cart(item_id):
    action = request.form.get('action')
    cart = session.get('cart', {})
    key = str(item_id)

    if key in cart:
        if action == 'increment':
            cart[key] += 1
        elif action == 'decrement':
            cart[key] -= 1
            if cart[key] <= 0:
                cart.pop(key)
        elif action == 'remove':
            cart.pop(key)
    session['cart'] = cart
    return redirect(url_for('view_cart'))


@app.route('/student/checkout', methods=['POST'])
@role_required('student')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('student_menu'))

    pickup_time = request.form.get('pickup_time')
    if not pickup_time:
        flash('Please select a pickup time.', 'warning')
        return redirect(url_for('view_cart'))

    order_num = f"ORD-{uuid.uuid4().hex[:6].upper()}"
    new_order = Order(
        order_number=order_num,
        user_id=session['user_id'],
        pickup_time=pickup_time,
        status='Pending',
        total=0.0
    )
    db.session.add(new_order)
    db.session.flush()

    total = 0.0
    for item_id_str, qty in cart.items():
        item = MenuItem.query.get(int(item_id_str))
        if item and item.is_available:
            subtotal = item.price * qty
            total += subtotal
            order_item = OrderItem(order_id=new_order.id, menu_item_id=item.id, quantity=qty, price=item.price)
            db.session.add(order_item)

    new_order.total = total
    db.session.commit()
    session['cart'] = {}
    flash(f'Order placed successfully! Reference: {order_num}', 'success')
    return redirect(url_for('student_orders'))


@app.route('/student/orders')
@role_required('student')
def student_orders():
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('student_orders.html', orders=orders)


@app.route('/staff/dashboard')
@role_required('staff', 'manager')
def staff_dashboard():
    orders = Order.query.filter(Order.status != 'Completed').order_by(Order.created_at.asc()).all()
    menu_items = MenuItem.query.all()
    return render_template('staff_dashboard.html', orders=orders, menu_items=menu_items)


@app.route('/staff/order//status', methods=['POST'])
@role_required('staff', 'manager')
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Preparing', 'Ready', 'Completed']:
        order.status = new_status
        db.session.commit()
        flash(f'Order {order.order_number} status updated to {new_status}.', 'success')
    return redirect(url_for('staff_dashboard'))


@app.route('/staff/item//toggle', methods=['POST'])
@role_required('staff', 'manager')
def toggle_item_availability(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.is_available = not item.is_available
    db.session.commit()
    flash(f"{item.name} is now {'Available' if item.is_available else 'Unavailable'}.", 'info')
    return redirect(url_for('staff_dashboard'))


@app.route('/manager/dashboard')
@role_required('manager')
def manager_dashboard():
    items = MenuItem.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('manager_dashboard.html', items=items, orders=orders)


@app.route('/manager/item/add', methods=['POST'])
@role_required('manager')
def add_menu_item():
    name = request.form.get('name')
    description = request.form.get('description')
    category = request.form.get('category')
    price = float(request.form.get('price', 0))
    is_avail = True if request.form.get('available') else False

    new_item = MenuItem(name=name, description=description, category=category, price=price, is_available=is_avail)
    db.session.add(new_item)
    db.session.commit()
    flash('New menu item added!', 'success')
    return redirect(url_for('manager_dashboard'))


@app.route('/manager/item//delete', methods=['POST'])
@role_required('manager')
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    has_orders = OrderItem.query.filter_by(menu_item_id=item.id).first()
    if has_orders:
        item.is_available = False
        db.session.commit()
        flash(f"{item.name} is associated with past orders and cannot be deleted; marked as unavailable instead.",
              "warning")
    else:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully.', 'success')
    return redirect(url_for('manager_dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)