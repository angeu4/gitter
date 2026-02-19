# Gitter

Git-like version control CLI tool built for engineering design evaluation.

## Development Setup

python -m venv .venv
source .venv/bin/activate

pip install -e .
pip install -r requirements-dev.txt

## Run Tests
pytest


## Continuous Integration
The project uses GitHub Actions to enforce quality gates on every push and pull request.

Checks Included:
Ruff → Linting and code quality
Bandit → Security scanning
Pytest → Test execution

CI runs automatically on:
Push to main
Push to development
Pull requests

## Storage Layer
Implements content-addressable object storage using SHA1 hashing.
Supports Blob, Tree and Commit object primitives.

## Repository Metadata Layer
Implements repository filesystem layout, HEAD pointer management and branch reference storage.

## Index Layer
Implements staging area abstraction with deterministic persistence.
