# Quick Start Guide

## 🚀 Getting Started in 3 Minutes

### Step 1: Open the Application
Open your web browser and navigate to:
```
http://localhost:5001
```

### Step 2: Upload Your First File

1. **Enter your name** in the "Your Name" field
2. **Select a file** to upload
3. **Optional**: Enable encryption by checking "Encrypt file with password"
   - Enter a strong password (you'll need this to download)
4. **Optional**: Configure access control:
   - Uncheck "Public file" for private access
   - Set "Max Downloads" to limit how many times it can be downloaded
   - Set "Expiration Hours" to auto-expire the file
5. **Click "Upload File"**
6. Wait for the block to be mined (takes a few seconds)

### Step 3: Explore the Features

#### 📁 View Files
- Scroll down to see all uploaded files
- Files show encryption status (🔒), verification status (✓), and version (v1, v2, etc.)

#### ⬇️ Download Files
- Click "Download" button
- For encrypted files, you'll be prompted for the password
- Downloads are recorded on the blockchain

#### ✓ Verify Files
- Click "Verify" button on any file
- Vote "Authentic" or "Suspicious"
- Help the community identify safe files
- Your reputation increases with participation

#### 📊 View Analytics
- Click the "Analytics" tab at the top
- See beautiful charts showing:
  - Activity over time
  - File type distribution
  - Top uploaders
  - Hourly activity patterns

#### ⛓️ Explore Blockchain
- Click the "Blockchain" tab
- View all blocks and transactions
- See hashes, timestamps, and Proof of Work nonces

#### 🔍 Search Files
- Use the search bar to find files by name
- Filter by file type (PDF, JPG, etc.)
- Filter encrypted files only

## 🎯 Common Use Cases

### Use Case 1: Share a Confidential Document
```
1. Select your document
2. ✓ Check "Encrypt file with password"
3. Enter a strong password
4. ✗ Uncheck "Public file"
5. Grant permission to specific users (coming soon)
6. Upload
7. Share the password separately with authorized users
```

### Use Case 2: Share a Public File with Limits
```
1. Select your file
2. ✓ Keep "Public file" checked
3. Set "Max Downloads" to 100
4. Set "Expiration Hours" to 24
5. Upload
6. File will auto-expire after 24 hours or 100 downloads
```

### Use Case 3: Upload Multiple Versions
```
1. Upload "report.pdf" - becomes v1
2. Make changes to the file
3. Upload "report.pdf" again - becomes v2
4. System automatically tracks versions
5. View version history in file details
```

## 🔐 Security Best Practices

### For Encryption
- Use strong passwords (12+ characters, mix of letters, numbers, symbols)
- Don't reuse passwords across files
- Store passwords securely (use a password manager)
- Remember: If you lose the password, the file cannot be decrypted

### For Verification
- Only vote on files you've actually checked
- Be honest in your assessments
- Add comments to explain suspicious files
- Build your reputation by consistent participation

## 📈 Understanding the Dashboard

### Statistics Explained
- **Total Blocks**: Number of blocks in the blockchain (increases with uploads/downloads)
- **Total Uploads**: Number of files uploaded
- **Total Downloads**: Number of download transactions
- **🔒 Encrypted**: Files protected with passwords
- **✓ Verified**: Files with authenticity score ≥75%
- **Chain Valid**: ✓ = blockchain integrity confirmed

### Verification Status
- **✓ Verified** (Green): Authenticity score ≥75% - Safe to download
- **⚠ Disputed** (Orange): Authenticity score 50-74% - Use caution
- **✗ Suspicious** (Red): Authenticity score <50% - Avoid downloading
- **Unverified** (Gray): No votes yet

## 🛠️ Troubleshooting

### File won't upload
- Check file type is allowed (txt, pdf, png, jpg, gif, doc, docx, zip, mp3, mp4)
- Ensure file is under 100MB
- Make sure you entered a name

### Can't download encrypted file
- Verify you have the correct password
- Password is case-sensitive
- Contact the uploader if you don't have the password

### Charts not loading
- Make sure you're on the "Analytics" tab
- Refresh the page if charts don't appear
- Check browser console for errors

### Search not working
- Try simpler search terms
- Use filters to narrow results
- Click "Refresh" to reload all files

## 💡 Pro Tips

1. **Save your name**: The system remembers your name in localStorage
2. **Check file details**: Click "Details" button for comprehensive info
3. **Monitor your uploads**: Track downloads and verification scores
4. **Build reputation**: Verify files regularly to increase your reputation score
5. **Use versioning**: Upload updated versions of files without losing history
6. **Explore blockchain**: Learn how each action creates a new block
7. **Set smart limits**: Use max downloads and expiration for sensitive files

## 🎓 Learning Resources

### Understanding Blockchain
- Each block contains: Index, Timestamp, Data, Previous Hash, Nonce, Hash
- Blocks are linked by hashes creating an immutable chain
- Proof of Work ensures computational security
- Any tampering invalidates the entire chain

### Understanding Encryption
- Files are encrypted with AES via Fernet
- Password is converted to key using PBKDF2 (100,000 iterations)
- Original file is deleted after encryption
- Decryption happens on-the-fly during download

### Understanding Smart Contracts
- Rules governing file access
- Can set public/private access
- Time-based expiration
- Download count limits
- User-specific permissions

## 🤝 Contributing

Want to verify files and build reputation?
1. Download and check files for authenticity
2. Vote honestly on file quality
3. Add helpful comments
4. Check the "Verification" tab to see your rank

Enjoy your advanced blockchain file sharing system! 🎉
