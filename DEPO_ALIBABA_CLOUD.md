# 🚀 DEPOYE SOU ALIBABA CLOUD / CLOUD PLATFORMS

**Language:** Haitian Creole / English | **Date:** February 2026

---

## 📋 TABLA MATERYÈL

1. [Alibaba Cloud Setup](#alibaba-cloud-setup)
2. [AWS Deployment](#aws-deployment)
3. [Render Deployment](#render-deployment)
4. [DigitalOcean Deployment](#digitalocean-deployment)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## 🟠 Alibaba Cloud Setup

### Step 1: Create Alibaba Cloud Account
1. Go to [www.alibabacloud.com](https://www.alibabacloud.com)
2. Click "Free Account" ou "Console"
3. Complete registration avèk email ou numero telefon

### Step 2: Create ECS Instance (Server)
1. Log in to Alibaba Cloud Console
2. Navigate to **Elastic Compute Service (ECS)**
3. Click **Create Instance**
4. Configure:
   - **Region**: Choose closest to your users (Singapore recommended for Caribbean)
   - **Instance Type**: `ecs.t5.large` (2 vCPU, 4 GB RAM)
   - **Image**: Ubuntu 20.04 LTS
   - **Storage**: 50 GB SSD
   - **Network**: Create VPC or use default
5. Click **Create**

### Step 3: Configure Security Groups
1. In ECS details, click **Security Groups**
2. Click **Edit Rules**
3. Add these inbound rules:
   ```
   Protocol: TCP
   Port: 80 (HTTP)
   Source: 0.0.0.0/0
   
   Protocol: TCP
   Port: 443 (HTTPS)
   Source: 0.0.0.0/0
   
   Protocol: TCP
   Port: 22 (SSH)
   Source: YOUR_IP/32
   ```
4. Save rules

### Step 4: SSH Into Your Server
```bash
# Get your instance's public IP from Alibaba console
ssh -i your-key.pem ubuntu@YOUR_ECS_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & dependencies
sudo apt install -y python3 python3-pip python3-venv git

# Install Nginx (reverse proxy)
sudo apt install -y nginx

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Step 5: Deploy Application
```bash
# Clone your GitHub repository
git clone https://github.com/tikit7145-stack/lokalmache.git
cd lokalmache

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your secrets
cat > .env << 'EOF'
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
EOF

# Test the app
python3 app.py
```

### Step 6: Configure Nginx (Reverse Proxy)
```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/default
```

Paste this configuration:
```nginx
upstream dash {
    server 127.0.0.1:8051;
}

server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    server_name YOUR_DOMAIN_OR_IP;
    
    location / {
        proxy_pass http://dash;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Restart Nginx:
```bash
sudo systemctl restart nginx
```

### Step 7: Run App with Gunicorn (Production)
```bash
# Install gunicorn (already in requirements.txt)
source venv/bin/activate
gunicorn app:server --bind 0.0.0.0:8051 --workers 4 --timeout 120

# Or run in background with nohup
nohup gunicorn app:server --bind 0.0.0.0:8051 --workers 4 > app.log 2>&1 &
```

### Step 8: Setup Systemd Service (Auto-start)
```bash
# Create service file
sudo nano /etc/systemd/system/lokalmache.service
```

Paste:
```ini
[Unit]
Description=LokalMache Dashboard
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/lokalmache
ExecStart=/home/ubuntu/lokalmache/venv/bin/gunicorn app:server --bind 0.0.0.0:8051 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable lokalmache
sudo systemctl start lokalmache
sudo systemctl status lokalmache
```

### Step 9: SSL Certificate (HTTPS)
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get free SSL from Let's Encrypt
sudo certbot certonly --nginx -d your-domain.com

# Update nginx config to use SSL
sudo nano /etc/nginx/sites-available/default
```

Update server block:
```nginx
listen 443 ssl http2;
ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
```

---

## 🌐 AWS Deployment (EC2 + RDS)

### Step 1: Launch EC2 Instance
1. Go to AWS Console → EC2
2. Click **Launch Instance**
3. Select **Ubuntu 20.04 LTS**
4. Choose **t3.medium** (2 vCPU, 4 GB RAM)
5. Configure security group:
   - Allow HTTP (80)
   - Allow HTTPS (443)
   - Allow SSH (22)
6. Launch and download `.pem` key file

### Step 2: Connect & Deploy
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
git clone https://github.com/tikit7145-stack/lokalmache.git
cd lokalmache
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Use Elastic Beanstalk (Easier)
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB
eb init -p python-3.9 lokalmache --region us-east-1

# Deploy
eb create lokalmache-env
eb deploy

# Open in browser
eb open
```

---

## 🎨 Render Deployment (Recommended - Easiest)

### Step 1: Push to GitHub
✅ Already done!

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Click **Sign up** with GitHub
3. Authorize Render

### Step 3: Create Web Service
1. Click **New** → **Web Service**
2. Select your GitHub repo
3. Configure:
   - **Name**: lokalmache-dashboard
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server --bind 0.0.0.0:10000`
4. Add Environment Variables:
   ```
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   ```
5. Click **Create Web Service**

### Step 4: Add Custom Domain
1. In Render dashboard, go to your service
2. Click **Settings** → **Custom Domain**
3. Add your domain
4. Update DNS records pointing to Render

**Cost**: Free tier available, $7/month for paid tier

---

## 💫 DigitalOcean Deployment

### Step 1: Create Droplet
1. Go to [digitalocean.com](https://digitalocean.com)
2. Click **Create** → **Droplet**
3. Select **Ubuntu 20.04**
4. Choose **Basic** - $6/month (1GB RAM, 1 vCPU)
5. Select datacenter closest to you
6. Create SSH key
7. Click **Create Droplet**

### Step 2: Connect & Setup
```bash
ssh root@your_droplet_ip

# Update system
apt update && apt upgrade -y

# Install requirements
apt install -y python3 python3-pip python3-venv git nginx

# Clone repository
git clone https://github.com/tikit7145-stack/lokalmache.git
cd lokalmache

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env
echo "SUPABASE_URL=..." > .env
echo "SUPABASE_KEY=..." >> .env
```

### Step 3: Configure Nginx
```bash
nano /etc/nginx/sites-enabled/default
```

Paste (same as Alibaba):
```nginx
upstream dash {
    server 127.0.0.1:8051;
}

server {
    listen 80;
    server_name your_domain_or_ip;
    
    location / {
        proxy_pass http://dash;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Step 4: Run with Supervisor
```bash
apt install -y supervisor

# Create supervisor config
nano /etc/supervisor/conf.d/lokalmache.conf
```

Paste:
```ini
[program:lokalmache]
directory=/root/lokalmache
command=/root/lokalmache/venv/bin/gunicorn app:server --bind 0.0.0.0:8051 --workers 4
autostart=true
autorestart=true
stderr_logfile=/var/log/lokalmache.err.log
stdout_logfile=/var/log/lokalmache.out.log
```

Start service:
```bash
supervisorctl reread
supervisorctl update
supervisorctl start lokalmache
```

---

## 🔐 Environment Variables

Create `.env` file in root directory:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# Optional: Application Settings
DEBUG=False
LOG_LEVEL=INFO
```

**Never commit `.env` to GitHub!**

---

## 🐛 Troubleshooting

### App not responding
```bash
# Check if running
ps aux | grep gunicorn

# Check logs
tail -100 /var/log/lokalmache.out.log
tail -100 /var/log/lokalmache.err.log

# Restart
supervisorctl restart lokalmache
```

### Port already in use
```bash
# Kill process on port 8051
lsof -i :8051
kill -9 PID
```

### Nginx 502 Bad Gateway
```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Restart Nginx
sudo systemctl restart nginx

# Check Nginx config
sudo nginx -t
```

### Supabase connection error
- Verify SUPABASE_URL is correct (includes `.co`)
- Verify SUPABASE_KEY is anon key (not service role)
- Check environment variables are set: `env | grep SUPABASE`

### Module not found
```bash
source venv/bin/activate
pip install -r requirements.txt
python3 -c "import dash; print('OK')"
```

---

## 📊 Monitoring & Updates

### Check App Status
```bash
# View logs (Render)
render logs

# View logs (Supervisor)
supervisorctl tail lokalmache -100

# Check resource usage
free -h
df -h
top
```

### Update Application
```bash
cd lokalmache
git pull origin main
source venv/bin/activate
pip install -r requirements.txt

# Restart service
supervisorctl restart lokalmache
# or for Render
git commit --allow-empty -m "Trigger deploy"
git push
```

---

## 💰 Cost Comparison

| Platform | Min Cost | Features | Setup Time |
|----------|----------|----------|-----------|
| **Alibaba Cloud** | $15/month | Full control, scalable | 30 min |
| **AWS EC2** | $10/month | Enterprise, complex | 20 min |
| **Render** | FREE | Easy, auto-deploy | 5 min |
| **DigitalOcean** | $6/month | Simple, reliable | 15 min |
| **PythonAnywhere** | $5/month | Python-specific | 10 min |

---

## ✅ Deployment Checklist

- [ ] GitHub repo created and code pushed
- [ ] Environment variables configured
- [ ] Supabase project and API keys ready
- [ ] Cloud provider account created
- [ ] Server/instance launched
- [ ] Python and dependencies installed
- [ ] Application tested locally
- [ ] Nginx configured (if using)
- [ ] SSL certificate installed
- [ ] Domain pointed to server
- [ ] Monitoring setup
- [ ] Backups configured

---

## 🚀 Your Dashboard is Ready!

Your **LokalMache Dashboard** is now production-ready and can be deployed anywhere!

**GitHub**: https://github.com/tikit7145-stack/lokalmache
**Local Dev**: http://localhost:8051
**Production**: https://your-domain.com (after deployment)

For questions, check the README.md or documentation files.

**Baybay wa nan entènèt! 🎉**

