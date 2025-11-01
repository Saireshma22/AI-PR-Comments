#AI-Powered Pull Request (PR) Review System
#Project Overview

This project automates **code reviews** for GitHub pull requests using **OpenAI’s GPT models**.
It analyzes code changes in PRs and generates **inline, line-specific comments** — pointing out mistakes, suggesting improvements, and even giving feedback on clean code.

No need for manual PR number input — the script automatically fetches the **latest open PR** and posts feedback directly into GitHub.

---

### 🧩 Key Features

* ✅ Automatically detects the latest open pull request
* 🧠 Uses **OpenAI GPT-4o-mini** for AI-based code analysis
* 💬 Posts **inline code review comments** directly in the PR
* 🪶 Gives short, clear, one-line suggestions per issue
* 🔐 Uses **GitHub Secrets** and `.env` for secure API key management
* ⚙️ Can be run manually or integrated into a **GitHub Action workflow**

---

### 🏗️ Project Structure

```
review/
│
├── scripts/
│   └── pr_ai_review.py     # Main Python script for PR review
│
├── .env                    # Stores your tokens securely
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation (this file)
```

---

### ⚙️ Setup Instructions

#### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/review.git
cd review
```

#### 2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

#### 3. Install required dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create a `.env` file in the project root and add:

```
GITHUB_TOKEN=your_github_personal_access_token
OPENAI_API_KEY=your_openai_api_key
GITHUB_REPOSITORY=your_github_username/repository_name
```

> ⚠️ Make sure your **GitHub Token** has `repo` and `pull_request` permissions.

#### 5. Run the review script

```bash
python scripts/pr_ai_review.py
```

The script will:

1. Find the latest open pull request.
2. Analyze all changed files.
3. Generate AI-based review comments.
4. Post them **inline** in your PR automatically.

---

### 🧠 Example Output

#### Inline PR Comment Example:

> 💡 *Line 5: Consider renaming the variable for clarity.*
> 🧩 *Line 9: Add input validation to handle unexpected input values.*

#### Terminal Output Example:

```
[AI-PR-Review] Fetching latest open pull request...
✅ Found latest PR: #2 - "Added new.java"
[AI-PR-Review] Fetched 1 files from PR #2
[AI-PR-Review] Querying OpenAI for inline feedback...
✅ AI Review Generated: 4 comments
✅ Inline comments posted successfully to PR #2
```

---

### 🛠️ Example GitHub Action Integration

If you want to run it automatically when someone opens a pull request, create a file at:

```
.github/workflows/ai_pr_review.yml
```

```yaml
name: AI PR Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run AI PR Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: python scripts/pr_ai_review.py
```

---

### 📊 Final Summary of What We Built

| Step                                 | Description                                                                      |
| ------------------------------------ | -------------------------------------------------------------------------------- |
| 🧱 **Base Setup**                    | Created project structure with Python script, `.env`, and workflow.              |
| 🔐 **Secure API Integration**        | Integrated OpenAI and GitHub APIs with token security.                           |
| 🧩 **AI Review Logic**               | AI analyzes pull request diffs line by line.                                     |
| 💬 **Inline Comment System**         | Automatically posts short review comments on the exact PR lines in GitHub.       |
| ⚙️ **Automation via GitHub Actions** | Configured workflow to trigger AI review whenever a new PR is opened or updated. |
| 🧠 **Enhanced Logic**                | Made PR detection automatic (no manual number entry).                            |

**✅ Final Output:**
When a developer submits a pull request, the AI instantly reviews it, posts inline feedback, and highlights corrections or improvements in concise, human-like comments.

---

### 👩‍💻 Built With

* **Python 3.11**
* **OpenAI API (GPT-4o-mini)**
* **GitHub REST API**
* **dotenv** for environment variables

