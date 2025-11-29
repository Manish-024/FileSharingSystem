# 🔗 Advanced Blockchain File Sharing System


Your Advanced Blockchain File Sharing System is now ready for deployment on multiple platforms!A sophisticated blockchain-based document sharing platform with encryption, smart contracts, peer verification, and comprehensive analytics.



---[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)



## ✅ What's Been Set Up## 🌟 Advanced Features



### 🔧 Configuration Files Created### Core Features

- ✅ **Procfile** - Railway.app and Heroku deployment- 🔗 **Blockchain-based Storage**: All file metadata is stored on an immutable blockchain with Proof of Work

- ✅ **railway.json** - Railway-specific configuration- � **File Encryption/Decryption**: AES encryption with password protection using PBKDF2 key derivation

- ✅ **runtime.txt** - Python 3.13 specification- 🤝 **Smart Contracts**: Permission-based access control with expiration times and download limits

- ✅ **config.py** - Environment-based configuration management- ✓ **Peer Verification System**: Community-driven file authenticity verification with reputation scoring

- ✅ **.env.example** - Environment variables template- 📊 **Advanced Analytics Dashboard**: Real-time charts and visualizations using Chart.js

- ✅ **Dockerfile** - Docker containerization- 🔄 **File Versioning**: Automatic version tracking with rollback capability

- ✅ **docker-compose.yml** - Docker Compose setup- 🔍 **Advanced Search & Filtering**: Search by filename, type, uploader, encryption status

- ✅ **render.yaml** - Render.com deployment config- �📤 **File Upload**: Upload files with automatic hashing and blockchain recording

- ✅ **vercel.json** - Vercel deployment config- 📥 **Secure Download**: Download files with access control and transaction tracking

- ✅ **app.json** - Heroku one-click deploy- ⛓️ **Blockchain Explorer**: View all blocks and transactions in detail

- 🎨 **Modern Tabbed UI**: Intuitive multi-tab interface with responsive design

### 📦 Dependencies Updated

- ✅ **gunicorn==21.2.0** - Production WSGI server### Smart Contract Features

- ✅ **python-dotenv==1.0.0** - Environment variable management- Public/Private file access control

- ✅ All dependencies installed in virtual environment- Maximum download limits

- Time-based expiration

### 📝 Documentation Created- User-specific permissions

- ✅ **DEPLOYMENT.md** - Complete deployment guide for 8+ platforms- Access logging and analytics

- ✅ **PLATFORMS.md** - Platform comparison and selection guide

- ✅ **README.md** - Updated with deployment instructions### Peer Verification Features

- ✅ **test_local.py** - Comprehensive test suite- Vote on file authenticity (Authentic/Suspicious)

- Reputation-weighted scoring system

### ✓ Tests Passed- Authenticity score calculation (0-100%)

- ✅ **8/8 tests passing**- Top verifiers leaderboard

  - Dependencies ✓- Comment system for verification

  - Directories ✓

  - Imports ✓### Analytics Features

  - Configuration ✓- Activity timeline (uploads/downloads over time)

  - Blockchain ✓- File type distribution

  - Encryption ✓- Top uploaders and downloaders

  - Smart Contracts ✓- Hourly activity patterns

  - Peer Verification ✓- Comprehensive blockchain statistics



---## Technology Stack



## 🚀 Quick Deploy Now- **Backend**: Python 3.13, Flask 3.0

- **Blockchain**: Custom implementation with Proof of Work (SHA-256)

### Option 1: Railway.app (Easiest)- **Encryption**: Cryptography library (AES via Fernet, PBKDF2HMAC)

- **Frontend**: HTML5, CSS3, JavaScript ES6+

```bash- **Charts**: Chart.js 4.4

# Install Railway CLI- **Storage**: Local file system + Blockchain metadata

npm install -g @railway/cli

## Installation

# Login and deploy

railway login1. **Clone or navigate to the project directory**:

railway init   ```bash

railway up   cd /Users/I527873/Documents/BITS/FileSharingSystem

```   ```



Your app will be live at: `https://your-app.railway.app`2. **Install Python dependencies**:

   ```bash

### Option 2: Render.com (Free Tier)   pip install -r requirements.txt

   ```

