#!/usr/bin/env python3
"""
Test script to check blueprint registration and routing
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../env.local')

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("🔍 Testing Blueprint Registration and Routing...")
print("=" * 60)

try:
    print("1. Creating Flask app...")
    from src.main import create_app
    app = create_app()
    print("   ✅ Flask app created successfully")
    
    print("\n2. Checking registered blueprints...")
    for blueprint_name, blueprint in app.blueprints.items():
        print(f"   📋 {blueprint_name}: {blueprint.name}")
        print(f"      URL Prefix: {blueprint.url_prefix}")
        print(f"      Routes:")
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith(blueprint_name):
                print(f"        {rule.rule} -> {rule.endpoint} [{', '.join(rule.methods)}]")
        print()
    
    print("\n3. Checking all registered routes...")
    for rule in app.url_map.iter_rules():
        print(f"   🌐 {rule.rule} -> {rule.endpoint} [{', '.join(rule.methods)}]")
    
    print("\n4. Testing AI endpoints specifically...")
    ai_routes = [rule for rule in app.url_map.iter_rules() if 'ai' in rule.endpoint]
    if ai_routes:
        print("   🤖 AI Routes found:")
        for route in ai_routes:
            print(f"      {route.rule} -> {route.endpoint} [{', '.join(rule.methods)}]")
    else:
        print("   ❌ No AI routes found!")
    
    print("\n🎉 Blueprint registration test completed!")
    
except Exception as e:
    print(f"\n❌ Error during testing: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
