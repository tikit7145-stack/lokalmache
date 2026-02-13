# 🗄️ SETUP SUPABASE - SENJIVIS KOMÈS 2026

## 📋 Table of Contents
1. Create Supabase Account
2. Create Database Tables
3. Configure Environment Variables
4. Connect Dashboard

---

## 1️⃣ CREATE SUPABASE ACCOUNT

### Step 1: Go to Supabase
1. Visit: https://supabase.com
2. Click **"Start your project"** or **Sign Up**
3. Create account with email/GitHub

### Step 2: Create New Project
1. Click **"New Project"**
2. Choose a name (example: `senjivis-komels`)
3. Create a strong password
4. Choose region (pick closest to you)
5. Click **"Create new project"**

### Step 3: Get Credentials
Once project is created:
1. Go to **Settings** → **API**
2. Copy:
   - **URL**: `https://xxxxx.supabase.co`
   - **Anon (public) Key**: `eyxx...`
3. Save these values safely!

---

## 2️⃣ CREATE DATABASE TABLES

### Table 1: VANT (Sales)

Go to **SQL Editor** and run:

```sql
CREATE TABLE vant (
  id BIGSERIAL PRIMARY KEY,
  kliyèn VARCHAR(255),
  pwodwi VARCHAR(255),
  kantite INTEGER,
  montan DECIMAL(10, 2),
  dat DATE DEFAULT CURRENT_DATE,
  estati VARCHAR(50) DEFAULT 'Anteri',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for better performance
CREATE INDEX vant_dat_idx ON vant(dat);
CREATE INDEX vant_kliyèn_idx ON vant(kliyèn);
```

### Table 2: PWODWI (Products)

```sql
CREATE TABLE pwodwi (
  id BIGSERIAL PRIMARY KEY,
  non VARCHAR(255) NOT NULL,
  sku VARCHAR(100) UNIQUE,
  pri DECIMAL(10, 2),
  stok INTEGER DEFAULT 0,
  kategori VARCHAR(100),
  deskripsyon TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX pwodwi_kategori_idx ON pwodwi(kategori);
CREATE INDEX pwodwi_sku_idx ON pwodwi(sku);
```

### Table 3: KLIYAN (Customers)

```sql
CREATE TABLE kliyan (
  id BIGSERIAL PRIMARY KEY,
  non VARCHAR(255) NOT NULL,
  imèl VARCHAR(255) UNIQUE,
  telefòn VARCHAR(20),
  vil VARCHAR(100),
  adres TEXT,
  dat_jinskripsyon DATE DEFAULT CURRENT_DATE,
  total_achte DECIMAL(10, 2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX kliyan_vil_idx ON kliyan(vil);
CREATE INDEX kliyan_imèl_idx ON kliyan(imèl);
```

### Table 4: KOMAND (Orders)

```sql
CREATE TABLE komand (
  id BIGSERIAL PRIMARY KEY,
  kliyan_id BIGINT REFERENCES kliyan(id),
  nimewo_komand VARCHAR(50) UNIQUE,
  montan_total DECIMAL(10, 2),
  estati VARCHAR(50) DEFAULT 'Tann',
  dat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dat_modifye TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX komand_estati_idx ON komand(estati);
CREATE INDEX komand_dat_idx ON komand(dat);
```

### Import Sample Data (Optional)

After creating tables, you can insert sample data:

```sql
INSERT INTO pwodwi (non, sku, pri, stok, kategori) VALUES
  ('Laptop Pro', 'LAP-001', 1200, 45, 'Teknoloji'),
  ('T-Shirt Premium', 'TSH-001', 35, 200, 'Vètman'),
  ('Sèndèj Modèn', 'FUR-001', 450, 30, 'Lakay'),
  ('Fri Elektrik', 'APP-001', 320, 15, 'Aparèy'),
  ('Smartphone 5G', 'PHN-001', 800, 60, 'Teknoloji');

INSERT INTO kliyan (non, imèl, telefòn, vil) VALUES
  ('Jean Paul', 'jean@example.ht', '+509 1234567', 'Port-au-Prince'),
  ('Marie Joseph', 'marie@example.ht', '+509 2345678', 'Cap-Haïtien'),
  ('Pierre Dubois', 'pierre@example.ht', '+509 3456789', 'Gonaïves');
```

---

## 3️⃣ CONFIGURE ENVIRONMENT VARIABLES

### Step 1: Copy Environment File
```bash
cd ~/ecommerce-dashboard
cp .env.example .env
```

### Step 2: Edit `.env` File
```bash
nano .env
```

Or open in VS Code and fill in:

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
USE_LOCAL_DATA=False
```

Replace:
- `SUPABASE_URL` with your actual URL
- `SUPABASE_KEY` with your anon key
- Set `USE_LOCAL_DATA=False` to use Supabase

### Step 3: Save File
Press `Ctrl + X` then `Y` then `Enter` (in nano)

---

## 4️⃣ CONNECT DASHBOARD

### Step 1: Install Dependencies
```bash
cd ~/ecommerce-dashboard
pip install -r requirements.txt
```

This will install:
- supabase==2.0.0
- python-dotenv==1.0.0

### Step 2: Update app.py (Already Done!)
The dashboard now supports both:
- ✅ **Supabase** (Real database)
- ✅ **Local Data** (Demo mode)

### Step 3: Run Dashboard
```bash
python app.py
```

You should see:
```
🚀 Conecte ak Supabase!
📊 Senjivis Komès 2026 ap demaré...
📊 Vizite: http://localhost:8050
```

---

## 🧪 TEST THE CONNECTION

### Check Supabase Connection
```python
from src.database import get_supabase_manager

