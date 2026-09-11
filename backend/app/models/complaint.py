from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Complaint source and customer info
    complaint_source = Column(String(100), nullable=True)
    customer_name = Column(String(255), nullable=True)
    
    # Product information
    product_name = Column(String(255), nullable=True)
    product_strength = Column(String(100), nullable=True)
    batch_number = Column(String(100), nullable=True, index=True)
    affected_quantity = Column(String(100), nullable=True)
    
    # Dates
    manufacturing_date = Column(String(50), nullable=True)
    expiry_date = Column(String(50), nullable=True)
    complaint_date = Column(String(50), nullable=True)
    
    # Site and material
    originating_site = Column(String(255), nullable=True)
    affected_material = Column(String(255), nullable=True)
    
    # Complaint details
    complaint_type = Column(String(255), nullable=True)
    complaint_description = Column(Text, nullable=True)
    initial_severity = Column(String(50), nullable=True)
    priority = Column(String(50), nullable=True)
    
    # Metadata
    completeness = Column(Float, nullable=True)
    risk_assessment = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "complaint_source": self.complaint_source,
            "customer_name": self.customer_name,
            "product_name": self.product_name,
            "product_strength": self.product_strength,
            "batch_number": self.batch_number,
            "affected_quantity": self.affected_quantity,
            "manufacturing_date": self.manufacturing_date,
            "expiry_date": self.expiry_date,
            "complaint_date": self.complaint_date,
            "originating_site": self.originating_site,
            "affected_material": self.affected_material,
            "complaint_type": self.complaint_type,
            "complaint_description": self.complaint_description,
            "initial_severity": self.initial_severity,
            "priority": self.priority,
            "completeness": self.completeness,
            "risk_assessment": self.risk_assessment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
