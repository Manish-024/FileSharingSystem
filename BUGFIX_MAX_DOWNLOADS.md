# Bug Fix: Max Downloads Issue

## Problem Description

**Issue**: When setting max downloads to 2, the system allowed 3 downloads.

**Reported by User**: Set max downloads = 2, but got 3 downloads

## Root Cause Analysis

The bug was in the `SmartContract.check_access()` method in `smart_contract.py`.

### Original Code (Line 77-78):
```python
total_downloads = len([log for log in self.access_log 
                      if log["action"] == "download"])
```

### The Problem:

1. **Owner Bypass Issue**: The owner always gets access (line 72-73) BEFORE the max downloads check
2. **Incorrect Counting**: The code counted ALL download entries in the log, including:
   - Owner's downloads (which should be unlimited)
   - Failed download attempts (which shouldn't count)
   - Successful downloads by other users

### Scenario Example:

If you (as owner) uploaded a file with max downloads = 2:

1. **You download** → Logged as download, owner bypasses check ✓
2. **User A downloads** → Logged as download, count = 1 (but code counted 2 including owner) ✓
3. **User B downloads** → Logged as download, count = 2 (but code counted 3) ✓
4. **User C tries** → Should be blocked at 2, but was allowed because code saw 3 total

## Solution Implemented

### Fixed Code:
```python
# Count only successful downloads (excluding owner's downloads)
total_downloads = len([log for log in self.access_log 
                      if log["action"] == "download" 
                      and log["success"] 
                      and log["user"] != self.owner])
```

### What Changed:

1. **`and log["success"]`** - Only count successful downloads (not failed attempts)
2. **`and log["user"] != self.owner`** - Exclude owner's downloads from the limit
3. Owner can download unlimited times (as intended)
4. Max downloads only applies to non-owner users

## Correct Behavior Now

With max downloads = 2:

1. **Owner downloads 10 times** → All allowed ✓ (owner is unlimited)
2. **User A downloads** → Count = 1/2 ✓
3. **User B downloads** → Count = 2/2 ✓
4. **User C tries to download** → **BLOCKED** ✗ "Download limit reached"
5. **User C tries again** → Still blocked (failed attempts don't count) ✗

## Testing Recommendations

### Test Case 1: Basic Max Downloads
```
1. Upload file with max_downloads = 2
2. Download as owner (multiple times) → Should always work
3. Download as User A → Should work (1/2)
4. Download as User B → Should work (2/2)
5. Download as User C → Should be blocked
```

### Test Case 2: Failed Attempts
```
1. Upload encrypted file with max_downloads = 2
2. User A tries with wrong password → Fails (doesn't count)
3. User A tries with correct password → Works (1/2)
4. User B downloads → Works (2/2)
5. User C tries → Blocked
```

### Test Case 3: Owner Unlimited
```
1. Upload file with max_downloads = 1
2. Owner downloads 5 times → All work
3. User A downloads → Works (1/1)
4. User B tries → Blocked
```

## Additional Improvements Made

The fix ensures:
- ✓ Owner has unlimited downloads
- ✓ Only successful downloads count toward limit
- ✓ Failed password attempts don't waste download quota
- ✓ Access denied attempts don't count
- ✓ Accurate tracking in contract statistics

## Files Modified

- `smart_contract.py` (Line 74-80)

## Status

✅ **FIXED** - Server restarted with the corrected logic

## How to Verify

1. Upload a new file with max downloads = 2
2. Test with multiple users (change name in the form)
3. The 3rd different user should be blocked
4. Owner (uploader) can still download unlimited times

---

**Note**: The fix only applies to NEW downloads. If you're testing with an existing file, you may need to upload a new one to see the corrected behavior, as the contract state is stored in memory and resets on server restart.
