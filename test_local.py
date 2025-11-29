#!/usr/bin/env python3
"""
Local deployment test script
Tests that the application works correctly with the new configuration system
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    try:
        import app
        import blockchain
        import config
        import encryption
        import smart_contract
        import peer_verification
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration system"""
    print("\n🔍 Testing configuration...")
    try:
        from config import get_config
        
        # Test development config
        os.environ['FLASK_ENV'] = 'development'
        dev_config = get_config()
        print(f"✅ Development config loaded: {dev_config.__class__.__name__}")
        print(f"   DEBUG: {dev_config.DEBUG}")
        print(f"   PORT: {dev_config.PORT}")
        
        # Test production config
        os.environ['FLASK_ENV'] = 'production'
        prod_config = get_config()
        print(f"✅ Production config loaded: {prod_config.__class__.__name__}")
        print(f"   DEBUG: {prod_config.DEBUG}")
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_blockchain():
    """Test blockchain functionality"""
    print("\n🔍 Testing blockchain...")
    try:
        from blockchain import Blockchain
        
        bc = Blockchain()
        initial_length = len(bc.chain)
        
        # Add a test transaction
        bc.add_file_transaction(
            file_name="test_file.txt",
            file_hash="test_hash_123",
            file_size=1024,
            uploader="test_user",
            file_path="/test/path/test_file.txt",
            is_encrypted=False
        )
        
        if len(bc.chain) > initial_length:
            print(f"✅ Blockchain working: {len(bc.chain)} blocks")
            print(f"   Last block hash: {bc.chain[-1].hash[:16]}...")
            return True
        else:
            print("❌ Blockchain not adding blocks")
            return False
    except Exception as e:
        print(f"❌ Blockchain error: {e}")
        return False

def test_encryption():
    """Test encryption functionality"""
    print("\n🔍 Testing encryption...")
    try:
        from encryption import FileEncryption
        import tempfile
        import os
        
        password = "test_password_123"
        test_data = b"This is test data for encryption"
        
        # Create temporary test file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp.write(test_data)
            tmp_path = tmp.name
        
        # Encrypt
        encrypted_path, salt = FileEncryption.encrypt_file(tmp_path, password)
        print(f"✅ Encryption working: file encrypted")
        
        # Decrypt
        decrypted_path = FileEncryption.decrypt_file(encrypted_path, password, salt, tmp_path + ".dec")
        
        # Verify
        with open(decrypted_path, 'rb') as f:
            decrypted = f.read()
        
        # Cleanup
        os.unlink(tmp_path)
        os.unlink(encrypted_path)
        os.unlink(decrypted_path)
        
        if decrypted == test_data:
            print("✅ Decryption working: data matches")
            return True
        else:
            print("❌ Decryption failed: data mismatch")
            return False
    except Exception as e:
        print(f"❌ Encryption error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_smart_contract():
    """Test smart contract functionality"""
    print("\n🔍 Testing smart contracts...")
    try:
        from smart_contract import SmartContract
        
        contract = SmartContract(
            file_hash="test_hash_456",
            owner="owner_user"
        )
        
        # Configure as private with max downloads
        contract.set_public_access(False)
        contract.set_max_downloads(2)
        
        # Test access for owner (should always work)
        owner_access = contract.check_access("owner_user")
        print(f"✅ Owner access: {owner_access}")
        
        # Test access for non-owner
        user_access = contract.check_access("other_user")
        print(f"✅ User access (no permission): {user_access}")
        
        # Grant permission and test
        contract.grant_permission("other_user")
        user_access_granted = contract.check_access("other_user")
        print(f"✅ User access (with permission): {user_access_granted}")
        
        return True
    except Exception as e:
        print(f"❌ Smart contract error: {e}")
        return False

def test_peer_verification():
    """Test peer verification functionality"""
    print("\n🔍 Testing peer verification...")
    try:
        from peer_verification import PeerVerification
        
        verifier = PeerVerification()
        
        # Test verification submission
        verifier.submit_verification("test_hash_789", "user1", True, "Looks good")
        verifier.submit_verification("test_hash_789", "user2", True, "Verified")
        
        status = verifier.get_file_verification("test_hash_789")
        print(f"✅ Verification working: {status['positive_votes']} positive, {status['negative_votes']} negative")
        print(f"   Authenticity score: {status['authenticity_score']:.2f}")
        
        # Test reputation
        rep = verifier.get_user_reputation("user1")
        print(f"✅ Reputation system: user1 has {rep:.2f} reputation")
        
        return True
    except Exception as e:
        print(f"❌ Peer verification error: {e}")
        return False

def test_directories():
    """Test that required directories exist"""
    print("\n🔍 Testing directories...")
    try:
        required_dirs = ['uploads', 'templates', 'static']
        
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                print(f"✅ Directory exists: {dir_name}/")
            else:
                print(f"⚠️  Creating directory: {dir_name}/")
                dir_path.mkdir(exist_ok=True)
        
        return True
    except Exception as e:
        print(f"❌ Directory error: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are installed"""
    print("\n🔍 Testing dependencies...")
    required_packages = [
        'flask',
        'flask_cors',
        'cryptography',
        'gunicorn',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all tests"""
    print("="*60)
    print("🚀 Local Deployment Test Suite")
    print("="*60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Directories", test_directories),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Blockchain", test_blockchain),
        ("Encryption", test_encryption),
        ("Smart Contracts", test_smart_contract),
        ("Peer Verification", test_peer_verification),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for local deployment.")
        print("\nTo run the app locally:")
        print("  1. Create .env file: cp .env.example .env")
        print("  2. Run: python app.py")
        print("  3. Visit: http://localhost:5001")
        return 0
    else:
        print("⚠️  Some tests failed. Check errors above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Create .env file: cp .env.example .env")
        return 1

if __name__ == "__main__":
    sys.exit(main())
