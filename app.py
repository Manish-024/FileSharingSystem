from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import hashlib
from blockchain import Blockchain
from smart_contract import ContractManager
from peer_verification import PeerVerification
from encryption import FileEncryption
from config import get_config
import json
import base64

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config = get_config()
app.config.from_object(config)

# Setup CORS
CORS(app, origins=config.CORS_ORIGINS)

# Configuration shortcuts
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
MAX_FILE_SIZE = app.config['MAX_CONTENT_LENGTH']

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize blockchain and advanced features
blockchain = Blockchain(difficulty=app.config['BLOCKCHAIN_DIFFICULTY'])
contract_manager = ContractManager()
peer_verification = PeerVerification()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a file and add to blockchain"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        uploader = request.form.get('uploader', 'Anonymous')
        encrypt = request.form.get('encrypt', 'false').lower() == 'true'
        password = request.form.get('password', '')
        is_public = request.form.get('is_public', 'true').lower() == 'true'
        max_downloads = request.form.get('max_downloads')
        expiration_hours = request.form.get('expiration_hours')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Handle duplicate filenames and versions
        base_name, extension = os.path.splitext(filename)
        version = 1
        previous_version_hash = None
        
        # Check for existing versions
        existing_files = blockchain.get_all_files()
        for existing in existing_files:
            if existing['file_name'].startswith(base_name):
                version = existing.get('version', 1) + 1
                previous_version_hash = existing['file_hash']
        
        if version > 1:
            filename = f"{base_name}_v{version}{extension}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(file_path)
        
        # Encryption handling
        salt = None
        is_encrypted = False
        if encrypt and password:
            try:
                encrypted_path, salt_bytes = FileEncryption.encrypt_file(file_path, password)
                # Remove original file and use encrypted one
                os.remove(file_path)
                os.rename(encrypted_path, file_path)
                salt = base64.b64encode(salt_bytes).decode('utf-8')
                is_encrypted = True
            except Exception as e:
                return jsonify({'error': f'Encryption failed: {str(e)}'}), 500
        
        # Calculate file hash and size
        file_hash = calculate_file_hash(file_path)
        file_size = os.path.getsize(file_path)
        
        # Add to blockchain
        block = blockchain.add_file_transaction(
            file_name=filename,
            file_hash=file_hash,
            file_size=file_size,
            uploader=uploader,
            file_path=file_path,
            is_encrypted=is_encrypted,
            salt=salt,
            version=version,
            previous_version_hash=previous_version_hash
        )
        
        # Create smart contract
        contract = contract_manager.create_contract(file_hash, uploader)
        contract.set_public_access(is_public)
        
        if max_downloads:
            contract.set_max_downloads(int(max_downloads))
        
        if expiration_hours:
            contract.set_expiration(int(expiration_hours))
        
        return jsonify({
            'message': 'File uploaded successfully',
            'file_name': filename,
            'file_hash': file_hash,
            'file_size': file_size,
            'is_encrypted': is_encrypted,
            'version': version,
            'block': block,
            'contract_id': contract.contract_id
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/files', methods=['GET'])
def get_files():
    """Get all files from blockchain"""
    try:
        files = blockchain.get_all_files()
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<file_hash>', methods=['POST'])
def download_file(file_hash):
    """Download a file by its hash"""
    try:
        data = request.get_json()
        downloader = data.get('downloader', 'Anonymous')
        password = data.get('password', '')
        
        # Get file info from blockchain
        file_info = blockchain.get_file_by_hash(file_hash)
        
        if not file_info:
            return jsonify({'error': 'File not found'}), 404
        
        # Check smart contract access
        contract = contract_manager.get_contract(file_hash)
        if contract:
            has_access, reason = contract.check_access(downloader)
            if not has_access:
                contract.log_access(downloader, "download", False, reason)
                contract_manager.save_to_disk()  # Persist access log
                return jsonify({'error': f'Access denied: {reason}'}), 403
            contract.log_access(downloader, "download", True, reason)
            contract_manager.save_to_disk()  # Persist access log
        
        file_path = file_info['file_path']
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found on server'}), 404
        
        # Handle encrypted files
        if file_info.get('is_encrypted'):
            if not password:
                return jsonify({'error': 'Password required for encrypted file'}), 400
            
            try:
                # Get salt from file info
                salt_b64 = file_info.get('salt')
                if not salt_b64:
                    return jsonify({'error': 'Encryption data missing'}), 500
                
                salt = base64.b64decode(salt_b64)
                
                # Decrypt file temporarily
                decrypted_path = FileEncryption.decrypt_file(
                    file_path, password, salt
                )
                
                # Record download in blockchain
                blockchain.add_download_transaction(
                    file_name=file_info['file_name'],
                    file_hash=file_hash,
                    downloader=downloader
                )
                
                # Send decrypted file
                response = send_file(
                    decrypted_path, 
                    as_attachment=True,
                    download_name=file_info['file_name'].replace('.encrypted', '')
                )
                
                # Clean up decrypted file after sending
                try:
                    os.remove(decrypted_path)
                except:
                    pass
                
                return response
                
            except ValueError as e:
                return jsonify({'error': 'Invalid password'}), 401
            except Exception as e:
                return jsonify({'error': f'Decryption failed: {str(e)}'}), 500
        
        # Record download in blockchain
        blockchain.add_download_transaction(
            file_name=file_info['file_name'],
            file_hash=file_hash,
            downloader=downloader
        )
        
        return send_file(file_path, as_attachment=True, 
                        download_name=file_info['file_name'])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    """Get the entire blockchain"""
    try:
        chain = blockchain.get_chain()
        return jsonify({'chain': chain}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/blockchain/validate', methods=['GET'])
def validate_blockchain():
    """Validate the blockchain"""
    try:
        is_valid = blockchain.is_chain_valid()
        return jsonify({'is_valid': is_valid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get blockchain statistics"""
    try:
        stats = blockchain.get_chain_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/file/<file_hash>', methods=['GET'])
def get_file_info(file_hash):
    """Get information about a specific file"""
    try:
        file_info = blockchain.get_file_by_hash(file_hash)
        
        if not file_info:
            return jsonify({'error': 'File not found'}), 404
        
        # Add verification data
        verification = peer_verification.get_file_verification(file_hash)
        file_info['verification'] = verification
        
        # Add contract info
        contract = contract_manager.get_contract(file_hash)
        if contract:
            file_info['contract'] = contract.get_stats()
        
        return jsonify(file_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Smart Contract Endpoints
@app.route('/api/contract/<file_hash>', methods=['GET'])
def get_contract(file_hash):
    """Get smart contract for a file"""
    try:
        contract = contract_manager.get_contract(file_hash)
        if not contract:
            return jsonify({'error': 'Contract not found'}), 404
        
        return jsonify(contract.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contract/<file_hash>/grant', methods=['POST'])
def grant_permission(file_hash):
    """Grant permission to a user"""
    try:
        data = request.get_json()
        user = data.get('user')
        duration_hours = data.get('duration_hours')
        max_downloads = data.get('max_downloads')
        
        contract = contract_manager.get_contract(file_hash)
        if not contract:
            return jsonify({'error': 'Contract not found'}), 404
        
        contract.grant_permission(user, duration_hours, max_downloads)
        contract_manager.save_to_disk()  # Persist changes
        
        return jsonify({
            'message': f'Permission granted to {user}',
            'contract': contract.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contract/<file_hash>/revoke', methods=['POST'])
def revoke_permission(file_hash):
    """Revoke permission from a user"""
    try:
        data = request.get_json()
        user = data.get('user')
        
        contract = contract_manager.get_contract(file_hash)
        if not contract:
            return jsonify({'error': 'Contract not found'}), 404
        
        success = contract.revoke_permission(user)
        contract_manager.save_to_disk()  # Persist changes
        
        if success:
            return jsonify({'message': f'Permission revoked from {user}'}), 200
        else:
            return jsonify({'error': 'User has no permission'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Peer Verification Endpoints
@app.route('/api/verify/<file_hash>', methods=['POST'])
def verify_file(file_hash):
    """Submit a verification vote for a file"""
    try:
        data = request.get_json()
        user = data.get('user', 'Anonymous')
        is_authentic = data.get('is_authentic', True)
        comment = data.get('comment', '')
        
        peer_verification.submit_verification(file_hash, user, is_authentic, comment)
        
        verification_data = peer_verification.get_file_verification(file_hash)
        
        return jsonify({
            'message': 'Verification submitted',
            'verification': verification_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/verification/<file_hash>', methods=['GET'])
def get_verification(file_hash):
    """Get verification data for a file"""
    try:
        verification = peer_verification.get_file_verification(file_hash)
        return jsonify(verification), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/verification/stats', methods=['GET'])
def get_verification_stats():
    """Get overall verification statistics"""
    try:
        stats = peer_verification.get_verification_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/verification/top-verifiers', methods=['GET'])
def get_top_verifiers():
    """Get top verifiers"""
    try:
        limit = request.args.get('limit', 10, type=int)
        verifiers = peer_verification.get_top_verifiers(limit)
        return jsonify({'verifiers': verifiers}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Analytics Endpoints
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get detailed analytics data"""
    try:
        analytics = blockchain.get_analytics_data()
        return jsonify(analytics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/files/versions/<base_name>', methods=['GET'])
def get_file_versions(base_name):
    """Get all versions of a file"""
    try:
        versions = blockchain.get_file_versions(base_name)
        return jsonify({'versions': versions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/files/search', methods=['GET'])
def search_files():
    """Search files with filters"""
    try:
        query = request.args.get('q', '').lower()
        uploader = request.args.get('uploader', '').lower()
        file_type = request.args.get('type', '').lower()
        encrypted_only = request.args.get('encrypted', 'false').lower() == 'true'
        
        files = blockchain.get_all_files()
        
        # Apply filters
        filtered_files = []
        for file in files:
            # Query filter
            if query and query not in file['file_name'].lower():
                continue
            
            # Uploader filter
            if uploader and uploader not in file.get('uploader', '').lower():
                continue
            
            # File type filter
            if file_type:
                ext = file['file_name'].split('.')[-1].lower()
                if ext != file_type:
                    continue
            
            # Encryption filter
            if encrypted_only and not file.get('is_encrypted', False):
                continue
            
            # Add verification status
            verification = peer_verification.get_file_verification(file['file_hash'])
            file['verification_status'] = verification['status']
            file['authenticity_score'] = verification['authenticity_score']
            
            filtered_files.append(file)
        
        return jsonify({
            'files': filtered_files,
            'total': len(filtered_files)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting Advanced Blockchain File Sharing System...")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Server running at http://{app.config['HOST']}:{app.config['PORT']}")
    print("\nFeatures enabled:")
    print("  ✓ File Encryption/Decryption")
    print("  ✓ Smart Contracts for Access Control")
    print("  ✓ Peer Verification System")
    print("  ✓ Advanced Analytics")
    print("  ✓ File Versioning")
    print("  ✓ Search & Filter")
    
    # Run the app
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
