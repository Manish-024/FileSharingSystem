# 💾 Persistence Feature - Multi-Device Support

## Overview

**YES! Files are now persistent across devices and server restarts!** 🎉

The blockchain file sharing system now uses **persistent storage** to save all data to disk, ensuring that your files, verifications, and smart contracts are available across multiple devices and survive server restarts.

---

## What's Persistent?

### 1. **Blockchain** 📦
- **All blocks** (genesis, uploads, downloads)
- **File metadata** (name, hash, size, uploader)
- **Transaction history**
- **Proof of Work** (nonces, hashes)

**Storage**: `data/blockchain.json`

### 2. **Peer Verifications** ✓
- **Verification votes** (authentic/suspicious)
- **User reputation scores**
- **Authenticity scores**
- **Vote history** with timestamps

**Storage**: `data/verifications.json`

### 3. **Smart Contracts** 📋
- **Access permissions** (granted users)
- **Access logs** (who accessed when)
- **Contract settings** (public/private, max downloads, expiration)
- **Permission expiration times**

**Storage**: `data/contracts.json`

---

## How It Works

### Automatic Saving

Every time you:
- ✅ Upload a file → Blockchain saved
- ✅ Download a file → Blockchain saved
- ✅ Vote on verification → Verifications saved
- ✅ Grant permission → Contracts saved
- ✅ Revoke permission → Contracts saved
- ✅ Access a file → Contract logs saved

### Automatic Loading

When the server starts:
- ✅ Loads existing blockchain from disk
- ✅ Loads all verifications and reputation data
- ✅ Loads all smart contracts and permissions

---

## Multi-Device Support

### Before Persistence ❌
```
Device A: Uploads file1.pdf
Device B: Can't see file1.pdf (different blockchain instance)
Server restart: All data lost
```

### After Persistence ✅
```
Device A: Uploads file1.pdf → Saved to data/blockchain.json
Device B: Sees file1.pdf immediately (reads from same file)
Server restart: All files and data restored automatically
```

---

## Technical Implementation

### Blockchain Persistence

```python
class Blockchain:
    def __init__(self, difficulty: int = 2, storage_path: str = "data/blockchain.json"):
        self.storage_path = storage_path
        
        # Load existing blockchain or create new
        if not self.load_from_disk():
            self.create_genesis_block()
    
    def save_to_disk(self):
        """Saves entire blockchain to JSON file"""
        # Called after every transaction
        
    def load_from_disk(self):
        """Loads blockchain from JSON file on startup"""
        # Reconstructs all blocks from saved data
```

### Verification Persistence

```python
class PeerVerification:
    def __init__(self, storage_path: str = "data/verifications.json"):
        self.storage_path = storage_path
        self.load_from_disk()
    
    def submit_verification(self, ...):
        # ... voting logic ...
        self.save_to_disk()  # Auto-save after vote
```

### Contract Persistence

```python
class ContractManager:
    def __init__(self, storage_path: str = "data/contracts.json"):
        self.storage_path = storage_path
        self.load_from_disk()
    
    def grant_permission(self, ...):
        # ... permission logic ...
        self.save_to_disk()  # Auto-save after grant
```

---

## Storage Format

### blockchain.json Structure
```json
{
  "difficulty": 2,
  "chain": [
    {
      "index": 0,
      "timestamp": 1732857600.0,
      "data": {
        "type": "file_upload",
        "file_name": "document.pdf",
        "file_hash": "abc123...",
        "file_size": 1024000,
        "uploader": "John"
      },
      "previous_hash": "0",
      "nonce": 193,
      "hash": "00abc123..."
    }
  ]
}
```

### verifications.json Structure
```json
{
  "verifications": {
    "abc123...": {
      "votes": [
        {
          "user": "Alice",
          "is_authentic": true,
          "comment": "Looks good",
          "timestamp": "2025-11-29T12:00:00",
          "reputation_weight": 1.0
        }
      ],
      "authenticity_score": 85.5,
      "total_votes": 5,
      "positive_votes": 4,
      "negative_votes": 1
    }
  },
  "reputation": {
    "Alice": 1.2,
    "Bob": 0.9
  }
}
```

### contracts.json Structure
```json
{
  "abc123...": {
    "file_hash": "abc123...",
    "owner": "John",
    "permissions": {
      "Alice": {
        "granted_at": "2025-11-29T12:00:00",
        "max_downloads": 5,
        "downloads_used": 2
      }
    },
    "access_log": [
      {
        "user": "Alice",
        "action": "download",
        "success": true,
        "timestamp": "2025-11-29T12:30:00"
      }
    ],
    "is_public": false
  }
}
```

---

## Data Directory Structure

```
data/
├── .gitkeep              # Keeps directory in git
├── blockchain.json       # All blockchain blocks
├── verifications.json    # Peer verification data
└── contracts.json        # Smart contract data
```

**Note**: The `data/` directory is in `.gitignore` (except `.gitkeep`) to prevent committing user data to version control.

---

## Benefits

### 1. **Multi-Device Access** 🌐
- All devices see the same files
- Upload from phone, download on laptop
- Shared blockchain across network

