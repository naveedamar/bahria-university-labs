import os
import secrets
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from models import db, User, MenuItem, Order, OrderItem

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-cafeteria-system-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    f"sqlite:///{os.path.join(BASE_DIR, 'cafeteria.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Role-based access control decorator
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login', next=request.url))
            if session.get('user_role') not in roles:
                flash('You do not have permission to view that resource.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.context_processor
def inject_cart_count():
    cart = session.get('cart', {})
    count = sum(int(qty) for qty in cart.values()) if cart else 0
    return dict(cart_count=count)


@app.route('/')
def index():
    if 'user_role' in session:
        role = session['user_role']
        if role == 'student':
            return redirect(url_for('student_menu'))
        elif role == 'staff':
            return redirect(url_for('staff_dashboard'))
        elif role == 'manager':
            return redirect(url_for('manager_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        login_input = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not login_input or not password:
            flash('Please enter both username/email and password.', 'warning')
            return render_template('login.html')

        user = User.query.filter(
            (User.username == login_input) | (User.email == login_input)
        ).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role
            session['student_id'] = user.student_id

            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Invalid username/email or password.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        student_id = request.form.get('student_id', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        # Validation
        if not username or not email or not student_id or not password:
            flash('All fields are required.', 'warning')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'warning')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username is already taken. Please choose another.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email address is already registered.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(student_id=student_id).first():
            flash('Student ID is already registered.', 'danger')
            return render_template('register.html')

        new_student = User(
            username=username,
            email=email,
            student_id=student_id,
            role='student'
        )
        new_student.set_password(password)

        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Registration successful! Please log in with your credentials.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'danger')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('login'))


# ==========================================
# STUDENT ROUTES
# ==========================================

@app.route('/student/menu')
@role_required('student')
def student_menu():
    category = request.args.get('category', 'All')
    categories = ['All', 'Meals', 'Fast Food', 'Sides', 'Beverages', 'Desserts']

    if category and category != 'All':
        items = MenuItem.query.filter_by(category=category).all()
    else:
        items = MenuItem.query.all()

    return render_template(
        'student_menu.html',
        items=items,
        categories=categories,
        selected_category=category
    )


@app.route('/student/cart')
@role_required('student')
def student_cart():
    cart = session.get('cart', {})
    cart_items = []
    total_amount = 0.0

    if cart:
        item_ids = [int(k) for k in cart.keys() if k.isdigit()]
        items = MenuItem.query.filter(MenuItem.id.in_(item_ids)).all()
        items_by_id = {item.id: item for item in items}

        for item_id_str, qty in cart.items():
            item_id = int(item_id_str)
            if item_id in items_by_id:
                item = items_by_id[item_id]
                subtotal = round(item.price * int(qty), 2)
                total_amount += subtotal
                cart_items.append({
                    'item': item,
                    'quantity': int(qty),
                    'subtotal': subtotal
                })

    total_amount = round(total_amount, 2)
    time_slots = [
        '11:00 AM - 11:30 AM',
        '11:30 AM - 12:00 PM',
        '12:00 PM - 12:30 PM',
        '12:30 PM - 01:00 PM',
        '01:00 PM - 01:30 PM',
        '01:30 PM - 02:00 PM',
        '02:00 PM - 02:30 PM',
        '02:30 PM - 03:00 PM'
    ]

    return render_template(
        'student_cart.html',
        cart_items=cart_items,
        total_amount=total_amount,
        time_slots=time_slots
    )


@app.route('/student/cart/add/<int:item_id>', methods=['POST'])
@role_required('student')
def student_cart_add(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if not item.available:
        flash(f'"{item.name}" is currently sold out and cannot be ordered.', 'danger')
        return redirect(url_for('student_menu'))

    cart = session.get('cart', {})
    key = str(item_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart
    session.modified = True

    flash(f'Added "{item.name}" to your cart.', 'success')
    return redirect(url_for('student_menu'))


@app.route('/student/cart/update/<int:item_id>', methods=['POST'])
@role_required('student')
def student_cart_update(item_id):
    action = request.form.get('action')
    cart = session.get('cart', {})
    key = str(item_id)

    if key in cart:
        if action == 'increase':
            cart[key] += 1
        elif action == 'decrease':
            cart[key] -= 1
            if cart[key] <= 0:
                del cart[key]
        elif action == 'remove':
            del cart[key]
            flash('Item removed from cart.', 'info')

        session['cart'] = cart
        session.modified = True

    return redirect(url_for('student_cart'))


@app.route('/student/checkout', methods=['POST'])
@role_required('student')
def student_checkout():
    pickup_time = request.form.get('pickup_time', '').strip()
    if not pickup_time:
        flash('Please select a valid pickup time slot.', 'warning')
        return redirect(url_for('student_cart'))

    payment_method = request.form.get('payment_method', 'Cash').strip()
    valid_methods = ['Cash', 'Digital Wallet']
    if payment_method not in valid_methods:
        payment_method = 'Cash'

    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty. Please add items before placing an order.', 'warning')
        return redirect(url_for('student_menu'))

    # Strict real-time DB re-validation
    item_ids = [int(k) for k in cart.keys() if k.isdigit()]
    items = MenuItem.query.filter(MenuItem.id.in_(item_ids)).all()
    items_map = {item.id: item for item in items}

    for item_id, qty in list(cart.items()):
        db_item = items_map.get(int(item_id))
        if not db_item:
            flash('One or more items in your cart no longer exist. Cart refreshed.', 'danger')
            del cart[item_id]
            session['cart'] = cart
            session.modified = True
            return redirect(url_for('student_cart'))

        if not db_item.available:
            flash(f'Item "{db_item.name}" is currently sold out. Please remove it from your cart.', 'danger')
            return redirect(url_for('student_cart'))

    # Generate unique order number
    while True:
        order_number = f"ORD-{secrets.token_hex(3).upper()}"
        if not Order.query.filter_by(order_number=order_number).first():
            break

    total_price = 0.0
    new_order = Order(
        order_number=order_number,
        user_id=session['user_id'],
        pickup_time=pickup_time,
        payment_method=payment_method,
        status='Pending',
        total=0.0
    )

    try:
        db.session.add(new_order)
        db.session.flush()  # assign new_order.id

        for item_id_str, qty in cart.items():
            db_item = items_map[int(item_id_str)]
            line_cost = round(db_item.price * int(qty), 2)
            total_price += line_cost

            order_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=db_item.id,
                quantity=int(qty),
                price=db_item.price
            )
            db.session.add(order_item)

        new_order.total = round(total_price, 2)
        db.session.commit()

        # Clear active cart
        session.pop('cart', None)
        if payment_method == 'Digital Wallet':
            flash(f'Order #{order_number} placed! 💳 Please scan the QR code at the cafeteria counter to complete payment via your digital wallet before or at pickup.', 'info')
        else:
            flash(f'Order #{order_number} successfully placed! Please pay Rs. {new_order.total:.2f} in cash at pickup. Pickup scheduled for {pickup_time}.', 'success')
        return redirect(url_for('student_orders'))

    except Exception as e:
        db.session.rollback()
        flash('An unexpected error occurred while placing your order. Please try again.', 'danger')
        return redirect(url_for('student_cart'))


@app.route('/student/orders')
@role_required('student')
def student_orders():
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('student_orders.html', orders=orders)


# ==========================================
# STAFF ROUTES
# ==========================================

@app.route('/staff/dashboard')
@role_required('staff', 'manager')
def staff_dashboard():
    active_orders = Order.query.filter(Order.status.in_(['Pending', 'Preparing', 'Ready'])).order_by(Order.created_at.asc()).all()
    completed_orders = Order.query.filter_by(status='Completed').order_by(Order.created_at.desc()).limit(15).all()
    menu_items = MenuItem.query.order_by(MenuItem.category, MenuItem.name).all()

    return render_template(
        'staff_dashboard.html',
        active_orders=active_orders,
        completed_orders=completed_orders,
        menu_items=menu_items
    )


@app.route('/staff/order/<int:order_id>/advance', methods=['POST'])
@role_required('staff', 'manager')
def staff_advance_order(order_id):
    order = Order.query.get_or_404(order_id)

    # Lifecycle transitions: Pending -> Preparing -> Ready -> Completed
    if order.status == 'Pending':
        order.status = 'Preparing'
        flash(f'Order #{order.order_number} is now marked as PREPARING.', 'info')
    elif order.status == 'Preparing':
        order.status = 'Ready'
        flash(f'Order #{order.order_number} is now marked as READY FOR PICKUP.', 'success')
    elif order.status == 'Ready':
        order.status = 'Completed'
        flash(f'Order #{order.order_number} has been marked as COMPLETED / HANDED OVER.', 'secondary')
    else:
        flash(f'Order #{order.order_number} is already completed.', 'warning')

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Could not update order status due to a database error.', 'danger')

    return redirect(url_for('staff_dashboard'))


@app.route('/staff/menu/<int:item_id>/toggle', methods=['POST'])
@role_required('staff', 'manager')
def staff_toggle_menu(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.available = not item.available
    try:
        db.session.commit()
        state = 'AVAILABLE' if item.available else 'SOLD OUT'
        flash(f'Item "{item.name}" status toggled to {state}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Could not toggle item availability.', 'danger')

    return redirect(url_for('staff_dashboard'))


# ==========================================
# MANAGER ROUTES
# ==========================================

@app.route('/manager/dashboard')
@role_required('manager')
def manager_dashboard():
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    menu_items = MenuItem.query.order_by(MenuItem.category, MenuItem.name).all()

    total_orders = len(all_orders)
    completed_orders = sum(1 for o in all_orders if o.status == 'Completed')
    total_revenue = sum(o.total for o in all_orders if o.status == 'Completed')
    active_menu_count = sum(1 for m in menu_items if m.available)

    return render_template(
        'manager_dashboard.html',
        all_orders=all_orders,
        menu_items=menu_items,
        total_orders=total_orders,
        completed_orders=completed_orders,
        total_revenue=total_revenue,
        active_menu_count=active_menu_count
    )


@app.route('/manager/menu/add', methods=['POST'])
@role_required('manager')
def manager_add_menu_item():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', 'Meals').strip()
    price_raw = request.form.get('price', '0').strip()
    image_url = request.form.get('image_url', '').strip()
    available = bool(request.form.get('available'))

    if not name or not description or not price_raw:
        flash('Name, description, and price are required.', 'warning')
        return redirect(url_for('manager_dashboard'))

    try:
        price = float(price_raw)
        if price < 0:
            raise ValueError()
    except ValueError:
        flash('Price must be a valid non-negative number.', 'danger')
        return redirect(url_for('manager_dashboard'))

    new_item = MenuItem(
        name=name,
        description=description,
        category=category,
        price=round(price, 2),
        image_url=image_url if image_url else None,
        available=available
    )

    try:
        db.session.add(new_item)
        db.session.commit()
        flash(f'New menu item "{name}" added successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add menu item due to a database error.', 'danger')

    return redirect(url_for('manager_dashboard'))


@app.route('/manager/menu/<int:item_id>/edit', methods=['GET', 'POST'])
@role_required('manager')
def manager_edit_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    categories = ['Meals', 'Fast Food', 'Sides', 'Beverages', 'Desserts']

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'Meals').strip()
        price_raw = request.form.get('price', '0').strip()
        image_url = request.form.get('image_url', '').strip()
        available = bool(request.form.get('available'))

        if not name or not description or not price_raw:
            flash('Name, description, and price are required.', 'warning')
            return render_template('edit_menu_item.html', item=item, categories=categories)

        try:
            price = float(price_raw)
            if price < 0:
                raise ValueError()
        except ValueError:
            flash('Price must be a valid non-negative number.', 'danger')
            return render_template('edit_menu_item.html', item=item, categories=categories)

        item.name = name
        item.description = description
        item.category = category
        item.price = round(price, 2)
        item.image_url = image_url if image_url else None
        item.available = available

        try:
            db.session.commit()
            flash(f'Menu item "{item.name}" updated successfully.', 'success')
            return redirect(url_for('manager_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update menu item due to database error.', 'danger')

    return render_template('edit_menu_item.html', item=item, categories=categories)


@app.route('/manager/menu/<int:item_id>/delete', methods=['POST'])
@role_required('manager')
def manager_delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)

    # Prevent deletion if referenced in order history to preserve audit logs
    order_items_count = OrderItem.query.filter_by(menu_item_id=item_id).count()
    if order_items_count > 0:
        flash(f'Cannot delete "{item.name}" because it is referenced in past student orders. Consider marking it as Sold Out instead.', 'danger')
        return redirect(url_for('manager_dashboard'))

    try:
        db.session.delete(item)
        db.session.commit()
        flash(f'Menu item "{item.name}" has been permanently removed.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Could not delete item due to a database error.', 'danger')

    return redirect(url_for('manager_dashboard'))


# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', error_code='404', error_message='Page Not Found'), 404


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('base.html', error_code='403', error_message='Access Forbidden'), 403


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html', error_code='500', error_message='Internal Server Error'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
