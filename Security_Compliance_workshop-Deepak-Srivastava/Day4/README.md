
### 📌 Pipeline Overview

This pipeline demonstrates secure coding and scanning in a CI/CD workflow.
It integrates **Bandit, Semgrep, Trivy, and OWASP ZAP**.

### 🚀 Steps

1. Build the vulnerable Flask app.
2. Run scans in pipeline stages:

   * **Bandit** → insecure Python code.
   * **Semgrep** → coding pattern issues.
   * **Trivy** → vulnerable dependencies & base image CVEs.
   * **OWASP ZAP** → runtime app vulnerabilities (DAST).
3. Save all reports as artifacts.
4. Fix one issue, push, observe improved reports.

---

### ❓ Core Concept Questions

**Pipeline Integration**

* **Why run Trivy scans in CI/CD instead of only after deployment?**
  → It detects vulnerabilities early, before code reaches production, reducing patching cost and exposure window.

* **Why run SAST, dependency scanning, and DAST in CI/CD instead of production only?**
  → Finding issues earlier enables faster remediation, prevents insecure builds, and reduces risk of production downtime.

**Tool Roles**

* **Bandit** → Detects Python-specific issues (e.g., `eval()`, hardcoded secrets).
* **Semgrep** → Flexible pattern matching (e.g., insecure Flask route decorators).
* **Trivy** → Flags vulnerable libraries & OS packages.
* **OWASP ZAP** → Finds runtime issues like XSS, SQL injection.

**Developer Actionability**

* If **Trivy reports HIGH severity in base image** → Update base image (`python:3.10-slim` → latest patched version).
* If **Bandit flags hardcoded secrets** → Move secrets to a vault (HashiCorp Vault, AWS Secrets Manager, GitHub Actions secrets).

---

⚡ Harun, I can also prepare the **GitLab CI version** of this pipeline (`.gitlab-ci.yml`).
Do you want me to generate that so you have both options handy?
