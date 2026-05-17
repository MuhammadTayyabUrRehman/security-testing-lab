"""
Security Testing Lab - Intentionally Vulnerable Web Application
Purpose: Educational demonstration of OWASP Top 10 vulnerabilities
WARNING: This application is intentionally vulnerable for security testing only
         DO NOT use in production environments
"""

from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

# Flask application initialization
app = Flask(__name__)

# INTENTIONAL SECURITY FLAW: Weak secret key for session management
# In production, this should be a strong, randomly generated key stored securely
app.secret_key = 'weak_secret_key_for_lab'

# INTENTIONAL SECURITY FLAW: Hardcoded credentials stored in plaintext
# This demonstrates weak authentication practices
USERS = {
    'admin': 'admin123',
    'user': 'password'
}

# INTENTIONAL SECURITY FLAW: Sample user data stored without encryption
USER_DATA = {
    1: {'username': 'admin', 'email': 'admin@example.com', 'role': 'Administrator'},
    2: {'username': 'user', 'email': 'user@example.com', 'role': 'User'},
    3: {'username': 'guest', 'email': 'guest@example.com', 'role': 'Guest'}
}


# Decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page - redirects to dashboard if logged in, else to login"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page with weak authentication
    INTENTIONAL VULNERABILITIES:
    - No password hashing (plaintext comparison)
    - No account lockout after failed attempts
    - No CSRF protection
    - Predictable credentials
    """
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # INTENTIONAL SECURITY FLAW: No input validation
        if not username or not password:
            error = 'Username and password are required'
        # INTENTIONAL SECURITY FLAW: Plaintext password comparison
        elif username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            # INTENTIONAL SECURITY FLAW: Generic error message would be better
            # But here we're showing specific information about login failures
            error = 'Invalid username or password'
    
    return render_template('login.html', error=error)


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard page accessible only to logged-in users
    Displays user information and navigation
    """
    username = session.get('username')
    return render_template('dashboard.html', username=username)


@app.route('/search')
@login_required
def search():
    """
    Search page with REFLECTED XSS VULNERABILITY
    INTENTIONAL VULNERABILITY:
    - Query parameter 'q' is directly reflected in HTML without sanitization
    - Vulnerable to Cross-Site Scripting (XSS) attacks
    - Example: /search?q=<script>alert('XSS')</script>
    """
    query = request.args.get('q', '')
    
    # INTENTIONAL SECURITY FLAW: Direct reflection of user input
    # No HTML escaping or sanitization performed
    # This allows script injection
    result = f"You searched for: {query}" if query else "Enter a search term"
    
    return render_template('search.html', result=result)


@app.route('/profile')
@login_required
def profile():
    """
    Profile page with PARAMETER MANIPULATION VULNERABILITY
    INTENTIONAL VULNERABILITY:
    - URL parameter 'id' is used without validation
    - No authorization check to ensure user can only view own profile
    - Demonstrates Broken Access Control (OWASP #1)
    - Example: /profile?id=999 or /profile?id=1
    """
    user_id = request.args.get('id', type=int)
    
    if not user_id:
        return '''
        <h2>Profile Page</h2>
        <p>No user ID specified.</p>
        <p><a href="/dashboard">Back to Dashboard</a></p>
        '''
    
    # INTENTIONAL SECURITY FLAW: No authorization check
    # Any logged-in user can view any other user's profile
    if user_id in USER_DATA:
        user = USER_DATA[user_id]
        return f'''
        <html>
        <head><title>User Profile</title></head>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h2>User Profile</h2>
            <p><strong>Username:</strong> {user['username']}</p>
            <p><strong>Email:</strong> {user['email']}</p>
            <p><strong>Role:</strong> {user['role']}</p>
            <hr>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''
    else:
        return f'''
        <html>
        <head><title>User Profile</title></head>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h2>User Profile</h2>
            <p>User with ID {user_id} not found.</p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''


@app.route('/logout')
def logout():
    """
    Logout functionality - clears user session
    """
    session.clear()
    return redirect(url_for('login'))


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return '''
    <html>
    <head><title>Page Not Found</title></head>
    <body style="font-family: Arial, sans-serif; margin: 20px;">
        <h2>404 - Page Not Found</h2>
        <p>The page you are looking for does not exist.</p>
        <p><a href="/">Go to Home</a></p>
    </body>
    </html>
    ''', 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return '''
    <html>
    <head><title>Internal Server Error</title></head>
    <body style="font-family: Arial, sans-serif; margin: 20px;">
        <h2>500 - Internal Server Error</h2>
        <p>An unexpected error occurred.</p>
        <p><a href="/">Go to Home</a></p>
    </body>
    </html>
    ''', 500


# ==================== APPLICATION ENTRY POINT ====================

if __name__ == '__main__':
    # INTENTIONAL: Debug mode enabled for lab environment
    # In production, debug=False should be used
    app.run(debug=True, host='127.0.0.1', port=5000)
