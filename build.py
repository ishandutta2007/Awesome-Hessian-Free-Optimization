import os
import re
import subprocess

readme_path = r"C:\Users\ishan\Documents\Projects\Awesome-Hessian-Free-Optimization\README.md"
repo_dir = r"C:\Users\ishan\Documents\Projects\Awesome-Hessian-Free-Optimization"

def run_git(commit_msg):
    # Using explicit git dir to avoid the issue from earlier
    git_cmd = ['git', '--git-dir=.git', '--work-tree=.']
    subprocess.run(git_cmd + ['add', '.'], cwd=repo_dir, check=True)
    subprocess.run(git_cmd + ['commit', '-m', commit_msg], cwd=repo_dir, check=False)
    subprocess.run(git_cmd + ['push'], cwd=repo_dir, check=True)

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# Step 1: Convert the 14 bullets into 5 tables
bullets = [
    (r"\*\s+\*\*The First-Order Gradient Descent Baseline Era \(Traditional ML, Pre-2010\)\*\*\n\s+\*\s+\*Concept:\* (.*?)(?=\n\*|\n\n|\Z)", 
     "The First-Order Gradient Descent Baseline Era (Traditional ML, Pre-2010)", "1951", "[Robbins & Monro (1951)](https://doi.org/10.1214/aoms/1177729586)", "details_first_order_gradient.md"),
    (r"\*\s+\*\*The Exact Newton Processing Bottleneck \(Classical Multi-Variate Calculus\)\*\*\n\s+\*\s+\*Concept:\* (.*?)\n\s+\*\s+\*Limitation:\* (.*?)(?=\n\*|\n\n|\Z)",
     "The Exact Newton Processing Bottleneck (Classical Multi-Variate Calculus)", "1671", "[Newton's Method](https://en.wikipedia.org/wiki/Newton%27s_method)", "details_newton_processing.md"),
    (r"\*\s+\*\*The Implicit Vector-Product Revolution \(Hessian-Free Framework, Martens, 2010–2012\)\*\*\n\s+\*\s+\*Concept:\* (.*?)\n\s+\*\s+\*Significance:\* (.*?)(?=\n\*|\n\n|\Z)",
     "The Implicit Vector-Product Revolution (Hessian-Free Framework, Martens, 2010–2012)", "2010", "[Martens, 2010](https://icml.cc/2010/papers/458.pdf)", "details_implicit_vector.md"),
    (r"\*\s+\*\*The Subspace & Low-Rank Second-Order Era \(~2020–Present\)\*\*\n\s+\*\s+\*Concept:\* (.*?)\n\s+\*\s+\*Significance:\* (.*?)(?=\n\*|\n\n|\Z)",
     "The Subspace & Low-Rank Second-Order Era (~2020–Present)", "2020", "[Hu et al., 2021](https://arxiv.org/abs/2106.09685)", "details_low_rank.md"),
    
    (r"-\s+### A\. The Pearlmutter Trick \(Implicit \$R\$-Operator Calculus\)\n\s+\*\s+\*\*Mechanism:\*\* (.*?)\n\s+\$\$(.*?)\$\$\n\s+\*\s+\*\*Pros:\*\* (.*?)(?=\n-|\n\n|\Z)",
     "A. The Pearlmutter Trick (Implicit $R$-Operator Calculus)", "1994", "[Pearlmutter, 1994](https://direct.mit.edu/neco/article/6/1/147/6078)", "details_pearlmutter.md"),
    (r"-\s+### B\. The Inner Conjugate Gradient \(CG\) Loop\n\s+\*\s+\*\*Mechanism:\*\* (.*?)\n\s+\*\s+\*\*Condition:\*\* (.*?)(?=\n-|\n\n|\Z)",
     "B. The Inner Conjugate Gradient (CG) Loop", "1952", "[Hestenes & Stiefel, 1952](https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_A1b.pdf)", "details_cg_loop.md"),
    (r"-\s+### C\. The Damped Gauss-Newton Approximation \(GNDA\)\n\s+\*\s+\*\*Mechanism:\*\* (.*?)(?=\n-|\n\n|\Z)",
     "C. The Damped Gauss-Newton Approximation (GNDA)", "1944", "[Levenberg, 1944](https://www.jstor.org/stable/43633451)", "details_gnda.md"),
     
    (r"\*\s+\*\*The Outer Loop / Inner Loop Split\*\*\n\s+\*\s+\*Profile:\* (.*?)(?=\n\*|\n\n|\Z)",
     "The Outer Loop / Inner Loop Split", "2010", "[Martens, 2010](https://icml.cc/2010/papers/458.pdf)", "details_outer_inner.md"),
    (r"\*\s+\*\*Damping Scaling Schedulers \(\$\\lambda\$\)\*\*\n\s+\*\s+\*Profile:\* (.*?)(?=\n\*|\n\n|\Z)",
     "Damping Scaling Schedulers ($\\lambda$)", "1963", "[Marquardt, 1963](https://epubs.siam.org/doi/10.1137/0111030)", "details_damping.md"),
     
    (r"\*\s+\*\*The Inner-Loop Sequential Communication Interconnect Barrier\*\*\n\s+\*\s+\*The Problem:\* (.*?)\n\s+\*\s+\*Mitigation:\* (.*?)(?=\n\*|\n\n|\Z)",
     "The Inner-Loop Sequential Communication Interconnect Barrier", "2010", "[Martens, 2010](https://icml.cc/2010/papers/458.pdf)", "details_comm_barrier.md"),
    (r"\*\s+\*\*The Low-Precision Mixed-Bits Underflow Hazard\*\*\n\s+\*\s+\*The Problem:\* (.*?)\n\s+\*\s+\*Mitigation:\* (.*?)(?=\n\*|\n\n|\Z)",
     "The Low-Precision Mixed-Bits Underflow Hazard", "2017", "[Micikevicius et al., 2017](https://arxiv.org/abs/1710.03740)", "details_mixed_precision.md"),
     
    (r"\*\s+\*\*Post-Training Low-Rank Alignment Optimization for Foundational LLMs\*\*\n\s+\*\s+\*Application:\* (.*?)(?=\n\*|\n\n|\Z)",
     "Post-Training Low-Rank Alignment Optimization for Foundational LLMs", "2021", "[Hu et al., 2021](https://arxiv.org/abs/2106.09685)", "details_post_train.md"),
    (r"\*\s+\*\*Unsupervised Latent Space Interpretability Mapping \(SAE Auditing\)\*\*\n\s+\*\s+\*Application:\* (.*?)(?=\n\*|\n\n|\Z)",
     "Unsupervised Latent Space Interpretability Mapping (SAE Auditing)", "2023", "[Bricken et al., 2023](https://transformer-circuits.pub/2023/monosemantic-features/index.html)", "details_sae.md"),
    (r"\*\s+\*\*High-Fidelity Medical Diagnostic Imaging Calibration Backbones\*\*\n\s+\*\s+\*Application:\* (.*?)(?=\n\*|\n\n|\Z)",
     "High-Fidelity Medical Diagnostic Imaging Calibration Backbones", "2010", "[Martens, 2010](https://icml.cc/2010/papers/458.pdf)", "details_medical.md")
]

