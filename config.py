"""
Configuration file para Senjivis Komès 2026
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
SRC_DIR = os.path.join(BASE_DIR, 'src')

# App configuration
APP_NAME = "Senjivis Komès 2026"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Dashboard E-Commerce konplè ak Dysèn Glassmorphism"

# Server configuration
HOST = '0.0.0.0'
PORT = 8050
DEBUG = True

# Data configuration
SAMPLE_DATA_SIZE = {
    'sales': 300,
    'customers': 150,
    'products': 20,
}

# Theme colors
THEME_COLORS = {
    'primary': '#6366f1',
    'secondary': '#ec4899',
    'accent': '#06b6d4',
    'dark_bg': '#0f0f1e',
    'light_text': '#e2e8f0',
}

# Pagination
ITEMS_PER_PAGE = 10
MAX_ROWS_TABLE = 50

# Currency
CURRENCY_SYMBOL = '$'
CURRENCY_FORMAT = '{:,.2f}'

# Date format
DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'

# UI Settings
GLASSMORPHISM_BLUR = '20px'
CARD_BORDER_RADIUS = '14px'
ANIMATION_DURATION = '0.3s'

# Analytics
REFRESH_INTERVAL = 60000  # ms (1 minute)
AUTO_UPDATE_ENABLED = True

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'ecommerce_dashboard.log'

# Feature flags
FEATURES = {
    'dark_mode': True,
    'analytics': True,
    'export_csv': False,
    'export_pdf': False,
    'real_time_updates': True,
    'notifications': False,
}

# ============ SUPABASE CONFIGURATION ============

# Use local data or Supabase
USE_LOCAL_DATA = os.getenv('USE_LOCAL_DATA', 'True').lower() == 'true'

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

# Supabase is configured if we have both URL and KEY
SUPABASE_ENABLED = bool(SUPABASE_URL and SUPABASE_KEY and not USE_LOCAL_DATA)

print(f"📊 Mòd: {'✅ Local Data' if USE_LOCAL_DATA else '✅ Supabase Database'}")

# Table names
TABLES = {
    'sales': 'vant',
    'products': 'pwodwi',
    'customers': 'kliyan',
    'orders': 'komand',
}
