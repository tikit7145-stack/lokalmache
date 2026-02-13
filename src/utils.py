"""
Utilities pou Dashboard Senjivis Komès
Advanced features ak helper functions
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class DataAnalytics:
    """Klas pou advanced analytics"""
    
    @staticmethod
    def calculate_growth_rate(current, previous):
        """Kalkile pousantaj kwasans"""
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100
    
    @staticmethod
    def get_date_range(period='month'):
        """Jwenn ranj dat dapre peryòd"""
        today = datetime.now()
        
        if period == 'today':
            start = today.replace(hour=0, minute=0, second=0)
            end = today.replace(hour=23, minute=59, second=59)
        elif period == 'week':
            start = today - timedelta(days=today.weekday())
            end = today
        elif period == 'month':
            start = today.replace(day=1)
            end = today
        elif period == 'year':
            start = today.replace(month=1, day=1)
            end = today
        else:
            start = today - timedelta(days=30)
            end = today
            
        return start, end
    
    @staticmethod
    def format_currency(amount):
        """Formate montan an dola"""
        return f"${amount:,.2f}"
    
    @staticmethod
    def format_percentage(value, decimals=1):
        """Formate pousantaj"""
        return f"{value:.{decimals}f}%"


class ValidationUtils:
    """Klas pou validation"""
    
    @staticmethod
    def is_valid_email(email):
        """Valide adrès imèl"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone):
        """Valide nimewo telefòn"""
        import re
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None
    
    @staticmethod
    def is_valid_amount(amount):
        """Valide montan"""
        try:
            return float(amount) >= 0
        except (ValueError, TypeError):
            return False


class DataFormatter:
    """Klas pou formating data"""
    
    @staticmethod
    def format_large_number(number):
        """Formate nimewo gwo"""
        if number >= 1_000_000:
            return f"{number/1_000_000:.1f}M"
        elif number >= 1_000:
            return f"{number/1_000:.1f}K"
        else:
            return str(number)
    
    @staticmethod
    def truncate_text(text, length=50):
        """Koupe tèks long"""
        if len(text) > length:
            return text[:length] + "..."
        return text
    
    @staticmethod
    def format_date(date_obj, format_str='%d/%m/%Y'):
        """Formate dat"""
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime(format_str)


class ChartUtils:
    """Klas pou chart utilities"""
    
    @staticmethod
    def get_color_palette(index, style='default'):
        """Jwenn koulè dapre index"""
        palettes = {
            'default': [
                'rgba(99, 102, 241, 0.8)',
                'rgba(236, 72, 153, 0.8)',
                'rgba(6, 182, 212, 0.8)',
                'rgba(139, 92, 246, 0.8)',
                'rgba(22, 163, 74, 0.8)',
            ],
            'dark': [
                'rgba(100, 200, 255, 0.8)',
                'rgba(255, 150, 200, 0.8)',
                'rgba(150, 200, 100, 0.8)',
                'rgba(255, 200, 100, 0.8)',
                'rgba(200, 150, 255, 0.8)',
            ]
        }
        colors = palettes.get(style, palettes['default'])
        return colors[index % len(colors)]
    
    @staticmethod
    def get_hover_template():
        """Jwenn hover template pou charts"""
        return "<b>%{x}</b><br>Valè: %{y:,.2f}<extra></extra>"


class PerformanceMonitor:
    """Klas pou monitor performance"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Demaré timer"""
        self.start_time = datetime.now()
    
    def stop(self):
        """Kanpe timer"""
        self.end_time = datetime.now()
    
    def get_duration(self):
        """Jwenn dirèkti an milisegond"""
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds() * 1000
            return f"{duration:.2f}ms"
        return "N/A"


class NotificationManager:
    """Klas pou manage notifications"""
    
    @staticmethod
    def create_success_message(title, message):
        """Kriye mesaj siksè"""
        return {
            'type': 'success',
            'title': title,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def create_error_message(title, message):
        """Kriye mesaj erè"""
        return {
            'type': 'error',
            'title': title,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def create_warning_message(title, message):
        """Kriye mesaj avètisman"""
        return {
            'type': 'warning',
            'title': title,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }


class ExportManager:
    """Klas pou jeneré exports"""
    
    @staticmethod
    def dataframe_to_csv(df, filename):
        """Ekspo DataFrame an CSV"""
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            return True, f"Fichye {filename} te kreye avèk siksè"
        except Exception as e:
            return False, f"Erè pandan creation fichye: {str(e)}"
    
    @staticmethod
    def dataframe_to_json(df):
        """Konvèti DataFrame an JSON"""
        return df.to_json(orient='records', date_format='iso')


# Helper functions
def get_haitien_creole_month(month_num):
    """Jwenn non mwa an Kreyòl"""
    months = {
        1: 'Janvye', 2: 'Fevriye', 3: 'Mas', 4: 'Avril',
        5: 'Me', 6: 'Jen', 7: 'Jiye', 8: 'Out',
        9: 'Septam', 10: 'Oktòb', 11: 'Novanm', 12: 'Desam'
    }
    return months.get(month_num, 'Mwa enkoni')


def get_haitien_creole_day(day_num):
    """Jwenn non jou an Kreyòl"""
    days = {
        0: 'Lindi', 1: 'Madi', 2: 'Mèkredi', 3: 'Jedi',
        4: 'Vandredi', 5: 'Samdi', 6: 'Dimanch'
    }
    return days.get(day_num, 'Jou enkoni')


def format_haitian_date(date_obj):
    """Formate dat an Kreyòl Ayisyen"""
    if isinstance(date_obj, str):
        return date_obj
    
    day = get_haitien_creole_day(date_obj.weekday())
    date_str = date_obj.strftime('%d')
    month = get_haitien_creole_month(date_obj.month)
    year = date_obj.strftime('%Y')
    
    return f"{day}, {date_str} {month} {year}"
