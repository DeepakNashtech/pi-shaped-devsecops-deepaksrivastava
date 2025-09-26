# Vulnerable Node App + OWASP ZAP CI/CD Demo

## Objective
Showcase Dynamic Application Security Testing (DAST) using OWASP ZAP in GitLab CI/CD.

## Steps
1. Built a simple vulnerable Node app (SQLi + XSS).
2. Added Dockerfile to run app.
3. Configured `.gitlab-ci.yml` with a ZAP scan stage.
4. On commit, pipeline runs → generates `zap-report.html`.
5. Analyzed vulnerabilities.

## Findings

### SQL Injection
- **Impact**: Database queries can be manipulated, leading to data theft.
- **Fix**: Use parameterized queries (`db.get("SELECT * FROM users WHERE id=?", [userId])`).

### Cross-Site Scripting (XSS)
- **Impact**: Attacker can inject scripts into pages, steal cookies/sessions.
- **Fix**: Escape user input, sanitize HTML, add `helmet` + CSP.

## Core Concepts

### **1. What is the purpose of DAST and how does it complement other security testing methods?**

* **Purpose of DAST (Dynamic Application Security Testing):**
  DAST tests a running application (black-box testing) by simulating real-world attacks to discover vulnerabilities in its runtime behavior. It doesn’t require access to source code.

* **How it complements other methods:**

  * **SAST (Static Analysis):** Scans source code for insecure patterns before build.
  * **IAST (Interactive Analysis):** Monitors applications while they run (gray-box).
  * **DAST adds value** by finding vulnerabilities (e.g., XSS, SQL injection, insecure headers) that may not be obvious in code but appear when the app is deployed and handling real HTTP requests.

👉 Together, SAST + DAST + IAST give full coverage (code, runtime, environment).

---

### **2. Explain how XSS or SQL injection vulnerabilities can affect an application and its users.**

* **Cross-Site Scripting (XSS):**

  * **Impact:** Attackers inject malicious JavaScript into web pages. Victims’ browsers execute the code, leading to stolen cookies, session hijacking, defacement, or redirection to malicious sites.
  * **Example:** A comment box allows `<script>alert('hacked')</script>` → runs in every visitor’s browser.

* **SQL Injection (SQLi):**

  * **Impact:** Attackers manipulate backend SQL queries by injecting malicious input. Can lead to unauthorized data access, modification, or even full database compromise.
  * **Example:** Login form without parameterized queries → attacker enters `' OR '1'='1` to bypass authentication.

---

### **3. Describe the steps you would take to fix the vulnerabilities detected in your ZAP scan.**

* **General Fixing Approach:**

  1. **Review ZAP report findings** → prioritize based on severity.
  2. **Apply Secure Coding Practices** → e.g.:

     * For XSS: Escape/encode output, use CSP headers, sanitize user input.
     * For SQLi: Use parameterized queries (prepared statements), ORM frameworks.
     * For Missing Security Headers: Add `Content-Security-Policy`, `X-Content-Type-Options`, `Strict-Transport-Security`.
  3. **Retest** → rerun ZAP to confirm fixes.
  4. **Document & monitor** → add regression tests so vulnerabilities don’t reappear.

---

### **4. How does integrating ZAP scans into CI/CD pipelines support shift-left security practices?**

* **Shift-left security** = finding and fixing issues **early in the SDLC** (before production).
* **ZAP in CI/CD helps because:**

  * Runs automatically on every push/PR → developers get immediate feedback.
  * Prevents vulnerable code from being merged or deployed.
  * Reduces cost & risk → vulnerabilities are cheaper to fix earlier than after release.
  * Creates a culture where developers treat security checks like unit tests → part of normal workflow, not an afterthought.

## Evidence
- Screenshot of ZAP Report

![ZAP Report](Screenshots/Screenshot%20from%202025-09-26%2012-42-50.png)

- Pipeline artifact: `zap-report.html`
