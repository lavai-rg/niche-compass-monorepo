#!/usr/bin/env python3
"""
Populate Sample Data for Niche Compass
Creates initial data for testing database functionality
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the backend src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database_adapter import get_collection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_users():
    """Create sample users"""
    users_collection = get_collection('users')
    
    sample_users = [
        {
            "username": "demo_user_1",
            "email": "demo1@nichecompass.com",
            "subscription_tier": "free",
            "created_at": datetime.utcnow(),
            "tracked_keywords": ["handmade jewelry", "vintage decor", "eco friendly"],
            "favorite_niches": ["jewelry", "home_decor", "sustainable_products"],
            "usage_stats": {
                "keywords_searched": 25,
                "products_analyzed": 12,
                "niches_explored": 8
            }
        },
        {
            "username": "pro_seller",
            "email": "pro@nichecompass.com", 
            "subscription_tier": "premium",
            "created_at": datetime.utcnow() - timedelta(days=30),
            "tracked_keywords": ["minimalist art", "personalized gifts", "wedding decorations"],
            "favorite_niches": ["art", "wedding", "personalization"],
            "usage_stats": {
                "keywords_searched": 150,
                "products_analyzed": 89,
                "niches_explored": 25
            }
        },
        {
            "username": "craft_enthusiast",
            "email": "crafter@nichecompass.com",
            "subscription_tier": "basic",
            "created_at": datetime.utcnow() - timedelta(days=15),
            "tracked_keywords": ["diy crafts", "knitting patterns", "scrapbook supplies"],
            "favorite_niches": ["crafts", "diy", "paper_goods"],
            "usage_stats": {
                "keywords_searched": 78,
                "products_analyzed": 34,
                "niches_explored": 15
            }
        }
    ]
    
    created_count = 0
    for user in sample_users:
        # Check if user already exists
        existing = users_collection.find_one({"email": user["email"]})
        if not existing:
            user_id = users_collection.insert_one(user)
            logger.info(f"Created user: {user['username']} (ID: {user_id})")
            created_count += 1
        else:
            logger.info(f"User already exists: {user['username']}")
    
    return created_count

def create_sample_keywords():
    """Create sample keywords"""
    keywords_collection = get_collection('keywords')
    
    sample_keywords = [
        {
            "keyword": "handmade jewelry",
            "search_volume": 2850,
            "competition_level": "medium",
            "trend_direction": "rising",
            "related_keywords": ["custom jewelry", "artisan jewelry", "unique jewelry", "personalized jewelry"],
            "price_range": {"min": 15, "max": 200, "avg": 45},
            "category": "jewelry",
            "difficulty_score": 65,
            "opportunity_score": 75,
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        },
        {
            "keyword": "vintage home decor",
            "search_volume": 3200,
            "competition_level": "high",
            "trend_direction": "stable",
            "related_keywords": ["retro decor", "antique decor", "vintage furniture", "mid century modern"],
            "price_range": {"min": 25, "max": 500, "avg": 85},
            "category": "home_decor",
            "difficulty_score": 80,
            "opportunity_score": 60,
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        },
        {
            "keyword": "eco friendly products",
            "search_volume": 1950,
            "competition_level": "low",
            "trend_direction": "rising",
            "related_keywords": ["sustainable products", "green products", "eco conscious", "zero waste"],
            "price_range": {"min": 10, "max": 150, "avg": 35},
            "category": "sustainable",
            "difficulty_score": 40,
            "opportunity_score": 85,
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        },
        {
            "keyword": "personalized gifts",
            "search_volume": 4100,
            "competition_level": "high",
            "trend_direction": "rising",
            "related_keywords": ["custom gifts", "engraved gifts", "monogrammed items", "bespoke presents"],
            "price_range": {"min": 20, "max": 300, "avg": 65},
            "category": "gifts",
            "difficulty_score": 75,
            "opportunity_score": 70,
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        },
        {
            "keyword": "minimalist art",
            "search_volume": 1650,
            "competition_level": "medium",
            "trend_direction": "stable",
            "related_keywords": ["abstract art", "simple art", "modern art prints", "geometric art"],
            "price_range": {"min": 15, "max": 120, "avg": 40},
            "category": "art",
            "difficulty_score": 55,
            "opportunity_score": 70,
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        }
    ]
    
    created_count = 0
    for keyword in sample_keywords:
        existing = keywords_collection.find_one({"keyword": keyword["keyword"]})
        if not existing:
            keyword_id = keywords_collection.insert_one(keyword)
            logger.info(f"Created keyword: {keyword['keyword']} (ID: {keyword_id})")
            created_count += 1
        else:
            logger.info(f"Keyword already exists: {keyword['keyword']}")
    
    return created_count

def create_sample_niches():
    """Create sample niches"""
    niches_collection = get_collection('niches')
    
    sample_niches = [
        {
            "name": "Handmade Jewelry",
            "category": "jewelry",
            "description": "Custom and artisan jewelry market focusing on unique, handcrafted pieces",
            "competition_score": 65,
            "demand_score": 80,
            "opportunity_score": 75,
            "trend_data": {
                "search_volume_trend": [2200, 2400, 2600, 2850, 3100, 2950, 3200],
                "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                "growth_rate": 18.5,
                "seasonality": "holiday_peaks"
            },
            "price_analysis": {
                "average_price": 45.50,
                "median_price": 32.00,
                "price_range": {"min": 15, "max": 200},
                "price_distribution": {
                    "under_25": 35,
                    "25_50": 30, 
                    "50_100": 25,
                    "over_100": 10
                }
            },
            "visual_analysis": {
                "dominant_colors": ["#FFD700", "#C0C0C0", "#E6E6FA"],
                "popular_styles": ["minimalist", "bohemian", "vintage", "modern"],
                "image_types": ["lifestyle", "flat_lay", "model_wearing"]
            },
            "top_keywords": ["handmade jewelry", "custom jewelry", "artisan jewelry"],
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        },
        {
            "name": "Sustainable Home Decor",
            "category": "home_decor",
            "description": "Eco-friendly home decoration items made from sustainable materials",
            "competition_score": 45,
            "demand_score": 85,
            "opportunity_score": 88,
            "trend_data": {
                "search_volume_trend": [1500, 1650, 1800, 2100, 2350, 2200, 2400],
                "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                "growth_rate": 25.5,
                "seasonality": "spring_summer_peak"
            },
            "price_analysis": {
                "average_price": 62.30,
                "median_price": 45.00,
                "price_range": {"min": 20, "max": 250},
                "price_distribution": {
                    "under_25": 15,
                    "25_50": 35,
                    "50_100": 35,
                    "over_100": 15
                }
            },
            "visual_analysis": {
                "dominant_colors": ["#228B22", "#8FBC8F", "#F5F5DC"],
                "popular_styles": ["natural", "rustic", "modern", "scandinavian"],
                "image_types": ["room_setting", "product_only", "lifestyle"]
            },
            "top_keywords": ["eco friendly decor", "sustainable home", "green decor"],
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        },
        {
            "name": "Personalized Pet Accessories",
            "category": "pets",
            "description": "Custom pet accessories including collars, tags, and toys",
            "competition_score": 55,
            "demand_score": 75,
            "opportunity_score": 72,
            "trend_data": {
                "search_volume_trend": [1800, 1900, 2100, 2300, 2200, 2400, 2500],
                "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                "growth_rate": 22.1,
                "seasonality": "consistent"
            },
            "price_analysis": {
                "average_price": 28.75,
                "median_price": 24.00,
                "price_range": {"min": 8, "max": 85},
                "price_distribution": {
                    "under_25": 50,
                    "25_50": 35,
                    "50_100": 15,
                    "over_100": 0
                }
            },
            "visual_analysis": {
                "dominant_colors": ["#4169E1", "#FF69B4", "#32CD32"],
                "popular_styles": ["cute", "functional", "colorful", "durable"],
                "image_types": ["pet_wearing", "product_only", "lifestyle"]
            },
            "top_keywords": ["personalized pet collar", "custom dog tag", "pet accessories"],
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        }
    ]
    
    created_count = 0
    for niche in sample_niches:
        existing = niches_collection.find_one({"name": niche["name"]})
        if not existing:
            niche_id = niches_collection.insert_one(niche)
            logger.info(f"Created niche: {niche['name']} (ID: {niche_id})")
            created_count += 1
        else:
            logger.info(f"Niche already exists: {niche['name']}")
    
    return created_count

def create_sample_products():
    """Create sample products"""
    products_collection = get_collection('products')
    
    sample_products = [
        {
            "title": "Handmade Sterling Silver Minimalist Ring",
            "url": "https://www.etsy.com/listing/sample-123456",
            "store_name": "SilverCraftStudio",
            "price": 45.00,
            "currency": "USD",
            "rating": 4.8,
            "reviews_count": 127,
            "sales_estimate": 250,
            "niche": "Handmade Jewelry",
            "category": "jewelry",
            "tags": ["minimalist", "sterling silver", "handmade", "modern", "elegant"],
            "description": "Beautiful minimalist sterling silver ring, perfect for everyday wear",
            "listing_date": datetime.utcnow() - timedelta(days=45),
            "last_analyzed": datetime.utcnow(),
            "sales_analysis": {
                "estimated_monthly_sales": 85,
                "estimated_monthly_revenue": 3825.00,
                "confidence_level": "high",
                "trend": "stable"
            },
            "competition_analysis": {
                "similar_products": 15,
                "avg_competitor_price": 52.30,
                "price_advantage": "lower"
            }
        },
        {
            "title": "Eco-Friendly Bamboo Wall Art Set",
            "url": "https://www.etsy.com/listing/sample-789012",
            "store_name": "GreenHomeDecor",
            "price": 68.50,
            "currency": "USD", 
            "rating": 4.9,
            "reviews_count": 89,
            "sales_estimate": 180,
            "niche": "Sustainable Home Decor",
            "category": "home_decor",
            "tags": ["eco-friendly", "bamboo", "wall art", "sustainable", "natural"],
            "description": "Set of 3 eco-friendly bamboo wall art pieces for modern homes",
            "listing_date": datetime.utcnow() - timedelta(days=30),
            "last_analyzed": datetime.utcnow(),
            "sales_analysis": {
                "estimated_monthly_sales": 60,
                "estimated_monthly_revenue": 4110.00,
                "confidence_level": "medium",
                "trend": "rising"
            },
            "competition_analysis": {
                "similar_products": 8,
                "avg_competitor_price": 75.20,
                "price_advantage": "lower"
            }
        },
        {
            "title": "Personalized Leather Dog Collar with Nameplate",
            "url": "https://www.etsy.com/listing/sample-345678",
            "store_name": "PawsomeCustoms",
            "price": 32.00,
            "currency": "USD",
            "rating": 4.7,
            "reviews_count": 203,
            "sales_estimate": 320,
            "niche": "Personalized Pet Accessories",
            "category": "pets",
            "tags": ["personalized", "leather", "dog collar", "custom", "durable"],
            "description": "High-quality leather dog collar with custom engraved nameplate",
            "listing_date": datetime.utcnow() - timedelta(days=60),
            "last_analyzed": datetime.utcnow(),
            "sales_analysis": {
                "estimated_monthly_sales": 110,
                "estimated_monthly_revenue": 3520.00,
                "confidence_level": "high",
                "trend": "stable"
            },
            "competition_analysis": {
                "similar_products": 25,
                "avg_competitor_price": 28.90,
                "price_advantage": "higher"
            }
        }
    ]
    
    created_count = 0
    for product in sample_products:
        existing = products_collection.find_one({"url": product["url"]})
        if not existing:
            product_id = products_collection.insert_one(product)
            logger.info(f"Created product: {product['title'][:50]}... (ID: {product_id})")
            created_count += 1
        else:
            logger.info(f"Product already exists: {product['title'][:50]}...")
    
    return created_count

def main():
    print("🚀 Populating Niche Compass with Sample Data")
    print("=" * 60)
    
    try:
        # Create sample data
        users_created = create_sample_users()
        keywords_created = create_sample_keywords() 
        niches_created = create_sample_niches()
        products_created = create_sample_products()
        
        print("\n📊 Sample Data Creation Summary:")
        print(f"✅ Users created: {users_created}")
        print(f"✅ Keywords created: {keywords_created}")
        print(f"✅ Niches created: {niches_created}")
        print(f"✅ Products created: {products_created}")
        
        total_created = users_created + keywords_created + niches_created + products_created
        print(f"\n🎉 Total items created: {total_created}")
        
        if total_created > 0:
            print("\n📋 Next steps:")
            print("1. Restart backend: pm2 restart niche-compass-backend")
            print("2. Test API endpoints with real data")
            print("3. Check frontend functionality")
        else:
            print("\n✅ All sample data already exists in database")
        
        return True
        
    except Exception as e:
        logger.error(f"Error populating sample data: {e}")
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)