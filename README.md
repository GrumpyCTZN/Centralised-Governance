# Setup for Collaborators

This README is for project collaborators only — it contains the exact, minimal steps to get the project running on your machine and keep your local DB in sync with the repository (migrations and seed data are provided by the project maintainer).

> Note: The project owner generates and commits migration files. Collaborators should run the commands below after pulling the latest changes.

---

## 1 — Clone the repo
```bash
git clone git@github.com:GrumpyCTZN/Centralised-Governance.git
cd repo
```

## 2 — Create & activate a virtual environment
- macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```
- Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate
```

## 3 — Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## To run the App
```bash
python app.py
# or
flask run
# Visit: http://127.0.0.1:5000
```