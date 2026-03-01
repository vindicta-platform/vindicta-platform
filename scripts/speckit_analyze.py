import os
import json
import logging
import re
from urllib.parse import urlparse

from github import Github
import ollama

MAX_TITLE_LEN = 256
MAX_BODY_LEN = 65_536
# Only allow links pointing to the project's own GitHub org
_ALLOWED_URL_HOSTS = {"github.com"}
_URL_PATTERN = re.compile(r"https?://[^\s)>]+")

logging.basicConfig(level=logging.INFO)


def main():
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    github_token = os.environ.get("GITHUB_TOKEN")

    if not github_token or not repo_name:
        logging.error("Missing GITHUB_REPOSITORY or GITHUB_TOKEN.")
        return

    context_path = "packages/vindicta-agents/repomix_context.xml"
    if not os.path.exists(context_path):
        logging.error(f"Context file {context_path} not found.")
        return

    with open(context_path, "r", encoding="utf-8") as f:
        repomix_context = f.read()

    prompt = f"""
You are an automated code and specification analyzer for the Vindicta platform.
Your job is to read the attached code context (which includes the project constitution, specifications, test reports, and the `.github/workflows/speckit-analyze-agents.yml` CI definition).
Identify any "drift" - where the test reports indicate the specifications and acceptance criteria are unfulfilled or failing.
Pay extreme attention to the rules defined in constitution.md and ensure our pipeline conforms to the configurations defined in the workflow file.

If drift or violations are found, output a JSON array of issues to be created.
If no drift is found, output an empty JSON array `[]`.

Format STRICTLY as a JSON array of objects. Example:
[
  {{
    "title": "Drift Detected: <short title>",
    "body": "<Detailed explanation of the drift and failed acceptance criteria>"
  }}
]

DO NOT include any markdown blocks around the JSON output. DO NOT include any explanatory text before or after the JSON.

Context:
{repomix_context}
"""

    logging.info("Calling Ollama (phi3)...")
    try:
        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}],
            format="json",
            options={"temperature": 0.0},
        )
        content = response["message"]["content"].strip()

        try:
            issues = json.loads(content)
        except json.JSONDecodeError:
            logging.error(f"Failed to parse JSON response. Response was: {content}")
            return

        if not isinstance(issues, list):
            logging.error(f"JSON response is not a list. Response was: {content}")
            return

        if len(issues) == 0:
            logging.info("No drift detected.")
            return

        logging.info(f"Found {len(issues)} drift issues.")

        g = Github(github_token)
        repo = g.get_repo(repo_name)

        for issue in issues:
            title = issue.get("title", "Detected Specification Drift")
            body = issue.get(
                "body",
                "Drift was detected by local speckit analysis, but no details were provided.",
            )

            # --- Validation gate ---
            if not isinstance(title, str) or not isinstance(body, str):
                logging.warning("Skipping issue: title/body must be strings.")
                continue

            if len(title) > MAX_TITLE_LEN:
                logging.warning(
                    f"Skipping issue: title exceeds {MAX_TITLE_LEN} chars."
                )
                continue

            if len(body) > MAX_BODY_LEN:
                logging.warning(
                    f"Skipping issue: body exceeds {MAX_BODY_LEN} chars."
                )
                continue

            # Reject issues that embed links to external (non-GitHub) sites
            urls_in_text = _URL_PATTERN.findall(f"{title} {body}")
            if any(
                urlparse(u).hostname not in _ALLOWED_URL_HOSTS
                for u in urls_in_text
            ):
                logging.warning(
                    f"Skipping issue with suspicious external URL(s): {title}"
                )
                continue
            # --- End validation ---

            repo.create_issue(
                title=title, body=body, labels=["quality", "speckit.analyze"]
            )
            logging.info(f"Created issue: {title}")

    except Exception as e:
        logging.error(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()
