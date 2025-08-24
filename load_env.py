#!/usr/bin/env python3
"""
Environment Variables Loader for Niche Compass
Loads environment variables from env.local file
"""

import os
import sys
from pathlib import Path

def load_environment_variables():
    """Load environment variables from env.local file"""
    
    # Look for environment file
    env_files = [
        '.env',
        'env.local',
        'production.env'
    ]
    
    env_file = None
    for file_name in env_files:
        if os.path.exists(file_name):
            env_file = file_name
            break
    
    if not env_file:
        print("⚠️  Warning: No environment file found")
        print("Available files:")
        for file_name in env_files:
            if os.path.exists(file_name):
                print(f"  ✅ {file_name}")
            else:
                print(f"  ❌ {file_name}")
        return False
    
    print(f"📁 Loading environment variables from: {env_file}")
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse key=value
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    # Set environment variable
                    os.environ[key] = value
                    print(f"  ✅ {key} = {'*' * len(value) if 'key' in key.lower() or 'secret' in key.lower() else value}")
        
        print(f"🎉 Environment variables loaded successfully from {env_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading environment variables: {str(e)}")
        return False

def check_environment_variables():
    """Check which environment variables are set"""
    
    print("\n🔍 Checking environment variables...")
    
    # Critical variables
    critical_vars = [
        'SECRET_KEY',
        'AZURE_COSMOS_ENDPOINT',
        'AZURE_COSMOS_KEY',
        'AZURE_VISION_ENDPOINT',
        'AZURE_VISION_API_KEY',
        'AZURE_TEXT_ANALYTICS_ENDPOINT',
        'AZURE_TEXT_ANALYTICS_API_KEY'
    ]
    
    # Optional variables
    optional_vars = [
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_API_KEY',
        'AUTH0_DOMAIN',
        'AUTH0_CLIENT_ID',
        'AUTH0_CLIENT_SECRET',
        'ETSY_API_KEY',
        'ETSY_API_SECRET'
    ]
    
    print("\n📋 Critical Variables:")
    for var in critical_vars:
        value = os.getenv(var)
        if value:
            masked_value = '*' * len(value) if 'key' in var.lower() or 'secret' in var.lower() else value
            print(f"  ✅ {var} = {masked_value}")
        else:
            print(f"  ❌ {var} = NOT SET")
    
    print("\n📋 Optional Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            masked_value = '*' * len(value) if 'key' in var.lower() or 'secret' in var.lower() else value
            print(f"  ✅ {var} = {masked_value}")
        else:
            print(f"  ⚠️  {var} = NOT SET (optional)")
    
    # Check if we have minimum required variables
    critical_missing = [var for var in critical_vars if not os.getenv(var)]
    
    if critical_missing:
        print(f"\n❌ Missing critical variables: {', '.join(critical_missing)}")
        print("Please set these variables in your environment file")
        return False
    else:
        print("\n🎉 All critical environment variables are set!")
        return True

def main():
    """Main function"""
    print("🚀 Niche Compass Environment Variables Loader")
    print("=" * 50)
    
    # Load environment variables
    if load_environment_variables():
        # Check what's loaded
        check_environment_variables()
        
        print("\n💡 Tips:")
        print("1. File env.local TIDAK akan di-commit ke GitHub")
        print("2. Ganti placeholder values dengan credentials asli Anda")
        print("3. Untuk production, gunakan Azure Key Vault atau environment variables")
        print("4. Jangan share credentials dengan siapapun")
        
    else:
        print("\n❌ Failed to load environment variables")
        sys.exit(1)

if __name__ == "__main__":
    main()
