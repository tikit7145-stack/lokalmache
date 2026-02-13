"""
Example: Itilize Dashboard Avèk Supabase
"""

from src.provider import get_data_provider
import pandas as pd

# ============ EXEMPLE 1: OTOMATIKAL DAPRE CONFIG ============

print("\n📊 EXEMPLE 1: Otomatikal Dapre Config")
print("=" * 50)

# Okréte yo va sèvi Supabase si SUPABASE_ENABLED=True nan config
provider = get_data_provider()

print(f"Sòs Data: {provider.get_source()}")
print(f"Aktif: {'Supabase' if provider.use_supabase else 'Local Data'}")

# ============ EXEMPLE 2: FÒSE LOKAL DATA ============

print("\n📊 EXEMPLE 2: Fòse Local Data")
print("=" * 50)

provider_local = get_data_provider(use_supabase=False)
print(f"Sòs: {provider_local.get_source()}")

# ============ EXEMPLE 3: FÒSE SUPABASE ============

print("\n📊 EXEMPLE 3: Fòse Supabase")
print("=" * 50)

provider_remote = get_data_provider(use_supabase=True)
print(f"Sòs: {provider_remote.get_source()}")

# ============ EXEMPLE 4: RECHÈCH DATA ============

print("\n📊 EXEMPLE 4: Rechèch Data")
print("=" * 50)

provider = get_data_provider()

# Kliyan
customers = provider.get_customers()
print(f"\n👥 Kantite Kliyan: {len(customers)}")
if not customers.empty:
    print(customers.head())

# Pwodwi
products = provider.get_products()
print(f"\n📦 Kantite Pwodwi: {len(products)}")
if not products.empty:
    print(products.head())

# Vant
sales = provider.get_sales()
print(f"\n💰 Kantite Vant: {len(sales)}")
print(f"Total Vant: ${provider.get_total_sales():,.2f}")

# ============ EXEMPLE 5: KRIYÈ DONE ============

print("\n📊 EXEMPLE 5: Kriyè Done")
print("=" * 50)

provider = get_data_provider()

# Kreye kliyan
new_customer = {
    'non': 'Nèy Kliyan',
    'imèl': 'kliyè@example.ht',
    'telefòn': '+509 1234567',
    'vil': 'Port-au-Prince'
}
result = provider.create_customer(new_customer)
print(f"✅ Kliyan Kreye: {result}")

# Kreye pwodwi
new_product = {
    'Non': 'Nouvo Pwodwi',
    'SKU': 'NEW-001',
    'Pris': 99.99,
    'Stok': 50,
    'Katègi': 'Teknoloji'
}
result = provider.create_product(new_product)
print(f"✅ Pwodwi Kreye: {result}")

# Kreye vant
new_sale = {
    'Kliyèn': 'Nèy Kliyan',
    'Pwodwi': 'Nouvo Pwodwi',
    'Kantite': 2,
    'Montan': 199.98
}
result = provider.create_sale(new_sale)
print(f"✅ Vant Kreye: {result}")

# ============ EXEMPLE 6: ANALYSÉ DATA ============

print("\n📊 EXEMPLE 6: Analysé Data")
print("=" * 50)

provider = get_data_provider()

print(f"\n💰 Total Vant: ${provider.get_total_sales():,.2f}")
print(f"👥 Nimewo Kliyan: {provider.get_customer_count()}")

top_products = provider.get_top_products(5)
print(f"\n🏆 Top 5 Pwodwi:")
print(top_products)

# ============ EXEMPLE 7: NAVIGUÉ SUPABASE DIRÈK (Avansé) ============

print("\n📊 EXEMPLE 7: Dirèk Supabase (Avansé)")
print("=" * 50)

try:
    from src.database import get_supabase_manager
    
    db = get_supabase_manager()
    
    # Konnen kantite vant
    total_sales = db.get_total_sales()
    print(f"Total Vant: ${total_sales:,.2f}")
    
    # Vant pa jou
    sales_by_date = db.get_sales_by_date()
    print(f"\nVant Pa Jou:")
    for date, amount in list(sales_by_date.items())[:5]:
        print(f"  {date}: ${amount:,.2f}")
    
    # Vant pa katègi
    sales_by_category = db.get_sales_by_category()
    print(f"\nVant Pa Katègi:")
    for category, amount in sales_by_category.items():
        print(f"  {category}: ${amount:,.2f}")
    
except Exception as e:
    print(f"⚠️  Supabase pa disponib: {e}")

print("\n✅ Egzanp Finye!")
