from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.complaint import Complaint
from typing import Optional

class ComplaintRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, complaint_data: dict) -> Complaint:
        """Create a new complaint"""
        complaint = Complaint(**complaint_data)
        self.db.add(complaint)
        self.db.commit()
        self.db.refresh(complaint)
        return complaint
    
    def get_by_id(self, complaint_id: int) -> Optional[Complaint]:
        """Get complaint by ID"""
        return self.db.query(Complaint).filter(Complaint.id == complaint_id).first()
    
    def get_by_batch_number(self, batch_number: str) -> list[Complaint]:
        """Get complaints by batch number"""
        return self.db.query(Complaint).filter(Complaint.batch_number == batch_number).all()
    
    def update(self, complaint_id: int, complaint_data: dict) -> Optional[Complaint]:
        """Update an existing complaint"""
        complaint = self.get_by_id(complaint_id)
        if complaint:
            for key, value in complaint_data.items():
                setattr(complaint, key, value)
            self.db.commit()
            self.db.refresh(complaint)
        return complaint
    
    def delete(self, complaint_id: int) -> bool:
        """Delete a complaint"""
        complaint = self.get_by_id(complaint_id)
        if complaint:
            self.db.delete(complaint)
            self.db.commit()
            return True
        return False
