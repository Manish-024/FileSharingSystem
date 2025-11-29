# 🚀 Deployment Guide - All Platforms

Complete guide for deploying the Advanced Blockchain File Sharing System on various cloud platforms.

---

## 📋 Table of Contents

1. [Railway.app](#1-railwayapp-recommended) ⭐ Recommended
2. [Render.com](#2-rendercom)
3. [Heroku](#3-heroku)
4. [Vercel](#4-vercel)
5. [Docker / Docker Compose](#5-docker--docker-compose)
6. [DigitalOcean App Platform](#6-digitalocean-app-platform)
7. [Google Cloud Run](#7-google-cloud-run)
8. [AWS Elastic Beanstalk](#8-aws-elastic-beanstalk)
9. [Local Deployment](#9-local-deployment)

---

## 🎯 Platform Comparison

| Platform | Cost | Ease | Performance | Best For |
|----------|------|------|-------------|----------|
| **Railway** | Free tier | ⭐⭐⭐⭐⭐ | Excellent | Quick deploy |
| **Render** | Free tier | ⭐⭐⭐⭐⭐ | Good | Free hosting |
| **Heroku** | Paid | ⭐⭐⭐⭐ | Good | Mature platform |
| **Vercel** | Free tier | ⭐⭐⭐ | Limited | Frontend focus |
| **Docker** | Self-hosted | ⭐⭐⭐⭐ | Excellent | Full control |
| **DigitalOcean** | $5/month | ⭐⭐⭐⭐ | Excellent | Reliable hosting |
| **Google Cloud** | Pay-as-go | ⭐⭐⭐ | Excellent | Enterprise |
| **AWS** | Pay-as-go | ⭐⭐ | Excellent | Enterprise |

---

## 1. Railway.app (Recommended) ⭐

### Why Railway?
- ✅ Easiest deployment
- ✅ Free tier available ($5 credit/month)
- ✅ Automatic SSL certificates
- ✅ GitHub integration
- ✅ Environment variables management
- ✅ Persistent storage

### Setup Steps:

#### Step 1: Prepare Your Repository
```bash
# Make sure you have these files (already created):
# - Procfile
# - railway.json
# - requirements.txt
# - runtime.txt

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Railway deployment"
```

#### Step 2: Deploy to Railway

**Option A: Using Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

**Option B: Using Railway Dashboard** (Easier)
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway auto-detects Python and deploys!

#### Step 3: Configure Environment Variables

In Railway Dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add these variables:

```bash
FLASK_ENV=production
SECRET_KEY=<generate-a-random-secret-key>
BLOCKCHAIN_DIFFICULTY=2
PORT=$PORT
```

#### Step 4: Enable Persistent Storage (Optional)

For persistent file uploads:
1. Go to "Volumes" tab
2. Add a volume at `/app/uploads`
3. Redeploy

#### Step 5: Access Your App

Railway provides a URL like: `https://your-app.railway.app`

### Environment Variables for Railway:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
BLOCKCHAIN_DIFFICULTY=2
PORT=$PORT
DEBUG=False
```

---

## 2. Render.com

### Setup Steps:

#### Step 1: Create render.yaml (Already Created)

#### Step 2: Deploy
1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click "New +"
4. Select "Web Service"
5. Connect your GitHub repository
6. Render auto-detects the `render.yaml` file
7. Click "Create Web Service"

#### Step 3: Configure
- **Name**: blockchain-file-sharing
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

#### Step 4: Add Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=<generate-random-key>
BLOCKCHAIN_DIFFICULTY=2
```

### Cost: Free tier available

---

## 3. Heroku

### Setup Steps:

#### Step 1: Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from heroku.com
```

#### Step 2: Login and Create App
```bash
heroku login
heroku create blockchain-file-sharing-app
```

#### Step 3: Configure Environment Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set BLOCKCHAIN_DIFFICULTY=2
```

#### Step 4: Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Step 5: Open App
```bash
heroku open
```

### One-Click Deploy:
You can also use the Heroku Button:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

---

## 4. Vercel

**⚠️ Note**: Vercel is primarily for serverless/frontend apps. Flask apps have limitations.

### Setup Steps:

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Deploy
```bash
vercel
```

#### Step 3: Configure (vercel.json already created)

**Limitations on Vercel**:
- Serverless functions have timeout limits
- No persistent file storage
- Better suited for static sites

---

## 5. Docker / Docker Compose

### Local Docker Deployment:

#### Step 1: Build Image
```bash
docker build -t blockchain-file-sharing .
```

#### Step 2: Run Container
```bash
docker run -d -p 5001:5001 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/uploads:/app/uploads \
  blockchain-file-sharing
```

### Using Docker Compose:

#### Step 1: Run
```bash
docker-compose up -d
```

#### Step 2: View Logs
```bash
docker-compose logs -f
```

#### Step 3: Stop
```bash
docker-compose down
```

### Deploy to Any VPS with Docker:

```bash
# Copy files to server
scp -r . user@your-server:/path/to/app

# SSH to server
ssh user@your-server

# Navigate to app directory
cd /path/to/app

# Run with Docker Compose
docker-compose up -d
```

---

## 6. DigitalOcean App Platform

### Setup Steps:

#### Step 1: Create Account
1. Go to [digitalocean.com](https://digitalocean.com)
2. Sign up and verify

#### Step 2: Create App
1. Click "Create" → "Apps"
2. Connect GitHub repository
3. Select your repo and branch
4. DigitalOcean auto-detects Python

#### Step 3: Configure
- **Type**: Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `gunicorn app:app --bind 0.0.0.0:8080`
- **HTTP Port**: 8080

#### Step 4: Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=<random-key>
BLOCKCHAIN_DIFFICULTY=2
PORT=8080
```

### Cost: $5/month minimum

---

## 7. Google Cloud Run

### Setup Steps:

#### Step 1: Install gcloud CLI
```bash
# Follow instructions at cloud.google.com/sdk
```

#### Step 2: Authenticate
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### Step 3: Build and Deploy
```bash
# Build with Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/blockchain-file-sharing

# Deploy to Cloud Run
gcloud run deploy blockchain-file-sharing \
  --image gcr.io/YOUR_PROJECT_ID/blockchain-file-sharing \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,SECRET_KEY=your-key
```

---

## 8. AWS Elastic Beanstalk

### Setup Steps:

#### Step 1: Install EB CLI
```bash
pip install awsebcli
```

#### Step 2: Initialize
```bash
eb init -p python-3.13 blockchain-file-sharing
```

#### Step 3: Create Environment
```bash
eb create production-env
```

#### Step 4: Deploy
```bash
eb deploy
```

#### Step 5: Open
```bash
eb open
```

---

## 9. Local Deployment

### For Development:

#### Step 1: Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Create .env File
```bash
cp .env.example .env
# Edit .env with your settings
```

#### Step 4: Run
```bash
python app.py
```

Access at: `http://localhost:5001`

### For Production (Local Server):

#### Using Gunicorn:
```bash
gunicorn app:app --bind 0.0.0.0:5001 --workers 4
```

#### With Supervisor (Process Manager):
```bash
# Install supervisor
sudo apt-get install supervisor

# Create config: /etc/supervisor/conf.d/blockchain-app.conf
[program:blockchain-app]
command=/path/to/venv/bin/gunicorn app:app --bind 0.0.0.0:5001 --workers 4
directory=/path/to/app
user=your-user
autostart=true
autorestart=true
```

---

## 🔒 Security Checklist for Production

Before deploying, ensure:

- [ ] Change `SECRET_KEY` to a random string
- [ ] Set `DEBUG=False`
- [ ] Configure proper `CORS_ORIGINS` (not `*`)
- [ ] Use HTTPS (most platforms provide this automatically)
- [ ] Set up database backup for contracts (if persisting)
- [ ] Configure file upload limits appropriately
- [ ] Set up monitoring and logging
- [ ] Review and set proper environment variables
- [ ] Enable firewall rules if using VPS
- [ ] Set up regular backups for uploads folder

---

## 🌐 Custom Domain Setup

### Railway:
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS records as shown

### Render:
1. Go to Settings → Custom Domains
2. Add domain
3. Update DNS CNAME

### Heroku:
```bash
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com
```

---

## 📊 Monitoring & Logs

### Railway:
```bash
railway logs
```

### Render:
View logs in Dashboard → Logs tab

### Heroku:
```bash
heroku logs --tail
```

### Docker:
```bash
docker logs -f <container-name>
```

---

## 🔧 Troubleshooting

### Common Issues:

#### 1. Port Binding Error
**Problem**: App not binding to correct port

**Solution**: Ensure using `PORT` environment variable
```python
app.run(port=int(os.getenv('PORT', 5001)))
```

#### 2. Module Not Found
**Problem**: Dependencies not installed

**Solution**: Check requirements.txt is complete
```bash
pip freeze > requirements.txt
```

#### 3. File Upload Issues
**Problem**: Files not persisting

**Solution**: Configure volume/persistent storage on your platform

#### 4. CORS Errors
**Problem**: Frontend can't access API

**Solution**: Set proper CORS origins in environment variables

---

## 📝 Quick Deploy Commands

### Railway:
```bash
railway up
```

### Render:
```bash
git push origin main  # Auto-deploys on push
```

### Heroku:
```bash
git push heroku main
```

### Docker:
```bash
docker-compose up -d
```

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] All configuration files present
- [ ] Environment variables configured
- [ ] requirements.txt updated
- [ ] .gitignore properly configured
- [ ] Security settings reviewed
- [ ] Platform selected
- [ ] Deploy command executed
- [ ] Application accessible
- [ ] SSL/HTTPS working
- [ ] File uploads working
- [ ] Blockchain mining working
- [ ] All features tested

---

## 🎉 Success!

Your blockchain file sharing system is now deployed! 

Share your deployment URL and start using your advanced blockchain application!

For issues or questions, check the platform-specific documentation or the troubleshooting section above.
