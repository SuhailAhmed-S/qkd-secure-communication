# QUICK REFERENCE - NEW SIMULATOR FEATURES

## 🎯 What's New in simulator.html v2.1

### 1️⃣ ALICE & BOB MEASUREMENTS TABLE
**How to Use**:
1. Run a simulation
2. Click "Measurements" tab
3. View detailed comparison of Alice's qubits vs Bob's measurements
4. See which bases matched (used for sifted key)

**Table Columns**:
| Column | What It Shows |
|--------|---------------|
| Index | Row number (0-49) |
| Alice Qubit | Value Alice sent (0 or 1) |
| Alice Basis | How Alice encoded (+Rectilinear or ×Diagonal) |
| Bob Basis | How Bob measured (random choice) |
| Bob Result | What Bob measured |
| Match | ✓ Yes if bases agree, ✗ No if different |
| Bit Used | If match=Yes, this bit goes in sifted key |

**Statistics**:
- Total Measurements: How many qubits processed
- Valid Sift: How many basis matches (sifted key size)
- Errors: Mismatches in measurement data

---

### 2️⃣ AMPLIFIED KEY DETAILS
**How to Use**:
1. Run a simulation
2. Click "Amplified Key" tab
3. See complete post-processing information

**Information Provided**:
```
Amplified Key Length: 62 bits (from 95 sifted bits)
Compression Ratio: 65.3% (how much key remains)
Sifted → Amplified: 95 → 62
Method: Toeplitz + SHA-256
Key (hex): a1f2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a...
```

**Compression Ratio Meaning**:
- **66%** = Clean channel (low QBER) → Aggressive compression
- **50%** = Normal channel → Moderate compression
- **30%** = Noisy channel (higher QBER) → Conservative compression
- **10%** = Very suspicious channel (high QBER) → Minimal key

---

### 3️⃣ ALICE ONLINE STATUS
**How to Use**:
1. Click "Check Status" button in right panel
2. See Alice/Eve/Bob server status
3. Color changes: 🟢 Green = Online, 🔴 Red = Offline

**Status Display**:
```
👩 ALICE (Sender)
● Online
Status: 🟢 Online
```

**Check Status Features**:
- Real-time server polling
- Individual service status
- Live feedback in message feed
- Auto-check on page load

---

### 4️⃣ TAB INTERFACE (4 Tabs)
**Tab 1: Summary**
- QBER percentage
- Secure or Compromised status
- Quick numbers (initial qubits, sifted, amplified, matches)

**Tab 2: Measurements**
- Alice/Bob measurement comparison table
- Detailed statistics

**Tab 3: Amplified Key**
- Key length and compression info
- Privacy amplification method
- Hex key display

**Tab 4: Encryption**
- Original message
- Encrypted message (hex)
- Decrypted message
- Success/Failure status

---

### 5️⃣ ERROR HANDLING & SAFETY

**Automatic Error Handling**:
- ✓ Null checks on all API responses
- ✓ Input validation on form fields
- ✓ Try-catch for display logic
- ✓ User-friendly error messages
- ✓ Console logging for debugging

**Example Error Messages**:
```
❌ Invalid qubit count. Must be between 10 and 1000.
❌ API error: 500
❌ Status check failed: Network error
```

---

## 🚀 QUICK START TEST

**To test all new features**:

1. Open browser to `http://localhost:8000/simulator`
2. Enter 100 in "Number of Qubits" (default)
3. Click "▶ Run Simulation"
4. Click "Check Status" to verify servers
5. Click through all 4 tabs to see different results:
   - **Summary**: Overview of protocol
   - **Measurements**: Alice vs Bob comparison
   - **Amplified Key**: Key compression details
   - **Encryption**: Message encryption/decryption
6. Try different qubit counts (10-1000)
7. Toggle "Enable Eve" and run again
8. Check message feed for all operations

---

## 📊 UNDERSTANDING THE NUMBERS

**Example with 100 qubits, 0% QBER (clean channel)**:
```
Initial Qubits: 100
  ↓
Sifted Key: ~50 (50% basis match)
  ↓
Amplified Key: ~33 (66% compression)

Compression Ratio: 66.0%
Security: Secure (100% confidence)
QBER: 0.00%
```

**Example with eavesdropping (Eve enabled)**:
```
Initial Qubits: 100
  ↓
Sifted Key: ~50 (50% basis match)
  ↓
Amplified Key: ~5 (10% compression - very conservative!)

Compression Ratio: 10.0%
Security: Compromised (Possible eavesdropping)
QBER: 25.00%
```

---

## 🔍 TROUBLESHOOTING

**Problem**: "Run simulation to see measurements" shows in table
**Solution**: Click "Run Simulation" first, then click Measurements tab

**Problem**: Amplified Key shows "-- bits"
**Solution**: Make sure simulation ran successfully (check message feed)

**Problem**: Alice shows "Offline"
**Solution**: Make sure Flask backend is running on port 8000

**Problem**: Page loads slowly
**Solution**: Check network connection, try refreshing

**Problem**: Encrypted/Decrypted message shows "N/A"
**Solution**: Common if API error - check browser console (F12)

---

## 💡 KEY INSIGHTS FROM DATA

**What to Look for**:
1. **QBER < 11%** = ✓ Secure
2. **QBER > 11%** = ✗ Possible eavesdropping
3. **Compression Ratio ~66%** = Channel is clean
4. **Compression Ratio ~10%** = Channel is noisy/compromised
5. **Matches = ~50%** = Normal for BB84 (randomness guarantee)

**Quality Indicators**:
- ✓ Original == Decrypted = Encryption working
- ✓ QBER near 0% = Clean quantum channel
- ✓ Compression 50-66% = Good key quality
- ✗ QBER > 25% = Serious concern
- ✗ Decryption fails = Protocol error

---

## 📱 RESPONSIVE BEHAVIOR

**On Different Devices**:

**Desktop** (Wide screens)
- 3-column layout (Configuration | Results | Status)
- Full table visible
- All information at once

**Tablet** (Medium screens)
- Single column layout
- Tables scrollable horizontally
- Touch-friendly buttons

**Mobile** (Small screens)
- Vertical layout
- Simplified tables
- Large tap targets

---

## 🎨 VISUAL INDICATORS

**Status Colors**:
- 🟢 **Green** = Good/Online/Secure
- 🔴 **Red** = Bad/Offline/Compromised
- 🔵 **Cyan** = Active/Information

**Message Types**:
- ℹ️ System (Cyan) = Protocol info
- ✓ Success (Green) = Secure channel
- ✗ Error (Red) = Problem detected
- ⚠️ Warning (Orange) = Advisory

---

## 🔐 SECURITY NOTES

- Full key not displayed (truncated to first 64 chars)
- User input safely escaped
- No XSS vulnerabilities
- All errors logged
- API responses validated

---

## 📞 SUPPORT

For issues or questions:
1. Check browser console (F12 → Console tab)
2. Verify Flask backend running
3. Check simulator_audit_report.md for full details
4. Review error messages in message feed

---

**Version**: 2.1  
**Last Updated**: 2025-03-25  
**Status**: ✅ Production Ready
