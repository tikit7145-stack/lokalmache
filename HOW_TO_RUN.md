# 🚀 KOUMAN POU RUN DASHBOARD LA ANKR

## ⚡ RAPID (Sèl 2 Liy Kode)

```bash
cd ~/ecommerce-dashboard
python app.py
```

Fini! Vizite: **http://localhost:8050**

---

## 📋 DETAYE PA PA

### Option 1: Lokal Data (No Supabase - Default)
```bash
# Ale nan folder
cd ~/ecommerce-dashboard

# Roulle dashboard
python app.py

# Apre sa tap sa URL:
# http://localhost:8050
```

### Option 2: Avèk Virtual Environment
```bash
cd ~/ecommerce-dashboard

# Aktive venv
source venv/bin/activate

# Roulle
python app.py
```

### Option 3: Avèk Supabase (Si ou gen config .env)
```bash
cd ~/ecommerce-dashboard

# Verifye .env file existe
ls -la .env

# Roulle
python app.py

# Dashboard ap konekte ak Supabase otomatikal
```

---

## 🛑 STOP DASHBOARD

Dalam terminal kote dashboard la ap kouri:
- Tape: **`Ctrl + C`**
- Patizan 1-2 segond
- Dashboard ferme

---

## 🔄 RUN ANKR APRE STOP

```bash
# Yon fwa dashboard la ferme:
python app.py

# Oswa ak venv:
source venv/bin/activate
python app.py
```

---

## ✅ VÉRIF SI DASHBOARD ROULLE

1. **Within Terminal:**
   ```
   Should show:
   🚀 Senjivis Komès 2026 ap demaré...
   📊 Vizite: http://localhost:8050
   Dash is running on http://0.0.0.0:8050/
   ```

2. **In Browser:**
   - Visit: http://localhost:8050
   - Should see: 🛍️ **SENJIVIS KOMÈS 2026** dashboard

3. **If Error:**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   
   # Run again
   python app.py
   ```

---

## 💾 SOVE WÒK OU

### Dòt Folder
```bash
# Sose lapo ka data (CSV)
python examples.py
```

### Nan Dashboard
- Charts ki ap generate otomatikal
- Data kap save nan Supabase (si use_local_data=False)

---

## 🎯 COMMANDS YO GENYEN

| Command | Fè sa |
|---------|-------|
| `python app.py` | Run dashboard |
| `python examples.py` | See code examples |
| `pip install -r requirements.txt` | Install packages |
| `cp .env.example .env` | Create .env |
| `Ctrl + C` | Stop dashboard |

---

## 📍 IMPORTANT

✅ Dashboard **pa ta bezwen Supabase** pou roulle
- Yap sèvi local data otomatikal
- Perfè pou testing/demo

✅ Supabase optional
- Sèlman si ou vle real database
- Mete .env file avèk credentials

---

## 🆘 TROUBLESHOOTING

| Pwoblèm | Solisyon |
|---------|----------|
| `Command not found: python` | Use `python3 app.py` instead |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Port 8050 in use` | Change port in app.py or `lsof -i :8050` |
| Page won't load | Wait 5 seconds, try refresh |
| Dashboard slow | Normal on first load |

---

## 🔁 TYPIKAL WORKFLOW

```bash
# 1. Open terminal
cd ~/ecommerce-dashboard

# 2. Activate virtual env (optional but recommended)
source venv/bin/activate

# 3. Start dashboard
python app.py

# 4. Open browser to http://localhost:8050

# 5. See dashboard running!

# 6. When done, press Ctrl+C to stop
```

---

## 📱 QUICK Commands

**Run Dashboard:**
```bash
cd ~/ecommerce-dashboard && python app.py
```

**With Virtual Env:**
```bash
cd ~/ecommerce-dashboard && source venv/bin/activate && python app.py
```

**Run Examples:**
```bash
cd ~/ecommerce-dashboard && python examples.py
```

---

**Prèt! Run li! 🚀**

🇭🇹 Senjivis Komès 2026 🇭🇹