# We will manually replace sections with tables
# Section 1
sec1_match = re.search(r"(\*\s+\*\*The First-Order.*?)(?=\n---)", content, re.DOTALL)
if sec1_match:
    sec1_text = sec1_match.group(1)
    table1 = "| Concept | Year | Paper | Details |\n|---|---|---|---|\n"
    table1 += f"| The First-Order Gradient Descent Baseline Era | 1951 | [Robbins & Monro (1951)](https://doi.org/10.1214/aoms/1177729586) | [Link](details_first_order_gradient.md) |\n"
    table1 += f"| The Exact Newton Processing Bottleneck | 1671 | [Newton's Method](https://en.wikipedia.org/wiki/Newton%27s_method) | [Link](details_newton_processing.md) |\n"
    table1 += f"| The Implicit Vector-Product Revolution | 2010 | [Martens, 2010](https://icml.cc/2010/papers/458.pdf) | [Link](details_implicit_vector.md) |\n"
    table1 += f"| The Subspace & Low-Rank Second-Order Era | 2020 | [Hu et al., 2021](https://arxiv.org/abs/2106.09685) | [Link](details_low_rank.md) |\n"
    content = content.replace(sec1_text, table1)

# Section 2
sec2_match = re.search(r"(-\s+### A\. The Pearlmutter Trick.*?)(?=\n---)", content, re.DOTALL)
if sec2_match:
    sec2_text = sec2_match.group(1)
    table2 = "| Component | Year | Paper | Details |\n|---|---|---|---|\n"
    table2 += f"| A. The Pearlmutter Trick (Implicit $R$-Operator Calculus) | 1994 | [Pearlmutter, 1994](https://direct.mit.edu/neco/article/6/1/147/6078) | [Link](details_pearlmutter.md) |\n"
    table2 += f"| B. The Inner Conjugate Gradient (CG) Loop | 1952 | [Hestenes & Stiefel, 1952](https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_A1b.pdf) | [Link](details_cg_loop.md) |\n"
    table2 += f"| C. The Damped Gauss-Newton Approximation (GNDA) | 1944 | [Levenberg, 1944](https://www.jstor.org/stable/43633451) | [Link](details_gnda.md) |\n"
    content = content.replace(sec2_text, table2)

