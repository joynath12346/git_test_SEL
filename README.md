# Task Management API - Git Lab Examination

A complete FastAPI Task Management service with pytest test suite and GitHub Actions CI workflow, designed for a 2-teammate Git collaboration exam.

---

## 👥 Two-Teammate Role Distribution

| Role | Teammate | Assigned Tasks | Git Branch |
|---|---|---|---|
| **API Developer** | **Teammate 1** | `src/__init__.py`, `src/main.py`, `requirements.txt` | `main` |
| **QA / Test Developer** | **Teammate 2** | `tests/__init__.py`, `tests/main_test.py`, `.github/workflows/python-tests.yml` | `test-development` (merged into `main` via PR) |

---

## 📁 Project File Structure (Matching Image 1)

```
task-management-api/
├── .github/
│   └── workflows/
│       └── python-tests.yml    # CI workflow triggered on push & pull_request to main
├── src/
│   ├── __init__.py             # Python package marker
│   └── main.py                 # FastAPI application with Task model, CRUD & validation
├── tests/
│   ├── __init__.py             # Test package marker
│   └── main_test.py            # Pytest test suite (positive & invalid scenarios)
├── requirements.txt            # Python dependencies (fastapi, uvicorn, pytest, etc.)
└── README.md                   # Project documentation & Git instructions
```

---

## 🚀 Step-by-Step Git Commands

### 1️⃣ Teammate 1: Setup Repository & Source Code (`src/`)

```bash
# Step 1: Initialize local git repository
git init
git branch -M main

# Step 2: Create virtual environment and install dependencies
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows CMD/PowerShell:
venv\Scripts\activate

pip install -r requirements.txt

# Step 3: Verify the API runs locally
uvicorn src.main:app --reload --port 8000
# Visit http://127.0.0.1:8000/docs for Swagger UI

# Step 4: Stage source files and commit
git add src/ requirements.txt .gitignore README.md
git commit -m "feat(api): implement Task Management REST API with FastAPI and Pydantic models"

# Step 5: Connect to GitHub remote and push to main
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/task-management-api.git
git push -u origin main
```

---

### 2️⃣ Teammate 2: Test Suite Development on Separate Git Branch (`tests/`)

```bash
# Step 1: Clone the repository created by Teammate 1
git clone https://github.com/<YOUR-GITHUB-USERNAME>/task-management-api.git
cd task-management-api

# Step 2: Create and switch to a separate test branch (CRITICAL EXAM REQUIREMENT)
git checkout -b test-development

# Step 3: Set up virtual environment & install requirements
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt

# Step 4: Run the pytest suite locally to verify all test cases pass
pytest tests/ -v

# Step 5: Stage test files and GitHub Actions workflow
git add tests/ .github/
git commit -m "test(api): add comprehensive pytest test suite and GitHub Actions CI workflow"

# Step 6: Push the branch to GitHub
git push -u origin test-development

# Step 7: On GitHub:
# - Open a Pull Request (PR) from `test-development` into `main`
# - Verify that GitHub Actions triggers automatically and passes all tests (green checkmark)
# - Merge the Pull Request into `main`
```

---

## 🧪 Included Test Scenarios

### Positive Operations
1. `test_root_endpoint`: GET `/` returns 200 health check.
2. `test_create_task_success`: POST `/tasks` returns 201 Created and auto-assigned ID.
3. `test_get_all_tasks_success`: GET `/tasks` returns list of all created tasks.
4. `test_get_task_by_id_success`: GET `/tasks/{id}` returns 200 with matching task details.
5. `test_update_task_success`: PUT `/tasks/{id}` updates task fields and returns 200.
6. `test_delete_task_success`: DELETE `/tasks/{id}` removes task and returns 200.

### Negative / Invalid Operations (Requirement: At least two invalid scenarios)
1. `test_get_task_not_found_invalid_scenario`: GET `/tasks/9999` -> 404 NOT FOUND.
2. `test_update_task_not_found_invalid_scenario`: PUT `/tasks/9999` -> 404 NOT FOUND.
3. `test_delete_task_not_found_invalid_scenario`: DELETE `/tasks/9999` -> 404 NOT FOUND.
4. `test_create_task_missing_required_title_invalid_scenario`: POST `/tasks` with missing `title` -> 422 Validation Error.
5. `test_create_task_invalid_status_enum_scenario`: POST `/tasks` with `status="not_valid"` -> 422 Validation Error.
6. `test_create_task_invalid_priority_enum_scenario`: POST `/tasks` with `priority="super_urgent"` -> 422 Validation Error.
