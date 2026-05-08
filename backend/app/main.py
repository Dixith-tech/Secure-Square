from fastapi import FastAPI, Depends, HTTPException, status, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import func, text
import logging
import os
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import asyncio
from dotenv import load_dotenv

# Internal imports
from app.database import engine, Base, get_db, test_connection, SessionLocal
from app.models import ThreatLog, User
from app.schemas import (
    ThreatCreate, ThreatResponse, ThreatUpdate, URLScanRequest, URLScanResponse,
    AnomalyDetectionRequest, AnomalyDetectionResponse, HealthCheckResponse,
    UserLogin, UserRegister, TokenResponse, UserResponse, ThreatsStatsResponse,
    PaginationParams, PaginatedResponse
)
from app.detection.phishing_detector import detect_phishing
from app.detection.anomaly_detection import detect_anomaly
from app.detection.geo_detection import get_location
from app.websocket import manage_connections, websocket_endpoint
from app.auth import (
    hash_password, verify_password, create_access_token, get_current_user,
    get_admin_user, detect_new_device
)

load_dotenv()

# ==================== LOGGING SETUP ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== DATABASE INITIALIZATION ====================
def create_tables():
    """Create database tables on startup"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created/verified")
    except Exception as e:
        logger.error(f"✗ Database table creation failed: {str(e)}")
        raise

# ==================== LIFESPAN ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting AI Security Platform...")
    create_tables()
    
    if not test_connection():
        logger.error("✗ Cannot start - Database connection failed")
        raise Exception("Database connection failed")
    
    logger.info("✅ Platform started successfully")
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down platform...")
    logger.info("✅ Platform shutdown complete")

# ==================== APP INITIALIZATION ====================
app = FastAPI(
    title="AI Security Platform",
    description="Real-time AI-powered cybersecurity threat detection",
    version="1.0.0",
    lifespan=lifespan
)

# ==================== MIDDLEWARE ====================
# CORS - Configure for production
ALLOWED_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=[
    "localhost",
    "127.0.0.1",
    os.getenv("ALLOWED_HOST", "localhost")
])

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ==================== HEALTH CHECK ====================
@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
async def health_check() -> HealthCheckResponse:
    """Health check endpoint"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = True
    except:
        db_status = False
    
    return HealthCheckResponse(
        status="healthy" if db_status else "degraded",
        database=db_status,
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )

# ==================== AUTHENTICATION ENDPOINTS ====================
@app.post("/api/v1/auth/register", response_model=TokenResponse, tags=["Auth"])
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        role="analyst"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create token
    token = create_access_token({"sub": new_user.id, "role": "analyst"})
    logger.info(f"✓ User registered: {user_data.email}")
    
    return TokenResponse(
        access_token=token,
        user=UserResponse.from_orm(new_user)
    )

@app.post("/api/v1/auth/login", response_model=TokenResponse, tags=["Auth"])
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Detect new device
    if credentials.device_fingerprint:
        is_new_device = detect_new_device(user.email, credentials.device_fingerprint)
        if is_new_device:
            logger.warning(f"⚠ New device detected for user: {user.email}")
    
    # Create token
    token = create_access_token({"sub": user.id, "role": user.role})
    logger.info(f"✓ User logged in: {user.email}")
    
    return TokenResponse(
        access_token=token,
        user=UserResponse.from_orm(user)
    )

