# 🔑 KIJAN POU ITILIZE SUPABASE KEY OU A

## 🎯 Sa ou gen:

```
SUPABASE_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJxdXJseXlzbGJycGRqbmFicnRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NTc4ODMsImV4cCI6MjA4MzUzMzg4M30.Jko5sA_Bv281uuPkFpwiZBKHooRBljoEO8x49Rwf4CE
```

**Project Reference:** `rqurlyyslbrpdjnabrts`

---

## 📋 KI JAN POU SETUP

### Step 1: Ale nan Supabase Dashboard
1. Visit: https://supabase.com/dashboard
2. Login
3. Find project: **rqurlyyslbrpdjnabrts**
4. Go to **Settings → API**

### Step 2: Copye SUPABASE_URL
Look for **Project URL** (exemple: `https://rqurlyyslbrpdjnabrts.supabase.co`)
- Copy the full URL

### Step 3: Create/Edit .env File
```bash
cd ~/ecommerce-dashboard
nano .env
```

Add:
```
SUPABASE_URL=https://rqurlyyslbrpdjnabrts.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJxdXJseXlzbGJycGRqbmFicnRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NTc4ODMsImV4cCI6MjA4MzUzMzg4M30.Jko5sA_Bv281uuPkFpwiZBKHooRBljoEO8x49Rwf4CE
USE_LOCAL_DATA=False
```

Replace **URL** avèk adrès rèl Supabase ou a.

### Step 4: Create Tables in Supabase
1. In Supabase dashboard, go to **SQL Editor**
2. Copy + Run SQL from: `SUPABASE_SETUP.md`
3. Create 4 tables: vant, pwodwi, kliyan, komand

### Step 5: Test Connection
```bash
python examples.py
```

Should show: `✅ Konekte ak Supabase!`

### Step 6: Run Dashboard
```bash
python app.py
```

Visit: http://localhost:8050

---

## ❓ KI JAN POU JWENN SUPABASE_URL?

### Method 1: Find in Dashboard
1. Visit https://supabase.com/dashboard
2. Click on your project
3. Settings → API → Project URL
4. Copy it (exemple: `https://rqurlyyslbrpdjnabrts.supabase.co`)

### Method 2: From Your JWT Token
Based on your token, your project reference is: `rqurlyyslbrpdjnabrts`

So URL should be:
```
https://rqurlyyslbrpdjnabrts.supabase.co
```

If this doesn't work, double-check in your Supabase dashboard.

---

## ✅ FINAL .env FILE

```
SUPABASE_URL=https://rqurlyyslbrpdjnabrts.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJxdXJseXlzbGJycGRqbmFicnRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NTc4ODMsImV4cCI6MjA4MzUzMzg4M30.Jko5sA_Bv281uuPkFpwiZBKHooRBljoEO8x49Rwf4CE
USE_LOCAL_DATA=False
DEBUG=True
PORT=8050
```

---

## 🚀 RUN DASHBOARD

```bash
cd ~/ecommerce-dashboard
python app.py
```

---

## 🧪 TEST CONNECTION

```bash
python examples.py
```

Look for: `✅ Konekte ak Supabase!`

---

## 🔗 NECESSARY STEPS

1. ✅ Get SUPABASE_URL from dashboard
2. ✅ Create .env file
3. ✅ Add SUPABASE_URL + SUPABASE_KEY
4. ✅ Create database tables (SQL from SUPABASE_SETUP.md)
5. ✅ Set USE_LOCAL_DATA=False
6. ✅ Run: `python app.py`
7. ✅ Visit: http://localhost:8050

---

**Si ou gen kesyon, pale! 🇭🇹**
