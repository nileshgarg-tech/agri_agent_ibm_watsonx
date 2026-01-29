"""
Demo Data Seeding Script
Populates the database with realistic farm activity data for testing.

Usage:
    python seed_data.py                    # Seeds all demo users
    python seed_data.py --user EMAIL       # Seeds specific user only
    python seed_data.py --clear            # Clears all data first
"""
import argparse
from datetime import datetime, timedelta
from db_storage import write_log, get_db_connection
import os


def clear_user_data(user_id: str):
    """Delete all data for a user"""
    from db_storage import get_data_file_path
    db_path = get_data_file_path(user_id)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Cleared data for {user_id}")


def seed_user_data(user_id: str, activities: list):
    """Seed a user's database with sample activities"""
    print(f"\n📊 Seeding data for {user_id}...")
    
    for activity in activities:
        try:
            write_log(activity, user_id)
            print(f"  ✓ Logged: {activity['action']} of {activity['item']}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
    
    print(f"✅ Seeded {len(activities)} activities for {user_id}")


# Demo user 1: Active farmer with diverse activities
TESTUSER_ACTIVITIES = [
    # Sales
    {
        "action": "sale",
        "item": "tomatoes",
        "quantity": 50,
        "unit": "pounds",
        "value_usd": 75.00,
        "note": "Sold at farmers market",
        "timestamp": (datetime.now(datetime.UTC) - timedelta(days=2)).isoformat()
    },
    {
        "action": "sale",
        "item": "carrots",
        "quantity": 30,
        "unit": "pounds",
        "value_usd": 45.00,
        "note": "Sold to local restaurant",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat()
    },
    {
        "action": "sale",
        "item": "eggs",
        "quantity": 24,
        "unit": "dozen",
        "value_usd": 96.00,
        "note": "Regular customer order",
        "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat()
    },
    {
        "action": "sale",
        "item": "potatoes",
        "quantity": 100,
        "unit": "pounds",
        "value_usd": 120.00,
        "note": "Bulk sale to grocery store",
        "timestamp": (datetime.utcnow() - timedelta(days=5)).isoformat()
    },
    {
        "action": "sale",
        "item": "lettuce",
        "quantity": 15,
        "unit": "heads",
        "value_usd": 30.00,
        "note": "Farmers market",
        "timestamp": (datetime.utcnow() - timedelta(days=4)).isoformat()
    },
    
    # Harvests
    {
        "action": "harvest",
        "item": "tomatoes",
        "quantity": 150,
        "unit": "pounds",
        "note": "West field, heirloom variety",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat()
    },
    {
        "action": "harvest",
        "item": "potatoes",
        "quantity": 200,
        "unit": "pounds",
        "note": "North field, Yukon gold",
        "timestamp": (datetime.utcnow() - timedelta(days=6)).isoformat()
    },
    {
        "action": "harvest",
        "item": "squash",
        "quantity": 45,
        "unit": "pounds",
        "note": "Butternut and acorn varieties",
        "timestamp": (datetime.utcnow() - timedelta(days=7)).isoformat()
    },
    
    # Expenses
    {
        "action": "expense",
        "item": "tractor fuel",
        "quantity": 15,
        "unit": "gallons",
        "value_usd": 52.50,
        "note": "Monthly refill",
        "timestamp": (datetime.utcnow() - timedelta(days=4)).isoformat()
    },
    {
        "action": "expense",
        "item": "irrigation repair",
        "value_usd": 85.00,
        "note": "Fixed broken sprinkler line",
        "timestamp": (datetime.utcnow() - timedelta(days=8)).isoformat()
    },
    
    # Purchases
    {
        "action": "purchase",
        "item": "fertilizer",
        "quantity": 5,
        "unit": "bags",
        "value_usd": 120.00,
        "note": "Organic compost blend",
        "timestamp": (datetime.utcnow() - timedelta(days=10)).isoformat()
    },
    {
        "action": "purchase",
        "item": "seeds",
        "value_usd": 45.00,
        "note": "Winter crop seeds (kale, spinach)",
        "timestamp": (datetime.utcnow() - timedelta(days=12)).isoformat()
    },
    {
        "action": "purchase",
        "item": "chicken feed",
        "quantity": 2,
        "unit": "bags",
        "value_usd": 38.00,
        "note": "50lb bags",
        "timestamp": (datetime.utcnow() - timedelta(days=7)).isoformat()
    },
    
    # Recent activities
    {
        "action": "sale",
        "item": "herbs",
        "quantity": 10,
        "unit": "bunches",
        "value_usd": 25.00,
        "note": "Basil and parsley",
        "timestamp": datetime.now(datetime.UTC).isoformat()
    },
    {
        "action": "harvest",
        "item": "carrots",
        "quantity": 80,
        "unit": "pounds",
        "note": "East field",
        "timestamp": (datetime.utcnow() - timedelta(hours=6)).isoformat()
    },
]

# Demo user 2: Smaller operation
DEMO_ACTIVITIES = [
    {
        "action": "sale",
        "item": "eggs",
        "quantity": 12,
        "unit": "dozen",
        "value_usd": 48.00,
        "note": "Weekly customer orders",
        "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat()
    },
    {
        "action": "harvest",
        "item": "zucchini",
        "quantity": 25,
        "unit": "pounds",
        "note": "Garden harvest",
        "timestamp": (datetime.now(datetime.UTC) - timedelta(days=2)).isoformat()
    },
    {
        "action": "sale",
        "item": "zucchini",
        "quantity": 20,
        "unit": "pounds",
        "value_usd": 30.00,
        "note": "Neighborhood sale",
        "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat()
    },
    {
        "action": "expense",
        "item": "chicken coop supplies",
        "value_usd": 65.00,
        "note": "Bedding and feeders",
        "timestamp": (datetime.utcnow() - timedelta(days=5)).isoformat()
    },
    {
        "action": "harvest",
        "item": "tomatoes",
        "quantity": 35,
        "unit": "pounds",
        "note": "Cherry and beefsteak",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat()
    },
]


def main():
    parser = argparse.ArgumentParser(description="Seed demo data for AgriAgent")
    parser.add_argument("--user", type=str, help="Seed specific user only (email)")
    parser.add_argument("--clear", action="store_true", help="Clear existing data before seeding")
    args = parser.parse_args()
    
    print("🌱 AgriAgent Demo Data Seeding Tool")
    print("=" * 50)
    
    users_to_seed = {
        "testuser@gmail.com": TESTUSER_ACTIVITIES,
        "demo@farm.com": DEMO_ACTIVITIES,
    }
    
    # Filter to specific user if requested
    if args.user:
        if args.user in users_to_seed:
            users_to_seed = {args.user: users_to_seed[args.user]}
        else:
            print(f"⚠️ Unknown user: {args.user}")
            print(f"Available: {', '.join(users_to_seed.keys())}")
            return
    
    # Clear data if requested
    if args.clear:
        print("\n🗑️  Clearing existing data...")
        for user_id in users_to_seed.keys():
            clear_user_data(user_id)
    
    # Seed each user
    for user_id, activities in users_to_seed.items():
        seed_user_data(user_id, activities)
    
    print("\n" + "=" * 50)
    print("🎉 Demo data seeding complete!")
    print("\nTest the app:")
    print("  - Streamlit: streamlit run app.py")
    print("  - CLI: python main.py")
    print("\nDemo users:")
    print("  - testuser@gmail.com (15 activities)")
    print("  - demo@farm.com (5 activities)")
    print("  - newbie@test.com (0 activities - test empty state)")


if __name__ == "__main__":
    main()
