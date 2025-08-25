import os
from dotenv import load_dotenv

# Load environment variables from env.local
load_dotenv('../env.local')

print("✅ Environment loaded successfully!")
print()

print("📊 DATABASE CONFIGURATION:")
print(f"  Endpoint: {os.getenv('AZURE_COSMOS_ENDPOINT')}")
print(f"  Database: {os.getenv('AZURE_COSMOS_DATABASE')}")
print(f"  Container: {os.getenv('AZURE_COSMOS_CONTAINER')}")
print()

print("🤖 AI SERVICES:")
print(f"  Vision Endpoint: {os.getenv('AZURE_VISION_ENDPOINT')}")
print(f"  Text Analytics Endpoint: {os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')}")
print(f"  OpenAI Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print()

print("🔐 AUTHENTICATION:")
print(f"  Auth0 Domain: {os.getenv('AUTH0_DOMAIN')}")
print(f"  Client ID: {os.getenv('AUTH0_CLIENT_ID')}")
print()

print("🛍️ ETSY API:")
print(f"  Shop ID: {os.getenv('ETSY_SHOP_ID')}")
print(f"  API Key: {os.getenv('ETSY_API_KEY')}")
print(f"  API Secret: {os.getenv('ETSY_API_SECRET')}")
print()

print("⚙️ APPLICATION:")
print(f"  Flask App: {os.getenv('FLASK_APP')}")
print(f"  Environment: {os.getenv('FLASK_ENV')}")
print(f"  Debug: {os.getenv('FLASK_DEBUG')}")
