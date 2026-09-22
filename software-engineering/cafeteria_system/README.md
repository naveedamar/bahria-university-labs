# Bahria Bites — University Cafeteria Pre-Order System

**Live Deployment:** [https://bahria-bites.onrender.com/login](https://bahria-bites.onrender.com/login)

A web-based cafeteria pre-ordering application built for university campuses to streamline food ordering, reduce counter queues, and manage kitchen operations in real-time.

---

## Demo Accounts

All test accounts use the password: `password123`

| Role | Username | Permissions / Access |
|---|---|---|
| **Student** | `student1` | Browse menu, filter categories, add to cart, checkout with pickup time slot & payment choice, track live order status |
| **Kitchen Staff** | `staff1` | View real-time active kitchen queue, advance order stages (Pending -> Preparing -> Ready -> Completed), toggle menu item availability |
| **Cafeteria Manager** | `manager1` | View revenue and sales analytics, manage menu catalog (add/edit/delete dishes), view comprehensive order audit logs |

*(New students can also register via the `/register` page).*

---

## Key Features

- **Role-Based Access Control:** Distinct workflows for Students, Kitchen Staff, and Managers.
- **Interactive Menu & Filtering:** 16 food items organized across Meals, Fast Food, Sides, Beverages, and Desserts.
- **Pickup Scheduling:** Selectable campus pickup slots during checkout.
- **Payment Method Selection:** Choice between *Cash (pay at pickup)* and *Digital Wallet (pay via QR at counter)* with a counter QR settlement reminder.
- **Kitchen Queue Management:** Staff dashboard for tracking incoming tickets and advancing preparation status.
- **Manager Control Center:** Metric cards for revenue, order fulfillment counts, and menu catalog management.
- **Dark Theme:** Clean UI built with Bootstrap 5 and customized dark palette.

---

## Tech Stack

- **Backend:** Python 3, Flask
- **Database & ORM:** SQLite, Flask-SQLAlchemy
- **Frontend:** HTML5, Jinja2 Templates, Bootstrap 5, Bootstrap Icons, Custom CSS
- **WSGI / Deployment:** Gunicorn, Render

---

## Local Setup & Running

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd software-engineering/cafeteria_system
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and seed the database:**
   ```bash
   python seed.py
   ```

5. **Start the development server:**
   ```bash
   python app.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
