import requests
import os

# 🔐 Get username (works locally + GitHub Actions)
username = os.getenv("GITHUB_REPOSITORY_OWNER") or "VickyBoy2309"

# ----------------------------
# FETCH USER DATA
# ----------------------------
user_url = f"https://api.github.com/users/{username}"
user = requests.get(user_url).json()

repo_count = user.get("public_repos", 0)

# ----------------------------
# FETCH REPOS
# ----------------------------
repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
repos = requests.get(repos_url).json()

# ----------------------------
# LANGUAGES (REAL)
# ----------------------------
languages_set = set()

for repo in repos:
    if repo.get("language"):
        languages_set.add(repo["language"])

languages = ", ".join(languages_set) if languages_set else "None"

# ----------------------------
# COMMITS (APPROX REAL)
# ----------------------------
total_commits = 0

for repo in repos[:]:  # limit for API safety
    repo_name = repo["name"]
    commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=1"

    res = requests.get(commits_url)

    if "Link" in res.headers:
        link = res.headers["Link"]
        if 'rel="last"' in link:
            last_page = int(link.split("page=")[-1].split(">")[0])
            total_commits += last_page
    else:
        total_commits += 1

# ----------------------------
# LOAD TEMPLATE
# ----------------------------
with open("assets/jarvis-template.svg", "r") as f:
    svg = f.read()

# ----------------------------
# REPLACE PLACEHOLDERS
# ----------------------------
svg = svg.replace("{{USERNAME}}", username.upper())
svg = svg.replace("{{COMMITS}}", str(total_commits))
svg = svg.replace("{{REPOS}}", str(repo_count))
svg = svg.replace("{{LANGUAGES}}", languages)

# ----------------------------
# WRITE FINAL SVG
# ----------------------------
with open("assets/jarvis.svg", "w") as f:
    f.write(svg)

print("✅ JARVIS SVG generated successfully!")