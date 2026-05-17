# Security Testing Lab: Vulnerability Identification and Risk Assessment

## 🔓 Intentionally Vulnerable Web Application for Educational Purposes

> **⚠️ WARNING**: This application is **intentionally vulnerable** for educational security testing only. **DO NOT** deploy to production or use with real data.

---

## Project Overview

This is a Flask-based web application designed to teach security testing methodologies and demonstrate OWASP Top 10 vulnerabilities. Students can identify, document, and understand common web application security flaws in a controlled educational environment.

### Learning Objectives

- Identify common web application vulnerabilities
- Understand OWASP Top 10 security risks
- Practice security testing techniques
- Learn proper remediation strategies
- Develop secure coding practices

---

## Features & Vulnerabilities

### ✅ Implemented Features

| Feature | Type | Vulnerability | Severity |
|---------|------|----------------|----------|
| **Authentication** | Login System | Weak Authentication (plaintext passwords, no lockout) | HIGH |
| **Session Management** | Flask Sessions | Weak Secret Key | HIGH |
| **Search Feature** | Query Parameter | Reflected XSS | HIGH |
| **Profile Access** | URL Parameter | Broken Access Control | **CRITICAL** |
| **Dashboard** | Protected Route | None (proper access control) | N/A |
| **Logout** | Session Clearing | None (proper implementation) | N/A |

### 🔴 OWASP Top 10 Vulnerabilities Demonstrated

1. **A01:2021 - Broken Access Control** - Profile endpoint lacks authorization checks
2. **A02:2021 - Cryptographic Failures** - Plaintext password storage
3. **A03:2021 - Injection** - Reflected XSS in search feature
4. **A05:2021 - Security Misconfiguration** - Weak session secret key
5. **A07:2021 - Identification and Authentication Failures** - No account lockout, weak credentials

---

## Quick Start

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Windows 10/11** or compatible OS
- Modern web browser

### Installation

```powershell
# 1. Navigate to project directory
cd "c:\Local Disk (D)\Semester Resources\semester 6\V&V Lab\lab 10\security-testing-lab"

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the Application

```powershell
# Ensure virtual environment is activated
python app.py
```

Application will start at: **http://127.0.0.1:5000**

### Test Credentials

| Username | Password |
|----------|----------|
| `admin` | `admin123` |
| `user` | `password` |

---

## Project Structure

```
security-testing-lab/
│
├── app.py                    # Main Flask application with all routes
├── requirements.txt          # Python package dependencies
├── README.md                 # This file
├── INSTALL.txt              # Detailed installation instructions
├── TESTING.txt              # Comprehensive testing guide
│
├── templates/
│   ├── login.html           # Login page (weak authentication demo)
│   ├── dashboard.html       # User dashboard (after login)
│   └── search.html          # Search feature (XSS vulnerability demo)
│
└── static/                  # Static files directory (CSS, JS, images)
    └── (empty for lab)
