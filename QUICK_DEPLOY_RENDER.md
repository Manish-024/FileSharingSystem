# 🎯 Render.com Quick Deploy

## 1️⃣ Go to Render
**https://render.com** → Sign in with GitHub

## 2️⃣ Create Web Service
**New +** → **Web Service** → Connect `FileSharingSystem`

## 3️⃣ Auto-Configuration
Render detects `render.yaml` automatically!

**Settings Verified:**
- Build: `pip install -r requirements.txt` ✅
- Start: `gunicorn app:app --bind 0.0.0.0:$PORT` ✅
- Plan: **Free** (750 hours/month) ✅

## 4️⃣ Click Deploy
**"Create Web Service"** → Wait 2-3 minutes ⏱️

## 5️⃣ Get Your URL
```
https://blockchain-file-sharing-xxxx.onrender.com
```

## 6️⃣ Update Frontend
After deploy, update `static/script_advanced.js`:
```javascript
const API_BASE_URL = 'https://YOUR-APP.onrender.com/api';
```

Then push:
```bash
git add static/script_advanced.js
git commit -m "Update API URL"
git push origin main
```

Render auto-deploys! ✨

---

## ⚠️ Free Tier Notes
- App sleeps after 15 min inactivity
- 30 sec cold start
- Perfect for demos!

---

## ✅ That's It!
Your blockchain app is live! 🎉

Full guide: [RENDER_DEPLOY.md](./RENDER_DEPLOY.md)