# ==================== THREAT ENDPOINTS ====================
@app.get("/api/v1/threats", response_model=PaginatedResponse, tags=["Threats"])
async def get_threats(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    severity: str = Query(None),
    threat_type: str = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated threats list"""
    query = db.query(ThreatLog)
    
    # Apply filters
    if severity:
        query = query.filter(ThreatLog.severity == severity)
    if threat_type:
        query = query.filter(ThreatLog.threat_type == threat_type)
    
    total = query.count()
    threats = query.order_by(ThreatLog.created_at.desc()).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[ThreatResponse.from_orm(t) for t in threats]
    )

@app.post("/api/v1/threats/report", response_model=ThreatResponse, tags=["Threats"])
async def report_threat(
    threat: ThreatCreate,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Report a new threat"""
    # Get location if not provided
    location_data = {}
    if not threat.country:
        try:
            location_data = await asyncio.to_thread(get_location, threat.ip_address)
        except Exception as e:
            logger.error(f"Failed to get location for {threat.ip_address}: {str(e)}")
    
    # Create threat log
    db_threat = ThreatLog(
        ip_address=threat.ip_address,
        port=threat.port,
        threat_type=threat.threat_type,
        severity=threat.severity,
        confidence=threat.confidence,
        risk_score=threat.risk_score,
        anomaly_score=threat.anomaly_score,
        location=threat.location or location_data.get("city"),
        country=threat.country or location_data.get("country"),
        device=threat.device,
        threat_description=threat.threat_description
    )
    
    db.add(db_threat)
    db.commit()
    db.refresh(db_threat)
    
    logger.info(f"✓ Threat reported: {threat.threat_type} from {threat.ip_address}")
    
    # Send notification in background
    background_tasks.add_task(send_threat_notification, db_threat)
    
    return ThreatResponse.from_orm(db_threat)

@app.put("/api/v1/threats/{threat_id}", response_model=ThreatResponse, tags=["Threats"])
async def update_threat(
    threat_id: int,
    threat_update: ThreatUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update threat status"""
    threat = db.query(ThreatLog).filter(ThreatLog.id == threat_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    # Update fields
    if threat_update.status:
        threat.status = threat_update.status
    if threat_update.is_blocked is not None:
        threat.is_blocked = threat_update.is_blocked
    if threat_update.is_whitelisted is not None:
        threat.is_whitelisted = threat_update.is_whitelisted
    
    db.commit()
    db.refresh(threat)
    
    logger.info(f"✓ Threat {threat_id} updated by user {current_user['user_id']}")
    return ThreatResponse.from_orm(threat)

# ==================== DETECTION ENDPOINTS ====================
@app.post("/api/v1/detection/scan-url", response_model=URLScanResponse, tags=["Detection"])
async def scan_url(request: URLScanRequest):
    """Scan URL for phishing"""
    try:
        is_phishing = detect_phishing(request.url)
        confidence = 0.95 if is_phishing else 0.05
        risk_score = 85.0 if is_phishing else 5.0
        
        logger.info(f"✓ URL scanned: {request.url} - Phishing: {is_phishing}")
        
        return URLScanResponse(
            url=request.url,
            is_phishing=is_phishing,
            confidence=confidence,
            risk_score=risk_score,
            details={
                "method": "keyword_detection",
                "checked_at": datetime.utcnow().isoformat()
            },
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"✗ URL scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Scan failed")

@app.post("/api/v1/detection/anomaly", response_model=AnomalyDetectionResponse, tags=["Detection"])
async def detect_anomaly_endpoint(request: AnomalyDetectionRequest):
    """Detect anomalies in user behavior"""
    try:
        is_anomaly = detect_anomaly(
            request.login_attempts,
            request.location_change,
            request.device_change
        )
        
        # Calculate anomaly score
        anomaly_score = (
            (request.login_attempts / 100) * 0.3 +
            (request.location_change * 0.4) +
            (request.device_change * 0.3)
        )
        
        risk_levels = {
            'Low': anomaly_score < 0.3,
            'Medium': 0.3 <= anomaly_score < 0.6,
            'High': 0.6 <= anomaly_score < 0.8,
            'Critical': anomaly_score >= 0.8
        }
        
        risk_level = next(level for level, check in risk_levels.items() if check)
        
        recommendations = []
        if request.location_change:
            recommendations.append("Verify unusual location activity")
        if request.device_change:
            recommendations.append("Authenticate new device")
        if request.login_attempts > 5:
            recommendations.append("Consider account lockout after multiple failures")
        
        logger.info(f"✓ Anomaly detection completed - Risk: {risk_level}")
        
        return AnomalyDetectionResponse(
            is_anomaly=is_anomaly,
            anomaly_score=min(anomaly_score, 1.0),
            risk_level=risk_level,
            recommendations=recommendations,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"✗ Anomaly detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Detection failed")

# ==================== STATISTICS ENDPOINTS ====================
@app.get("/api/v1/stats/threats", response_model=ThreatsStatsResponse, tags=["Stats"])
async def get_threat_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get threat statistics"""
    total_threats = db.query(ThreatLog).count()
    critical_count = db.query(ThreatLog).filter(ThreatLog.severity == "Critical").count()
    high_count = db.query(ThreatLog).filter(ThreatLog.severity == "High").count()
    medium_count = db.query(ThreatLog).filter(ThreatLog.severity == "Medium").count()
    low_count = db.query(ThreatLog).filter(ThreatLog.severity == "Low").count()
    blocked_count = db.query(ThreatLog).filter(ThreatLog.is_blocked == True).count()
    
    # Calculate metrics
    detection_rate = (critical_count + high_count) / max(total_threats, 1) * 100
    avg_risk = db.query(func.avg(ThreatLog.risk_score)).scalar() or 0
    
    return ThreatsStatsResponse(
        total_threats=total_threats,
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        blocked_count=blocked_count,
        detection_rate=detection_rate,
        average_risk_score=float(avg_risk)
    )

# ==================== WEBSOCKET ====================
@app.websocket("/ws")
async def websocket_route(websocket):
    """WebSocket connection for real-time threat updates"""
    await websocket_endpoint(websocket)

# ==================== ERROR HANDLERS ====================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP Exception: {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return {
        "error": "Internal server error",
        "status_code": 500
    }

# ==================== BACKGROUND TASKS ====================
async def send_threat_notification(threat: ThreatLog):
    """Send notification for critical threats"""
    if threat.severity in ["Critical", "High"]:
        logger.warning(f"⚠ ALERT: {threat.threat_type} threat from {threat.ip_address}")
        # TODO: Integrate with email/SMS notification service
        # TODO: Publish to WebSocket for real-time dashboard update

# ==================== STARTUP ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
