import hashlib
import json
import time
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Mine the block using Proof of Work"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    """Blockchain for file sharing system with persistent storage"""
    
    def __init__(self, difficulty: int = 2, storage_path: str = "data/blockchain.json"):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict[str, Any]] = []
        self.storage_path = storage_path
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        # Load existing blockchain or create new one
        if not self.load_from_disk():
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, time.time(), {
            "type": "genesis",
            "message": "Genesis Block - File Sharing System"
        }, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.save_to_disk()
    
    def save_to_disk(self):
        """Save blockchain to disk for persistence"""
        try:
            blockchain_data = {
                "difficulty": self.difficulty,
                "chain": [block.to_dict() for block in self.chain]
            }
            with open(self.storage_path, 'w') as f:
                json.dump(blockchain_data, f, indent=2)
        except Exception as e:
            print(f"Error saving blockchain: {e}")
    
    def load_from_disk(self) -> bool:
        """Load blockchain from disk"""
        try:
            if not os.path.exists(self.storage_path):
                return False
            
            with open(self.storage_path, 'r') as f:
                blockchain_data = json.load(f)
            
            self.difficulty = blockchain_data.get("difficulty", self.difficulty)
            
            # Reconstruct blocks
            for block_dict in blockchain_data.get("chain", []):
                block = Block(
                    index=block_dict["index"],
                    timestamp=block_dict["timestamp"],
                    data=block_dict["data"],
                    previous_hash=block_dict["previous_hash"],
                    nonce=block_dict["nonce"]
                )
                block.hash = block_dict["hash"]
                self.chain.append(block)
            
            print(f"✓ Loaded blockchain with {len(self.chain)} blocks from disk")
            return len(self.chain) > 0
            
        except Exception as e:
            print(f"Error loading blockchain: {e}")
            return False
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_file_transaction(self, file_name: str, file_hash: str, 
                            file_size: int, uploader: str, 
                            file_path: str, is_encrypted: bool = False,
                            salt: str = None, version: int = 1,
                            previous_version_hash: str = None) -> Dict[str, Any]:
        """Add a file sharing transaction to the blockchain"""
        transaction = {
            "type": "file_upload",
            "file_name": file_name,
            "file_hash": file_hash,
            "file_size": file_size,
            "uploader": uploader,
            "file_path": file_path,
            "is_encrypted": is_encrypted,
            "salt": salt,
            "version": version,
            "previous_version_hash": previous_version_hash,
            "timestamp": datetime.now().isoformat()
        }
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=transaction,
            previous_hash=self.get_latest_block().hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_to_disk()  # Persist to disk
        
        return new_block.to_dict()
    
    def add_download_transaction(self, file_name: str, file_hash: str, 
                                 downloader: str) -> Dict[str, Any]:
        """Record a file download transaction"""
        transaction = {
            "type": "file_download",
            "file_name": file_name,
            "file_hash": file_hash,
            "downloader": downloader,
            "timestamp": datetime.now().isoformat()
        }
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=transaction,
            previous_hash=self.get_latest_block().hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_to_disk()  # Persist to disk
        
        return new_block.to_dict()
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof of work
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def get_all_files(self) -> List[Dict[str, Any]]:
        """Get all uploaded files from the blockchain"""
        files = []
        file_dict = {}
        
        for block in self.chain:
            if block.data.get("type") == "file_upload":
                file_hash = block.data.get("file_hash")
                file_dict[file_hash] = {
                    "file_name": block.data.get("file_name"),
                    "file_hash": file_hash,
                    "file_size": block.data.get("file_size"),
                    "uploader": block.data.get("uploader"),
                    "file_path": block.data.get("file_path"),
                    "timestamp": block.data.get("timestamp"),
                    "block_index": block.index
                }
        
        return list(file_dict.values())
    
    def get_file_by_hash(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """Get file information by its hash"""
        for block in self.chain:
            if (block.data.get("type") == "file_upload" and 
                block.data.get("file_hash") == file_hash):
                return {
                    "file_name": block.data.get("file_name"),
                    "file_hash": file_hash,
                    "file_size": block.data.get("file_size"),
                    "uploader": block.data.get("uploader"),
                    "file_path": block.data.get("file_path"),
                    "timestamp": block.data.get("timestamp"),
                    "block_index": block.index
                }
        return None
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """Get the entire blockchain as a list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_chain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        total_uploads = sum(1 for block in self.chain 
                          if block.data.get("type") == "file_upload")
        total_downloads = sum(1 for block in self.chain 
                            if block.data.get("type") == "file_download")
        
        # Advanced statistics
        uploaders = set()
        downloaders = set()
        total_size = 0
        encrypted_files = 0
        
        for block in self.chain:
            if block.data.get("type") == "file_upload":
                uploaders.add(block.data.get("uploader"))
                total_size += block.data.get("file_size", 0)
                if block.data.get("is_encrypted"):
                    encrypted_files += 1
            elif block.data.get("type") == "file_download":
                downloaders.add(block.data.get("downloader"))
        
        return {
            "total_blocks": len(self.chain),
            "total_uploads": total_uploads,
            "total_downloads": total_downloads,
            "unique_uploaders": len(uploaders),
            "unique_downloaders": len(downloaders),
            "total_storage_bytes": total_size,
            "encrypted_files": encrypted_files,
            "is_valid": self.is_chain_valid(),
            "difficulty": self.difficulty
        }
    
    def get_file_versions(self, base_file_name: str) -> List[Dict[str, Any]]:
        """Get all versions of a file"""
        versions = []
        for block in self.chain:
            if (block.data.get("type") == "file_upload" and 
                block.data.get("file_name", "").startswith(base_file_name.split("_v")[0])):
                versions.append({
                    "file_name": block.data.get("file_name"),
                    "file_hash": block.data.get("file_hash"),
                    "version": block.data.get("version", 1),
                    "uploader": block.data.get("uploader"),
                    "timestamp": block.data.get("timestamp"),
                    "block_index": block.index
                })
        
        return sorted(versions, key=lambda x: x["version"], reverse=True)
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """Get detailed analytics data for visualization"""
        # Activity by date
        activity_by_date = defaultdict(lambda: {"uploads": 0, "downloads": 0})
        activity_by_hour = defaultdict(lambda: {"uploads": 0, "downloads": 0})
        
        # Top uploaders and downloaders
        uploader_counts = defaultdict(int)
        downloader_counts = defaultdict(int)
        
        # File types
        file_types = defaultdict(int)
        
        for block in self.chain:
            if block.data.get("type") == "file_upload":
                timestamp = block.data.get("timestamp")
                if timestamp:
                    date = timestamp.split("T")[0]
                    hour = datetime.fromisoformat(timestamp).hour
                    activity_by_date[date]["uploads"] += 1
                    activity_by_hour[hour]["uploads"] += 1
                
                uploader = block.data.get("uploader")
                uploader_counts[uploader] += 1
                
                file_name = block.data.get("file_name", "")
                ext = file_name.split(".")[-1] if "." in file_name else "unknown"
                file_types[ext] += 1
                
            elif block.data.get("type") == "file_download":
                timestamp = block.data.get("timestamp")
                if timestamp:
                    date = timestamp.split("T")[0]
                    hour = datetime.fromisoformat(timestamp).hour
                    activity_by_date[date]["downloads"] += 1
                    activity_by_hour[hour]["downloads"] += 1
                
                downloader = block.data.get("downloader")
                downloader_counts[downloader] += 1
        
        # Convert to sorted lists
        activity_timeline = [
            {"date": date, **counts} 
            for date, counts in sorted(activity_by_date.items())
        ]
        
        hourly_activity = [
            {"hour": hour, **counts}
            for hour, counts in sorted(activity_by_hour.items())
        ]
        
        top_uploaders = [
            {"user": user, "count": count}
            for user, count in sorted(uploader_counts.items(), 
                                    key=lambda x: x[1], reverse=True)[:10]
        ]
        
        top_downloaders = [
            {"user": user, "count": count}
            for user, count in sorted(downloader_counts.items(), 
                                    key=lambda x: x[1], reverse=True)[:10]
        ]
        
        file_type_dist = [
            {"type": ftype, "count": count}
            for ftype, count in sorted(file_types.items(), 
                                      key=lambda x: x[1], reverse=True)
        ]
        
        return {
            "activity_timeline": activity_timeline,
            "hourly_activity": hourly_activity,
            "top_uploaders": top_uploaders,
            "top_downloaders": top_downloaders,
            "file_type_distribution": file_type_dist
        }