```

---

## Application Routes

### Public Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page (redirects to dashboard or login) |
| `/login` | GET, POST | User authentication |

### Protected Routes (Requires Login)

| Route | Method | Vulnerability | Example |
|-------|--------|----------------|---------|
| `/dashboard` | GET | None (proper protection) | http://127.0.0.1:5000/dashboard |
| `/search` | GET | Reflected XSS | http://127.0.0.1:5000/search?q=<script>alert('XSS')</script> |
| `/profile` | GET | Broken Access Control | http://127.0.0.1:5000/profile?id=1 |
| `/logout` | GET | None (proper implementation) | http://127.0.0.1:5000/logout |

---

## Key Vulnerabilities & Test Cases

### 1. Broken Access Control (CRITICAL)

**Location**: `/profile` endpoint

**Issue**: No authorization checks - any authenticated user can view any user's profile

**Test**:
```
1. Login as 'user' account
2. Visit: http://127.0.0.1:5000/profile?id=1
3. Result: Can view ADMIN's profile information
```

**Impact**: Data breach, unauthorized information disclosure

---

### 2. Reflected XSS Injection

**Location**: `/search` endpoint - query parameter `q`

**Issue**: User input directly reflected in HTML without sanitization

**Test**:
```
1. Navigate to: http://127.0.0.1:5000/search?q=<script>alert('XSS')</script>
2. Result: JavaScript alert box appears
3. Input is reflected unescaped in the HTML response
```

**Impact**: Session hijacking, malware distribution, credential theft

---

### 3. Weak Authentication

**Location**: `/login` endpoint

**Issues**:
- Plaintext password storage
- No account lockout after failed attempts
- No rate limiting
- Weak credentials provided

**Test**:
```
1. Attempt login with 'admin / admin123' repeatedly
2. No lockout after failed attempts
3. No delays between attempts
4. Vulnerable to brute force attacks
```

**Impact**: Unauthorized account access

---

### 4. Security Misconfiguration

**Location**: `app.secret_key` in app.py

**Issue**: Weak session secret key - easy to guess

```python
app.secret_key = 'weak_secret_key_for_lab'  # Too simple!
```

**Impact**: Session token forgery, authentication bypass

---

## Testing Instructions

### Quick Test Scenarios

**Scenario 1: Valid Login**
- Navigate to http://127.0.0.1:5000/login
- Enter: `admin` / `admin123`
- Expected: Redirected to dashboard

**Scenario 2: XSS Attack**
- Click "Search Feature" on dashboard
- Enter: `<img src=x onerror=alert('Hacked')>`
- Expected: Alert box appears (XSS successful)

**Scenario 3: Access Control Bypass**
- Login as regular user
- Visit: http://127.0.0.1:5000/profile?id=1
- Expected: Can view admin's profile (unauthorized access)

**Scenario 4: Brute Force**
- Try multiple failed login attempts
- Expected: No account lockout, unlimited attempts

### Comprehensive Testing Guide

See [TESTING.txt](TESTING.txt) for:
- Detailed test cases (50+ scenarios)
- OWASP vulnerability mapping
- Attack scenarios and payloads
- Remediation recommendations
- Testing tools and techniques

---

## Security Vulnerabilities Details

### Critical Security Issues

#### Issue #1: Plaintext Password Storage
```python
# INSECURE - DO NOT USE IN PRODUCTION
USERS = {
    'admin': 'admin123',    # Password visible in plaintext
    'user': 'password'
}
```

**Remediation**: Use bcrypt, argon2, or scrypt for password hashing

---

#### Issue #2: No Input Sanitization (XSS)
```python
# INSECURE - Direct reflection without escaping
{{ result | safe }}  # Raw HTML, no escaping
```

**Remediation**: Use HTML escaping
```python
{{ result | escape }}  # Properly escaped
```

---

#### Issue #3: No Authorization Checks
```python
# INSECURE - No check if user owns this profile
if user_id in USER_DATA:
    return render_profile(user_id)  # Any user can access
```

**Remediation**: Add authorization check
```python
if user_id != current_user_id:
    return "Unauthorized", 403
```

---

#### Issue #4: No Account Lockout
```python
# INSECURE - Unlimited login attempts
while True:
    attempt_password()  # No lockout mechanism
```

**Remediation**: Implement rate limiting and lockout
```python
if failed_attempts[username] > 5:
    return "Account locked", 429
