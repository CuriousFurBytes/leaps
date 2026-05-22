# =============================================================================
# LEAPS Learning Environment — {{TOPIC_NAME}}
#
# Provides a fully configured environment for studying {{TOPIC_NAME}}.
# Includes Jupyter, common Python scientific packages, and development tools.
#
# Build:
#   docker build -t leaps-{{TOPIC_SLUG}} .
#
# Run (Jupyter):
#   docker run -p 8888:8888 -v $(pwd):/workspace leaps-{{TOPIC_SLUG}}
#
# Run (interactive shell):
#   docker run -it -v $(pwd):/workspace leaps-{{TOPIC_SLUG}} bash
# =============================================================================

FROM python:3.12-slim

# Metadata
LABEL maintainer="{{MAINTAINER_EMAIL}}"
LABEL description="Learning environment for {{TOPIC_NAME}} — LEAPS"
LABEL topic="{{TOPIC_NAME}}"
LABEL version="1.0.0"

# =============================================================================
# System dependencies
# =============================================================================

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Version control
    git \
    # Network tools
    curl \
    wget \
    # Text editors
    vim \
    nano \
    # Build tools (needed for some Python packages)
    build-essential \
    gcc \
    g++ \
    gfortran \
    # Compression tools
    zip \
    unzip \
    # Process management
    procps \
    # Useful shell utilities
    less \
    tree \
    jq \
    # LaTeX for matplotlib (optional — comment out if slow to install)
    # texlive-latex-base \
    # texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Python environment
# =============================================================================

# Upgrade pip and install essential tools
RUN pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

# Copy requirements file
COPY requirements.txt /tmp/requirements.txt

# Install all Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# =============================================================================
# Jupyter configuration
# =============================================================================

# Create Jupyter configuration directory
RUN mkdir -p /root/.jupyter

# Configure Jupyter to run without a browser, listen on all interfaces,
# and disable token authentication (acceptable for local dev containers only)
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.notebook_dir = '/workspace'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py

# Install useful Jupyter extensions
RUN pip install --no-cache-dir \
    jupyterlab \
    nbextensions \
    jupyter_contrib_nbextensions \
    && jupyter contrib nbextension install --system \
    && jupyter nbextension enable varInspector/main \
    && jupyter nbextension enable toc2/main \
    && jupyter nbextension enable execute_time/ExecuteTime \
    || true  # Don't fail if extensions don't install perfectly

# =============================================================================
# Git configuration
# =============================================================================

RUN git config --global core.editor "vim" && \
    git config --global init.defaultBranch main && \
    git config --global advice.detachedHead false

# =============================================================================
# Shell configuration
# =============================================================================

# Add useful aliases
RUN echo '\n\
# LEAPS aliases\n\
alias ll="ls -alF"\n\
alias la="ls -A"\n\
alias ..="cd .."\n\
alias ...="cd ../.."\n\
alias jnb="jupyter notebook"\n\
alias jlab="jupyter lab"\n\
# Python shortcuts\n\
alias py="python3"\n\
alias ipy="ipython"\n\
' >> /root/.bashrc

# =============================================================================
# Workspace
# =============================================================================

# Create workspace directory
RUN mkdir -p /workspace
WORKDIR /workspace

# Copy any topic-specific setup files (if they exist)
# COPY setup.py /workspace/setup.py
# COPY data/ /workspace/data/

# =============================================================================
# Expose ports
# =============================================================================

# Jupyter Notebook
EXPOSE 8888

# JupyterLab
EXPOSE 8889

# Additional ports for topic-specific services (uncomment as needed)
# EXPOSE 5000   # Flask / API server
# EXPOSE 6006   # TensorBoard
# EXPOSE 8080   # Generic web server

# =============================================================================
# Entrypoint
# =============================================================================

# Default: start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", \
     "--allow-root", "--notebook-dir=/workspace"]

# Alternative entrypoints (pass as docker run argument):
#   bash                         — interactive shell
#   jupyter notebook             — classic Jupyter Notebook
#   python3 script.py            — run a specific script
