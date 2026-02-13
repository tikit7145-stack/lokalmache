# 🔗 SUPABASE INTEGRATION GUIDE

## 📌 Quick Summary

Your dashboard now supports **Supabase** for real database integration! 

### Two Modes:
1. **Local Mode** (Demo): Use generated sample data
2. **Supabase Mode** (Production): Connect to real database

---

## 🚀 QUICK START WITH SUPABASE

### 1️⃣ Install Dependencies
```bash
cd ~/ecommerce-dashboard
pip install -r requirements.txt
```

### 2️⃣ Get Supabase Credentials
- Visit: https://supabase.com/dashboard
- Create account/project
- Go to Settings → API
- Copy **URL** and **Anon Key**

### 3️⃣ Configure Environment
```bash
# Copy example
cp .env.example .env

# Edit with your credentials
nano .env
```

Add:
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyxx...
USE_LOCAL_DATA=False
```

### 4️⃣ Create Database Tables
Go to Supabase SQL Editor and run the SQL scripts from `SUPABASE_SETUP.md`

Tables needed:
- `vant` (Sales)
- `pwodwi` (Products)
- `kliyan` (Customers)
- `komand` (Orders)

### 5️⃣ Start Dashboard
```bash
python app.py
```

Should see:
```
✅ Konekte ak Supabase!
📊 Senjivis Komès 2026 ap demaré...
📊 Vizite: http://localhost:8050
```

---

## 📂 NEW FILES ADDED

```
ecommerce-dashboard/
├── .env                      ← Your private config (CREATE THIS)
├── .env.example             ← Template for .env
├── src/database.py          ← Supabase database functions
├── src/provider.py          ← Smart data provider (local/remote)
├── examples.py              ← Usage examples
├── SUPABASE_SETUP.md       ← Full Supabase guide
└── SUPABASE_INTEGRATION.md ← This file
```

---

## 🔀 SWITCH BETWEEN LOCAL & SUPABASE

### Option A: Edit `.env`
```bash
# Use Supabase
USE_LOCAL_DATA=False

# Use Local Data
USE_LOCAL_DATA=True
```

### Option B: In Python Code
```python
from src.provider import get_data_provider

# Force local data
provider = get_data_provider(use_supabase=False)

# Force Supabase
provider = get_data_provider(use_supabase=True)

# Auto (based on .env)
provider = get_data_provider()
```

---

## 💻 USAGE EXAMPLES

### Get Sales Data
```python
from src.provider import get_data_provider

provider = get_data_provider()
sales = provider.get_sales()
print(f"Total: ${provider.get_total_sales():,.2f}")
```

### Get Products by Category
```python
products = provider.get_products_by_category('Teknoloji')
print(products)
```

### Create New Customer
```python
customer = provider.create_customer({
    'non': 'Jean Paul',
    'imèl': 'jean@example.ht',
    'telefòn': '+509 1234567',
    'vil': 'Port-au-Prince'
})
```

### Direct Database Access
```python
from src.database import get_supabase_manager

db = get_supabase_manager()

# Get analytics
total = db.get_total_sales()
count = db.get_customer_count()
top = db.get_top_products(5)

# Get by date
sales = db.get_sales_by_date_range('2026-02-01', '2026-02-12')

# Get by category
products = db.get_products_by_category('Vètman')
```

---

## 📊 DATABASE SCHEMA

### VANT (Sales Table)
```sql
id              BIGSERIAL PRIMARY KEY
kliyèn          VARCHAR(255) - Customer name
pwodwi          VARCHAR(255) - Product name
kantite         INTEGER - Quantity
montan          DECIMAL(10,2) - Amount
dat             DATE - Date
estati          VARCHAR(50) - Status
created_at      TIMESTAMP - Creation time
```

### PWODWI (Products Table)
```sql
id              BIGSERIAL PRIMARY KEY
non             VARCHAR(255) - Product name
sku             VARCHAR(100) - Stock keeping unit
pri             DECIMAL(10,2) - Price
stok            INTEGER - Stock quantity
kategori        VARCHAR(100) - Category
deskripsyon     TEXT - Description
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### KLIYAN (Customers Table)
```sql
id              BIGSERIAL PRIMARY KEY
non             VARCHAR(255) - Customer name
imèl            VARCHAR(255) - Email
telefòn         VARCHAR(20) - Phone
vil             VARCHAR(100) - City
adres           TEXT - Address
dat_jinskripsyon DATE - Registration date
total_achte     DECIMAL(10,2) - Total purchases
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### KOMAND (Orders Table)
```sql
id              BIGSERIAL PRIMARY KEY
kliyan_id       BIGINT - Customer ID (Foreign Key)
nimewo_komand   VARCHAR(50) - Order number
montan_total    DECIMAL(10,2) - Total amount
estati          VARCHAR(50) - Status
dat             TIMESTAMP - Date
dat_modifye     TIMESTAMP - Modified date
created_at      TIMESTAMP
```

---

## 🛡️ SECURITY

### Environment Variables
- ✅ `.env` is in `.gitignore` (won't be committed)
- ✅ Use "Anon" key for frontend (limited access)
- ✅ Never commit secrets to Git

### Supabase Row Level Security
1. Go to Supabase dashboard
2. All tables → RLS → Enable
3. Set policies to restrict access

Example Policy:
```sql
CREATE POLICY "Public read access" ON vant
  FOR SELECT USING (true);

