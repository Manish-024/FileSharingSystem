from datetime import datetime
from typing import Dict, List
import statistics


class PeerVerification:
    """System for peer verification and voting on files"""
    
    def __init__(self):
        self.verifications: Dict[str, Dict] = {}  # file_hash -> verification data
        self.reputation: Dict[str, float] = {}  # user -> reputation score
    
    def submit_verification(self, file_hash: str, user: str, 
                          is_authentic: bool, comment: str = ""):
        """Submit a verification vote for a file"""
        if file_hash not in self.verifications:
            self.verifications[file_hash] = {
                "votes": [],
                "authenticity_score": 0,
                "total_votes": 0,
                "positive_votes": 0,
                "negative_votes": 0
            }
        
        # Check if user already voted
        existing_vote = next((v for v in self.verifications[file_hash]["votes"] 
                            if v["user"] == user), None)
        
        if existing_vote:
            # Update existing vote
            existing_vote["is_authentic"] = is_authentic
            existing_vote["comment"] = comment
            existing_vote["updated_at"] = datetime.now().isoformat()
        else:
            # Add new vote
            vote = {
                "user": user,
                "is_authentic": is_authentic,
                "comment": comment,
                "timestamp": datetime.now().isoformat(),
                "reputation_weight": self.get_user_reputation(user)
            }
            self.verifications[file_hash]["votes"].append(vote)
        
        # Recalculate scores
        self._calculate_authenticity_score(file_hash)
        
        # Update user reputation
        self._update_user_reputation(user)
    
    def _calculate_authenticity_score(self, file_hash: str):
        """Calculate weighted authenticity score"""
        if file_hash not in self.verifications:
            return
        
        votes = self.verifications[file_hash]["votes"]
        if not votes:
            return
        
        # Calculate weighted score
        total_weight = 0
        weighted_sum = 0
        positive_count = 0
        negative_count = 0
        
        for vote in votes:
            weight = vote["reputation_weight"]
            total_weight += weight
            
            if vote["is_authentic"]:
                weighted_sum += weight
                positive_count += 1
            else:
                negative_count += 1
        
        # Authenticity score (0-100)
        if total_weight > 0:
            score = (weighted_sum / total_weight) * 100
        else:
            score = 0
        
        self.verifications[file_hash]["authenticity_score"] = round(score, 2)
        self.verifications[file_hash]["total_votes"] = len(votes)
        self.verifications[file_hash]["positive_votes"] = positive_count
        self.verifications[file_hash]["negative_votes"] = negative_count
    
    def _update_user_reputation(self, user: str):
        """Update user reputation based on voting activity"""
        # Simple reputation system: more votes = higher reputation
        user_votes = 0
        for file_data in self.verifications.values():
            user_votes += sum(1 for v in file_data["votes"] if v["user"] == user)
        
        # Base reputation + activity bonus
        self.reputation[user] = min(1.0 + (user_votes * 0.1), 2.0)
    
    def get_user_reputation(self, user: str) -> float:
        """Get user reputation score (1.0 is default)"""
        return self.reputation.get(user, 1.0)
    
    def get_file_verification(self, file_hash: str) -> Dict:
        """Get verification data for a file"""
        if file_hash not in self.verifications:
            return {
                "authenticity_score": 0,
                "total_votes": 0,
                "positive_votes": 0,
                "negative_votes": 0,
                "votes": [],
                "status": "unverified"
            }
        
        data = self.verifications[file_hash].copy()
        
        # Determine status
        if data["total_votes"] == 0:
            data["status"] = "unverified"
        elif data["authenticity_score"] >= 75:
            data["status"] = "verified"
        elif data["authenticity_score"] >= 50:
            data["status"] = "disputed"
        else:
            data["status"] = "suspicious"
        
        return data
    
    def get_top_verifiers(self, limit: int = 10) -> List[Dict]:
        """Get top verifiers by reputation"""
        sorted_users = sorted(self.reputation.items(), 
                            key=lambda x: x[1], reverse=True)
        
        return [
            {
                "user": user,
                "reputation": rep,
                "rank": idx + 1
            }
            for idx, (user, rep) in enumerate(sorted_users[:limit])
        ]
    
    def get_verification_stats(self) -> Dict:
        """Get overall verification statistics"""
        if not self.verifications:
            return {
                "total_files_verified": 0,
                "total_votes": 0,
                "verified_files": 0,
                "disputed_files": 0,
                "suspicious_files": 0,
                "average_authenticity": 0
            }
        
        total_votes = sum(v["total_votes"] for v in self.verifications.values())
        scores = [v["authenticity_score"] for v in self.verifications.values() 
                 if v["total_votes"] > 0]
        
        verified = sum(1 for v in self.verifications.values() 
                      if v["authenticity_score"] >= 75)
        disputed = sum(1 for v in self.verifications.values() 
                      if 50 <= v["authenticity_score"] < 75)
        suspicious = sum(1 for v in self.verifications.values() 
                        if v["authenticity_score"] < 50 and v["total_votes"] > 0)
        
        return {
            "total_files_verified": len(self.verifications),
            "total_votes": total_votes,
            "verified_files": verified,
            "disputed_files": disputed,
            "suspicious_files": suspicious,
            "average_authenticity": round(statistics.mean(scores), 2) if scores else 0,
            "total_verifiers": len(self.reputation)
        }
