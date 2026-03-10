# 🚀 How to Run - QKD BB84 Protocol

## Quick Start (2 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Browser
```
http://localhost:8000
```

### Step 4: Click "Launch Simulator"
Done! 🎉

---

## Detailed Instructions

### Prerequisites
- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Browser**: Chrome, Firefox, Safari, or Edge

### Check Python Version
```bash
python --version
```
Should show: `Python 3.8.0` or higher

---

## Installation Steps

### 1. Navigate to Project Directory
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed Flask-2.3.3 Werkzeug-2.3.7 ...
```

### 4. Verify Installation
```bash
python test_qkd.py
```

Expected output:
```
Ran 31 tests in 0.048s
OK
```

---

## Running the Application

### Option 1: Web Interface (Recommended)
```bash
python app.py
```

**Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:8000
```

**Then:**
1. Open browser: http://localhost:8000
2. Click "Launch Simulator"
3. Set parameters and click "Run QKD Simulation"

### Option 2: Command Line
```bash
python qkd_main.py
```

**Output:**
```
======================================================================
  BB84 Quantum Key Distribution — Full Simulation
======================================================================
  Qubits     : 200
  Message    : Secure message from Alice!
  Eve Active : False

[1] ALICE — Qubit Preparation
    Generated 200 random bits & bases.
    ...
```

### Option 3: Python Script
```python
from qkd_main import run_qkd

result = run_qkd(
    num_qubits=100,
    message="Hello, Quantum World!",
    eve_enabled=False
)

print(f"QBER: {result['qber']*100:.2f}%")
print(f"Secure: {result['secure']}")
print(f"Decrypted: {result['decrypted']}")
```

---

## Web Interface Guide

### Home Page (http://localhost:8000)
- Overview of QKD BB84 protocol
- Feature highlights
- Protocol explanation
- Security comparison
- **Click "Launch Simulator" to start**

### Simulator Page (http://localhost:8000/simulator)

#### Left Panel - Controls
1. **Number of Qubits**: 10-1000 (default: 100)
2. **Message to Encrypt**: Enter any text
3. **Eve (Eavesdropper)**: Toggle to enable/disable
4. **Run QKD Simulation**: Click to execute

#### Center Panel - Results
- Protocol flow visualization
- Metrics dashboard (QBER, sifted key, errors)
- Security status (SECURE or COMPROMISED)
- Quantum key (hex)
- Encrypted message
- Decrypted message
- Qubit analysis table

#### Right Panel - Communication Feed
- Live message log
- Server status
- Protocol execution steps

### Documentation Page (http://localhost:8000/documentation)
- Complete protocol explanation
- Security analysis
- QBER calculation
- Implementation details
- Performance metrics
- References

---

## Testing

### Run All Tests
```bash
python test_qkd.py
```

Expected output:
```
Ran 31 tests in 0.048s
OK
```

### Run Specific Test
```bash
python -m unittest test_qkd.TestSecurityModule -v
```

### Run with Coverage
```bash
pytest --cov=. test_qkd.py
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution 1:** Kill the process using port 8000
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**Solution 2:** Use different port
```bash
python app.py --port 5000
# Then open http://localhost:5000
```

### Issue: "Connection refused" or "Timeout"
**Solution:** Make sure you're using in-process mode (not distributed servers)
```bash
python app.py  # Correct
# NOT: python alice_server_improved.py
```

### Issue: Tests fail
**Solution:** Verify Python version and reinstall dependencies
```bash
python --version  # Should be 3.8+
pip install -r requirements.txt --upgrade
python test_qkd.py
```

---

## Docker Deployment

### Build Docker Image
```bash
docker build -t qkd-app .
```

### Run Docker Container
```bash
docker run -p 8000:8000 qkd-app
```

### Or Use Docker Compose
```bash
docker-compose up -d
```

Then open: http://localhost:8000

---

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

### Using Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Common Commands

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Run web app | `python app.py` |
| Run standalone | `python qkd_main.py` |
| Run tests | `python test_qkd.py` |
| Check status | `python diagnose.py` |
| Build Docker | `docker build -t qkd-app .` |
| Run Docker | `docker run -p 8000:8000 qkd-app` |

---

## File Structure

```
qkd-secure-communication/
├── app.py                    # Flask web application
├── qkd_main.py              # Standalone protocol runner
├── alice.py                 # Alice module
├── bob.py                   # Bob module
├── eve.py                   # Eve module
├── security.py              # Security analysis
├── quantum_channel.py       # Channel simulation
├── test_qkd.py             # Test suite
├── requirements.txt         # Dependencies
├── templates/
│   ├── home.html           # Home page
│   ├── simulator.html      # Simulator interface
│   └── documentation.html  # Documentation
└── [documentation files]
```

---

## Expected Output

### Web Interface
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:8000
 * Press CTRL+C to quit
```

### Simulator Results
```
QBER: 0.00%
Status: SECURE — Communication Successful
Sifted Key: 50 bits
Encrypted: 545fd7a8326f0bca...
Decrypted: Hello, Quantum World!
```

### Tests
```
Ran 31 tests in 0.048s
OK
```

---

## Performance

| Qubits | Time | Sifted Key | QBER |
|--------|------|-----------|------|
| 100 | ~100ms | ~50 bits | 0% |
| 500 | ~300ms | ~250 bits | 0% |
| 1000 | ~500ms | ~500 bits | 0% |

---

## Next Steps

1. ✅ Install: `pip install -r requirements.txt`
2. ✅ Run: `python app.py`
3. ✅ Open: http://localhost:8000
4. ✅ Click: "Launch Simulator"
5. ✅ Explore: Try different parameters
6. ✅ Learn: Read documentation

---

## Support

- **Quick Start**: START_HERE.md
- **Installation**: SETUP.md
- **Troubleshooting**: DEBUG_GUIDE.md
- **Documentation**: documentation.html (in web interface)
- **Diagnostic**: `python diagnose.py`

---

**Everything is ready. Start now!** 🚀

```bash
python app.py
```

Then open: **http://localhost:8000**
