#!/usr/bin/env python3
"""
Test script untuk cek environment variables
"""

import os
from dotenv import load_dotenv

def test_env_vars():
    """Test environment variables loading"""
    print("🔍 Testing Environment Variables...")
    print("=" * 50)
    
    # Load env.local
    print("📁 Loading env.local...")
    load_dotenv('env.local')
    
    # Check JWT settings
    print("\n🔐 JWT Settings:")
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    print(f"JWT_SECRET_KEY: {jwt_secret[:30] if jwt_secret else 'NOT SET'}...")
    
    # Check Flask settings
    print("\n⚙️ Flask Settings:")
    flask_env = os.getenv('FLASK_ENV')
    flask_debug = os.getenv('FLASK_DEBUG')
    print(f"FLASK_ENV: {flask_env}")
    print(f"FLASK_DEBUG: {flask_debug}")
    
    # Check Azure settings
    print("\n☁️ Azure Settings:")
    cosmos_endpoint = os.getenv('AZURE_COSMOS_ENDPOINT')
    vision_endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    print(f"AZURE_COSMOS_ENDPOINT: {cosmos_endpoint}")
    print(f"AZURE_VISION_ENDPOINT: {vision_endpoint}")
    
    # Check Auth0 settings
    print("\n🔑 Auth0 Settings:")
    auth0_domain = os.getenv('AUTH0_DOMAIN')
    auth0_client_id = os.getenv('AUTH0_CLIENT_ID')
    print(f"AUTH0_DOMAIN: {auth0_domain}")
    print(f"AUTH0_CLIENT_ID: {auth0_client_id[:20] if auth0_client_id else 'NOT SET'}...")
    
    # Check Etsy settings
    print("\n🛍️ Etsy Settings:")
    etsy_api_key = os.getenv('ETSY_API_KEY')
    etsy_shop_id = os.getenv('ETSY_SHOP_ID')
    print(f"ETSY_API_KEY: {etsy_api_key[:20] if etsy_api_key else 'NOT SET'}...")
    print(f"ETSY_SHOP_ID: {etsy_shop_id}")
    
    print("\n" + "=" * 50)
    
    # Test if JWT secret is accessible
    if jwt_secret:
        print("✅ JWT_SECRET_KEY is set and accessible")
        return True
    else:
        print("❌ JWT_SECRET_KEY is NOT set or accessible")
        return False

if __name__ == "__main__":
    test_env_vars()
