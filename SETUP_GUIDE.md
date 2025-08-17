# 🚀 Niche Compass Setup Guide

## 📋 Overview
Niche Compass adalah aplikasi untuk riset niche Etsy yang menggunakan AI untuk analisis produk, keyword research, dan competitor analysis.

**Current Status:**
- ✅ Backend API: RUNNING (Mock Mode)
- ✅ Frontend: RUNNING 
- ⚠️ Database: Mock Mode (data tidak persistent)
- ⚠️ AI Services: Mock Mode (tidak menggunakan real AI)

## 🌐 Live URLs
- **Backend API**: https://5000-i20omqxrp5gsgyv7zvab9-6532622b.e2b.dev
- **Frontend App**: https://5173-i20omqxrp5gsgyv7zvab9-6532622b.e2b.dev

---

## 🔴 CRITICAL: Fitur Yang Belum Diaktifkan

### 1. **Database Connection (KRITIS)**
**Problem**: Aplikasi berjalan dalam mock mode - data tidak tersimpan
**Impact**: 
- ❌ User data hilang saat restart
- ❌ Keyword tracking tidak persistent  
- ❌ History analysis tidak tersimpan

**Solution**: Setup Azure Cosmos DB
```bash
# 1. Create Azure Cosmos DB account with MongoDB API
# 2. Get connection string from Azure portal
# 3. Update COSMOS_DB_CONNECTION_STRING in .env
```

### 2. **Azure AI Services (AI Features)**
**Problem**: AI analysis menggunakan mock data
**Impact**:
- ❌ Image analysis produk tidak real
- ❌ Sentiment analysis review tidak akurat
- ❌ Text analytics tidak berfungsi

**Solution**: Setup Azure Cognitive Services
```bash
# 1. Create Cognitive Services resource in Azure
# 2. Create Computer Vision resource  
# 3. Create Text Analytics resource
# 4. Update Azure keys in .env
```

### 3. **Etsy API Integration (Data Real)**
**Problem**: Product data menggunakan mock/dummy data  
**Impact**:
- ❌ Pricing data tidak real
- ❌ Sales estimates tidak akurat
- ❌ Product info tidak up-to-date

**Solution**: Get Etsy API access
```bash
# 1. Register for Etsy Developer account
# 2. Create Etsy app and get API key
# 3. Update ETSY_API_KEY in .env
```

---

## ⚡ Quick Setup Steps

### Step 1: Environment Configuration
```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your actual credentials
nano .env
```

### Step 2: Database Setup (Azure Cosmos DB)
1. Go to Azure Portal → Create Cosmos DB Account
2. Choose MongoDB API
3. Get connection string
4. Update `COSMOS_DB_CONNECTION_STRING` in .env

### Step 3: Azure AI Services Setup
1. Create Cognitive Services resource
2. Create Computer Vision resource
3. Create Text Analytics resource  
4. Update all Azure keys in .env

### Step 4: Etsy API Setup
1. Go to https://developers.etsy.com/
2. Create developer account and app
3. Get API key
4. Update `ETSY_API_KEY` in .env

### Step 5: Restart Services
```bash
# Restart backend to load new environment
pm2 restart niche-compass-backend

# Restart frontend if needed
pm2 restart niche-compass-frontend
```

---

## 🧪 Testing Real Features

After setup, test these endpoints to verify real data:

### Test Database Connection
```bash
curl https://5000-i20omqxrp5gsgyv7zvab9-6532622b.e2b.dev/api/health
# Should show "database": "connected"
```

### Test Keyword Analysis (Real AI)
```bash
curl -X POST https://5000-i20omqxrp5gsgyv7zvab9-6532622b.e2b.dev/api/keywords/analyze \
  -H "Content-Type: application/json" \
  -d '{"keyword": "handmade jewelry"}'
```

### Test Product Analysis (Real Etsy + AI)
```bash
curl -X POST https://5000-i20omqxrp5gsgyv7zvab9-6532622b.e2b.dev/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.etsy.com/listing/real-listing-id"}'
```

---

## 📈 Feature Implementation Priority

### PHASE 1: Critical (MVP Functional)
1. ✅ Basic app structure (DONE)
2. 🔴 Database connection (NEEDED)  
3. 🔴 Environment configuration (NEEDED)

### PHASE 2: Core Features  
4. 🔴 Azure AI Services (NEEDED)
5. 🔴 Etsy API integration (NEEDED)
6. 🟡 User authentication (OPTIONAL)

### PHASE 3: Advanced Features
7. 🟡 Real-time monitoring (OPTIONAL)
8. 🟡 Caching layer (OPTIONAL)
9. 🟡 Push notifications (OPTIONAL)

---

## 🛟 Troubleshooting

### Backend Won't Start
```bash
# Check PM2 logs
pm2 logs niche-compass-backend

# Common issues:
# - Missing Python dependencies
# - Invalid environment variables
# - Port conflicts
```

### Frontend Build Errors
```bash
# Check Node.js version
node --version  # Should be 16+

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Database Connection Issues
```bash
# Test connection string manually
# Check Azure Cosmos DB firewall settings
# Verify MongoDB API is enabled
```

---

## 📞 Support

Jika mengalami kesulitan dalam setup:
1. Check logs dengan `pm2 logs [service-name]`
2. Verify environment variables di `.env`
3. Test individual components step by step
4. Check Azure resource configuration

**Current Working State**: Aplikasi berfungsi dengan mock data. Real features akan aktif setelah environment variables dikonfigurasi dengan benar.