# Section 3
sec3_match = re.search(r"(\*\s+\*\*The Outer Loop / Inner Loop Split\*\*.*?)(?=\n---)", content, re.DOTALL)
if sec3_match:
    sec3_text = sec3_match.group(1)
    table3 = "| Component | Year | Paper | Details |\n|---|---|---|---|\n"
    table3 += f"| The Outer Loop / Inner Loop Split | 2010 | [Martens, 2010](https://icml.cc/2010/papers/458.pdf) | [Link](details_outer_inner.md) |\n"
    table3 += f"| Damping Scaling Schedulers ($\\lambda$) | 1963 | [Marquardt, 1963](https://epubs.siam.org/doi/10.1137/0111030) | [Link](details_damping.md) |\n"
    content = content.replace(sec3_text, table3)

# Section 4
sec4_match = re.search(r"(\*\s+\*\*The Inner-Loop Sequential Communication Interconnect Barrier\*\*.*?)(?=\n---)", content, re.DOTALL)
if sec4_match:
    sec4_text = sec4_match.group(1)
    table4 = "| Challenge | Year | Paper | Details |\n|---|---|---|---|\n"
    table4 += f"| The Inner-Loop Sequential Communication Interconnect Barrier | 2010 | [Martens, 2010](https://icml.cc/2010/papers/458.pdf) | [Link](details_comm_barrier.md) |\n"
    table4 += f"| The Low-Precision Mixed-Bits Underflow Hazard | 2017 | [Micikevicius et al., 2017](https://arxiv.org/abs/1710.03740) | [Link](details_mixed_precision.md) |\n"
    content = content.replace(sec4_text, table4)

# Section 5
sec5_match = re.search(r"(\*\s+\*\*Post-Training Low-Rank Alignment Optimization for Foundational LLMs\*\*.*?)(?=\n---)", content, re.DOTALL)
if sec5_match:
    sec5_text = sec5_match.group(1)
    table5 = "| Application | Year | Paper | Details |\n|---|---|---|---|\n"
    table5 += f"| Post-Training Low-Rank Alignment Optimization for Foundational LLMs | 2021 | [Hu et al., 2021](https://arxiv.org/abs/2106.09685) | [Link](details_post_train.md) |\n"
    table5 += f"| Unsupervised Latent Space Interpretability Mapping (SAE Auditing) | 2023 | [Bricken et al., 2023](https://transformer-circuits.pub/2023/monosemantic-features/index.html) | [Link](details_sae.md) |\n"
    table5 += f"| High-Fidelity Medical Diagnostic Imaging Calibration Backbones | 2010 | [Martens, 2010](https://icml.cc/2010/papers/458.pdf) | [Link](details_medical.md) |\n"
    content = content.replace(sec5_text, table5)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

# Commit 1
run_git("tabularised the bullets")

