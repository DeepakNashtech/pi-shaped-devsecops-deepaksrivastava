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
- **DAST purpose**: Tests running applications dynamically, complements SAST.
- **XSS/SQLi effects**: User data theft, account hijacking, DB compromise.
- **Fix steps**: Refactor vulnerable code, sanitize inputs, use secure defaults.
- **Shift-left security**: Integrating ZAP scans in CI/CD prevents deploying exploitable apps.

## Evidence
- Screenshot of ZAP Reportss
- Pipeline artifact: `zap-report.html`