1. Go to [render.com](https://render.com)

2. Connect your GitHub repository## Running the Application

3. Render auto-detects `render.yaml`

4. Click "Create Web Service"1. **Start the Flask server**:

5. Your app deploys automatically!   ```bash

   python app.py

### Option 3: Docker (Self-Hosted)   ```



```bash2. **Open your browser** and navigate to:

# Build and run   ```

docker-compose up -d   http://localhost:5000

   ```

# Access at http://localhost:5001

```## How It Works



### Option 4: Heroku### Blockchain Structure



```bashEach block in the blockchain contains:

# Login and create app- **Index**: Block number in the chain

heroku login- **Timestamp**: When the block was created

heroku create your-app-name- **Data**: Transaction data (file upload/download)

- **Previous Hash**: Hash of the previous block

# Set environment variables- **Nonce**: Proof of Work nonce

heroku config:set FLASK_ENV=production- **Hash**: SHA-256 hash of the block

heroku config:set SECRET_KEY=$(openssl rand -hex 32)

### File Upload Process

# Deploy

git push heroku main1. User selects a file and enters their name

```2. File is uploaded to the server

3. SHA-256 hash is calculated for the file

---4. A new block is created with file metadata

5. Block is mined using Proof of Work (difficulty: 2)

## 📋 Pre-Deployment Checklist6. Block is added to the blockchain



Before deploying to production:### File Download Process



- [ ] Create `.env` file from `.env.example`1. User clicks download button

- [ ] Generate secure `SECRET_KEY`: `openssl rand -hex 32`2. File is retrieved from storage

- [ ] Set `FLASK_ENV=production`3. A download transaction is recorded on the blockchain

- [ ] Set `DEBUG=False`4. File is sent to the user

- [ ] Configure `CORS_ORIGINS` (not `*`)

- [ ] Push code to GitHub repository## API Endpoints

- [ ] Choose deployment platform

- [ ] Configure environment variables on platform### Core Endpoints

- [ ] Deploy and test!- `GET /` - Main web interface

- `POST /api/upload` - Upload a file (supports encryption, access control)

---- `GET /api/files` - Get all uploaded files

- `POST /api/download/<hash>` - Download a file (supports decryption)

## 🌐 Supported Platforms Summary- `GET /api/blockchain` - Get the entire blockchain

- `GET /api/blockchain/validate` - Validate blockchain integrity

| Platform | Free Tier | Setup Time | Best For |- `GET /api/stats` - Get comprehensive blockchain statistics

|----------|-----------|------------|----------|- `GET /api/file/<hash>` - Get detailed file information

| **Railway** | ✅ $5 credit | 2 min | Quick deploy, anyone |

| **Render** | ✅ Yes | 3 min | Free hosting |### Smart Contract Endpoints

| **Heroku** | ❌ $7/mo | 5 min | Mature platform |- `GET /api/contract/<hash>` - Get smart contract for a file

| **Vercel** | ✅ Yes | 2 min | Serverless |- `POST /api/contract/<hash>/grant` - Grant permission to a user

| **Docker** | Self-host | 5 min | Full control |- `POST /api/contract/<hash>/revoke` - Revoke permission from a user

| **DigitalOcean** | ❌ $5/mo | 5 min | Reliable VPS |

| **Google Cloud** | ✅ $300 credit | 10 min | Enterprise |### Peer Verification Endpoints

| **AWS** | ✅ 12 months | 15 min | Enterprise |- `POST /api/verify/<hash>` - Submit a verification vote

- `GET /api/verification/<hash>` - Get verification data for a file

---- `GET /api/verification/stats` - Get overall verification statistics

- `GET /api/verification/top-verifiers` - Get top verifiers leaderboard

## 🎯 Next Steps

### Analytics Endpoints

### For Local Development:- `GET /api/analytics` - Get detailed analytics data

- `GET /api/files/versions/<name>` - Get all versions of a file

```bash- `GET /api/files/search` - Search files with filters

# 1. Activate virtual environment (already done)

source .venv/bin/activate## File Support



# 2. Create .env fileSupported file types:

cp .env.example .env- Documents: txt, pdf, doc, docx

- Images: png, jpg, jpeg, gif

# 3. Run the application- Archives: zip

python app.py- Media: mp3, mp4



# 4. Visit http://localhost:5001Maximum file size: 100MB

```

## Security Features

### For Production Deployment:

- **End-to-End Encryption**: AES encryption using Fernet with PBKDF2 key derivation (100,000 iterations)

**Railway (Recommended):**- **File Integrity**: SHA-256 hashing for tamper detection

```bash- **Immutable Blockchain**: Prevents data tampering

railway up- **Proof of Work**: Computational consensus mechanism (difficulty: 2)

```- **Access Control**: Smart contract-based permissions

- **Secure File Handling**: Sanitized filenames and path validation

**Render:**- **Password Protection**: Strong password-based encryption for sensitive files

- Push to GitHub

- Connect repo on render.com## Project Structure

- Auto-deploys!

```

**Docker:**FileSharingSystem/

```bash├── app.py                      # Flask application and REST API

docker-compose up -d├── blockchain.py               # Blockchain implementation with analytics

```├── encryption.py               # File encryption/decryption utilities

├── smart_contract.py           # Smart contract for access control

---├── peer_verification.py        # Peer verification and voting system

├── requirements.txt            # Python dependencies

## 📖 Documentation Guide├── README.md                   # Comprehensive documentation

├── .gitignore                 # Git ignore rules

### Start Here:├── templates/

1. **[README.md](./README.md)** - Project overview and quick start│   └── index.html             # Advanced multi-tab UI

2. **[PLATFORMS.md](./PLATFORMS.md)** - Choose your platform (8+ options)├── static/

3. **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Detailed deployment steps│   ├── style.css              # Enhanced stylesheet with animations

│   └── script_advanced.js     # Advanced frontend logic with Chart.js

### Reference:└── uploads/                   # Uploaded files storage (encrypted/plain)

- **[.env.example](./.env.example)** - Environment variable template```

- **[test_local.py](./test_local.py)** - Run tests

- **[USER_IDENTIFICATION.md](./USER_IDENTIFICATION.md)** - Auth system details## Usage Examples



---### Upload an Encrypted File

```python

## 🔐 Security Reminders# Using the web interface:

1. Enter your name

### For Development (Local):2. Select a file

```bash3. Check "Encrypt file with password"

FLASK_ENV=development4. Enter a strong password

SECRET_KEY=dev-key-not-for-production5. Set access control options (public/private, expiration, max downloads)

DEBUG=True6. Click "Upload File"

CORS_ORIGINS=*```

```

### Download an Encrypted File

### For Production (Deployment):```python

```bash# The system will automatically prompt for password

FLASK_ENV=production# Enter the same password used during upload

SECRET_KEY=<generate-random-32-byte-hex>  # openssl rand -hex 32```

DEBUG=False

CORS_ORIGINS=https://your-domain.com### Verify a File

``````python

# Click "Verify" button on any file

**⚠️ IMPORTANT:**# Vote "Authentic" or "Suspicious"

- Always generate a new `SECRET_KEY` for production# Optionally add a comment

- Never commit `.env` file to Git (already in `.gitignore`)# Your reputation score increases with participation

- Restrict `CORS_ORIGINS` to your actual domain```

- Set `DEBUG=False` in production

### View Analytics

---```python

# Navigate to "Analytics" tab

## ✨ Features Ready for Deployment# View charts for:

# - Activity timeline

Your system includes:# - File type distribution

# - Top uploaders

### Core Blockchain# - Hourly activity patterns

- ✅ SHA-256 hashing```

- ✅ Proof of Work mining

- ✅ Chain validation## Advanced Configuration

- ✅ Block explorer

### Blockchain Difficulty

### File ManagementAdjust mining difficulty in `blockchain.py`:

- ✅ Upload with encryption```python

- ✅ Download with decryptionblockchain = Blockchain(difficulty=2)  # Higher = more secure, slower mining

- ✅ File versioning```

- ✅ Search & filter

### Encryption Iterations

### SecurityModify PBKDF2 iterations in `encryption.py`:

- ✅ AES-256 encryption```python

- ✅ Password protectioniterations=100000  # Higher = more secure, slower encryption

- ✅ Smart contracts```

- ✅ Access control

### File Size Limits

### Social FeaturesChange in `app.py`:

- ✅ Peer verification```python

- ✅ Reputation systemMAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB default

- ✅ User voting```

- ✅ Comments

## Future Enhancements

### Analytics

- ✅ Upload trends- [ ] Peer-to-peer distributed network

- ✅ File statistics- [ ] Multi-node consensus mechanism

- ✅ User leaderboards- [ ] IPFS integration for decentralized storage

- ✅ Chart.js visualizations- [ ] User authentication with JWT tokens

- [ ] File streaming for large files

---- [ ] Database persistence (PostgreSQL/MongoDB)

- [ ] WebSocket for real-time updates

## 🧪 Verify Your Setup- [ ] Mobile application (React Native)

- [ ] Advanced cryptographic features (digital signatures)

Run the test suite to ensure everything works:- [ ] Blockchain compression and pruning



```bash## License

python test_local.py

```This project is for educational purposes.



Expected output:---

```

🎉 All tests passed! Ready for local deployment.## 🚀 Deployment

Total: 8/8 tests passed

```### ⭐ Railway.app (Recommended - 2 Minutes)



---**Quick Deploy:**

```bash

## 📞 Need Help?railway login

railway init

### Deployment Issues:railway up

1. Check [DEPLOYMENT.md](./DEPLOYMENT.md) for platform-specific troubleshooting```

2. Run `python test_local.py` to diagnose local issues

3. Verify environment variables are set correctly**Or click:** [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

4. Check platform logs for errors

### 🌐 All Supported Platforms

### Common Issues:

| Platform | Cost | Ease | Deploy Time |

**"Module not found"**|----------|------|------|-------------|

```bash| **Railway** | Free tier | ⭐⭐⭐⭐⭐ | 2 minutes |

pip install -r requirements.txt| **Render** | Free tier | ⭐⭐⭐⭐⭐ | 3 minutes |

```| **Heroku** | $7/month | ⭐⭐⭐⭐ | 5 minutes |

| **Docker** | Self-host | ⭐⭐⭐⭐ | 5 minutes |

**"Port already in use"**

```bash**Complete guides available:**

# Change PORT in .env- 📖 [DEPLOYMENT.md](./DEPLOYMENT.md) - Detailed instructions for all platforms

PORT=5002- 📋 [PLATFORMS.md](./PLATFORMS.md) - Platform comparison guide

```- 🧪 [test_local.py](./test_local.py) - Test suite for local verification



**"Tests failing"**---

```bash

# Ensure venv is activated## 🔧 Environment Configuration

source .venv/bin/activate

```Create a `.env` file (copy from `.env.example`):



---```bash

# Flask Configuration

## 🎉 Deployment Options at a GlanceFLASK_ENV=development        # Use 'production' for deployment

SECRET_KEY=your-secret-key   # Generate: openssl rand -hex 32

### Fastest Deploy (2 minutes):DEBUG=True                   # Set to False in production

```bash

railway up# Server Configuration

```HOST=0.0.0.0

PORT=5001

### Free Hosting:

- Render.com (free tier)# Blockchain Configuration

- Vercel (free tier)BLOCKCHAIN_DIFFICULTY=2      # Higher = more secure, slower mining

- Google Cloud ($300 credit)

- AWS (12 months free)# Security

CORS_ORIGINS=*              # Restrict in production!

### Full Control:MAX_CONTENT_LENGTH=104857600  # 100MB file upload limit

```bash```

docker-compose up -d

```---



### Traditional VPS:## ✅ Local Setup Test

- DigitalOcean App Platform

- Custom VPS with DockerVerify everything works:



---```bash

# Run the test suite

## 🏆 Success!python test_local.py

```

Your blockchain file sharing system is production-ready! 

Expected output:

Choose your platform from [PLATFORMS.md](./PLATFORMS.md) and deploy using the instructions in [DEPLOYMENT.md](./DEPLOYMENT.md).```

🎉 All tests passed! Ready for local deployment.

**Quick deploy:** `railway up` 🚀Total: 8/8 tests passed

```

---

---

## 📊 System Status

## 📚 Complete Documentation

```

✅ Code: Ready- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Step-by-step deployment for Railway, Render, Heroku, Vercel, Docker, DigitalOcean, Google Cloud, AWS

✅ Tests: 8/8 Passing- **[PLATFORMS.md](./PLATFORMS.md)** - Detailed platform comparison with pros/cons

✅ Dependencies: Installed- **[USER_IDENTIFICATION.md](./USER_IDENTIFICATION.md)** - User authentication system details and limitations

✅ Configuration: Complete

✅ Documentation: Comprehensive---

✅ Deployment Configs: 8+ Platforms

```## 🐛 Troubleshooting



**Status: READY TO DEPLOY! 🎉**### Dependencies Not Found

```bash

---pip install -r requirements.txt

```

**Made with ❤️ - Deploy with confidence!**

### Port Already in Use

Get started: Choose a platform from [PLATFORMS.md](./PLATFORMS.md)```bash

# Change PORT in .env file
PORT=5002
```

### Tests Failing
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 🤝 Contributing

This is an educational project. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Run tests: `python test_local.py`
4. Submit a pull request

---

## 📝 Author & License

Created as an educational demonstration of blockchain technology in file sharing systems.

**Made with ❤️ for blockchain education**

---

## 🎉 Quick Commands

```bash
# Local development
python app.py

# Run tests
python test_local.py

# Deploy to Railway
railway up

# Docker deployment
docker-compose up -d
```

**Get started now:** Visit http://localhost:5001 after running `python app.py` 🚀