```

---

## Files Overview

### app.py
- **Lines 1-50**: Flask setup and configuration (intentionally weak)
- **Lines 51-80**: User data storage (intentionally insecure)
- **Lines 81-120**: Authentication routes with vulnerabilities
- **Lines 121-160**: Protected routes with access control issues
- **Lines 161-200**: XSS vulnerable search route
- **Lines 201-240**: Access control vulnerable profile route
- **Lines 241+**: Error handlers and app execution

### HTML Templates

**login.html** (~150 lines)
- Responsive login form
- Displays test credentials for educational purposes
- Shows error messages from failed login attempts
- Professional UI for security lab

**dashboard.html** (~200 lines)
- Welcome message with logged-in username
- Navigation cards for lab features
- Feature explanations
- Interactive guide button

**search.html** (~250 lines)
- Search input form
- Vulnerable output display (XSS demo)
- Vulnerability explanation section
- Test cases and payload examples
- Educational comments about XSS risks

---

## Troubleshooting

### Issue: "Module not found: flask"
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Issue: "Address already in use"
```powershell
# Port 5000 is already in use
# Option 1: Stop other process on port 5000
# Option 2: Change port in app.py
#   Change: app.run(port=5000)
#   To:     app.run(port=5001)
```

### Issue: "Permission denied" when activating venv
```powershell
# Run PowerShell as Administrator
# Or set execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Best Practices & Recommendations

### For Instructors

1. **Lab Duration**: 2-3 hours recommended
2. **Prerequisites**: Basic web development knowledge helpful
3. **Assessment**: Have students document vulnerabilities found
4. **Discussion**: Review remediation strategies after testing

### For Students

1. **Follow Lab Safely**: Use only in isolated local environment
2. **Document Findings**: Create security testing reports
3. **Understand Root Causes**: Learn WHY each vulnerability exists
4. **Learn Remediation**: Study how to fix each vulnerability
5. **Never Replicate**: Don't use techniques on real systems without permission

### Security Disclaimer

```
⚠️  THIS APPLICATION IS INTENTIONALLY VULNERABLE ⚠️

✓ USE ONLY FOR:
  - Educational and training purposes
  - Laboratory environments
  - Security testing practice
  - Academic research

✗ DO NOT:
  - Deploy to production
  - Expose to the internet
  - Use with real data
  - Use as code reference for real applications
  - Use on systems you don't own
```

---

## Learning Resources

### OWASP Top 10
- https://owasp.org/www-project-top-ten/

### Flask Security
- https://flask.palletsprojects.com/en/latest/security/

### OWASP Testing Guide
- https://owasp.org/www-project-web-security-testing-guide/

### CWE Top 25
- https://cwe.mitre.org/top25/

---

## Requirements

### Python Packages
- `Flask==2.3.2` - Web framework
- `Werkzeug==2.3.6` - WSGI utility library

### System Requirements
- Python 3.8 or higher
- Windows 10/11 or compatible OS
- 100MB free disk space
- Modern web browser (Chrome, Firefox, Edge, Safari)

---

## Project Submission Checklist

When submitting this project:

- [ ] All files present and properly organized
- [ ] `app.py` contains all required routes
- [ ] All HTML templates display correctly
- [ ] Application runs without errors
- [ ] Both test accounts work (admin/user)
- [ ] Search feature demonstrates XSS
- [ ] Profile endpoint shows broken access control
- [ ] `INSTALL.txt` provides clear setup instructions
- [ ] `TESTING.txt` includes comprehensive test cases
- [ ] `requirements.txt` lists all dependencies
- [ ] Project is properly formatted and ready for submission

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | May 2026 | Initial release with 5 core vulnerabilities |

---

## Author & Academic Use

**Created for**: University V&V Lab Course  
**Purpose**: Security Testing Education  
**Semester**: 6 (Academic Year 2026)  

**This project is an academic deliverable demonstrating intentional vulnerability implementation for educational security testing purposes.**

---

## Support & Questions

For issues or questions:
1. Review [INSTALL.txt](INSTALL.txt) for setup issues
2. Check [TESTING.txt](TESTING.txt) for testing guidance
3. Review inline comments in `app.py`
4. Consult OWASP documentation
5. Review Flask security documentation

---

## License

Educational Use Only  
© 2026 V&V Lab - Security Testing Course  

**NOT FOR PRODUCTION USE**

---

**Last Updated**: May 17, 2026  
**Status**: Ready for Academic Submission  
**Compliance**: OWASP Top 10 2021

