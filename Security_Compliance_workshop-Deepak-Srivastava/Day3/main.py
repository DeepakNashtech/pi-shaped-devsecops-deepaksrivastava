import os
from flask import Flask, request, redirect, render_template_string
import subprocess

app = Flask(__name__)

# --- VULNERABILITY 1: Hardcoded Secret (for Gitleaks) ---
# Hardcoded credentials are a major security flaw.
SECRET_API_KEY = "sk-live-prod-b14e9f9c-7d34-4a2b-8c5e-8e5f2a1b3c4d"

# --- VULNERABILITY 2: Insecure Code - Command Injection (for Bandit/Semgrep) ---
@app.route('/command')
def run_command():
    # Flaw: Uses shell=True which allows for command injection if input is not sanitized.
    user_input = request.args.get('input', 'echo "No input"')
    
    # B404: Consider possible security implications associated with the use of 'subprocess' module.
    # Semgrep rule 'python.lang.security.command-injection.subprocess-popen-shell-true' should catch this.
    try:
        # Intentionally insecure use of shell=True
        result = subprocess.check_output(f'bash -c "{user_input}"', shell=True, text=True)
        return f"<pre>Command Output:\n{result}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}", 500

# --- VULNERABILITY 3: Insecure Code - Template Injection possibility (for Semgrep) ---
@app.route('/hello')
def hello_page():
    name = request.args.get('name', 'Guest')
    
    # Semgrep rule 'python.flask.security.audit.jinja.direct-render.direct-render' might flag this, 
    # though the primary risk is if the input 'name' could execute code.
    # We use f-string and render_template_string to demonstrate direct rendering.
    html_template = f"<h1>Hello, {name}!</h1><p>This is a test page for DAST scanning.</p>"
    return render_template_string(html_template)

@app.route('/')
def home():
    return """
    <h1>Secure CI/CD Practice App</h1>
    <p>Endpoints to test security scans:</p>
    <ul>
        <li><a href="/hello?name=CI/CD">/hello?name=CI/CD</a> (SAST/DAST target)</li>
        <li><a href="/command?input=ls -l">/command?input=ls -l</a> (Insecure Command Execution)</li>
    </ul>
    """

if __name__ == '__main__':
    # Flask development server is used for local testing, Gunicorn/Waitress is better for production.
    # We will use Gunicorn in the CI pipeline for a realistic scenario.
    app.run(host='0.0.0.0', port=5000)
