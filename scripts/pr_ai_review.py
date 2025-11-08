import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GH_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO = os.getenv("GITHUB_REPOSITORY")

if not all([GITHUB_TOKEN, OPENAI_API_KEY, REPO]):
    raise ValueError("Missing required environment variables (GH_TOKEN, OPENAI_API_KEY, GITHUB_REPOSITORY)")

client = OpenAI(api_key=OPENAI_API_KEY)
headers = {"Authorization": f"token {GH_TOKEN}"}

print("[AI-PR-Review] Fetching latest open pull request...")

# Step 1: Get the latest open PR
pr_list_url = f"https://api.github.com/repos/{REPO}/pulls?state=open&sort=created&direction=desc"
pr_list_response = requests.get(pr_list_url, headers=headers)
if pr_list_response.status_code != 200:
    raise Exception(f"Failed to fetch pull requests: {pr_list_response.text}")

pr_list = pr_list_response.json()
if not pr_list:
    raise Exception("No open pull requests found in the repository.")

latest_pr = pr_list[0]
PR_NUMBER = latest_pr["number"]
print(f"✅ Found latest PR: #{PR_NUMBER} - {latest_pr['title']}")

# Step 2: Fetch PR files
files_url = latest_pr["url"] + "/files"
files_response = requests.get(files_url, headers=headers)
if files_response.status_code != 200:
    raise Exception(f"Failed to fetch PR files: {files_response.text}")

files = files_response.json()
print(f"[AI-PR-Review] Fetched {len(files)} files from PR #{PR_NUMBER}")

# Step 3: Build diff summary
diff_summary = ""
for f in files:
    if "patch" in f:
        diff_summary += f"File: {f['filename']}\n{f['patch']}\n\n"

# Step 4: Ask OpenAI for inline-style JSON review
prompt = f"""
You are an expert code reviewer.
Analyze the following GitHub pull request diff and suggest *only short, line-specific corrections*.
For each issue, respond as JSON with:
[
  {{
    "file": "filename",
    "line": line_number,
    "comment": "Brief correction or suggestion (<=1 sentence)"
  }}
]
Do not include markdown, explanations, or summaries.

Here is the diff:
{diff_summary}
"""

print("[AI-PR-Review] Querying OpenAI for inline feedback...")

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    ai_text = response.choices[0].message.content.strip()

    # Step 5: Parse JSON
    if ai_text.startswith("```"):
        ai_text = ai_text.strip("```json").strip("```")

    comments = json.loads(ai_text)
    print(f"✅ AI Review Generated: {len(comments)} comments")

    # Step 6: Post comments inline on PR
    commit_id = latest_pr["head"]["sha"]
    review_url = latest_pr["url"] + "/reviews"
    review_data = {
        "commit_id": commit_id,
        "body": "🤖 AI Inline Code Review",
        "event": "COMMENT",
        "comments": [
            {"path": c["file"], "line": c["line"], "body": c["comment"]}
            for c in comments
        ],
    }

    gh_response = requests.post(review_url, headers=headers, json=review_data)
    if gh_response.status_code == 200:
        print(f"✅ Inline comments posted successfully to PR #{PR_NUMBER}")
    else:
        print(f"❌ Failed to post inline review: {gh_response.text}")

except Exception as e:
    print(f"❌ Error during AI review: {e}")
