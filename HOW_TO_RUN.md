# How to Run the QKD BB84 Protocol System

## Quick Start (5 minutes)

### Option 1: Standalone Mode (Easiest)
Run the complete protocol in a single Python script without distributed servers:

```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python qkd_main.py
```

**Output**: Shows complete BB84 protocol execution with QBER calculation and encryption results.

---

## Option 2: Distributed Mode (Advanced)

This runs Alice, Bob, and Eve as separate servers communicating over network sockets.

### Prerequisites
```bash
pip install -r requirements.txt
```

### Step 1: Start Eve Server (Terminal 1)
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python eve_server_improved.py
```

**Expected Output**:
```
======================================================================
  EVE SERVER — Quantum Channel Eavesdropper
======================================================================
Listening on port 5002...

Waiting for Alice's qubits...
```

### Step 2: Start Bob Server (Terminal 2)
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python bob_server_improved.py
```

**Expected Output**:
```
======================================================================
  BOB SERVER — Quantum Receiver
======================================================================
Listening on port 5003...

Waiting for qubits...
```

### Step 3: Start Alice Server (Terminal 3)
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python alice_server_improved.py
```

**Expected Output**:
```
======================================================================
  ALICE SERVER — Quantum Key Distribution Transmitter
======================================================================
Listening on port 5004...

Waiting for configuration from Flask...
```

### Step 4: Start Flask Web Application (Terminal 4)
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python app.py
```

**Expected Output**:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:8000
```

### Step 5: Open Web Browser
Navigate to: **http://localhost:8000**

You should see the QKD simulator interface.

---

## Option 3: Run Tests

### Run All Tests
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python test_qkd.py
```

**Expected Output**:
```
test_prepare_returns_correct_structure ... ok
test_prepare_correct_lengths ... ok
test_prepare_bits_are_binary ... ok
...
Ran 31 tests in 0.048s
OK
```

### Run Specific Test Class
```bash
python -m unittest test_qkd.TestSecurityModule -v
```

### Run with Coverage
```bash
pytest --cov=. test_qkd.py
```

---

## Using the Web Interface

### 1. Home Page (`/`)
- Overview of BB84 protocol
- Feature showcase
- Educational information

### 2. Simulator Page (`/simulator`)
- **Number of Qubits**: Set between 10-1000 (default: 100)
- **Message**: Enter text to encrypt (default: "Hello QKD!")
- **Enable Eve**: Toggle eavesdropping simulation
- **Run Protocol**: Click to execute

### 3. Results Display
After running, you'll see:
- **QBER**: Quantum Bit Error Rate percentage
- **Security Status**: SECURE or COMPROMISED
- **Sifted Key Length**: Number of bits kept after basis reconciliation
- **Encrypted Message**: Hex-encoded ciphertext
- **Decrypted Message**: Recovered plaintext
- **Live Message Feed**: Real-time protocol communication
- **Qubit Analysis**: Detailed table of basis matching

### 4. Documentation Page (`/documentation`)
- Complete protocol explanation
- Security analysis
- Mathematical background

---

## API Usage (Programmatic)

### Python Script Example
```python
from qkd_main import run_qkd

# Run QKD protocol
result = run_qkd(
    num_qubits=200,
    message="Secret message",
    eve_enabled=False
)

# Check results
print(f"QBER: {result['qber']*100:.2f}%")
print(f"Secure: {result['secure']}")
print(f"Sifted Key Length: {result['sift_count']}")
print(f"Encrypted: {result['encrypted']}")
print(f"Decrypted: {result['decrypted']}")
```

### cURL Example (Distributed Mode)
```bash
curl -X POST http://localhost:8000/api/run_qkd \
  -H "Content-Type: application/json" \
  -d '{
    "num_qubits": 100,
    "message": "Hello Quantum",
    "eve_enabled": false
  }'
```

### Python Requests Example
```python
import requests
import json

url = "http://localhost:8000/api/run_qkd"
payload = {
    "num_qubits": 100,
    "message": "Hello Quantum",
    "eve_enabled": False
}

response = requests.post(url, json=payload)
result = response.json()

print(f"QBER: {result['qber_pct']}")
print(f"Status: {result['status']}")
print(f"Decrypted: {result['decrypted']}")
```

---

## Troubleshooting

