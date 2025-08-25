#!/usr/bin/env python3
"""
Test script to check AI services import
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("🔍 Testing AI Services Import...")
print("=" * 50)

try:
    print("1. Testing AI Monitoring Service...")
    from ai.ai_monitoring_service import ai_monitor, MetricType
    print("   ✅ AI Monitoring Service imported successfully")
    
    print("2. Testing Azure Vision Service...")
    from ai.azure_vision_service import AzureVisionService, VisionFeature
    print("   ✅ Azure Vision Service imported successfully")
    
    print("3. Testing Azure Text Analytics Service...")
    from ai.azure_text_analytics_service import AzureTextAnalyticsService, TextAnalyticsFeature
    print("   ✅ Azure Text Analytics Service imported successfully")
    
    print("4. Testing AI Monitoring API...")
    from ai.ai_monitoring_api import ai_monitoring_bp
    print("   ✅ AI Monitoring API imported successfully")
    
    print("5. Testing AI Vision Routes...")
    from src.routes.ai_vision import ai_vision_bp
    print("   ✅ AI Vision Routes imported successfully")
    
    print("6. Testing AI Text Routes...")
    from src.routes.ai_text import ai_text_bp
    print("   ✅ AI Text Routes imported successfully")
    
    print("\n🎉 All AI Services imported successfully!")
    print("=" * 50)
    
    # Test blueprint registration
    print("\n🔧 Testing Blueprint Registration...")
    print(f"   AI Monitoring Blueprint: {ai_monitoring_bp.name}")
    print(f"   AI Vision Blueprint: {ai_vision_bp.name}")
    print(f"   AI Text Blueprint: {ai_text_bp.name}")
    
    print("\n✅ All tests passed!")
    
except Exception as e:
    print(f"\n❌ Error during import: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
