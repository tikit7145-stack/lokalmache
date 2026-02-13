"""
Koneksyon Supabase pou Senjivis Komès 2026
Database integration ak real-time data
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()


class SupabaseManager:
    """Klas pou jere koneksyon Supabase"""
    
    def __init__(self, url: str = None, key: str = None):
        """Inisyalize Supabase client"""
        self.url = url or os.getenv('SUPABASE_URL')
        self.key = key or os.getenv('SUPABASE_KEY')
        
        if not self.url or not self.key:
            raise ValueError(
                "Supabase URL ak Key obligatwa. "
                "Mete SUPABASE_URL ak SUPABASE_KEY nan .env"
            )
        
        self.client: Client = create_client(self.url, self.key)
    
    # ============ ORDERS / KOMAND (Sèvi Direk) ============
    
    def get_sales(self, limit: int = 500) -> pd.DataFrame:
        """Rechèch tout komand (orders)"""
        try:
            response = self.client.table('orders').select('*').limit(limit).execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Erè pandan rechèch komand: {e}")
            return pd.DataFrame()
    
    def get_sales_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Rechèch komand nan yon ranj dat"""
        try:
            response = self.client.table('orders').select('*').gte(
                'created_at', start_date
            ).lte('created_at', end_date).execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Erè pandan rechèch komand pa ranj: {e}")
            return pd.DataFrame()
    
    def create_sale(self, sale_data: Dict) -> Optional[Dict]:
        """Kreye yon nouvo komand"""
        try:
            response = self.client.table('orders').insert(sale_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erè pandan kreyasyon komand: {e}")
            return None
    
    def update_sale(self, sale_id: int, sale_data: Dict) -> Optional[Dict]:
        """Modifye yon komand"""
        try:
            response = self.client.table('orders').update(
                sale_data
            ).eq('id', sale_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erè pandan modifikasyon komand: {e}")
            return None
    
    def delete_sale(self, sale_id: int) -> bool:
        """Efase yon komand"""
        try:
            self.client.table('orders').delete().eq('id', sale_id).execute()
            return True
        except Exception as e:
            print(f"Erè pandan efasman komand: {e}")
            return False
    
    # ============ PRODUCTS / PWODWI (Sèvi Direk) ============
    
    def get_products(self, limit: int = 100) -> pd.DataFrame:
        """Rechèch tout pwodwi"""
        try:
            response = self.client.table('products').select('*').limit(limit).execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Erè pandan rechèch pwodwi: {e}")
            return pd.DataFrame()
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Rechèch yon pwodwi dapre ID"""
        try:
            response = self.client.table('products').select('*').eq(
                'id', product_id
            ).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erè pandan rechèch pwodwi: {e}")
            return None
    
    def get_products_by_category(self, category: str) -> pd.DataFrame:
        """Rechèch pwodwi pa katègi"""
        try:
            response = self.client.table('products').select('*').eq(
                'category', category
            ).execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Erè pandan rechèch pwodwi pa katègi: {e}")
            return pd.DataFrame()
    
    def create_product(self, product_data: Dict) -> Optional[Dict]:
        """Kreye yon nouvo pwodwi"""
        try:
            response = self.client.table('products').insert(product_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erè pandan kreyasyon pwodwi: {e}")
            return None
    
    def update_product(self, product_id: int, product_data: Dict) -> Optional[Dict]:
        """Modifye yon pwodwi"""
        try:
            response = self.client.table('products').update(
                product_data
            ).eq('id', product_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erè pandan modifikasyon pwodwi: {e}")
            return None
    
    # ============ CUSTOMERS / KLIYAN (Extract from Orders) ============
    
    def get_customers(self, limit: int = 500) -> pd.DataFrame:
        """Rechèch kliyan (extract from orders)"""
        try:
            # Get unique customers from orders table
            orders = self.get_sales(limit * 10)
            if orders.empty:
                return pd.DataFrame()
            
            # Extract unique customers from orders
            customer_cols = ['user_id', 'user_name', 'user_email', 'user_phone', 'user_address']
            available_cols = [col for col in customer_cols if col in orders.columns]
            
            if available_cols:
                customers = orders[available_cols].drop_duplicates('user_id').head(limit)
                return customers
            return orders.head(limit)
        except Exception as e:
            print(f"Erè pandan rechèch kliyan: {e}")
            return pd.DataFrame()
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Dict]:
        """Rechèch yon kliyan dapre ID"""
        try:
            sales = self.get_sales()
            if 'user_id' in sales.columns:
                result = sales[sales['user_id'] == customer_id]
                return result.iloc[0].to_dict() if not result.empty else None
            return None
        except Exception as e:
            print(f"Erè pandan rechèch kliyan: {e}")
            return None
    
    def create_customer(self, customer_data: Dict) -> Optional[Dict]:
        """Kreye yon nouvo kliyan (insert as order)"""
        try:
            # Customers don't have a dedicated table, created through orders
            return customer_data
        except Exception as e:
            print(f"Erè pandan kreyasyon kliyan: {e}")
            return None
    
    def update_customer(self, customer_id: int, customer_data: Dict) -> Optional[Dict]:
        """Modifye yon kliyan (update order user data)"""
        try:
            response = self.client.table('orders').update(
                customer_data
            ).eq('user_id', customer_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erè pandan modifikasyon kliyan: {e}")
            return None
    
    # ============ ANALYTICS / ANALIZ ============
    
    def get_total_sales(self) -> float:
        """Kalkil total vant"""
        try:
            sales = self.get_sales()
            # Try different column names
            if 'total_amount' in sales.columns:
                return float(sales['total_amount'].sum())
            elif 'Montan' in sales.columns:
                return float(sales['Montan'].sum())
            elif 'montan' in sales.columns:
                return float(sales['montan'].sum())
            return float(sales.iloc[:, -1].sum()) if not sales.empty else 0.0
        except Exception as e:
            print(f"Erè pandan kalkil total vant: {e}")
            return 0.0
    
    def get_customer_count(self) -> int:
        """Konnen kantite kliyan"""
        try:
            sales = self.get_sales()
            if 'user_id' in sales.columns:
                return len(sales['user_id'].unique())
            return len(sales)
        except Exception as e:
            print(f"Erè pandan konte kliyan: {e}")
            return 0
    
    def get_top_products(self, limit: int = 5) -> pd.DataFrame:
        """Jwenn top n pwodwi pa pris oswa vant"""
        try:
            products = self.get_products()
            if not products.empty:
                if 'price' in products.columns:
                    return products.nlargest(limit, 'price')
                elif 'Pris' in products.columns:
                    return products.nlargest(limit, 'Pris')
            return products.head(limit)
        except Exception as e:
            print(f"Erè pandan rechèch top pwodwi: {e}")
            return pd.DataFrame()
    
    def get_sales_by_category(self) -> Dict:
        """Jwenn vant pa katègi"""
        try:
            products = self.get_products()
            if products.empty or 'category' not in products.columns:
                return {}
            return products.groupby('category').size().to_dict()
        except Exception as e:
            print(f"Erè pandan kalkil vant pa katègi: {e}")
            return {}
    
    def get_sales_by_date(self) -> Dict:
        """Jwenn vant pa jou"""
        try:
            sales = self.get_sales()
            if sales.empty or 'created_at' not in sales.columns:
                return {}
            sales['created_at'] = pd.to_datetime(sales['created_at'])
            result = sales.groupby(sales['created_at'].dt.date).size().to_dict()
            return result
        except Exception as e:
            print(f"Erè pandan kalkil vant pa jou: {e}")
            return {}
    
    # ============ ORDERS / KÒMAND ============
    
    def get_orders(self, limit: int = 100) -> pd.DataFrame:
        """Rechèch kòmand resan"""
        try:
            response = self.client.table('orders').select('*').limit(
                limit
            ).order('created_at', desc=True).execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Erè pandan rechèch kòmand: {e}")
            return pd.DataFrame()
    
    def create_order(self, order_data: Dict) -> Optional[Dict]:
        """Kreye yon nouvo kòmand"""
        try:
            response = self.client.table('orders').insert(order_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erè pandan kreyasyon kòmand: {e}")
            return None
    
    def update_order_status(self, order_id: int, status: str) -> Optional[Dict]:
        """Modifye estati kòmand"""
        try:
            response = self.client.table('orders').update({
                'status': status,
            }).eq('id', order_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erè pandan modifikasyon estati kòmand: {e}")
            return None


# Global instance
_supabase_manager: Optional[SupabaseManager] = None


def get_supabase_manager() -> SupabaseManager:
    """Jwenn global Supabase manager instance"""
    global _supabase_manager
    if _supabase_manager is None:
        _supabase_manager = SupabaseManager()
    return _supabase_manager


def initialize_supabase(url: str = None, key: str = None) -> SupabaseManager:
    """Inisyalize Supabase"""
    global _supabase_manager
    _supabase_manager = SupabaseManager(url, key)
    return _supabase_manager
