# Shift-Left Security Demo

**Objective:** Demonstrate shift-left security by scanning a repo for secrets (Gitleaks), removing them safely, and deploying a small Flask app in Docker. This repo intentionally contains a demo hardcoded secret so you can follow the detection/removal flow.

## Contents
- `app.py` — sample Flask app (contains a demo hardcoded secret)
- `requirements.txt` — Python requirements
- `.env.example` — example env file
- `.gitleaks.toml` — optional gitleaks config
- `Dockerfile` and `docker-compose.yml` — for local Docker deploy
- `.github/workflows/gitleaks.yml` — GitHub Action to run gitleaks on pushes/PRs

---

## Quick start (local)

1. Clone and inspect the repo:
```bash
git clone https://github.com/DeepakNashtech/pi-shaped-devsecops-deepaksrivastava/tree/main/Security_Compliance_workshop-Deepak-Srivastava/Day1
cd Day1
```

2. Run the app locally:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

3. Scan with Gitleaks:
```bash
gitleaks detect --source=. --report=gitleaks-report.json --format=json
cat gitleaks-report.json | jq .
```

4. Remove secrets from all history (example using git-filter-repo):
```bash
pip install git-filter-repo
echo "sk_live_1234567890_DEMOSECRET==REDACTED_DEMO_API_KEY" > replacements.txt
git filter-repo --replace-text replacements.txt
```

5. Add `.env` and .gitignore:
```
cp .env.example .env
# edit .env for local secrets (do not commit)
```

6. Build & run Docker:
```bash
docker compose up -d --build
docker compose logs -f
curl -f http://localhost:5000/health
```

---

## CI: Gitleaks in GitHub Actions
A workflow at `.github/workflows/gitleaks.yml` runs on push & PR. It will fail the check if leaks are detected — this enforces shift-left scanning before merges.

---

## How to safely remove secrets from history

Two recommended tools:
- `git filter-repo` (recommended)
- `BFG Repo-Cleaner` (alternative)

**Important:** after rewriting history, force-push and coordinate with contributors — they must re-clone or reset their local clones.

---

## Best practices for secrets management
- Store in a dedicated secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
- Keep secrets out of source control
- Use ephemeral credentials or short-lived tokens where possible
- Add pre-commit checks / CI scans (gitleaks, trufflehog) to catch secrets early
- Audit and rotate keys immediately if exposed

---

## Core Concept Questions (for your README or presentation)

### 1. Explain the concept of shift-left security and why it is important in DevSecOps.
**Answer:**  
Shift-left security means integrating security activities early in the software development lifecycle — during requirements, design, coding and CI — rather than treating security as a final phase. By moving security checks left (earlier), teams catch vulnerabilities sooner when they’re cheaper and faster to fix, reduce the risk of insecure releases, and improve developer security awareness. In DevSecOps, shift-left practices (static analysis, secret scanning, dependency checks, threat modeling) embed security into the development pipeline and make secure delivery continuous and automated.

### 2. How does detecting secrets early in the CI/CD pipeline prevent production vulnerabilities?
**Answer:**  
Detecting secrets early prevents accidental exposure of credentials in source control. If secrets are committed to a repo, attackers scanning public repos (or leaked mirrors) may find and exploit them. Early detection allows teams to block the commit/merge before the secret becomes part of history or deployed. Even if a secret gets committed, detecting it early reduces the time window an attacker might have and prompts immediate rotation. It also reduces remediation effort since history rewrite/rotation is more contained.

### 3. What strategies can be used to store secrets securely instead of hardcoding them?
**Answer:**  
- Use cloud-managed secret stores (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, HashiCorp Vault).
- Inject secrets via environment variables at runtime (via container orchestrators or CI/CD secrets).
- Use CI/CD secret storage for build-time values (GitHub Actions secrets, GitLab CI variables).
- Use hardware or cloud KMS to encrypt secrets and fetch decrypted values at runtime.
- Use short-lived credentials and role-based access (e.g., IAM roles for compute instances).

### 4. Describe a situation where a secret could still be exposed even after scanning, and how to prevent it.
**Answer:**  
**Situation:** A developer copies a secret into a shared Slack channel, logs it in an issue tracker, or leaves it in a CI build log. Gitleaks scans the repo but cannot detect secrets outside git history.  
**Prevention:** Complement repository scanning with other controls: monitor logs for secrets (redaction), prevent secrets in chat with DLP tools or integration scanners, ensure CI logs mask secrets, restrict who can view logs, enforce minimal privilege, and run comprehensive audits that include external channels and infrastructure configurations. Use runtime secret rotation and auditing to limit risk.

---

## Final notes & recommendations
- Treat any secret found in a repo as **compromised** — rotate it immediately.
- Integrate scanning tools into local pre-commit hooks plus CI to enforce early detection.
- Train developers on secure secret handling and provide easy secure alternatives (secret manager libs, automation templates).

