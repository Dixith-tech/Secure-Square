from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, JSON, Index, event
from sqlalchemy.orm import validates
from app.database import Base
import datetime
import json
from typing import Optional

class ThreatLog(Base):
    """Database model for storing threat logs"""
    __tablename__ = "threat_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Network info
    ip_address = Column(String(15), index=True, nullable=False)
    port = Column(Integer, nullable=True)
    protocol = Column(String(10), default="TCP")
    
    # Threat classification
    threat_type = Column(String(50), index=True, nullable=False)  # Phishing, DDoS, Brute Force, etc.
    severity = Column(String(20), index=True, nullable=False)     # Low, Medium, High, Critical
    confidence = Column(Float, default=0.0)                        # ML confidence score (0-1)
    
    # Geographic & Device info
    location = Column(String(100), nullable=True)
    country = Column(String(50), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    device = Column(String(100), nullable=True)
    device_fingerprint = Column(String(255), nullable=True)
    
    # Additional threat info
    threat_description = Column(String(500), nullable=True)
    threat_payload = Column(JSON, nullable=True)  # Store threat details
    
    # Risk assessment
    risk_score = Column(Float, default=0.0)        # 0-100
    anomaly_score = Column(Float, default=0.0)     # ML anomaly detection score
    is_blocked = Column(Boolean, default=False)
    
    # Status tracking
    status = Column(String(20), default="active")  # active, investigated, resolved, false_positive
    is_whitelisted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    detected_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_ip_created', 'ip_address', 'created_at'),
        Index('idx_severity_timestamp', 'severity', 'created_at'),
        Index('idx_threat_type', 'threat_type'),
    )

    @validates('severity')
    def validate_severity(self, key, value):
        allowed = ['Low', 'Medium', 'High', 'Critical']
        if value not in allowed:
            raise ValueError(f"Severity must be one of {allowed}")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'port': self.port,
            'threat_type': self.threat_type,
            'severity': self.severity,
            'confidence': self.confidence,
            'location': self.location,
            'country': self.country,
            'device': self.device,
            'risk_score': self.risk_score,
            'anomaly_score': self.anomaly_score,
            'is_blocked': self.is_blocked,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'detected_at': self.detected_at.isoformat(),
        }

class SystemAlert(Base):
    """Model for system-level alerts"""
    __tablename__ = "system_alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50), index=True)  # DDoS, PortScan, Anomaly, etc.
    message = Column(String(500))
    severity = Column(String(20))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_alert_severity_time', 'severity', 'created_at'),
    )

class User(Base):
    """Model for authenticated users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="analyst")  # analyst, admin, viewer
    device_fingerprint = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index('idx_email', 'email'),
    )

class AnomalyModel(Base):
    """Store trained ML models metadata"""
    __tablename__ = "anomaly_models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), unique=True)
    model_version = Column(String(20))
    accuracy = Column(Float)
    training_samples = Column(Integer)
    trained_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    model_path = Column(String(255))