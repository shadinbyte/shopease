import os

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopease.settings")
django.setup()

import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth.models import User

from shop.models import Category, Customer, Order, OrderItem, Product


def clear_data():
    """Clear existing data"""
    print("🗑️  Clearing existing data...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    Customer.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("✅ Data cleared!\n")


def create_categories():
    """Create product categories"""
    print("📁 Creating categories...")
    categories_data = [
        {"name": "Electronics", "description": "Electronic devices and gadgets"},
        {"name": "Fashion", "description": "Clothing and accessories"},
        {"name": "Home & Garden", "description": "Home decor and garden supplies"},
        {"name": "Sports", "description": "Sports equipment and gear"},
        {"name": "Books", "description": "Books and educational materials"},
        {"name": "Toys", "description": "Toys and games for all ages"},
        {"name": "Beauty", "description": "Beauty and personal care products"},
        {"name": "Food & Beverages", "description": "Food items and drinks"},
    ]

    categories = []
    for cat_data in categories_data:
        category = Category.objects.create(**cat_data)
        categories.append(category)
        print(f"  ✓ Created category: {category.name}")

    print(f"✅ Created {len(categories)} categories!\n")
    return categories


def create_products(categories):
    """Create sample products"""
    print("📦 Creating products...")

    products_data = {
        "Electronics": [
            {"name": "Wireless Headphones", "price": 79.99, "stock": 50},
            {"name": "Smart Watch", "price": 199.99, "stock": 30},
            {"name": "Laptop Stand", "price": 49.99, "stock": 100},
            {"name": "USB-C Hub", "price": 39.99, "stock": 75},
            {"name": "Bluetooth Speaker", "price": 59.99, "stock": 60},
        ],
        "Fashion": [
            {"name": "Cotton T-Shirt", "price": 19.99, "stock": 200},
            {"name": "Denim Jeans", "price": 49.99, "stock": 150},
            {"name": "Leather Wallet", "price": 34.99, "stock": 80},
            {"name": "Sunglasses", "price": 89.99, "stock": 40},
            {"name": "Running Shoes", "price": 79.99, "stock": 120},
        ],
        "Home & Garden": [
            {"name": "Table Lamp", "price": 45.99, "stock": 50},
            {"name": "Throw Pillow", "price": 24.99, "stock": 100},
            {"name": "Wall Clock", "price": 39.99, "stock": 60},
            {"name": "Plant Pot Set", "price": 29.99, "stock": 80},
            {"name": "Area Rug", "price": 149.99, "stock": 25},
        ],
        "Sports": [
            {"name": "Yoga Mat", "price": 29.99, "stock": 90},
            {"name": "Dumbbell Set", "price": 99.99, "stock": 40},
            {"name": "Water Bottle", "price": 19.99, "stock": 150},
            {"name": "Resistance Bands", "price": 24.99, "stock": 100},
            {"name": "Jump Rope", "price": 12.99, "stock": 120},
        ],
        "Books": [
            {"name": "Python Programming Guide", "price": 39.99, "stock": 70},
            {"name": "Web Development Handbook", "price": 44.99, "stock": 60},
            {"name": "Business Strategy Book", "price": 34.99, "stock": 50},
            {"name": "Self-Help Collection", "price": 29.99, "stock": 80},
            {"name": "Cookbook Essentials", "price": 24.99, "stock": 100},
        ],
        "Toys": [
            {"name": "Building Blocks Set", "price": 49.99, "stock": 60},
            {"name": "Puzzle Game", "price": 19.99, "stock": 100},
            {"name": "Remote Control Car", "price": 69.99, "stock": 40},
            {"name": "Board Game", "price": 34.99, "stock": 70},
            {"name": "Plush Toy", "price": 24.99, "stock": 120},
        ],
        "Beauty": [
            {"name": "Face Moisturizer", "price": 29.99, "stock": 80},
            {"name": "Shampoo & Conditioner Set", "price": 24.99, "stock": 100},
            {"name": "Makeup Brush Set", "price": 39.99, "stock": 60},
            {"name": "Perfume", "price": 89.99, "stock": 40},
            {"name": "Skincare Kit", "price": 79.99, "stock": 50},
        ],
        "Food & Beverages": [
            {"name": "Organic Coffee Beans", "price": 19.99, "stock": 150},
            {"name": "Green Tea Set", "price": 24.99, "stock": 100},
            {"name": "Protein Powder", "price": 49.99, "stock": 70},
            {"name": "Energy Bars Pack", "price": 14.99, "stock": 200},
            {"name": "Dark Chocolate", "price": 9.99, "stock": 180},
        ],
    }

    products = []
    for category in categories:
        if category.name in products_data:
            for prod_data in products_data[category.name]:
                product = Product.objects.create(
                    category=category,
                    description=f"High-quality {prod_data['name'].lower()} for your needs.",
                    **prod_data,
                )
                products.append(product)
                print(f"  ✓ Created: {product.name} (${product.price})")

    print(f"✅ Created {len(products)} products!\n")
    return products


def create_customers():
    """Create sample customers"""
    print("👥 Creating customers...")

    customers_data = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "555-0101",
            "city": "New York",
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "555-0102",
            "city": "Los Angeles",
        },
        {
            "username": "bob_wilson",
            "email": "bob@example.com",
            "first_name": "Bob",
            "last_name": "Wilson",
            "phone": "555-0103",
            "city": "Chicago",
        },
        {
            "username": "alice_brown",
            "email": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Brown",
            "phone": "555-0104",
            "city": "Houston",
        },
        {
            "username": "charlie_davis",
            "email": "charlie@example.com",
            "first_name": "Charlie",
            "last_name": "Davis",
            "phone": "555-0105",
            "city": "Phoenix",
        },
        {
            "username": "emma_johnson",
            "email": "emma@example.com",
            "first_name": "Emma",
            "last_name": "Johnson",
            "phone": "555-0106",
            "city": "Philadelphia",
        },
        {
            "username": "david_lee",
            "email": "david@example.com",
            "first_name": "David",
            "last_name": "Lee",
            "phone": "555-0107",
            "city": "San Antonio",
        },
        {
            "username": "sophia_martin",
            "email": "sophia@example.com",
            "first_name": "Sophia",
            "last_name": "Martin",
            "phone": "555-0108",
            "city": "San Diego",
        },
        {
            "username": "michael_garcia",
            "email": "michael@example.com",
            "first_name": "Michael",
            "last_name": "Garcia",
            "phone": "555-0109",
            "city": "Dallas",
        },
        {
            "username": "olivia_white",
            "email": "olivia@example.com",
            "first_name": "Olivia",
            "last_name": "White",
            "phone": "555-0110",
            "city": "San Jose",
        },
    ]

    customers = []
    for cust_data in customers_data:
        phone = cust_data.pop("phone")
        city = cust_data.pop("city")

        user = User.objects.create_user(password="password123", **cust_data)

        customer = Customer.objects.create(
            user=user,
            phone=phone,
            city=city,
            address=f"{random.randint(100, 999)} Main Street",
            postal_code=f"{random.randint(10000, 99999)}",
        )
        customers.append(customer)
        print(f"  ✓ Created customer: {customer.full_name}")

    print(f"✅ Created {len(customers)} customers!\n")
    return customers


