"""
Order Status Management System
Trete Kòmand - Pending, Confirmed, In Transit, Delivered
"""

import pandas as pd
from datetime import datetime
from src.database import get_supabase_manager

db = get_supabase_manager()

class OrderStatusManager:
    """Jesyone estati kòmand yo"""
    
    # Status definitions (Haitian Creole)
    STATUSES = {
        'pending': {'label': '⏳ Atant', 'color': '#FFA500', 'description': 'Atant konfmasyon'},
        'confirmed': {'label': '✅ Konfime', 'color': '#4CAF50', 'description': 'Kòmand konfime'},
        'in_transit': {'label': '🚚 Nan Wout', 'color': '#2196F3', 'description': 'Se pale vini'},
        'delivered': {'label': '📦 Rive', 'color': '#673AB7', 'description': 'Kòmand rive'},
    }
    
    @staticmethod
    def get_orders_by_status(status):
        """Jwenn kòmand dapre estati yo"""
        try:
            orders = db.get_orders(limit=500)
            if orders.empty:
                return pd.DataFrame()
            
            # Filter by status
            filtered = orders[orders['status'].str.lower() == status.lower()]
            return filtered
        except Exception as e:
            print(f"Erè nan rekiperasyon kòmand: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def get_status_counts():
        """Konte kòmand pou chak estati"""
        try:
            orders = db.get_orders(limit=500)
            if orders.empty:
                return {}
            
            # Count by status
            status_counts = {}
            for status_key in OrderStatusManager.STATUSES.keys():
                count = len(orders[orders['status'].str.lower() == status_key.lower()])
                status_counts[status_key] = count
            
            return status_counts
        except Exception as e:
            print(f"Erè: {e}")
            return {}
    
    @staticmethod
    def update_order_status(order_id, new_status):
        """Mete ajou estati yon kòmand"""
        try:
            if new_status not in OrderStatusManager.STATUSES:
                return False, f"Estati '{new_status}' pa valid"
            
            # Update order status in database
            result = db.update_order_status(order_id, new_status)
            return True, f"Estati mete ajou a '{new_status}'"
        except Exception as e:
            return False, f"Erè: {e}"
    
    @staticmethod
    def get_status_summary():
        """Jwenn rezime estati kòmand"""
        counts = OrderStatusManager.get_status_counts()
        summary = {}
        
        for status_key, count in counts.items():
            status_info = OrderStatusManager.STATUSES[status_key]
            summary[status_key] = {
                'status': status_key,
                'label': status_info['label'],
                'count': count,
                'color': status_info['color'],
                'description': status_info['description']
            }
        
        return summary
    
    @staticmethod
    def get_order_timeline(order_id):
        """Jwenn timeline youn kòmand"""
        try:
            orders = db.get_orders(limit=500)
            order = orders[orders['id'] == order_id]
            
            if order.empty:
                return None
            
            order_data = order.iloc[0]
            return {
                'id': order_data.get('id'),
                'user_name': order_data.get('user_name'),
                'status': order_data.get('status'),
                'total_amount': order_data.get('total_amount'),
                'created_at': order_data.get('created_at'),
                'payment_method': order_data.get('payment_method'),
            }
        except Exception as e:
            print(f"Erè: {e}")
            return None


    @staticmethod
    def get_order_status_chart_data():
        """Prepare done pou chart estati kòmand"""
        summary = OrderStatusManager.get_status_summary()
        
        labels = [item['label'] for item in summary.values()]
        values = [item['count'] for item in summary.values()]
        colors = [item['color'] for item in summary.values()]
        
        return {
            'labels': labels,
            'values': values,
            'colors': colors
        }


if __name__ == '__main__':
    # Test
    print("Order Status Manager Test")
    print("=" * 60)
    
    summary = OrderStatusManager.get_status_summary()
    for item in summary:
        print(f"{item['label']}: {item['count']} kòmand")
