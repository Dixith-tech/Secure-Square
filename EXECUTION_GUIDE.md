# QUICK START GUIDE

## Summary of Fixes Applied

✅ Fixed missing imports in `backend/app/main.py` (database and models)
✅ Fixed incomplete JSX in `frontend/app/dashboard/page.js` 
✅ Created missing component files:
   - `AlertPopup.js`
   - `Navbar.js`
   - `ThreatTable.js`
   - `ThreatCard.js`
   - `LiveChart.js`
   - `AttackMap.js`
✅ Created missing service files:
   - `frontend/services/websocket.js`
✅ Added Python `__init__.py` files for all packages
✅ Created frontend configuration files (layout, globals.css, etc.)
✅ Updated `package.json` to use Next.js instead of Vite
✅ Fixed ML model path in `train_model.py`
✅ Created `.gitignore` and `.env.example` files

---

## HOW TO EXECUTE

### **Step 1: Backend Setup (Terminal 1)**

```powershell
# Navigate to backend
cd backend

# Activate virtual environment (already done in your terminal)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train ML model (FIRST TIME ONLY)
python -m app.ml.train_model

# Start backend server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
```

---

### **Step 2: Frontend Setup (Terminal 2)**

```powershell
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Start frontend server
npm run dev
```

**Expected Output:**
```
> ai-security-frontend@0.0.0 dev
> next dev -p 3000

  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
  - Environments: .env.local

  ✓ Ready in 2.5s
```

---

### **Step 3: Access the Application**

1. Open browser and go to: **http://localhost:3000**
2. You'll be redirected to login page
3. Use demo credentials:
   - Email: `admin@example.com`
   - Password: `password`
4. You'll see the Security Dashboard

---

## VERIFICATION CHECKLIST

- [ ] Backend server running on http://127.0.0.1:8000
- [ ] Frontend server running on http://localhost:3000
- [ ] Can log in with demo credentials
- [ ] Dashboard loads with threat data
- [ ] No console errors in browser
- [ ] No errors in backend terminal

---

## TESTING THE API

Test backend endpoints using curl or Postman:

```powershell
# Get threats
curl http://127.0.0.1:8000/threats

# Health check
curl http://127.0.0.1:8000/

# Scan URL
curl -X POST "http://127.0.0.1:8000/scan-url?url=paypa1.com"
```

---

## COMMON ISSUES & FIXES

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | `netstat -ano \| findstr :8000` then change port in main.py |
| Port 3000 already in use | `npm run dev -- --port 3001` |
| Module not found errors | Ensure `.venv` is activated |
| "model.pkl not found" | Run `python -m app.ml.train_model` |
| CORS errors | Already configured in main.py for `*` origins |
| Database errors | SQLite is default, PostgreSQL is optional |

---

## FILE PATHS (DO NOT CHANGE)

✓ Backend: `c:\Users\Deekshith\Downloads\ai-security-platform\backend`
✓ Frontend: `c:\Users\Deekshith\Downloads\ai-security-platform\frontend`
✓ Config: All paths remain unchanged as requested

---

## STOPPING THE SERVERS

- **Backend:** Press `Ctrl+C` in backend terminal
- **Frontend:** Press `Ctrl+C` in frontend terminal

---

## NEXT STEPS

1. Keep both terminals open and running
2. Make changes to code - both will auto-reload
3. Check browser DevTools (F12) for any errors
4. Check backend terminal for API errors
5. Frontend changes auto-update, backend changes require manual refresh

---

## PRODUCTION DEPLOYMENT

For production, update:
1. `DATABASE_URL` to PostgreSQL connection string
2. `SECRET_KEY` to a secure random value
3. `allow_origins` in main.py to specific domains
4. SMTP credentials for email alerts
5. Build frontend: `npm run build`

See README.md for more details.
