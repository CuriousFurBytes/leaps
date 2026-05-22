# Environments

Reproducible learning environments for **leaps** (Learning Environment for Any Progressive Subject). Every environment here is designed to get you from zero to running code in minutes, regardless of your host operating system.

---

## Why Reproducible Environments?

Learning is interrupted when setup fails. Reproducible environments mean:

- The same code runs the same way for every learner
- You can blow away and rebuild without fear
- Notebooks and exercises work without "it works on my machine" debugging
- Dependencies are explicit and versioned

---

## Approaches

### 1. venv / uv (Lightweight)

Best for quick topic exploration on a machine you control.

```bash
# Standard venv
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\activate             # Windows

pip install jupyter numpy scipy matplotlib sympy pandas requests pytest

# --- OR with uv (faster) ---
uv venv
source .venv/bin/activate
uv pip install jupyter numpy scipy matplotlib sympy pandas requests pytest
```

**When to use:** You want the fastest startup, you trust your host Python, and you are working on a single topic at a time.

**Drawbacks:** No isolation from system packages; dependency conflicts possible across topics.

---

### 2. Docker (Isolated)

Best for full isolation or when sharing work with others.

```bash
# From the environments/docker/ directory:
docker compose up

# Or build and run manually:
docker build -t leaps ./environments/docker/
docker run -p 8888:8888 -v $(pwd):/workspace leaps
```

Open JupyterLab at: `http://localhost:8888`

**When to use:** You need a clean slate, you are on a machine where you cannot install packages globally, or you want to ensure exact reproducibility.

**Drawbacks:** Heavier than venv; requires Docker Desktop on macOS/Windows.

See [`docker/`](./docker/) for the Dockerfile and compose file.

---

### 3. Devcontainer (VS Code Integrated)

Best for a fully configured VS Code experience with zero manual setup.

**Prerequisites:** VS Code + [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) + Docker

```bash
# 1. Open the leaps repo in VS Code
# 2. Press Ctrl+Shift+P → "Dev Containers: Reopen in Container"
# 3. Wait for the container to build (~2 minutes first time)
# Done. All extensions and packages are installed automatically.
```

**When to use:** You use VS Code as your primary editor and want extensions, linting, and Python/Jupyter all pre-configured with no manual steps.

**Drawbacks:** Requires Docker and VS Code; slower first build than venv.

See [`devcontainer/`](./devcontainer/) for the full configuration.

---

### 4. conda (Data Science)

Best for topics heavy in scientific computing, machine learning, or when you need non-Python packages (e.g., BLAS, CUDA).

```bash
# Create environment from scratch
conda create -n leaps python=3.12
conda activate leaps
conda install jupyter numpy scipy matplotlib sympy pandas scikit-learn
conda install -c conda-forge jupyterlab

# Or from a topic's environment.yml if one exists
conda env create -f topics/<topic>/environment.yml
conda activate leaps-<topic>
```

**When to use:** Topics involving ML/data science, when you need optimized linear algebra libraries, or when a topic's guide specifies a conda environment.

**Drawbacks:** Slower solver than uv/pip; larger disk footprint.

---

## Quick-Reference Comparison

| Approach | Setup Time | Isolation | Best For |
|---|---|---|---|
| venv / uv | ~1 min | Low | Quick exploration |
| Docker | ~5 min | High | Full isolation |
| Devcontainer | ~5 min (first) | High | VS Code users |
| conda | ~3 min | Medium | Data science |

---

## Directory Structure

```
environments/
├── README.md                   # This file
├── devcontainer/
│   └── devcontainer.json       # Global devcontainer for the full repo
└── docker/
    ├── Dockerfile              # General-purpose learning image
    └── docker-compose.yml      # Compose for the learning environment
```

Topic-specific environments (when a topic needs unusual dependencies) live inside their own topic directory:

```
TOPICS/<topic>/
└── environment.yml   # or requirements.txt / pyproject.toml
```

---

## Adding a Topic-Specific Environment

If a topic needs packages beyond the base set, add a `requirements.txt` or `environment.yml` to its directory and document the setup in the topic's `README.md`. Keep the base environment as lean as possible; install heavy packages only in the topic that needs them.
