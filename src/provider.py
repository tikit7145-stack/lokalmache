"""
Data Provider - Sèvi sou Supabase oswa Local Data
"""

import pandas as pd
from config import SUPABASE_ENABLED, USE_LOCAL_DATA
from src.data import (
    generate_sales_data,
    generate_product_data,
    generate_customer_data
)

try:
    from src.database import get_supabase_manager
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class DataProvider:
    """Sèvi local data oswa Supabase"""
    
    def __init__(self, use_supabase: bool = None):
        """
        Inisyalize data provider
        
        Args:
            use_supabase: Si True, sèvi Supabase. Si False, local data.
                         Si None, otomatikal dapre config.
        """
        if use_supabase is None:
            self.use_supabase = SUPABASE_ENABLED and SUPABASE_AVAILABLE
        else:
            self.use_supabase = use_supabase and SUPABASE_AVAILABLE
        
        self.db = None
        if self.use_supabase:
            try:
                self.db = get_supabase_manager()
                print("✅ Konekte ak Supabase!")
            except Exception as e:
                print(f"⚠️  Erè koneksyon Supabase: {e}")
                print("🔄 Sèvi local data...")
                self.use_supabase = False
    
    def get_sales(self, limit: int = 500) -> pd.DataFrame:
        """Jwenn data vant"""
        if self.use_supabase:
            try:
                return self.db.get_sales(limit)
            except Exception as e:
                print(f"Erè pandan rechèch vant: {e}")
        return generate_sales_data()
    
    def get_products(self, limit: int = 100) -> pd.DataFrame:
        """Jwenn data pwodwi"""
        if self.use_supabase:
            try:
                return self.db.get_products(limit)
            except Exception as e:
                print(f"Erè pandan rechèch pwodwi: {e}")
        return generate_product_data()
    
    def get_customers(self, limit: int = 500) -> pd.DataFrame:
        """Jwenn data kliyan"""
        if self.use_supabase:
            try:
                return self.db.get_customers(limit)
            except Exception as e:
                print(f"Erè pandan rechèch kliyan: {e}")
        return generate_customer_data()
    
    def get_sales_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Jwenn vant nan yon ranj dat"""
        if self.use_supabase:
            try:
                return self.db.get_sales_by_date_range(start_date, end_date)
            except Exception as e:
                print(f"Erè: {e}")
        return generate_sales_data()
    
    def get_products_by_category(self, category: str) -> pd.DataFrame:
        """Jwenn pwodwi pa katègi"""
        if self.use_supabase:
            try:
                return self.db.get_products_by_category(category)
            except Exception as e:
                print(f"Erè: {e}")
        
        products = generate_product_data()
        if 'Katègi' in products.columns:
            return products[products['Katègi'] == category]
        return products
    
    def get_total_sales(self) -> float:
        """Kalkil total vant"""
        sales = self.get_sales()
        if 'Montan' in sales.columns:
            return float(sales['Montan'].sum())
        elif 'montan' in sales.columns:
            return float(sales['montan'].sum())
        return 0.0
    
    def get_customer_count(self) -> int:
        """Konnen kantite kliyan"""
        return len(self.get_customers())
    
    def get_top_products(self, limit: int = 5) -> pd.DataFrame:
        """Jwenn top pwodwi"""
        if self.use_supabase and self.db:
            try:
                return self.db.get_top_products(limit)
            except Exception as e:
                print(f"Erè: {e}")
        
        products = self.get_products()
        if 'Pris' in products.columns:
            return products.nlargest(limit, 'Pris')
        return products.head(limit)
    
    def get_sales_by_category(self) -> dict:
        """Vant pa katègi"""
        if self.use_supabase and self.db:
            try:
                return self.db.get_sales_by_category()
            except Exception as e:
                print(f"Erè: {e}")
        
        # Local calculation
        sales = self.get_sales()
        products = self.get_products()
        
        if sales.empty or products.empty:
            return {}
        
        try:
            merged = sales.merge(products, left_on='Pwodwi', right_on='Non')
            return merged.groupby('Katègi')['Montan'].sum().to_dict()
        except:
            return {}
    
    def create_sale(self, sale_data: dict) -> dict:
        """Kreye yon nouvo vant"""
        if self.use_supabase:
            try:
                return self.db.create_sale(sale_data)
            except Exception as e:
                print(f"Erè: {e}")
        return sale_data
    
    def create_customer(self, customer_data: dict) -> dict:
        """Kreye yon nouvo kliyan"""
        if self.use_supabase:
            try:
                return self.db.create_customer(customer_data)
            except Exception as e:
                print(f"Erè: {e}")
        return customer_data
    
    def create_product(self, product_data: dict) -> dict:
        """Kreye yon nouvo pwodwi"""
        if self.use_supabase:
            try:
                return self.db.create_product(product_data)
            except Exception as e:
                print(f"Erè: {e}")
        return product_data
    
    def get_source(self) -> str:
        """Jwenn sòs data"""
        return "Supabase" if self.use_supabase else "Local Data"


# Global instance
_provider = None


def get_data_provider(use_supabase: bool = None) -> DataProvider:
    """Jwenn data provider instance"""
    global _provider
    if _provider is None:
        _provider = DataProvider(use_supabase)
    return _provider
