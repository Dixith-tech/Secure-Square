# AI Security Platform

An advanced threat detection and monitoring system with real-time security analytics, anomaly detection, and phishing identification.

## Project Structure

```
.
├── backend/               # FastAPI backend server
│   ├── app/
│   │   ├── main.py       # Main FastAPI application
│   │   ├── models.py     # SQLAlchemy database models
│   │   ├── database.py   # Database configuration
│   │   ├── websocket.py  # WebSocket connections
│   │   ├── detection/    # Threat detection modules
│   │   ├── ml/           # Machine learning models
│   │   ├── monitoring/   # System monitoring
│   │   └── notifications/# Alert notifications
│   └── requirements.txt  # Python dependencies
└── frontend/             # Next.js React frontend
    ├── app/              # Next.js app directory
    ├── components/       # React components
    ├── services/         # API services
    └── package.json      # Node dependencies
```

## Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- PostgreSQL 12+ (or you can use SQLite for development)
- Virtual environment (venv/conda)

## Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```
   cd backend
   ```

2. **Create virtual environment:**
   ```
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   
   **Windows:**
   ```
   .venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Train ML model (first time only):**
   ```
   python -m app.ml.train_model
   ```
   This creates `app/ml/model.pkl` for anomaly detection.

6. **(Optional) Set up PostgreSQL database:**
   Edit `app/database.py` and update the `DATABASE_URL` with your PostgreSQL credentials:
   ```
   DATABASE_URL = "postgresql://username:password@localhost/securitydb"
   ```
   Then create the database:
   ```
   createdb securitydb
   ```

### Frontend Setup

1. **Navigate to frontend directory (from project root):**
   ```
   cd frontend
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Install Tailwind CSS (if needed):**
   ```
   npm install -D tailwindcss postcss autoprefixer
   ```

## Running the Application

### Option 1: Run Both Servers Separately (Recommended for Development)

**Terminal 1 - Backend Server:**
```
cd backend
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Mac/Linux
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend Server:**
```
cd frontend
npm run dev
```

Access the application at: **http://localhost:5173**

### Option 2: Using VS Code Integrated Terminals

1. Open backend/app/main.py in VS Code
2. Run the backend with uvicorn
3. Run `npm run dev` in frontend directory

## API Endpoints

- `GET /` - Health check
- `GET /threats` - Get all current threats
- `POST /scan-url` - Scan URL for phishing

## Available npm Scripts

```
npm run dev      # Start development server (port 5173)
npm run build    # Build for production
npm run preview  # Preview production build
```

## Backend Routes

```
GET  /                - API health check
GET  /threats         - Fetch all threats
POST /scan-url        - Scan URL for phishing
WS   /ws              - WebSocket connection for real-time updates
```

## Configuration

### Backend Environment (optional .env file)
```
DATABASE_URL=postgresql://user:password@localhost/securitydb
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend API Base URL
Update in `services/api.js` if backend URL changes:
```javascript
const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});
```

## Login Credentials (Demo)

```
Email: admin@example.com
Password: password
```

## Troubleshooting

### "Module not found" errors for Python
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`
- Check that all `__init__.py` files exist in app subdirectories

### Frontend port already in use
Change the port in `vite.config.js` or run: `npm run dev -- --port 3000`

### Database connection errors
- Ensure PostgreSQL is running
- Check `DATABASE_URL` in `app/database.py`
- Use SQLite for local testing (change DATABASE_URL to `sqlite:///./test.db`)

### Model file not found
Run: `python -m app.ml.train_model` to regenerate `app/ml/model.pkl`

## Features

- ✅ Real-time threat detection
- ✅ Phishing URL detection
- ✅ Anomaly detection using ML
- ✅ Geographic threat mapping
- ✅ Live attack graphs and analytics
- ✅ Alert notifications
- ✅ WebSocket real-time updates
- ✅ Responsive dashboard UI

## Technology Stack

**Backend:**
- FastAPI
- SQLAlchemy (ORM)
- scikit-learn (ML)
- Uvicorn (ASGI server)

**Frontend:**
- React 18
- Next.js
- Tailwind CSS
- Recharts (data visualization)
- Axios (HTTP client)

## Development Notes

- Database models are in `app/models.py`
- Update CORS settings in `app/main.py` for production
- WebSocket endpoint at `/ws` for real-time updates
- All imports use relative paths with app/ prefix

## License

MIT