CREATE POLICY "Authenticated insert" ON vant
  FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

---

## 🐛 TROUBLESHOOTING

### Error: "Supabase URL required"
**Solution:**
```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env
```

### Error: "Invalid API key"
**Solution:**
1. Go to Supabase dashboard
2. Settings → API
3. Copy the correct "Anon" key (not "Service Role")
4. Paste in `.env`

### Error: "Table does not exist"
**Solution:**
1. Open Supabase SQL Editor
2. Run the SQL from `SUPABASE_SETUP.md`
3. Create all tables: vant, pwodwi, kliyan, komand

### Dashboard shows "Local Data" instead of Supabase
**Solution:**
1. Check `USE_LOCAL_DATA=False` in `.env`
2. Check `SUPABASE_URL` and `SUPABASE_KEY` are filled
3. Restart dashboard: `python app.py`

### Slow queries / timeout
**Solution:**
1. Add database indexes (in SUPABASE_SETUP.md they're included)
2. Reduce `limit` parameter
3. Use date ranges instead of fetching all data

---

## 📈 PERFORMANCE TIPS

1. **Use Indexes**
   ```sql
   CREATE INDEX vant_dat_idx ON vant(dat);
   CREATE INDEX kliyan_vil_idx ON kliyan(vil);
   ```

2. **Paginate Results**
   ```python
   # Fetch first 100
   sales = db.get_sales(limit=100)
   ```

3. **Use Date Ranges**
   ```python
   # Better than get_sales()
   sales = db.get_sales_by_date_range('2026-02-01', '2026-02-12')
   ```

4. **Cache Results**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def get_cached_products():
       return provider.get_products()
   ```

---

## 🔄 UPDATE DASHBOARD DATA

### Refresh Sales Table
```python
from src.provider import get_data_provider

provider = get_data_provider()
sales = provider.get_sales()
# Use in dashboard
```

### Real-time Updates (Future)
```python
# Supabase supports realtime
db.client.realtime.on(
    'postgres_changes',
    {'event': '*', 'schema': 'public', 'table': 'vant'},
    on_change
).subscribe()
```

---

## 📚 COMPLETE WORKFLOW

### Development (Local Data)
```bash
# .env
USE_LOCAL_DATA=True
```
- Fast for testing
- No external dependencies
- Perfect for demo

### Staging (Supabase)
```bash
# .env
USE_LOCAL_DATA=False
SUPABASE_URL=https://staging.supabase.co
SUPABASE_KEY=staging_key
```
- Test with real data
- Same as production

### Production (Supabase)
```bash
# .env
USE_LOCAL_DATA=False
SUPABASE_URL=https://prod.supabase.co
SUPABASE_KEY=prod_key
```
- Live data
- Backups enabled
- RLS policies active

---

## 🧪 TEST YOUR CONNECTION

### Python Script
```python
from src.database import get_supabase_manager

db = get_supabase_manager()

# Test connection
customers = db.get_customers()
print(f"✅ Connected! {len(customers)} customers found")
```

### Dashboard
```bash
python app.py
# Look for message:
# ✅ Konekte ak Supabase!
```

---

## 📞 SUPPORT

| Issue | File to Check |
|-------|--------------|
| Connection error | `.env` file |
| Missing tables | Supabase SQL Editor |
| Slow queries | Database indexes |
| Wrong data | Table names in config.py |

---

## 🎯 NEXT STEPS

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Create `.env` file with Supabase credentials
3. ✅ Create database tables (SQL from SUPABASE_SETUP.md)
4. ✅ Run: `python app.py`
5. ✅ Test: http://localhost:8050

---

## 📖 DOCUMENTATION FILES

- `SUPABASE_SETUP.md` - Detailed Supabase setup
- `SUPABASE_INTEGRATION.md` - This file
- `README.md` - General overview
- `QUICKSTART.md` - Quick start guide
- `src/database.py` - Database class (view for available methods)
- `src/provider.py` - Data provider (switch local/remote)
- `examples.py` - Working examples

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready with Supabase Support

🇭🇹 **Senjivis Komès 2026** 🇭🇹
