import requests
import os

username = os.getenv("GITHUB_REPOSITORY_OWNER")

url = f"https://api.github.com/users/{username}"

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"GitHub API error: {response.status_code}")

user = response.json()

repo_count = user.get("public_repos", 0)
followers = user.get("followers", 0)

commit_estimate = repo_count * 120

languages = ["Python", "Java", "JavaScript", "C"]

svg = f"""
<svg viewBox="0 0 700 260" xmlns="http://www.w3.org/2000/svg">

<style>

.title {{
font-family:'JetBrains Mono','Fira Code','Consolas',monospace;
font-size:24px;
font-weight:700;
fill:#00ffff;
}}

.text {{
font-family:'JetBrains Mono','Fira Code','Consolas',monospace;
font-size:16px;
fill:#00ffff;
}}

.box {{
fill:#020b14;
stroke:#00ffff;
stroke-width:2;
}}

</style>

<!-- Background panel -->
<rect x="5" y="5" width="690" height="250" class="box"/>

<!-- Title -->
<text x="350" y="45" text-anchor="middle" class="title">
JARVIS AI
</text>

<!-- Username -->
<text x="350" y="70" text-anchor="middle" class="text">
VICKYBOY2309
</text>

<!-- Section -->
<text x="40" y="120" class="text">ARC REACTOR STATUS</text>

<!-- Stats -->
<text x="40" y="150" class="text">⚡ Commits: {commit_estimate}</text>
<text x="40" y="180" class="text">⚡ Repositories: {repo_count}</text>
<text x="40" y="210" class="text">⚡ Languages: {', '.join(languages)}</text>

</svg>
"""

os.makedirs("assets", exist_ok=True)

with open("assets/jarvis.svg", "w") as f:
    f.write(svg)