db = get_supabase_manager()
customers = db.get_customers()
print(f"Nombre kliyan: {len(customers)}")
```

### Insert Sample Data
```python
from src.database import get_supabase_manager

db = get_supabase_manager()

# Add a customer
new_customer = db.create_customer({
    'non': 'Nèy Kliyan',
    'imèl': 'kliyè@example.ht',
    'telefòn': '+509 1234567',
    'vil': 'Port-au-Prince'
})

print(f"Kliyan kreye: {new_customer}")
```

---

## 📊 DATABASE SCHEMA OVERVIEW

```
┌─────────────────────────────────────────────────┐
│                   SENJIVIS KOMÈS                │
├─────────────────────────────────────────────────┤
│                                                 │
│  📦 PWODWI (Products)                          │
│  ├─ id (PRIMARY KEY)                           │
│  ├─ non (Name)                                 │
│  ├─ pri (Price)                                │
│  ├─ stok (Stock)                               │
│  └─ kategori (Category)                        │
│                                                 │
│  👥 KLIYAN (Customers)                         │
│  ├─ id (PRIMARY KEY)                           │
│  ├─ non (Name)                                 │
│  ├─ imèl (Email)                               │
│  ├─ vil (City)                                 │
│  └─ total_achte (Total Purchases)              │
│                                                 │
│  💰 VANT (Sales)                               │
│  ├─ id (PRIMARY KEY)                           │
│  ├─ kliyèn (Customer)                          │
│  ├─ pwodwi (Product)                           │
│  ├─ montan (Amount)                            │
│  ├─ dat (Date)                                 │
│  └─ estati (Status)                            │
│                                                 │
│  📋 KOMAND (Orders)                            │
│  ├─ id (PRIMARY KEY)                           │
│  ├─ kliyan_id (FK to KLIYAN)                   │
│  ├─ montan_total (Total Amount)                │
│  ├─ estati (Status)                            │
│  └─ dat (Date)                                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔧 AVAILABLE DATABASE METHODS

### Sales (Vant)
```python
db.get_sales()                          # Get all sales
db.get_sales_by_date_range()           # Sales in date range
db.create_sale(data)                   # Add new sale
db.update_sale(id, data)               # Update sale
db.delete_sale(id)                     # Delete sale
```

### Products (Pwodwi)
```python
db.get_products()                      # Get all products
db.get_product_by_id(id)              # Get one product
db.get_products_by_category()          # Filter by category
db.create_product(data)                # Add new product
db.update_product(id, data)            # Update product
```

### Customers (Kliyan)
```python
db.get_customers()                     # Get all customers
db.get_customer_by_id(id)             # Get one customer
db.create_customer(data)               # Add new customer
db.update_customer(id, data)           # Update customer
```

### Orders (Komand)
```python
db.get_orders()                        # Get recent orders
db.create_order(data)                  # Create new order
db.update_order_status(id, status)     # Update order status
```

### Analytics (Analiz)
```python
db.get_total_sales()                   # Total sales amount
db.get_customer_count()                # Number of customers
db.get_top_products()                  # Top products
db.get_sales_by_category()             # Sales per category
db.get_sales_by_date()                 # Sales per day
```

---

## 🔐 SECURITY TIPS

1. **Never commit .env file**
   - Already in .gitignore ✅

2. **Use Row Level Security (RLS)**
   - Go to Supabase dashboard
   - Enable RLS on tables
   - Set appropriate policies

3. **Restrict API Key**
   - Use "Anon (public)" key in frontend
   - Use "Service Role" key only on backend (protected)

4. **Set Up Backups**
   - Supabase auto-backs up
   - Check Settings → Database → Backups

---

## 🆘 TROUBLESHOOTING

| Pwoblèm | Solisyon |
|---------|----------|
| "Supabase URL required" | Check .env file has SUPABASE_URL |
| "Invalid API key" | Verify SUPABASE_KEY is correct |
| "Connection refused" | Check internet connection |
| "Table does not exist" | Run SQL to create tables |
| "Row-level security" | Disable RLS temporarily or set policies |

---

## 📞 NEXT STEPS

1. ✅ Create Supabase account
2. ✅ Create database tables
3. ✅ Configure .env file
4. ✅ Run `pip install -r requirements.txt`
5. ✅ Start dashboard: `python app.py`
6. ✅ Visit: http://localhost:8050

---

## 📚 RESOURCES

- Supabase Docs: https://supabase.com/docs
- Supabase SQL Editor: https://supabase.com/dashboard
- Python Supabase Client: https://github.com/supabase-community/supabase-py

---

**Happy coding! 🚀 Senjivis Komès 2026**

🇭🇹 Fè pa Ayisyen, Pou Ayisyen 🇭🇹
