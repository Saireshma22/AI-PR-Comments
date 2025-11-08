#AI-Powered Pull Request (PR) Review System
#Project Overview

This project automates **code reviews** for GitHub pull requests using **OpenAI’s GPT models**.

It analyzes code changes in PRs and generates **inline, line-specific comments** — pointing out mistakes, suggesting improvements, and even giving feedback on clean code.

No need for manual PR number input — the script automatically fetches the **latest open PR** and posts feedback directly into GitHub.

# Key Features
Automatically detects the latest open pull request
Uses **OpenAI GPT-4o-mini** for AI-based code analysis
Posts **inline code review comments** directly in the PR
Gives short, clear, one-line suggestions per issue
Uses **GitHub Secrets** and `.env` for secure API key management
Can be run manually or integrated into a **GitHub Action workflow**

# Setup Instructions

# 1. Clone the repository
# 2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
#  3. Install required dependencies
pip install -r requirements.txt
# 4. Create a `.env` file in the project root and add:
GITHUB_TOKEN=
OPENAI_API_KEY=
GITHUB_REPOSITORY=
>  Make sure your **GitHub Token** has `repo` and `pull_request` permissions.
# 5. Run the review script
python scripts/pr_ai_review.py


The script will:
1. Find the latest open pull request.
2. Analyze all changed files.
3. Generate AI-based review comments.
4. Post them **inline** in your PR automatically.


If you want to run it automatically when someone opens a pull request, create a file at:
.github/workflows/ai_pr_review.yml

# Final Output:
When a developer submits a pull request, the AI instantly reviews it, posts inline feedback, and highlights corrections or improvements in concise, human-like comments.

# Built With
**Python 3.11**
**OpenAI API (GPT-4o-mini)**
**GitHub REST API**
**dotenv** for environment variables
