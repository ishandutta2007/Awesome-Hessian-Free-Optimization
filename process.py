import os
import re

readme_path = r"C:\Users\ishan\Documents\Projects\Awesome-Hessian-Free-Optimization\README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make the changes in README.md
# We will do this via regex or manual replacement.

# Emojis and SEO friendly
content = content.replace("# Awesome-Hessian-Free-Optimization", "# 🚀 Awesome-Hessian-Free-Optimization 🌟\n\n![Banner](assets/banner.svg)")

badges_left = '<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>'
badges_right = '<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
badges = f'<div align="center">\n{badges_left}\n{badges_right}\n</div>\n\n'
content = content.replace("![Banner](assets/banner.svg)", f"![Banner](assets/banner.svg)\n\n{badges}")

# Let's manually reconstruct the README since regex might be brittle
new_readme = []
lines = content.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    new_readme.append(line)
    i += 1

with open(readme_path, "w", encoding="utf-8") as f:
    f.write("\n".join(new_readme))