def create_orders(customers, products):
    """Create sample orders"""
    print("🛍️  Creating orders...")

    statuses = ["pending", "processing", "shipped", "delivered"]
    orders_count = 30

    for i in range(orders_count):
        customer = random.choice(customers)
        status = random.choice(statuses)

        # Create order
        order = Order.objects.create(
            customer=customer,
            status=status,
            shipping_address=f"{customer.address}, {customer.city} {customer.postal_code}",
            order_notes=f"Order notes for order {i+1}" if random.random() > 0.7 else "",
        )

        # Add random items to order
        num_items = random.randint(1, 5)
        selected_products = random.sample(products, num_items)

        for product in selected_products:
            quantity = random.randint(1, 3)
            OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=product.price
            )

        # Calculate total
        order.calculate_total()

        # Set realistic created date (last 60 days)
        days_ago = random.randint(0, 60)
        order.created_at = datetime.now() - timedelta(days=days_ago)
        order.save()

        print(
            f"  ✓ Order #{order.id}: {order.items.count()} items, ${order.total_amount}"
        )

    print(f"✅ Created {orders_count} orders!\n")


def main():
    print("\n" + "=" * 50)
    print("🚀 SHOPEASE DATA POPULATION SCRIPT")
    print("=" * 50 + "\n")

    # Clear existing data
    clear_data()

    # Create data
    categories = create_categories()
    products = create_products(categories)
    customers = create_customers()
    create_orders(customers, products)

    print("=" * 50)
    print("🎉 DATA POPULATION COMPLETE!")
    print("=" * 50)
    print("\n📊 Summary:")
    print(f"  Categories: {Category.objects.count()}")
    print(f"  Products: {Product.objects.count()}")
    print(f"  Customers: {Customer.objects.count()}")
    print(f"  Orders: {Order.objects.count()}")
    print(f"  Order Items: {OrderItem.objects.count()}")
    print("\n💡 Test Credentials:")
    print("  Username: john_doe")
    print("  Password: password123")
    print("  (All customers use password123)")
    print("\n")


if __name__ == "__main__":
    main()