# Step 2: Create detailed pages
details = [
    ("details_first_order_gradient.md", "First-Order Gradient Descent", "Details about First-Order Gradients."),
    ("details_newton_processing.md", "Newton Processing", "Details about Newton Processing Bottleneck."),
    ("details_implicit_vector.md", "Implicit Vector-Product", "Details about Implicit Vector-Product."),
    ("details_low_rank.md", "Subspace & Low-Rank", "Details about Subspace & Low-Rank Era."),
    ("details_pearlmutter.md", "Pearlmutter Trick", "Details about Pearlmutter Trick."),
    ("details_cg_loop.md", "Conjugate Gradient Loop", "Details about Inner CG Loop."),
    ("details_gnda.md", "Damped Gauss-Newton", "Details about Damped Gauss-Newton Approximation."),
    ("details_outer_inner.md", "Outer/Inner Loop Split", "Details about Outer and Inner Loop Split."),
    ("details_damping.md", "Damping Scaling Schedulers", "Details about Damping Scaling."),
    ("details_comm_barrier.md", "Sequential Communication Barrier", "Details about Communication Barrier."),
    ("details_mixed_precision.md", "Low-Precision Underflow Hazard", "Details about Mixed-Bits Underflow Hazard."),
    ("details_post_train.md", "Post-Training Low-Rank Alignment", "Details about Alignment Optimization."),
    ("details_sae.md", "Unsupervised Latent Space", "Details about SAE Auditing."),
    ("details_medical.md", "High-Fidelity Medical Diagnostic", "Details about Medical Diagnostic Imaging.")
]

for filename, title, desc in details:
    filepath = os.path.join(repo_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{desc}\n\n```mermaid\nflowchart TD\n    A[Start] --> B[{title}]\n```\n")

run_git("detailed pages created")

# Step 3: Decorate with emojis, banners
os.makedirs(os.path.join(repo_dir, "assets"), exist_ok=True)
svg_content = '''<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:rgb(255,255,0);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="200" fill="url(#grad1)" />
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="40" fill="white" font-family="Arial">
    Awesome Hessian-Free Optimization
    <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite" />
  </text>
</svg>'''
with open(os.path.join(repo_dir, "assets", "banner.svg"), "w") as f:
    f.write(svg_content)

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("# Awesome-Hessian-Free-Optimization", "# 🚀 Awesome-Hessian-Free-Optimization 🌟\n\n![Banner](assets/banner.svg)")
# Add emojis to headings
content = content.replace("## 1. The Macro Chronological Evolution", "## 🕰️ 1. The Macro Chronological Evolution")
content = content.replace("## 2. Core Functional & Algorithmic Components", "## ⚙️ 2. Core Functional & Algorithmic Components")
content = content.replace("## 3. The Hessian-Free Optimization Inversion Matrix", "## 🧮 3. The Hessian-Free Optimization Inversion Matrix")
content = content.replace("## 4. Production Engineering Challenges & Cluster Solutions", "## 🏗️ 4. Production Engineering Challenges & Cluster Solutions")
content = content.replace("## 5. Frontier Real-World AI Industrial Applications", "## 🌐 5. Frontier Real-World AI Industrial Applications")

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("added emojis and banner")

# Step 4: SEO Optimised and Badges to left added
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

badges_left = '<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>'

if "![Banner](assets/banner.svg)" in content:
    content = content.replace("![Banner](assets/banner.svg)", f"![Banner](assets/banner.svg)\n\n<div align=\"center\">\n{badges_left}\n</div>\n")
else:
    content = f"<div align=\"center\">\n{badges_left}\n</div>\n\n" + content

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("seo optimised and badges to left added")

# Step 5: Badges to right added
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

badges_right = '<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'

content = content.replace(f"{badges_left}\n</div>", f"{badges_left}\n{badges_right}\n</div>")

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("badges to right added")

# Step 6: Star history added
star_history_text = """
##  Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007%2FAwesome-Hessian-Free-Optimization&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Hessian-Free-Optimization&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Hessian-Free-Optimization&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Hessian-Free-Optimization&type=date&legend=bottom-right" />
</picture>
</a>
</div>
"""

with open(readme_path, "a", encoding="utf-8") as f:
    f.write(star_history_text)

run_git("star history added")

# Step 7: fixed star plot
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("chartrepos", "chart?repos")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_git("fixed star plot")

# Step 8: invalid awesome link fixed
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("https://github.com/sindresorhus/awesome", "https://github.com/ishandutta2007/Awesome-Awesome-Awesome")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_git("invalid awesome link fixed")

print("All done!")
