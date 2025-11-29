# 🔍 Hash Code Visibility Guide

## Where Can I See Hash Codes?

This guide shows you **exactly where** to find hash codes throughout the application.

---

## 🏠 Home Tab

### 1. **Hash Tracker Banner** (Top of Page)
- **Location**: Purple gradient banner at the very top
- **Shows**: Currently active hash during operations
- **When**: Appears automatically during:
  - File upload
  - File download
  - Viewing file details
  - Initiating any download
- **Features**: 
  - Copy button (📋)
  - Auto-hides after 10 seconds
  - Shows full 64-character SHA-256 hash

### 2. **Chain Valid Card** (Statistics Section)
- **Location**: In the stats grid, bottom right card
- **Action**: **CLICK IT** to see detailed verification
- **Shows**: 
  - ✅ Blockchain Valid/Invalid status
  - Complete verification modal with ALL hashes

### 3. **Verify Blockchain Button** (Purple Gradient Card)
- **Location**: Below statistics, above search
- **Text**: "🔍 Verify Now & Show All Hashes"
- **Action**: Click to see **detailed blockchain verification modal**
- **Shows**:
  - **Block Hashes**: Every block's SHA-256 hash with validation status
  - **Previous Hashes**: Chain linkage verification
  - **File Hashes**: SHA-256 of uploaded files
  - **Proof of Work**: Nonce values
  - **Copy buttons** for each hash

### 4. **File Listings** (Shared Files Section)
- **Location**: Each file card in the files list
- **Shows**: Full 64-character file hash
- **Style**: Pink text (#d63384) with gray background
- **Format**: `Hash: abc123...` (full hash, not truncated)

### 5. **Upload Success**
- **When**: Right after uploading a file
- **Shows**:
  - Alert popup with full hash
  - Hash tracker banner at top
  - Success message with hash

### 6. **Download Modal**
- **When**: Click "Download" on any file
- **Shows**: Yellow highlighted box with full file hash
- **Features**: Visible before password entry

### 7. **File Details Modal**
- **Action**: Click on file name or "Details" button
- **Shows**:
  - Yellow box with full file hash
  - Copy button (📋)
  - Hash tracker banner displays automatically

---

## ⛓️ Blockchain Tab

### 8. **Block Explorer**
- **Location**: Blockchain tab (click "⛓️ Blockchain" at top)
- **Shows**: Every block with:
  - **Block Hash**: Blue background box
  - **Previous Hash**: Gray text
  - **File Hash**: Blue background (for upload blocks)
- **Format**: Full 64-character hashes, not truncated

---

## 📊 Analytics Tab

### 9. **Activity Timeline**
- Shows transaction hashes in chart tooltips
- Hover over data points to see hash details

---

## ✓ Verification Tab

### 10. **Peer Verification Stats**
- Shows verified files with their hashes
- Verification scores linked to file hashes

---

## 🔍 Detailed Blockchain Verification Modal

### Access Methods:
1. **Click** the "Chain Valid" card (stats section)
2. **Click** the purple "Verify Now" button
3. **Click** any verification link

### What You'll See:

#### ✅ Overall Status
- Large banner showing "✅ Blockchain VALID" or "❌ Blockchain INVALID"
- Total blocks verified count

#### 📊 Verification Summary
- Total Blocks
- Valid Hashes count
- Files count

#### 📋 Detailed Block Information

**For Each Block:**

1. **Block Number & Status**
   - Block #0, #1, #2, etc.
   - ✅ or ⚠️ status indicator

2. **File Information** (if upload block)
   - 📄 File name (yellow background)
   - 📎 File Hash (blue background)
     - Full 64-character SHA-256 hash
     - Copy button (📋)

3. **Block Hash** (green or red background)
   - 🔗 Hash validation status (✓ or ✗)
   - Full 64-character hash
   - Copy button (📋)

4. **Previous Hash** (blue or red background)
   - ⬅️ Chain linkage status (✓ Linked or ✗ Broken)
   - Full 64-character hash
   - Shows connection to previous block

5. **Proof of Work**
   - ⛏️ Nonce value
   - ✅ PoW validation status

---

## 🎨 Hash Display Styles

### Color Coding:
- **Pink (#d63384)**: File hashes in listings
- **Blue (#0d6efd)**: Block hashes, file hashes in explorer
- **Gray (#6c757d)**: Previous block hashes
- **Yellow (#fef3c7)**: File info in verification modal
- **Green (#10b981)**: Valid/verified status
- **Red (#ef4444)**: Invalid/error status
- **Purple (#667eea-#764ba2)**: Hash tracker banner

### Copy Features:
- Every major hash display has a **📋 Copy** button
- Clicking copies full hash to clipboard
- Shows confirmation message
- Updates hash tracker banner

---

## 📝 Hash Information Summary

### What Hashes You Can See:

1. **File Hashes** (SHA-256)
   - Calculated from file content
   - 64 hexadecimal characters
   - Unique identifier for each file
   - **Locations**: Listings, details, download, upload, verification modal

2. **Block Hashes** (SHA-256)
   - Calculated from block data
   - Includes previous hash, timestamp, nonce, data
   - Proof of Work validated (starts with "00")
   - **Locations**: Blockchain explorer, verification modal

3. **Previous Block Hashes**
   - Links blocks together in chain
   - **Locations**: Blockchain explorer, verification modal

---

## 🎯 Quick Access Tips

### Want to see hashes quickly?
1. **Best Option**: Click purple "🔍 Verify Now & Show All Hashes" button
2. **Second Best**: Click "Chain Valid" card
3. **For specific file**: Click file name to see its hash

### Want to copy a hash?
- Every hash display has a copy button (📋)
- Hashes are shown in monospace font for easy selection
- Can also manually select and copy

### Want to verify blockchain integrity?
- Click "Verify Now" button
- See complete validation report
- Every block's hash is verified and displayed

---

## 🚀 Coming Soon

- Hash history panel showing recent operations
- Hash search functionality
- Hash comparison tools
- Block-to-block hash verification visualization

---

## 💡 Pro Tips

1. **Hash Tracker**: Appears automatically on every operation - watch the top of the page!
2. **Verification Modal**: Most comprehensive view of all hashes in the system
3. **Copy Buttons**: Use them instead of manual selection - faster and error-free
4. **Color Codes**: Learn the colors to quickly identify hash types
5. **Mobile**: All hash displays are mobile-responsive with horizontal scrolling

---

## ❓ Still Can't Find Hashes?

### Troubleshooting:
1. **Refresh the page**: Hashes load with blockchain data
2. **Upload a file**: Creates new hashes to see
3. **Click "Verify Now"**: Shows all existing hashes
4. **Check browser console**: Debug information available
5. **Clear cache**: Force reload of latest version

---

**Remember**: Hashes are EVERYWHERE now! Every interaction shows them prominently. 🎉
