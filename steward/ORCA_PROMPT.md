Read steward/scoreboard/latest.json.
If summary.red == 0, stop after a one-line report.
If summary.red > 0, for each red criterion: open one GitHub issue on mrodgersjs-web/mrodgersjs-web labeled github-steward if an open issue with that criterion id does not already exist. Then fix the cheapest reds in this worktree (LICENSE, badge URL, description typo, missing CODEOWNERS) and open a PR. Do not git push to main. Do not change private repos. Do not publish to PyPI/npm.
For criteria with check=llm still null: run `python3 steward/judge.py`; if it prints FALLBACK_PAID, fill those rows yourself and write them back to latest.json in the PR, not on main.
