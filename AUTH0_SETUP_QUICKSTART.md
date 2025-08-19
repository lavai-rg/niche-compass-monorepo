# 🚀 **QUICK START - SETUP AUTH0 UNTUK NICHE COMPASS**

## **📋 Langkah-langkah Setup (5 Menit)**

### **1. Buat Auth0 Account** 
1. Pergi ke [auth0.com](https://auth0.com)
2. Sign up untuk account gratis
3. Pilih region terdekat (Asia Pacific/Singapore)

### **2. Setup Auth0 Application**
1. Di Auth0 Dashboard → **Applications** → **Create Application**
2. **Application Name**: `Niche Compass Frontend`
3. **Application Type**: `Single Page Web Applications`
4. Klik **Create**

**Konfigurasi Application:**
- **Allowed Callback URLs**: 
  ```
  http://localhost:3000/callback,
  http://localhost:3000,
  https://your-production-domain.com/callback
  ```
- **Allowed Logout URLs**: 
  ```
  http://localhost:3000,
  https://your-production-domain.com
  ```
- **Allowed Web Origins**: 
  ```
  http://localhost:3000,
  https://your-production-domain.com
  ```

### **3. Setup Auth0 API**
1. Di Auth0 Dashboard → **APIs** → **Create API**
2. **Name**: `Niche Compass API`
3. **Identifier**: `https://nichecompass-api`
4. **Signing Algorithm**: `RS256`

### **4. Update Environment Variables**

**File: `/home/user/webapp/.env`**
```bash
# Ganti nilai ini dengan credentials asli dari Auth0 Dashboard
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_CLIENT_ID=your_actual_client_id_from_dashboard
AUTH0_CLIENT_SECRET=your_actual_client_secret_from_dashboard
AUTH0_AUDIENCE=https://nichecompass-api
AUTH0_CALLBACK_URL=http://localhost:3000/callback

# Frontend vars
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_actual_client_id_from_dashboard
VITE_AUTH0_AUDIENCE=https://nichecompass-api
VITE_AUTH0_CALLBACK_URL=http://localhost:3000/callback
```

### **5. Testing Setup**

**Jalankan Backend:**
```bash
cd /home/user/webapp/backend
pip install -r requirements.txt
python src/main.py
```

**Jalankan Frontend (terminal baru):**
```bash
cd /home/user/webapp/frontend
npm install --legacy-peer-deps
npm run dev
```

**Test Authentication:**
1. Buka `http://localhost:3000`
2. Klik tombol **"Masuk"**
3. Login dengan akun Google/email
4. Setelah redirect, user profile muncul di header
5. Coba akses fitur Keywords/Niches (harus berjalan dengan token)

---

## **🔍 Debugging Common Issues**

### **Issue 1: "Auth0 domain tidak dikonfigurasi"**
- ✅ Pastikan `.env` file ada di folder root `/home/user/webapp/`
- ✅ Restart aplikasi setelah update environment variables

### **Issue 2: "Callback error" saat login**
- ✅ Cek Allowed Callback URLs di Auth0 Dashboard
- ✅ Pastikan URL persis sama dengan environment variable

### **Issue 3: "Token invalid" di API**
- ✅ Cek Auth0 Audience sama antara frontend dan backend
- ✅ Pastikan API identifier di Auth0 Dashboard: `https://nichecompass-api`

---

## **🎯 Hasil Yang Diharapkan**

Setelah setup benar, Anda akan mendapatkan:

✅ **Login Flow**: User bisa login dengan Auth0  
✅ **Protected Pages**: Dashboard, Keywords, Niches require authentication  
✅ **User Profile**: Avatar dan info user di header  
✅ **API Security**: All sensitive endpoints protected dengan JWT  
✅ **Logout**: User bisa logout dengan aman  

---

## **📞 Butuh Bantuan?**

Jika ada masalah setup, cek:
1. File `AUTH0_IMPLEMENTATION_GUIDE.md` untuk dokumentasi lengkap
2. Console browser untuk error messages
3. Backend logs untuk authentication errors
4. Auth0 Dashboard → Logs untuk login attempts

**Auth0 sudah FULLY IMPLEMENTED dan siap pakai!** 🚀