FROM python:3.12-slim

LABEL maintainer="leaps"
LABEL description="Learning Environment for Any Progressive Subject"

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    nano \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python learning packages
# Core scientific stack
RUN pip install --no-cache-dir \
    numpy \
    scipy \
    matplotlib \
    sympy \
    pandas

# Networking and testing
RUN pip install --no-cache-dir \
    requests \
    httpx \
    pytest \
    pytest-cov

# Code quality
RUN pip install --no-cache-dir \
    black \
    ruff

# Visualization
RUN pip install --no-cache-dir \
    plotly \
    scikit-learn

WORKDIR /workspace

CMD ["bash"]
