from flask import Flask, render_template, request, jsonify, redirect, url_for
from zxcvbn import zxcvbn
import random
import time
from datetime import datetime
from urllib.parse import urlparse # Needed for URL checking
from data.scenarios import phishing_scenarios # Assuming this is the correct path

app = Flask(__name__)

# --- Utility/Context Processor ---
@app.context_processor
def inject_current_year():
    """Injects the current year into all templates for the footer."""
    return {'current_year': datetime.now().year}

# --- Core Routes ---

@app.route('/')
def index():
    """Homepage: Links to all info hubs and tools."""
    return render_template('index.html')

# --- Information Hub Routes ---

@app.route('/youth_info')
def youth_info():
    return render_template('info_hub/youth.html', title="Cyber Safety for Youth")

@app.route('/business_info')
def business_info():
    return render_template('info_hub/business.html', title="Digital Defense for Small Businesses")

@app.route('/farmer_info')
def farmer_info():
    return render_template('info_hub/farmers.html', title="Secure Technology for Tea Farmers")

@app.route('/checklist')
def checklist():
    return render_template('info_hub/checklist.html', title="Cyber Safety Checklist")


# --- Tool 1: Password Strength Checker ---

@app.route('/password_checker', methods=['GET'])
def password_checker():
    return render_template('password/password_check.html', title="Password Strength Checker")

@app.route('/check_password', methods=['POST'])
def check_password():
    """API endpoint to check password strength using zxcvbn."""
    password = request.json.get('password')
    if not password:
        return jsonify({"score": 0, "feedback": "Enter a password to check."})
    
    result = zxcvbn(password)
    score = result['score'] # 0 (worst) to 4 (best)
    
    # Simple, community-focused feedback
    if score == 0:
        feedback = "Very Weak! Use a unique, long passphrase of 15+ characters."
    elif score == 4:
        feedback = "Excellent! You are secure. Remember to enable MFA everywhere."
    else:
        feedback = result['feedback']['suggestions'][0] if result['feedback']['suggestions'] else "Good."

    return jsonify({"score": score, "feedback": feedback})


# --- Tool 2: Phishing Simulator ---

@app.route('/phishing_simulator', methods=['GET'])
def phishing_simulator_start():
    """Selects a random scenario and presents the simulated email."""
    scenario = random.choice(phishing_scenarios)
    return render_template('phishing/phish_test.html', scenario=scenario, title="Phishing Simulator")

@app.route('/phishing_result', methods=['POST'])
def phishing_result():
    """
    Handles the user's click. 
    If they click the phishing link, they are redirected to the fake login page.
    If they click the safe link, they go straight to the explanation.
    """
    scenario_id = request.form.get('scenario_id')
    user_action = request.form.get('action') # Either 'phishing_link' or 'safe_link'
    
    # Find the scenario details for the explanation
    scenario = next((s for s in phishing_scenarios if s['id'] == int(scenario_id)), None)
    
    if not scenario:
        return redirect(url_for('index'))
    
    # --- NEW BEHAVIOR: Redirect to fake login if phishing link is clicked ---
    if user_action == 'phishing_link':
        # Log the initial click and then redirect to the credential capture page
        with open('data/user_logs.txt', 'a') as f:
            f.write(f"[{time.ctime()}] IP: {request.remote_addr}, Scenario ID: {scenario_id}, Result: CLICKED_PHISHING_LINK\n")
        return redirect(url_for('fake_login_page'))
    
    # --- Safe Link clicked (Original behavior) ---
    # Log the safe attempt
    with open('data/user_logs.txt', 'a') as f:
        f.write(f"[{time.ctime()}] IP: {request.remote_addr}, Scenario ID: {scenario_id}, Result: {user_action}\n")

    is_safe = (user_action == 'safe_link')
    
    return render_template('phishing/explanation.html', 
                           is_safe=is_safe, 
                           explanation=scenario['explanation'],
                           scenario_name=scenario['subject'])


@app.route('/fake_login', methods=['GET'])
def fake_login_page():
    """Renders the fake login page when the user clicks the phishing link."""
    # This page looks like the real target (e.g., bank/M-Pesa login)
    return render_template('phishing/fake_login.html', title="Account Verification")

@app.route('/log_credentials', methods=['POST'])
def log_credentials():
    """Logs the (fake) credentials entered by the user and redirects to the explanation."""
    
    # Log the data, which is the key instructional moment
    username = request.form.get('username', 'N/A')
    password = request.form.get('password', 'N/A')
    
    with open('data/user_logs.txt', 'a') as f:
        f.write(f"[{time.ctime()}] IP: {request.remote_addr}, Action: CREDENTIALS_STOLEN, User: {username}, Pass: [LOGGED]\n")

    # Redirect them to the explanation page for the final warning
    return redirect(url_for('phishing_result_direct', 
                            action='credentials_stolen', 
                            subject='Fake Login Attempt'))

@app.route('/phishing_result_direct')
def phishing_result_direct():
    """Renders the explanation page directly after a fake login attempt."""
    user_action = request.args.get('action')
    scenario_name = request.args.get('subject', 'Phishing Attempt')
    
    explanation_text = "CREDENTIALS STOLEN! You entered your username and password into a fake login page. This is the final, most damaging step of a phishing attack. **Always check the URL in the address bar before typing your details.**"
    
    is_safe = (user_action != 'credentials_stolen')
    
    return render_template('phishing/explanation.html', 
                           is_safe=is_safe, 
                           explanation=explanation_text,
                           scenario_name=scenario_name)


# --- Tool 3: URL Checker ---

@app.route('/url_checker', methods=['GET'])
def url_checker():
    """Renders the URL checker input page."""
    return render_template('url_checker/url_checker.html', title="Link Safety Checker")

@app.route('/check_url', methods=['POST'])
def check_url():
    """API endpoint to perform basic URL safety checks."""
    url = request.json.get('url', '').strip()
    
    if not url:
        return jsonify({"status": "error", "message": "Please enter a link to check."})

    # 1. Check for HTTPS (Secure connection)
    is_https = url.lower().startswith('https://')
    
    # Get the hostname from the URL
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc
    except Exception:
        hostname = ""

    # Simple check for numeric IP address used instead of domain
    is_ip_address = hostname and all(part.isdigit() for part in hostname.split('.')) and hostname.count('.') == 3
    
    # Simple check for very long, obfuscated subdomains
    is_obfuscated = len(hostname) > 50

    if not is_https:
        status = "Warning"
        message = "This link uses **HTTP** (not HTTPS). Your connection is **NOT encrypted** and data sent may be visible to others. A major red flag!"
    elif is_ip_address:
        status = "Danger"
        message = "This link leads directly to an **IP address** instead of a verified domain name. This is often used by scammers. Do not proceed!"
    elif is_obfuscated:
        status = "Warning"
        message = "The domain name is extremely long and complex. This is often a sign of **obfuscation** used in phishing."
    else:
        status = "Safe"
        message = "This link uses **HTTPS** (encrypted). The connection appears secure, but **always check the domain name yourself** for misspellings!"

    return jsonify({"status": status, "message": message, "is_https": is_https})


if __name__ == '__main__':
    app.run(debug=True)