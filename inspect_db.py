"""
Gade strukti Supabase Database
Check existing tables + schema
"""

import os
from dotenv import load_dotenv

# Load .env if exists
load_dotenv()

# Test connection and inspect database
def inspect_database():
    """Gade ki tab ak data ki genyen nan Supabase"""
    
    try:
        from supabase import create_client
        
        # Use the key provided
        SUPABASE_URL = "https://rqurlyyslbrpdjnabrts.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJxdXJseXlzbGJycGRqbmFicnRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NTc4ODMsImV4cCI6MjA4MzUzMzg4M30.Jko5sA_Bv281uuPkFpwiZBKHooRBljoEO8x49Rwf4CE"
        
        print("🔗 Konektasyon...")
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ KONEKTE AK SUPABASE!\n")
        
        # Try to get information about existing tables
        print("=" * 60)
        print("📊 EGZAMEN STRUKTI DATABASE")
        print("=" * 60)
        
        # List of tables to check
        tables = ['vant', 'pwodwi', 'kliyan', 'komand', 'users', 'products', 'customers', 'orders', 'sales']
        
        found_tables = []
        
        for table_name in tables:
            try:
                print(f"\n🔍 Verifye table: '{table_name}'...", end=" ")
                response = client.table(table_name).select('*').limit(1).execute()
                
                if response.data or response:
                    print(f"✅ GENYEN!")
                    found_tables.append(table_name)
                    
                    # Get count
                    count_response = client.table(table_name).select('*', count='exact').execute()
                    record_count = len(count_response.data) if count_response.data else 0
                    print(f"   └─ Records: {record_count}")
                    
                    # Show columns
                    if count_response.data:
                        first_record = count_response.data[0]
                        columns = list(first_record.keys())
                        print(f"   └─ Columns: {columns}")
                else:
                    print("❌ PA GENYEN")
                    
            except Exception as e:
                if "not found" in str(e).lower() or "does not exist" in str(e).lower():
                    print("❌ PA GENYEN")
                else:
                    print(f"⚠️  {str(e)[:50]}")
        
        print("\n" + "=" * 60)
        print("📋 REZIME")
        print("=" * 60)
        
        if found_tables:
            print(f"\n✅ Tables ki genyen: {len(found_tables)}")
            for i, table in enumerate(found_tables, 1):
                print(f"   {i}. {table}")
            
            print("\n💡 REKOMANTASYON:")
            print("   • Ou ka direkteman sèvi tables sa yo")
            print("   • Pa bezwen kriye tab ankò")
            print("   • Pèp antre done dirèk")
        else:
            print("\n❌ PA gen tab ankò")
            print("\n💡 REKOMANTASYON:")
            print("   • Gade SUPABASE_SETUP.md")
            print("   • Kopy SQL la")
            print("   • Kour nan Supabase SQL Editor")
            print("   • Kriye 4 tables: vant, pwodwi, kliyan, komand")
        
        print("\n" + "=" * 60)
        
        # Try to get detailed schema info
        print("\n🔧 DETAY STRUKTURÈL (Advanced):")
        print("=" * 60)
        
        try:
            # Get schema from information_schema
            schema_response = client.table('information_schema.tables').select('*').execute()
            print("\n✅ Database accessible via information_schema")
        except:
            print("\n⚠️  Information_schema not accessible (normal for Anon key)")
        
        return found_tables
        
    except Exception as e:
        print(f"❌ ERÈ KONEKSYON: {e}")
        print("\n💡 SOLISYON:")
        print("   1. Verifye SUPABASE_URL correct")
        print("   2. Verifye SUPABASE_KEY correct")
        print("   3. Verifye internet connection")
        print("   4. Check Supabase project active")
        return []

if __name__ == "__main__":
    inspect_database()
