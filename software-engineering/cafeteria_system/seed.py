from app import app
from models import db, User, MenuItem

with app.app_context():
    db.drop_all()
    db.create_all()

    student = User(username='student1', email='student@test.com', student_id='BU-2026-001', role='student')
    student.set_password('password123')

    staff = User(username='staff1', email='staff@test.com', role='staff')
    staff.set_password('password123')

    manager = User(username='manager1', email='manager@test.com', role='manager')
    manager.set_password('password123')

    db.session.add_all([student, staff, manager])

    items = [
        MenuItem(name='Chicken Biryani', category='Meals', price=250.0, is_available=True, description='Fragrant basmati rice served with raita and salad'),
        MenuItem(name='Club Sandwich', category='Snacks', price=180.0, is_available=True, description='Toasted double-decker sandwich with chicken, egg, and fries'),
        MenuItem(name='Chicken Roll', category='Snacks', price=120.0, is_available=True, description='Crispy paratha wrap filled with spicy boti chunks'),
        MenuItem(name='Samosa Plate', category='Snacks', price=60.0, is_available=True, description='Two crispy spiced potato samosas with green chutney'),
        MenuItem(name='Fresh Lime 7Up', category='Beverages', price=90.0, is_available=True, description='Chilled soda served with mint and fresh lemon squeeze'),
        MenuItem(name='Karak Chai', category='Beverages', price=50.0, is_available=True, description='Freshly brewed traditional Pakistani milk tea')
    ]

    db.session.add_all(items)
    db.session.commit()
    print("Database seeded successfully!")