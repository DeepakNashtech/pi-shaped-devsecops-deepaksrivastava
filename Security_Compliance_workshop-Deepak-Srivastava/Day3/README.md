# CI/CD-Based Secure Coding & Code Scanning (GitHub Actions Workflow)

This repository demonstrates a foundational **Shift-Left Security** workflow using a GitHub Actions pipeline. We integrate multiple security tools to catch different classes of vulnerabilities—from hardcoded secrets and insecure coding practices to runtime web application flaws—before code ever reaches production.

---

## 1. Project Setup and Intentionally Introduced Issues

The `main.py` file contains a simple Python Flask application that serves as the target for our security scanners. We have intentionally introduced three common security flaws:

| Flaw Category         | File       | Description                                                                                  | Tool to Detect                  |
|----------------------|------------|----------------------------------------------------------------------------------------------|--------------------------------|
| Secrets Leak         | main.py     | A hardcoded API key (`SECRET_API_KEY`) is stored directly in the source code.                | Gitleaks                        |
| Insecure Code (SAST) | main.py (`run_command`) | Using `subprocess.check_output(..., shell=True)` with unsanitized user input, creating a Command Injection vulnerability. | Bandit / Semgrep                |
| Vulnerable Dependency| requirements.txt | Using an outdated and vulnerable version of `flask==1.1.2`.                                   | Bandit (or similar dependency scanner) |
| Runtime Vulnerability (DAST) | main.py (`/command`, `/hello`) | The application routes are susceptible to exploitation by runtime attacks.               | OWASP ZAP                       |

---

## 2. GitHub Actions Pipeline Steps

The pipeline is defined in `.github/workflows/security_pipeline.yml`. It uses dedicated GitHub Actions for simplicity and reliability:

| Stage (Conceptual) | Step Name                 | Tool / Action Used                                | Type        | Artifacts Generated      |
|-------------------|--------------------------|--------------------------------------------------|------------|------------------------|
| Install           | Setup Python / Install Dependencies | `actions/setup-python`, `pip`                    | Setup      | None                   |
| SAST              | Run Bandit Scan           | Bandit (via pip and run)                          | SAST (Python) | bandit-report.html      |
| SAST              | Run Semgrep Scan          | `returntocorp/semgrep-action`                     | SAST (Generic) | semgrep-report.json    |
| Secrets           | Run Gitleaks Scan         | `zricethezav/gitleaks-action`                     | Secrets    | gitleaks-report.json   |
| DAST              | Start Flask App / Run ZAP | `gunicorn` / `anmol093/zap-baseline-scan-action`| DAST       | zap-report.html        |
| Report            | Upload Scan Artifacts     | `actions/upload-artifact`                         | Reporting  | All reports            |

**Execution Flow in GitHub Actions:**

1. The workflow is triggered on `push` and `pull_request`.
2. Python environment and all necessary dependencies (`flask`, `gunicorn`, `bandit`) are installed.
3. SAST and Secrets scans execute instantly against the static code and git history.
4. For DAST, the Flask application is started in the background using `gunicorn`.
5. OWASP ZAP runs against the live server (`http://127.0.0.1:5000`).
6. The Flask application is reliably stopped using the captured Process ID (PID).
7. All generated reports (`.html` and `.json`) are uploaded as workflow artifacts.

---

## 3. Core Concept Questions

### What is the difference between SAST, DAST, and secrets scanning, and why should all be part of a CI/CD pipeline?

| Scan Type                | Acronym | Method                                      | Focus                                                                 |
|---------------------------|--------|--------------------------------------------|-----------------------------------------------------------------------|
| Static Application Security Testing | SAST   | Analyzes source code without executing it | Flaws in the code itself (e.g., SQL injection, insecure cryptography) |
| Dynamic Application Security Testing | DAST   | Analyzes the running application by simulating attacks | Flaws exposed at runtime (e.g., server misconfigurations, HTTP headers) |
| Secrets Scanning         | N/A    | Analyzes source code and commit history for high-entropy strings | Confidential credentials (e.g., API keys, tokens)                     |

**Why include all three?**  
Each scan type covers a unique attack surface. Combining SAST, DAST, and secrets scanning provides comprehensive coverage:

- **SAST:** Catches code logic flaws.  
- **Secrets Scanning:** Catches critical credential exposure.  
- **DAST:** Validates operational environment and runtime behavior.  

Failing to include one leaves a security gap.

---

### Why is storing secrets in code dangerous? What’s a secure alternative?

**Risks of hardcoding secrets:**

- **High Visibility:** Anyone with repository access can see the secret.
- **Compromise Risk:** Exposure occurs if the repository is cloned, forked, or made public.
- **Lack of Control:** Cannot rotate or revoke secrets without code changes and redeployment.

**Secure Alternatives:**

- **CI/CD Variables:** Use platform-provided secure variables (e.g., GitHub Secrets, accessed via `secrets.<SECRET_NAME>`).  
- **Dedicated Tools:** HashiCorp Vault, AWS Secrets Manager, Google Secret Manager, etc.  

Retrieve secrets from these secure stores at runtime; never store raw values in the codebase.

---

### How does adding these scans to a pipeline help enforce Shift-Left Security?

**Shift-Left Security** integrates security activities early in the Software Development Life Cycle (SDLC).

Benefits of adding automated security scans to CI/CD:

- **Early Feedback:** Developers get instant reports on vulnerabilities or leaked secrets.
- **Automation & Consistency:** Security checks run on every change.
- **Developer Ownership:** Shifts responsibility for basic security to developers, embedding security in the development process.

---

### If a scan fails in your pipeline, what is the next step for a developer or DevOps engineer?

1. **Review the Artifacts:** Download and analyze reports (`bandit-report.html`, `gitleaks-report.json`).
2. **Prioritize:** Assess severity (High/Medium/Low). Critical issues require immediate attention.
3. **Fix the Code:**
   - **Gitleaks:** Remove secrets from code and clean git history (e.g., `git filter-repo`).
   - **SAST/DAST:** Fix vulnerable code (e.g., sanitize input, update dependencies, patch runtime flaws).
4. **Re-Run the Pipeline:** Commit the fix and push. The pipeline confirms resolution.

---

### Demonstration: Fixing an Issue

**Original Vulnerable Code (`main.py`):**

```python
SECRET_API_KEY = "sk-live-prod-b14e9f9c-7d34-4a2b-8c5e-8e5f2a1b3c4d"
```

**Fixed Code (using environment variable):**

```python
import os

SECRET_API_KEY = os.environ.get("API_KEY_SECURE", "default_safe_value")
``` 

**Steps:**
1. Remove secret from code.
2. Commit & push changes.
3. After pipeline runs, the `gitleaks-report.json` shows zero findings for the secret, validating the fix.

