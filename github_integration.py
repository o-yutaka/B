import datetime as dt
import json
import os
import subprocess
from pathlib import Path
from typing import Dict

import requests

GITHUB_API = "https://api.github.com"


class GitHubAutomation:
    def __init__(self) -> None:
        self.token = os.getenv("GITHUB_TOKEN", "").strip()
        self.owner = os.getenv("GITHUB_OWNER", "").strip()
        self.repo = os.getenv("GITHUB_REPO", "").strip()
        self.max_pr_per_day = int(os.getenv("MAX_PR_PER_DAY", "5"))
        self.log_path = Path("github_pr_log.json")
        if not self.log_path.exists():
            self.log_path.write_text("[]", encoding="utf-8")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _can_create_pr(self) -> bool:
        today = dt.datetime.utcnow().strftime("%Y-%m-%d")
        logs = json.loads(self.log_path.read_text(encoding="utf-8"))
        today_count = len([x for x in logs if x.get("date") == today])
        return today_count < self.max_pr_per_day

    def _record_pr(self) -> None:
        today = dt.datetime.utcnow().strftime("%Y-%m-%d")
        logs = json.loads(self.log_path.read_text(encoding="utf-8"))
        logs.append({"date": today, "time": dt.datetime.utcnow().isoformat()})
        self.log_path.write_text(json.dumps(logs[-500:], ensure_ascii=False, indent=2), encoding="utf-8")

    def create_repo(self, name: str, private: bool = True) -> Dict[str, str]:
        if not self.token:
            return {"ok": "false", "error": "GITHUB_TOKEN未設定"}
        response = requests.post(
            f"{GITHUB_API}/user/repos",
            headers=self._headers(),
            json={"name": name, "private": private},
            timeout=30,
        )
        if response.status_code >= 300:
            return {"ok": "false", "error": response.text}
        payload = response.json()
        self.repo = payload.get("name", name)
        if not self.owner:
            self.owner = payload.get("owner", {}).get("login", "")
        return {"ok": "true", "repo": self.repo, "owner": self.owner}

    def create_branch_commit_push(self, branch_prefix: str = "ai-generated") -> Dict[str, str]:
        stamp = dt.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        branch = f"{branch_prefix}-{stamp}"
        try:
            subprocess.run(["git", "checkout", "-b", branch], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"AI generated update {stamp}"], check=True)
            subprocess.run(["git", "push", "-u", "origin", branch], check=True)
            return {"ok": "true", "branch": branch}
        except subprocess.CalledProcessError as exc:
            return {"ok": "false", "error": str(exc), "branch": branch}

    def create_pull_request(self, title: str, body: str, head: str, base: str = "main") -> Dict[str, str]:
        if not self._can_create_pr():
            return {"ok": "false", "error": "1日のPR上限に達しました"}
        if not self.token or not self.owner or not self.repo:
            return {"ok": "false", "error": "GitHub設定不足"}
        response = requests.post(
            f"{GITHUB_API}/repos/{self.owner}/{self.repo}/pulls",
            headers=self._headers(),
            json={"title": title, "body": body, "head": head, "base": base},
            timeout=30,
        )
        if response.status_code >= 300:
            return {"ok": "false", "error": response.text}
        self._record_pr()
        return {"ok": "true", "url": response.json().get("html_url", "")}

    def auto_pr(self, title: str, body: str, base: str = "main") -> Dict[str, str]:
        step = self.create_branch_commit_push("ai-generated")
        if step.get("ok") != "true":
            return step
        return self.create_pull_request(title=title, body=body, head=step["branch"], base=base)
