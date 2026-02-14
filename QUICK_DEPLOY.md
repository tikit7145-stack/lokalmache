# 🚀 Depo Byèf - Quick Cloud Deployment Guide

**Lokalmache Dashboard** - prèt pou internet! Tchoje platfom ou a pi ba a:

---

## 1️⃣ RENDER (Rekomande - Li difisil!)

### Etap 1: Prepare GitHub
```bash
git push origin main  # ✅ Fèt deja
```

### Etap 2: Create Render Account
1. Ale nan https://render.com
2. Klik "Sign Up" → GitHub Sign In
3. Authoriz Render pou GitHub

### Etap 3: New Web Service
1. Klik "New +" → "Web Service"
2. Select repository: `lokalmache`
3. Settings:
   - **Name**: lokalmache-dashboard
   - **Region**: Frankfurt (or closest to you)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server`
   - **Port**: 8051

### Etap 4: Environment Variables
Click "Environment" → Add these:
```
SUPABASE_URL = [kopimanm nan Supabase]
SUPABASE_KEY = [kopimanm nan Supabase]
```

### Etap 5: Deploy
Click "Create Web Service" → Wait 3-5 minutes

**Ti konsèy**: Free tier rete dòmi apre 15min inaktivite - sèn! Upgrade pou $7/mwa pou production.

---

## 2️⃣ DIGITALOCEAN (Bon pri, Fasil)

### Etap 1: Create DigitalOcean Account
1. Ale nan https://www.digitalocean.com
2. Sign up → Create account
3. Add payment method

### Etap 2: Create App Platform
1. Klik "Apps" (left menu)
2. Klik "Create Apps"
3. Connect GitHub → Select `lokalmache` repository

### Etap 3: Configure App
1. **Name**: lokalmache
2. **Region**: NYC (or closest)
3. **HTTP Port**: 8051

### Etap 4: Set Environment Variables
Klik "Edit" → Add:
```
SUPABASE_URL = [URL]
SUPABASE_KEY = [KEY]
```

### Etap 5: Deploy
Click "Deploy" → Wait 5-10 minutes

**Pri**: $5-$12/mwa depan sou need. First month free ($200 credit).

---

## 3️⃣ AWS EC2 (Pwisan, Orijinal)

### Etap 1: Create AWS Account
1. Ale nan https://aws.amazon.com
2. Create Free Tier account
3. Add payment method

### Etap 2: Launch EC2 Instance
1. Klik "EC2" → "Launch Instance"
2. Select: **Ubuntu 22.04 LTS** (free tier elijib)
3. Instance Type: **t2.micro** (free)
4. Security Group: Allow ports 80, 443, 8051

### Etap 3: Connect to Server
```bash
ssh -i "your-key.pem" ubuntu@your-public-ip
```

### Etap 4: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & git
sudo apt install python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/tikit7145-stack/lokalmache.git
cd lokalmache

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Etap 5: Set Environment Variables
```bash
nano .env
# Paste these:
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
# Save: Ctrl+O → Enter → Ctrl+X
```

### Etap 6: Run Application
```bash
gunicorn app:server --bind 0.0.0.0:8051
# Or better - use screen or forever:
screen -S dashboard
gunicorn app:server --bind 0.0.0.0:8051
# Detach: Ctrl+A then D
```

**Aksè**: http://your-ec2-public-ip:8051

---

## 4️⃣ ALIBABA CLOUD (Enterprise, Enpèyal)

### Etap 1: Create Account
1. Ale nan https://www.alibabacloud.com
2. Sign up
3. Verify email
4. Add payment method

### Etap 2: Launch ECS Instance
1. Klik "Products" → "Elastic Compute Service (ECS)"
2. Click "Create Instance"
3. Settings:
   - **Region**: Singapore (or closest)
   - **Image**: Ubuntu 22.04
   - **Instance Type**: ecs.t6-c1m1.large (free tier)
   - **Storage**: 40GB SSD
   - **Network**: Create new VPC
   - **Security Group**: Allow ports 22, 80, 443, 8051

### Etap 3: Connect via SSH
```bash
ssh -i "your-key.pem" root@your-public-ip
```

### Etap 4: Setup (same as AWS)
```bash
apt update && apt upgrade -y
apt install python3-pip python3-venv git nginx -y
git clone https://github.com/tikit7145-stack/lokalmache.git
cd lokalmache
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Etap 5: Configure Nginx (Reverse Proxy)
```bash
sudo nano /etc/nginx/sites-available/default
```

Replace content with:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8051;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Etap 6: Start Services
```bash
# Start application (in background)
nohup gunicorn app:server --bind 127.0.0.1:8051 > app.log 2>&1 &

# Restart nginx
sudo systemctl restart nginx
```

**Aksè**: http://your-domain.com

---

## 🔐 KOTE JWENN Supabase Credentials

1. Log in sa https://supabase.com
2. Select your project
3. Go to "Settings" (bottom of left menu)
4. Click "API" section
5. Copy:
   - **Project URL** → SUPABASE_URL
   - **anon public** key → SUPABASE_KEY

---

## ✅ Checklist Dèpwèl

- [ ] Repo pushed to GitHub
- [ ] Supabase credentials copied
- [ ] Cloud account created
- [ ] Environment variables set
- [ ] Application deployed
- [ ] Test dashboard loading at URL
- [ ] Test sample order update
- [ ] Configure domain (optional)
- [ ] Setup SSL (optional)
- [ ] Monitor app logs

---

## 🎯 Next Steps

**After Deployment:**

1. **Setup Domain**
   ```bash
   # For Render: just add custom domain in settings
   # For DO/AWS: Update DNS to point to IP/load balancer
   ```

2. **Enable SSL**
   - Render/DO: Automatic (free)
   - AWS: Use ACM + CloudFront
   - Alibaba: Use SSL Certificate service

3. **Monitor Performance**
   ```bash
   # Check logs on Render: Dashboard > Logs
   # Check logs on EC2/Alibaba:
   tail -f app.log
   ```

4. **Scale if Needed**
   - Render: Upgrade to Pro plan
   - DigitalOcean: Increase App size
   - AWS: Use Auto Scaling Groups
   - Alibaba: Scale up instance type

---

## 🆘 Tibilasyon Moun

**App Not Loading:**
- Check environment variables set correctly
- Check logs for error messages
- Verify SUPABASE_URL and SUPABASE_KEY

**Port Already in Use:**
```bash
# Kill process on port 8051
kill -9 $(lsof -t -i:8051)
# Or choose different port
gunicorn app:server --bind 0.0.0.0:8052
```

**Database Connection Error:**
- Verify SUPABASE_URL format: `https://xxxxx.supabase.co`
- Check SUPABASE_KEY is correct
- Verify Supabase project is "Active"

**Slow Performance:**
- Upgrade instance size
- Enable caching on Supabase
- Use CDN (CloudFront/Cloudflare)

---

✨ **Ready to deploy!** Choose your platform above and follow the steps.

Questions? Check `DEPO_ALIBABA_CLOUD.md` for detailed guide.