### 2. **Server Restart Resilience** 🔄
- No data loss on restart
- Automatic recovery
- Instant reload on startup

### 3. **Data Integrity** 🔒
- Atomic saves (all or nothing)
- JSON format (human-readable)
- Easy backup and restore

### 4. **Scalability** 📈
- Can migrate to database later
- Current JSON works for small-medium deployments
- Easy to export/import data

---

## Deployment Considerations

### Production Deployment

When deploying to platforms like Render.com, Railway, or Heroku:

#### ⚠️ Important: Ephemeral File Systems

Most free-tier platforms have **ephemeral file systems** that reset on:
- Server restart
- New deployment
- Platform maintenance

#### Solution Options:

##### Option 1: Database Migration (Recommended for Production)
```python
# Migrate to PostgreSQL/MongoDB for true persistence
# Example with SQLAlchemy:
from sqlalchemy import create_engine
engine = create_engine(os.environ.get('DATABASE_URL'))
```

##### Option 2: Cloud Storage (S3, Google Cloud Storage)
```python
# Save JSON files to cloud storage
import boto3
s3 = boto3.client('s3')
s3.upload_file('data/blockchain.json', 'my-bucket', 'blockchain.json')
```

##### Option 3: Persistent Volumes (Paid Tiers)
- Render.com: Use persistent disks (paid)
- Railway: Use volumes (paid)
- DigitalOcean: Use block storage

##### Option 4: Keep Current (Good for Testing)
- Works perfectly for local development
- Works for self-hosted servers
- Data resets on cloud platform restarts (acceptable for demos)

---

## Testing Persistence

### Test 1: Server Restart
```bash
# Upload a file
# Stop server (Ctrl+C)
# Restart server
python app.py
# Check if file still appears → ✅ Should work
```

### Test 2: Multi-Device
```bash
# Device A: Upload file at http://localhost:5005
# Device B: Access http://192.168.x.x:5005
# Device B should see the file → ✅ Should work
```

### Test 3: Data Recovery
```bash
# Backup data directory
cp -r data data_backup
# Delete data directory
rm -rf data
# Restore backup
mv data_backup data
# Restart server → ✅ All data restored
```

---

## Backup Strategy

### Manual Backup
```bash
# Backup all persistent data
tar -czf backup-$(date +%Y%m%d).tar.gz data/ uploads/

# Restore from backup
tar -xzf backup-20251129.tar.gz
```

### Automated Backup (Cron)
```bash
# Add to crontab (every day at 2 AM)
0 2 * * * tar -czf /backups/filesync-$(date +\%Y\%m\%d).tar.gz /path/to/data /path/to/uploads
```

### Cloud Backup Script
```python
# backup_to_cloud.py
import os
import boto3
from datetime import datetime

def backup_to_s3():
    s3 = boto3.client('s3')
    files = ['data/blockchain.json', 'data/verifications.json', 'data/contracts.json']
    
    for file in files:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        key = f"backups/{timestamp}_{os.path.basename(file)}"
        s3.upload_file(file, 'my-bucket', key)
        print(f"✓ Backed up {file} to S3")

if __name__ == '__main__':
    backup_to_s3()
```

---

## Monitoring

### Check Data Files
```bash
# View blockchain
cat data/blockchain.json | python -m json.tool

# Count blocks
cat data/blockchain.json | jq '.chain | length'

# View verifications
cat data/verifications.json | python -m json.tool

# View contracts
cat data/contracts.json | python -m json.tool
```

### Server Logs
```
✓ Loaded blockchain with 42 blocks from disk
✓ Loaded 15 verifications from disk
✓ Loaded 8 contracts from disk
```

---

## Troubleshooting

### Issue: Files not persisting
**Solution**: Check data directory permissions
```bash
ls -la data/
# Should be writable
chmod 755 data/
```

### Issue: Data corrupted
**Solution**: Delete and restart
```bash
rm data/*.json
# Server will create new blockchain on restart
```

### Issue: Different data on different devices
**Solution**: Ensure all devices point to same data directory
```bash
# Use network shared folder
# Or configure same database connection
```

---

## Future Enhancements

### Short-term
- [ ] Add data compression (gzip)
- [ ] Implement incremental saves (only changes)
- [ ] Add data validation on load

### Medium-term
- [ ] Migrate to SQLite (embedded database)
- [ ] Add real-time sync between instances
- [ ] Implement data replication

### Long-term
- [ ] Full PostgreSQL support
- [ ] Distributed blockchain (P2P sync)
- [ ] IPFS integration for file storage

---

## Summary

✅ **Persistence is FULLY IMPLEMENTED**

- ✅ Blockchain persists to `data/blockchain.json`
- ✅ Verifications persist to `data/verifications.json`
- ✅ Contracts persist to `data/contracts.json`
- ✅ Auto-save after every operation
- ✅ Auto-load on server startup
- ✅ Works across multiple devices
- ✅ Survives server restarts (on local/self-hosted)
- ⚠️ Cloud platforms may need database for true persistence

**For local development and self-hosted servers: Everything works perfectly!** 🎉

**For cloud deployment: Consider migrating to a database for production use.** 📊
