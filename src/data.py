"""
Jenere Data Egzanp pou Dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data():
    """Jenere data ven egzanp"""
    dates = pd.date_range(start='2026-01-01', end='2026-02-12', freq='D')
    sales_records = []
    
    for date in dates:
        for _ in range(np.random.randint(5, 15)):
            sales_records.append({
                'ID': np.random.randint(1000, 9999),
                'Dat': date.strftime('%d/%m/%Y'),
                'Kliyèn': np.random.choice([
                    'Jean Paul', 'Marie Joseph', 'Pierre Dubois', 
                    'Ysaline Pérez', 'André Martin', 'Sophie Laurent',
                    'Michel Toussaint', 'Béatrice Rousseau'
                ]),
                'Pwodwi': np.random.choice([
                    'Laptop Pro', 'T-Shirt Kalite', 'Sèndèj Modèn',
                    'Fri Elektrik', 'Kabini Bambu', 'Riz 25kg',
                    'Laboutique Sikwit', 'Lemètad Alimantè'
                ]),
                'Kantite': np.random.randint(1, 10),
                'Montan': round(np.random.uniform(50, 500), 2),
            })
    
    return pd.DataFrame(sales_records)

def generate_product_data():
    """Jenere data pwodwi"""
    products = [
        {'Non': 'Laptop Pro', 'SKU': 'LAP-001', 'Pris': 1200, 'Stok': 45, 'Katègi': 'Teknoloji'},
        {'Non': 'T-Shirt Premium', 'SKU': 'TSH-001', 'Pris': 35, 'Stok': 200, 'Katègi': 'Vètman'},
        {'Non': 'Sèndèj Modèn', 'SKU': 'FUR-001', 'Pris': 450, 'Stok': 30, 'Katègi': 'Lakay'},
        {'Non': 'Fri Elektrik', 'SKU': 'APP-001', 'Pris': 320, 'Stok': 15, 'Katègi': 'Aparèy'},
        {'Non': 'Kabini Bambu', 'SKU': 'FUR-002', 'Pris': 280, 'Stok': 20, 'Katègi': 'Lakay'},
        {'Non': 'Riz Ekstra', 'SKU': 'FOD-001', 'Pris': 45, 'Stok': 500, 'Katègi': 'Manje'},
        {'Non': 'Smartphone 5G', 'SKU': 'PHN-001', 'Pris': 800, 'Stok': 60, 'Katègi': 'Teknoloji'},
        {'Non': 'Pantalon Klas', 'SKU': 'TSH-002', 'Pris': 65, 'Stok': 150, 'Katègi': 'Vètman'},
        {'Non': 'Mashin Kafè', 'SKU': 'APP-002', 'Pris': 850, 'Stok': 12, 'Katègi': 'Aparèy'},
        {'Non': 'Liv Edikasyon', 'SKU': 'BOK-001', 'Pris': 28, 'Stok': 100, 'Katègi': 'Lib'},
    ]
    return pd.DataFrame(products)

def generate_customer_data():
    """Jenere data kliyan"""
    first_names = ['Jean', 'Marie', 'Pierre', 'Ysaline', 'André', 'Sophie', 'Michel', 'Béatrice',
                   'François', 'Margot', 'Claude', 'Denise', 'Philippe', 'Lucette', 'René']
    last_names = ['Paul', 'Joseph', 'Dubois', 'Pérez', 'Martin', 'Laurent', 'Toussaint', 'Rousseau',
                  'Bernard', 'Leclerc', 'Duvall', 'Mercier', 'Sanchez', 'Fontaine', 'Benoit']
    
    cities = ['Port-au-Prince', 'Cap-Haïtien', 'Gonaïves', 'Jacmel', 'Jérémie', 'Hinche',
              'Pétion-Ville', 'Tabarre', 'Delmas', 'Carrefour', 'Léogâne', 'Saint-Marc']
    
    customers = []
    for i in range(150):
        customers.append({
            'ID': 10000 + i,
            'Non': f"{np.random.choice(first_names)} {np.random.choice(last_names)}",
            'Imèl': f"client{i}@example.ht",
            'Telefòn': f"+509 {np.random.randint(10000000, 99999999)}",
            'Vil': np.random.choice(cities),
            'Adrès': f"{np.random.randint(1, 999)} Ri {np.random.choice(['Lamè', 'Palèn', 'Prensip', 'Sosyal'])}",
            'Dat Jinskripsyon': (datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime('%d/%m/%Y'),
            'Total Achte': round(np.random.uniform(100, 5000), 2),
        })
    
    return pd.DataFrame(customers)
