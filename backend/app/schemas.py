from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import re

# ==================== THREAT SCHEMAS ====================

class ThreatBase(BaseModel):
    ip_address: str = Field(..., min_length=7, max_length=15)
    threat_type: str
    severity: str
    location: Optional[str] = None
    device: Optional[str] = None

    @validator('ip_address')
    def validate_ip(cls, v):
        # Simple IP validation
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid IP address format')
        return v

    @validator('severity')
    def validate_severity(cls, v):
        allowed = ['Low', 'Medium', 'High', 'Critical']
        if v not in allowed:
            raise ValueError(f'Severity must be one of {allowed}')
        return v

class ThreatCreate(ThreatBase):
    port: Optional[int] = None
    confidence: float = Field(default=0.0, ge=0, le=1)
    risk_score: float = Field(default=0.0, ge=0, le=100)
    anomaly_score: float = Field(default=0.0, ge=0, le=1)
    threat_description: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ThreatResponse(ThreatBase):
    id: int
    confidence: float
    risk_score: float
    anomaly_score: float
    is_blocked: bool
    status: str
    created_at: datetime
    detected_at: datetime

    class Config:
        from_attributes = True

class ThreatUpdate(BaseModel):
    status: Optional[str] = None
    is_blocked: Optional[bool] = None
    is_whitelisted: Optional[bool] = None

# ==================== AUTHENTICATION SCHEMAS ====================

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    device_fingerprint: Optional[str] = None

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    device_fingerprint: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ==================== DETECTION SCHEMAS ====================

class URLScanRequest(BaseModel):
    url: str = Field(..., min_length=5)
    
    @validator('url')
    def validate_url(cls, v):
        # Basic URL validation
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

class URLScanResponse(BaseModel):
    url: str
    is_phishing: bool
    confidence: float
    risk_score: float
    details: Optional[dict] = None
    timestamp: datetime

class AnomalyDetectionRequest(BaseModel):
    login_attempts: int = Field(..., ge=0)
    location_change: int = Field(..., ge=0, le=1)
    device_change: int = Field(..., ge=0, le=1)
    time_anomaly: float = Field(default=0.0)
    ip_reputation: float = Field(default=0.5)

class AnomalyDetectionResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    risk_level: str  # Low, Medium, High, Critical
    recommendations: List[str]
    timestamp: datetime

# ==================== SYSTEM SCHEMAS ====================

class HealthCheckResponse(BaseModel):
    status: str
    database: bool
    timestamp: datetime
    version: str = "1.0.0"

class ThreatsStatsResponse(BaseModel):
    total_threats: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    blocked_count: int
    detection_rate: float
    average_risk_score: float

class SystemAlertResponse(BaseModel):
    id: int
    alert_type: str
    message: str
    severity: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== PAGINATION ====================

class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=1000)
    sort_by: Optional[str] = None
    order: str = Field(default="desc")  # asc or desc

class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List