### Issue: "Connection refused" when starting Flask
**Solution**: Make sure all three servers (Alice, Bob, Eve) are running first.

### Issue: "Port already in use"
**Solution**: Kill the process using the port:
```bash
# Windows
netstat -ano | findstr :5004
taskkill /PID <PID> /F

# Or change port in code
```

### Issue: "No module named 'flask'"
**Solution**: Install requirements:
```bash
pip install -r requirements.txt
```

### Issue: Timeout waiting for results
**Solution**: 
1. Check all three servers are running
2. Check network connectivity
3. Increase timeout in `app.py` (line 105)

### Issue: "Malformed JSON" error
**Solution**: Ensure all servers are using the same Python version and have compatible libraries.

---

## Performance Notes

| Qubits | Time | Sifted Key | QBER (no Eve) |
|--------|------|-----------|---------------|
| 100 | ~50ms | ~50 bits | 0% |
| 500 | ~200ms | ~250 bits | 0% |
| 1000 | ~400ms | ~500 bits | 0% |

---

## Expected Results

### Scenario 1: Secure Channel (eve_enabled=false)
```
QBER: 0.00%
Status: SECURE — Communication Successful
Sifted Key: ~50% of transmitted qubits
Encrypted: Successfully encrypted
Decrypted: Matches original message
```

### Scenario 2: With Eavesdropping (eve_enabled=true)
```
QBER: ~25.00%
Status: COMPROMISED — Eavesdropping Detected
Sifted Key: ~50% of transmitted qubits
Encrypted: Not used (channel aborted)
Decrypted: None (communication aborted)
```

---

## Docker Deployment (Optional)

### Build Docker Image
```bash
docker build -t qkd-app .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

### Access Application
```
http://localhost:5000
```

### Stop Services
```bash
docker-compose down
```

---

## Development Mode

### Enable Debug Logging
Edit `app.py` and set:
```python
app.run(debug=True, port=8000, host='0.0.0.0')
```

### View Server Logs
Each server prints detailed logs to console:
- `[ALICE]` - Alice server messages
- `[BOB]` - Bob server messages
- `[EVE]` - Eve server messages
- `[SYSTEM]` - Flask system messages

### Monitor Network Traffic
```bash
# Windows
netstat -an | findstr ESTABLISHED

# Check specific ports
netstat -ano | findstr :5002
netstat -ano | findstr :5003
netstat -ano | findstr :5004
```

---

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

### Using Nginx Reverse Proxy
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

### Environment Variables
```bash
export FLASK_ENV=production
export FLASK_APP=app.py
export PYTHONUNBUFFERED=1
```

---

## Common Commands

### Check Python Version
```bash
python --version
```

### Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Linting
```bash
flake8 *.py
pylint *.py
```

### Format Code
```bash
black *.py
```

### Type Checking
```bash
mypy *.py
```

---

## File Structure Reference

```
qkd-secure-communication/
├── qkd_main.py                 # Standalone protocol runner
├── alice_server_improved.py    # Alice distributed server
├── bob_server_improved.py      # Bob distributed server
├── eve_server_improved.py      # Eve distributed server
├── app.py                      # Flask web application
├── alice.py                    # Alice module
├── bob.py                      # Bob module
├── eve.py                      # Eve module
├── security.py                 # Security analysis
├── quantum_channel.py          # Channel simulation
├── config.py                   # Configuration
├── test_qkd.py                 # Test suite
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker image
├── docker-compose.yml          # Docker Compose
└── templates/
    ├── home.html              # Home page
    ├── simulator.html         # Simulator interface
    └── documentation.html     # Documentation
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Run standalone | `python qkd_main.py` |
| Run tests | `python test_qkd.py` |
| Start Eve | `python eve_server_improved.py` |
| Start Bob | `python bob_server_improved.py` |
| Start Alice | `python alice_server_improved.py` |
| Start Flask | `python app.py` |
| Open web UI | `http://localhost:8000` |
| Check servers | `netstat -ano \| findstr :500` |

---

## Support

For issues or questions:
1. Check the `FIXES_APPLIED.md` for recent changes
2. Review server console output for error messages
3. Check `test_qkd.py` for usage examples
4. Read docstrings in source files for API details

---

**Last Updated**: 2024
**Status**: Ready to run ✅
