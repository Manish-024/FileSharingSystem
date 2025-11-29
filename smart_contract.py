from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os


class SmartContract:
    """Smart contract for file access control"""
    
    def __init__(self, file_hash: str, owner: str):
        self.file_hash = file_hash
        self.owner = owner
        self.permissions: Dict[str, Dict] = {}
        self.access_log: List[Dict] = []
        self.creation_time = datetime.now()
        self.is_public = False
        self.max_downloads = None
        self.expiration_time = None
        self.contract_id = f"contract_{file_hash[:16]}"
    
    def set_public_access(self, is_public: bool):
        """Set file as public or private"""
        self.is_public = is_public
    
    def set_max_downloads(self, max_downloads: int):
        """Set maximum number of downloads allowed"""
        self.max_downloads = max_downloads
    
    def set_expiration(self, hours: int):
        """Set contract expiration time"""
        self.expiration_time = datetime.now() + timedelta(hours=hours)
    
    def grant_permission(self, user: str, duration_hours: int = None, 
                        max_downloads: int = None):
        """Grant permission to a specific user"""
        permission = {
            "granted_at": datetime.now().isoformat(),
            "granted_by": self.owner,
            "max_downloads": max_downloads,
            "downloads_used": 0,
            "expiration": None
        }
        
        if duration_hours:
            permission["expiration"] = (
                datetime.now() + timedelta(hours=duration_hours)
            ).isoformat()
        
        self.permissions[user] = permission
    
    def revoke_permission(self, user: str) -> bool:
        """Revoke permission from a user"""
        if user in self.permissions:
            del self.permissions[user]
            return True
        return False
    
    def check_access(self, user: str) -> tuple[bool, str]:
        """
        Check if user has access to the file
        Returns: (has_access, reason)
        """
        # Check if contract is expired
        if self.expiration_time and datetime.now() > self.expiration_time:
            return False, "Contract expired"
        
        # Owner always has access
        if user == self.owner:
            return True, "Owner access"
        
        # Check public access
        if self.is_public:
            # Check max downloads limit
            if self.max_downloads:
                # Count only successful downloads (excluding owner's downloads)
                total_downloads = len([log for log in self.access_log 
                                      if log["action"] == "download" 
                                      and log["success"] 
                                      and log["user"] != self.owner])
                if total_downloads >= self.max_downloads:
                    return False, "Download limit reached"
            return True, "Public access"
        
        # Check user-specific permissions
        if user not in self.permissions:
            return False, "No permission granted"
        
        permission = self.permissions[user]
        
        # Check if permission expired
        if permission["expiration"]:
            exp_time = datetime.fromisoformat(permission["expiration"])
            if datetime.now() > exp_time:
                return False, "Permission expired"
        
        # Check user download limit
        if permission["max_downloads"]:
            if permission["downloads_used"] >= permission["max_downloads"]:
                return False, "User download limit reached"
        
        return True, "User permission"
    
    def log_access(self, user: str, action: str, success: bool, reason: str = ""):
        """Log access attempt"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "action": action,
            "success": success,
            "reason": reason
        }
        self.access_log.append(log_entry)
        
        # Update download count for user
        if success and action == "download" and user in self.permissions:
            self.permissions[user]["downloads_used"] += 1
    
    def get_stats(self) -> Dict:
        """Get contract statistics"""
        total_accesses = len(self.access_log)
        successful_downloads = len([log for log in self.access_log 
                                   if log["action"] == "download" and log["success"]])
        failed_accesses = len([log for log in self.access_log if not log["success"]])
        
        return {
            "contract_id": self.contract_id,
            "file_hash": self.file_hash,
            "owner": self.owner,
            "is_public": self.is_public,
            "total_permissions": len(self.permissions),
            "total_accesses": total_accesses,
            "successful_downloads": successful_downloads,
            "failed_accesses": failed_accesses,
            "creation_time": self.creation_time.isoformat(),
            "expiration_time": self.expiration_time.isoformat() if self.expiration_time else None
        }
    
    def to_dict(self) -> Dict:
        """Convert contract to dictionary"""
        return {
            "contract_id": self.contract_id,
            "file_hash": self.file_hash,
            "owner": self.owner,
            "is_public": self.is_public,
            "max_downloads": self.max_downloads,
            "expiration_time": self.expiration_time.isoformat() if self.expiration_time else None,
            "permissions": self.permissions,
            "access_log": self.access_log,
            "creation_time": self.creation_time.isoformat()
        }


class ContractManager:
    """Manage smart contracts for files with persistence"""
    
    def __init__(self, storage_path: str = "data/contracts.json"):
        self.contracts: Dict[str, SmartContract] = {}
        self.storage_path = storage_path
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        # Load existing contracts
        self.load_from_disk()
    
    def create_contract(self, file_hash: str, owner: str) -> SmartContract:
        """Create a new smart contract"""
        contract = SmartContract(file_hash, owner)
        self.contracts[file_hash] = contract
        self.save_to_disk()  # Persist to disk
        return contract
    
    def get_contract(self, file_hash: str) -> Optional[SmartContract]:
        """Get contract by file hash"""
        return self.contracts.get(file_hash)
    
    def get_all_contracts(self) -> List[Dict]:
        """Get all contracts"""
        return [contract.to_dict() for contract in self.contracts.values()]
    
    def save_to_disk(self):
        """Save contracts to disk"""
        try:
            contracts_data = {
                file_hash: contract.to_dict() 
                for file_hash, contract in self.contracts.items()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(contracts_data, f, indent=2)
        except Exception as e:
            print(f"Error saving contracts: {e}")
    
    def load_from_disk(self):
        """Load contracts from disk"""
        try:
            if not os.path.exists(self.storage_path):
                return
            
            with open(self.storage_path, 'r') as f:
                contracts_data = json.load(f)
            
            for file_hash, contract_dict in contracts_data.items():
                contract = SmartContract(
                    file_hash=contract_dict["file_hash"],
                    owner=contract_dict["owner"]
                )
                # Restore contract state
                contract.permissions = contract_dict.get("permissions", {})
                contract.access_log = contract_dict.get("access_log", [])
                contract.is_public = contract_dict.get("is_public", False)
                contract.max_downloads = contract_dict.get("max_downloads")
                contract.expiration_time = contract_dict.get("expiration_time")
                contract.contract_id = contract_dict.get("contract_id")
                
                self.contracts[file_hash] = contract
            
            print(f"✓ Loaded {len(self.contracts)} contracts from disk")
            
        except Exception as e:
            print(f"Error loading contracts: {e}")
