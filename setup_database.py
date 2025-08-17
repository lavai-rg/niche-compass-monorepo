#!/usr/bin/env python3
"""
Database Setup Script for Niche Compass
Supports both MongoDB Atlas (cloud) and local development database setup
"""

import os
import sys
from pymongo import MongoClient
from datetime import datetime
import json

def test_connection(connection_string, database_name):
    """Test database connection"""
    try:
        print("🔄 Testing database connection...")
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Database connection successful!")
        
        # Get database
        db = client[database_name]
        
        # Test basic operations
        test_collection = db.test_connection
        test_doc = {
            "test": True,
            "timestamp": datetime.utcnow(),
            "message": "Database connection test successful"
        }
        
        # Insert test document
        result = test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Read test document
        found_doc = test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Test document retrieved: {found_doc['message']}")
        
        # Delete test document
        test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")
        
        # List existing collections
        collections = db.list_collection_names()
        print(f"📁 Existing collections: {collections if collections else 'None (fresh database)'}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def create_sample_data(connection_string, database_name):
    """Create sample data for testing"""
    try:
        print("\n🔄 Creating sample data...")
        client = MongoClient(connection_string)
        db = client[database_name]
        
        # Sample users
        users_collection = db.users
        sample_users = [
            {
                "username": "demo_user",
                "email": "demo@example.com",
                "subscription_tier": "free",
                "created_at": datetime.utcnow(),
                "tracked_keywords": ["handmade jewelry", "vintage decor"],
                "favorite_niches": ["jewelry", "home_decor"]
            }
        ]
        
        # Insert sample users if collection is empty
        if users_collection.count_documents({}) == 0:
            result = users_collection.insert_many(sample_users)
            print(f"✅ Created {len(result.inserted_ids)} sample users")
        
        # Sample keywords
        keywords_collection = db.keywords
        sample_keywords = [
            {
                "keyword": "handmade jewelry",
                "search_volume": 2500,
                "competition_level": "medium",
                "trend_direction": "rising",
                "related_keywords": ["custom jewelry", "artisan jewelry", "unique jewelry"],
                "price_range": {"min": 15, "max": 200, "avg": 45},
                "created_at": datetime.utcnow()
            },
            {
                "keyword": "vintage home decor",
                "search_volume": 3200,
                "competition_level": "high",
                "trend_direction": "stable",
                "related_keywords": ["retro decor", "antique decor", "vintage furniture"],
                "price_range": {"min": 25, "max": 500, "avg": 85},
                "created_at": datetime.utcnow()
            },
            {
                "keyword": "eco friendly products",
                "search_volume": 1800,
                "competition_level": "low",
                "trend_direction": "rising",
                "related_keywords": ["sustainable products", "green products", "eco conscious"],
                "price_range": {"min": 10, "max": 150, "avg": 35},
                "created_at": datetime.utcnow()
            }
        ]
        
        if keywords_collection.count_documents({}) == 0:
            result = keywords_collection.insert_many(sample_keywords)
            print(f"✅ Created {len(result.inserted_ids)} sample keywords")
        
        # Sample niches
        niches_collection = db.niches
        sample_niches = [
            {
                "name": "Handmade Jewelry",
                "category": "jewelry",
                "description": "Custom and artisan jewelry niche",
                "competition_score": 65,
                "demand_score": 80,
                "trend_data": {
                    "search_volume_trend": [100, 120, 150, 180, 200, 190, 210],
                    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                    "growth_rate": 15.5
                },
                "price_analysis": {
                    "average_price": 45.50,
                    "price_range": {"min": 15, "max": 200}
                },
                "created_at": datetime.utcnow()
            }
        ]
        
        if niches_collection.count_documents({}) == 0:
            result = niches_collection.insert_many(sample_niches)
            print(f"✅ Created {len(result.inserted_ids)} sample niches")
        
        client.close()
        print("✅ Sample data creation completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {str(e)}")
        return False

def setup_indexes(connection_string, database_name):
    """Setup database indexes for better performance"""
    try:
        print("\n🔄 Setting up database indexes...")
        client = MongoClient(connection_string)
        db = client[database_name]
        
        # Users indexes
        db.users.create_index("email", unique=True)
        db.users.create_index("username", unique=True)
        print("✅ Users indexes created")
        
        # Keywords indexes
        db.keywords.create_index("keyword", unique=True)
        db.keywords.create_index("search_volume")
        db.keywords.create_index("competition_level")
        print("✅ Keywords indexes created")
        
        # Niches indexes
        db.niches.create_index("name", unique=True)
        db.niches.create_index("category")
        db.niches.create_index("competition_score")
        db.niches.create_index("demand_score")
        print("✅ Niches indexes created")
        
        # Products indexes (for future use)
        db.products.create_index("url", unique=True)
        db.products.create_index("niche")
        db.products.create_index("price")
        print("✅ Products indexes created")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to setup indexes: {str(e)}")
        return False

def main():
    print("🚀 Niche Compass Database Setup")
    print("=" * 50)
    
    # Check if .env exists
    env_file = "/home/user/webapp/.env"
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        print("📝 Please create .env file with database configuration:")
        print("")
        print("COSMOS_DB_CONNECTION_STRING=your_connection_string_here")
        print("DATABASE_NAME=nichecompass")
        print("")
        print("💡 For MongoDB Atlas (free):")
        print("1. Go to https://cloud.mongodb.com/")
        print("2. Create free account and cluster")
        print("3. Get connection string")
        print("4. Add to .env file")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING')
    database_name = os.getenv('DATABASE_NAME', 'nichecompass')
    
    if not connection_string:
        print("❌ COSMOS_DB_CONNECTION_STRING not found in .env file!")
        print("📝 Please add your database connection string to .env")
        return False
    
    if 'YOUR_PRIMARY_KEY' in connection_string or 'your_' in connection_string.lower():
        print("❌ Please replace placeholder with actual connection string!")
        return False
    
    print(f"🔄 Connecting to database: {database_name}")
    print(f"🔗 Connection: {connection_string[:50]}...")
    
    # Test connection
    if not test_connection(connection_string, database_name):
        return False
    
    # Setup indexes
    if not setup_indexes(connection_string, database_name):
        print("⚠️ Index setup failed, but database connection works")
    
    # Create sample data
    if not create_sample_data(connection_string, database_name):
        print("⚠️ Sample data creation failed, but database connection works")
    
    print("\n🎉 Database setup completed successfully!")
    print("✅ Your application is now ready to use real database!")
    print("\n📋 Next steps:")
    print("1. Restart backend: pm2 restart niche-compass-backend")
    print("2. Test health endpoint: curl .../api/health")
    print("3. Verify database status shows 'connected'")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)