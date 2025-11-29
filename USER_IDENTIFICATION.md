# User Identification in the System

## 🆔 Current Implementation: Self-Declared Names

### How It Works Now

The system currently identifies users **by their self-declared name** - it's an **honor system** with **no authentication**.

#### 1. **User Input**
```javascript
// User enters their name in the "Your Name" field
<input type="text" id="uploader" name="uploader" placeholder="Enter your name" required>
```

#### 2. **Name Storage**
```javascript
// Name is saved in browser's localStorage
localStorage.setItem('userName', currentUser);

// Retrieved on page load
const savedUser = localStorage.getItem('userName');
```

#### 3. **Name Usage**
The name is sent to the server with every action:
- **Uploads**: Recorded as the "uploader"
- **Downloads**: Recorded as the "downloader"
- **Verifications**: Recorded as the "user" who voted

### ⚠️ Current Limitations

#### Major Security Issues:

1. **❌ No Authentication**
   - Anyone can enter any name
   - No password verification
   - No account system

2. **❌ Easy to Impersonate**
   ```javascript
   // User A uploads as "Alice"
   uploader: "Alice"
   
   // User B can download as "Alice" (just type the same name)
   downloader: "Alice"
   
   // System thinks it's the same person!
   ```

3. **❌ No Session Management**
   - No login/logout
   - No user sessions
   - No session tokens

4. **❌ Browser-Based Only**
   - Name stored in localStorage (per browser)
   - Different browsers = different identity
   - Incognito mode = anonymous each time

### How Smart Contracts "Identify" Users

The smart contract uses **string comparison** of names:

```python
# In smart_contract.py, line 72-73
if user == self.owner:
    return True, "Owner access"
```

**This means:**
- If you upload as "Alice", you're the owner
- If you download as "Alice", system thinks you're the same person
- If someone else types "Alice", system thinks they're you! ⚠️

### Real-World Scenario

Let's say you set max downloads = 2:

```
1. You upload file as "John" (you're the owner)
2. You download as "John" (owner, unlimited ✓)
3. Friend downloads as "Mike" (count: 1/2 ✓)
4. Friend downloads as "Sarah" (count: 2/2 ✓)
5. Stranger types "Mike" and downloads (system thinks they're Mike - but allowed since owner bypass works)

BUT:
6. Stranger types "John" and downloads → System thinks they're the OWNER! ⚠️
```

## 🔐 Proper User Identification Solutions

### Solution 1: Basic Authentication (Recommended for Learning)

Add username + password login:

```python
# New file: auth.py
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.user_id = secrets.token_hex(16)  # Unique ID
        
class AuthManager:
    def __init__(self):
        self.users = {}  # username -> User
        self.sessions = {}  # session_token -> username
    
    def register(self, username, password):
        if username in self.users:
            return False, "Username exists"
        self.users[username] = User(username, password)
        return True, "Registered"
    
    def login(self, username, password):
        user = self.users.get(username)
        if not user:
            return None, "User not found"
        if not check_password_hash(user.password_hash, password):
            return None, "Wrong password"
        
        # Create session
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = username
        return session_token, "Login successful"
    
    def verify_session(self, session_token):
        return self.sessions.get(session_token)
```

#### Frontend Changes:
```javascript
// Login form
async function login(username, password) {
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    
    // Store session token
    localStorage.setItem('sessionToken', data.session_token);
}

// Use session for all requests
const sessionToken = localStorage.getItem('sessionToken');
headers: {
    'Authorization': `Bearer ${sessionToken}`
}
```

### Solution 2: JWT (JSON Web Tokens)

More secure, stateless authentication:

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-here"

def create_token(username):
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### Solution 3: OAuth2 / Third-Party Authentication

Use existing identity providers:
- Google Sign-In
- GitHub OAuth
- Microsoft Account
- Firebase Authentication

### Solution 4: Blockchain-Based Identity (Advanced)

Use cryptographic keys for identity:

```python
# Each user has a private/public key pair
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class BlockchainIdentity:
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
    
    def sign_action(self, action_data):
        """Sign an action with private key"""
        signature = self.private_key.sign(
            action_data.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return signature
    
    def verify_signature(self, action_data, signature, public_key):
        """Verify action was signed by the claimed user"""
        try:
            public_key.verify(
                signature,
                action_data.encode(),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            return True
        except:
            return False
```

## 📊 Comparison of Solutions

| Solution | Security | Complexity | Best For |
|----------|----------|------------|----------|
| **Current (Name Only)** | ❌ Very Low | ✅ Very Simple | Demo/Learning |
| **Username + Password** | ⚠️ Medium | ⚠️ Medium | Small Projects |
| **JWT Tokens** | ✅ Good | ⚠️ Medium | Web Apps |
| **OAuth2** | ✅ Very Good | ❌ Complex | Production Apps |
| **Blockchain Identity** | ✅✅ Excellent | ❌ Very Complex | Decentralized Apps |

## 🛠️ Quick Fix for Current System

### Temporary Improvement (Without Full Auth)

Add a "secret phrase" for file owners:

```python
# In app.py upload endpoint
secret_phrase = request.form.get('secret_phrase', '')
file_secret = hashlib.sha256(secret_phrase.encode()).hexdigest()

# Store in blockchain
transaction = {
    # ... other fields ...
    "owner_secret_hash": file_secret
}

# In download endpoint, for owner verification
if user == file_info['uploader']:
    # Ask for secret phrase
    provided_secret = request.form.get('secret_phrase', '')
    provided_hash = hashlib.sha256(provided_secret.encode()).hexdigest()
    
    if provided_hash != file_info.get('owner_secret_hash'):
        return jsonify({'error': 'Not the real owner'}), 403
```

## 🎯 Recommended Implementation Path

For your learning project, I recommend implementing **Solution 1 (Basic Authentication)** because:

1. ✅ Teaches authentication fundamentals
2. ✅ Relatively simple to implement
3. ✅ Significantly more secure than current
4. ✅ Can be upgraded to JWT later
5. ✅ Demonstrates real-world concepts

### Implementation Steps:

1. **Create auth.py** - User management and session handling
2. **Add login/register endpoints** to app.py
3. **Create login UI** - Login/register forms
4. **Update all API calls** - Include session tokens
5. **Add middleware** - Verify tokens on protected routes
6. **Update smart contracts** - Use user_id instead of username

## 📝 Summary

### Current System:
- Uses **self-declared names** (honor system)
- **No authentication** or verification
- Easy to impersonate anyone
- Suitable for **demo/learning** only

### Why It's a Problem:
- Anyone can claim to be the owner
- Max downloads can be bypassed by changing names
- No real security or access control
- Not suitable for production use

### Recommended Next Steps:
1. Implement basic username/password authentication
2. Use session tokens or JWT for API calls
3. Store user_id (not username) in blockchain
4. Add login/logout functionality
5. Protect API endpoints with authentication middleware

Would you like me to implement a basic authentication system for your project? 🔐
