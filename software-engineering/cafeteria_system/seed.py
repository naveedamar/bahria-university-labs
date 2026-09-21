import sys
from app import app
from models import db, User, MenuItem


def seed_database():
    with app.app_context():
        print("Resetting database schema...")
        db.drop_all()
        db.create_all()

        print("Seeding default users...")
        # 1. Manager account
        manager = User(
            username="manager1",
            email="manager@cafeteria.edu",
            role="manager"
        )
        manager.set_password("password123")

        # 2. Staff account
        staff = User(
            username="staff1",
            email="staff@cafeteria.edu",
            role="staff"
        )
        staff.set_password("password123")

        # 3. Student account
        student = User(
            username="student1",
            email="student@cafeteria.edu",
            student_id="STU-001",
            role="student"
        )
        student.set_password("password123")

        db.session.add_all([manager, staff, student])

        print("Seeding cafeteria menu items (16 items across 5 categories)...")
        menu_items = [
            # MEALS
            MenuItem(
                name="Chicken Biryani",
                description="Fragrant basmati rice slow-cooked with spiced chicken chunks, potatoes, and signature herbs. Served with cooling raita.",
                category="Meals",
                price=280.00,
                image_url="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Chicken Karahi",
                description="Wok-cooked tender chicken simmered with freshly crushed tomatoes, ginger slivers, green chilies, and desi spices. Served with 2 hot rotis.",
                category="Meals",
                price=380.00,
                image_url="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Daal Chawal",
                description="Comforting yellow lentil tadka cooked with cumin, garlic, and red chilies, served alongside fragrant basmati steamed rice and onion salad.",
                category="Meals",
                price=180.00,
                image_url="https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600&auto=format&fit=crop&q=80",
                available=True
            ),

            # FAST FOOD
            MenuItem(
                name="Club Sandwich",
                description="Triple-decker toasted sandwich layered with grilled chicken, omelette, cheese slice, fresh lettuce, and seasoned mayo. Served with potato crisps.",
                category="Fast Food",
                price=220.00,
                image_url="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Beef Burger",
                description="Juicy seasoned beef patty grilled with melted cheese, caramelized onions, crisp lettuce, and special house burger sauce in a sesame seed bun.",
                category="Fast Food",
                price=260.00,
                image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Chicken Shawarma",
                description="Thinly sliced spiced rotisserie chicken wrapped in warm pita bread with shredded cabbage, crunchy pickles, and creamy tahini garlic sauce.",
                category="Fast Food",
                price=160.00,
                image_url="https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Chicken Paratha Roll",
                description="Crispy golden layered paratha stuffed with spicy grilled chicken boti, sliced onions, and garlic herb mayo dressing.",
                category="Fast Food",
                price=180.00,
                image_url="https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Chicken Sandwich",
                description="Fresh white sandwich bread filled with shredded tender chicken, creamy mayo, cracked black pepper, and crisp cucumber slices.",
                category="Fast Food",
                price=150.00,
                image_url="https://images.unsplash.com/photo-1553909489-cd47e0907980?w=600&auto=format&fit=crop&q=80",
                available=True
            ),

            # SIDES
            MenuItem(
                name="French Fries",
                description="Golden crispy hand-cut potato fries lightly salted and seasoned with zesty chaat masala, served with chili garlic dip.",
                category="Sides",
                price=120.00,
                image_url="https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Vegetable Pakora",
                description="Golden deep-fried fritters made with sliced potatoes, onions, and spinach tossed in seasoned gram flour batter, served with spicy tamarind chutney.",
                category="Sides",
                price=100.00,
                image_url="https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Crispy Samosa Plate",
                description="Pair of fresh, crunchy pastry pockets filled with zesty potatoes and peas, garnished with chaat masala and mint chutney.",
                category="Sides",
                price=90.00,
                image_url="https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&auto=format&fit=crop&q=80",
                available=True
            ),

            # BEVERAGES
            MenuItem(
                name="Cold Coffee",
                description="Rich espresso blended smooth with chilled whole milk, sweet vanilla cream, and dark chocolate drizzle.",
                category="Beverages",
                price=180.00,
                image_url="https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Special Karak Chai",
                description="Authentic strong slow-simmered spiced black tea brewed with whole milk, crushed green cardamom pods, and caramelized sugar.",
                category="Beverages",
                price=60.00,
                image_url="https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Fresh Lime 7Up",
                description="Chilled lemon-lime soda infused with freshly pressed key lime juice, aromatic mint leaves, and a pinch of rock salt.",
                category="Beverages",
                price=110.00,
                image_url="https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&auto=format&fit=crop&q=80",
                available=True
            ),
            MenuItem(
                name="Mineral Water",
                description="500ml purified bottled drinking water, sealed and served ice-cold.",
                category="Beverages",
                price=50.00,
                image_url="https://images.unsplash.com/photo-1523362628745-0c100150b504?w=600&auto=format&fit=crop&q=80",
                available=True
            ),

            # DESSERTS
            MenuItem(
                name="Fruit Chaat",
                description="Refreshing bowl of seasonal fresh fruits (apples, bananas, melons, pomegranate) tossed with tangy citrus dressing and spicy sweet chaat masala.",
                category="Desserts",
                price=140.00,
                image_url="https://images.unsplash.com/photo-1568158879083-c42860933ed7?w=600&auto=format&fit=crop&q=80",
                available=True
            )
        ]

        db.session.add_all(menu_items)
        db.session.commit()

        print(f"Database seeded successfully with default accounts and {len(menu_items)} cafeteria items!")
        print("  - Manager: manager1 / password123")
        print("  - Staff:   staff1   / password123")
        print("  - Student: student1 / password123")


if __name__ == "__main__":
    seed_database()
