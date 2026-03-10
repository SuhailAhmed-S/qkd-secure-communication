# 🚀 QKD BB84 Protocol - Complete Setup Guide

## Quick Start (2 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open Browser
```
http://localhost:8000
```

### 4. Click "Run Protocol"
Done! 🎉

---

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 512 MB minimum
- **Disk**: 100 MB

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/qkd-secure-communication.git
cd qkd-secure-communication
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python test_qkd.py
```

Should show: `Ran 31 tests in X.XXXs - OK`

---

## Running the Application

### Option 1: Web Interface (Recommended)
```bash
python app.py
```
- Opens on: http://localhost:8000
- Features: Interactive UI, real-time results, visualization

### Option 2: Command Line
```bash
python qkd_main.py
```
- Direct protocol execution
- Console output only
- No web interface

### Option 3: Python Script
```python
from qkd_main import run_qkd

result = run_qkd(
    num_qubits=100,
    message="Secret message",
    eve_enabled=False
)

print(f"QBER: {result['qber']*100:.2f}%")
print(f"Secure: {result['secure']}")
print(f"Decrypted: {result['decrypted']}")
```

---

## Web Interface Guide

### Home Page (`/`)
- Protocol overview
- Feature showcase
- Getting started guide

### Simulator Page (`/simulator`)
- **Number of Qubits**: 10-1000 (default: 100)
- **Message**: Text to encrypt (default: "Hello QKD!")
- **Enable Eve**: Toggle eavesdropping simulation
- **Run Protocol**: Execute the protocol

### Results Display
- **QBER**: Quantum Bit Error Rate percentage
- **Status**: SECURE or COMPROMISED
- **Sifted Key**: Number of bits kept after basis reconciliation
- **Encrypted**: Hex-encoded ciphertext
- **Decrypted**: Recovered plaintext
- **Message Feed**: Real-time protocol execution log
- **Qubit Analysis**: Detailed basis matching table

### Documentation Page (`/documentation`)
- Complete protocol explanation
- Security analysis
- Mathematical background

---

## API Endpoints

### GET `/`
Returns home page

### GET `/simulator`
Returns simulator interface

### GET `/documentation`
Returns documentation page

### POST `/api/run_qkd`
Executes QKD protocol

**Request**:
```json
{
  "num_qubits": 100,
  "message": "Hello QKD!",
  "eve_enabled": false
}
```

**Response**:
```json
{
  "num_qubits": 100,
  "sift_count": 50,
  "qber": 0.0,
  "qber_pct": "0.00%",
  "secure": true,
  "status": "SECURE — Communication Successful",
  "key_hex": "073ab4dd400a2ba7280204cba24e73c7",
  "encrypted": "545fd7a8326f0bca...",
  "decrypted": "Hello QKD!",
  ...
}
```

### GET `/api/messages`
Returns message log

### POST `/api/clear_messages`
Clears message log

---

## Testing

### Run All Tests
```bash
python test_qkd.py
```

### Run Specific Test
```bash
python -m unittest test_qkd.TestSecurityModule -v
```

### Run with Coverage
```bash
pytest --cov=. test_qkd.py
```

### Expected Output
```
Ran 31 tests in 0.048s
OK

All tests passed successfully!
```

---

## Project Structure

```
qkd-secure-communication/
├── Core Modules
│   ├── alice.py              # Alice's qubit preparation
│   ├── bob.py                # Bob's measurement & sifting
│   ├── eve.py                # Eve's intercept-resend attack
│   ├── quantum_channel.py    # Quantum channel simulation
│   ├── security.py           # QBER calculation & encryption
│   └── qkd_main.py           # Protocol orchestrator
│
├── Web Application
│   ├── app.py                # Flask web application
│   ├── config.py             # Configuration management
│   └── templates/
│       ├── home.html         # Home page
│       ├── simulator.html    # Simulator interface
│       ├── documentation.html # Documentation
│       └── index.html        # Legacy index
│
├── Testing & Deployment
│   ├── test_qkd.py           # Comprehensive test suite
│   ├── test_flask.py         # Flask tests
│   ├── requirements.txt      # Python dependencies
│   ├── setup.py              # Setup script
│   ├── Dockerfile            # Docker image
│   └── docker-compose.yml    # Docker Compose
│
└── Documentation
    ├── README.md             # Main documentation
    ├── SETUP.md              # This file
    ├── FINAL_FIX.md          # Solution summary
    └── [other guides]
```

---

## Configuration

### Environment Variables
```bash
export FLASK_ENV=development
export FLASK_APP=app.py
export FLASK_DEBUG=1
```

### Config File (`config.py`)
```python
class Config:
    DEBUG = False
    MIN_QUBITS = 10
    MAX_QUBITS = 1000
    QBER_THRESHOLD = 0.11
    PREVIEW_LENGTH = 20
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution**: Use different port
```bash
python app.py --port 5000
```

Or kill the process using the port:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Issue: "Connection refused" or "Timeout"
**Solution**: Make sure you're using in-process mode (not distributed servers)
```bash
python app.py  # Correct
# NOT: python alice_server_improved.py
```

### Issue: Tests fail
**Solution**: Verify Python version and dependencies
```bash
python --version  # Should be 3.8+
pip install -r requirements.txt --upgrade
python test_qkd.py
```

---

## Performance Optimization

### For Large Qubit Counts
```python
# Increase timeout for large simulations
result = run_qkd(num_qubits=10000, message="Test", eve_enabled=False)
```

### For Production Deployment
```bash
# Use Gunicorn instead of Flask development server
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

### For Docker Deployment
```bash
# Build image
docker build -t qkd-app .

# Run container
docker run -p 8000:8000 qkd-app

# Or use Docker Compose
docker-compose up -d
```

---

## Development

### Code Style
```bash
# Format code
black *.py

# Check style
flake8 *.py

# Type checking
mypy *.py
```

### Adding New Features
1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes with tests
3. Run tests: `python test_qkd.py`
4. Commit: `git commit -am "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Create pull request

---

## Security Notes

⚠️ **Educational Implementation**
- ✓ Correct BB84 protocol
- ✓ Proper QBER calculation
- ✓ Eavesdropping detection works
- ⚠️ Classical channel not authenticated
- ⚠️ XOR cipher is simple (not production-grade)
- ⚠️ Simulated quantum mechanics (not real quantum)

**Not for production use with real secrets!**

---

## Support & Resources

### Documentation
- `README.md` - Main documentation
- `FINAL_FIX.md` - Solution summary
- `IN_PROCESS_FIX.md` - Architecture explanation
- `DEBUG_GUIDE.md` - Troubleshooting guide

### References
- [BB84 Protocol Paper](https://en.wikipedia.org/wiki/BB84)
- [Quantum Cryptography](https://en.wikipedia.org/wiki/Quantum_cryptography)
- [QBER Threshold](https://en.wikipedia.org/wiki/Quantum_key_distribution#Security)

### Getting Help
- Check `DEBUG_GUIDE.md` for common issues
- Run `python diagnose.py` to check system status
- Review test output: `python test_qkd.py -v`

---

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Run tests: `python test_qkd.py`
3. ✅ Start app: `python app.py`
4. ✅ Open browser: http://localhost:8000
5. ✅ Click "Run Protocol"
6. ✅ Enjoy! 🎉

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
