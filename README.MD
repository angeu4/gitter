# Gitter

Git-like version control CLI tool built for engineering design evaluation.

## Development Setup

`python -m venv .venv`
`source .venv/bin/activate`

`pip install -e .`
`pip install -r requirements-dev.txt`

## Run Tests with code coverage
`python -m pytest --cov=gitter`


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

## Quality Gates
- Ruff — Linting
- Bandit — Security scanning
- Pytest — Unit tests
- Coverage enforced at ≥90%

## Supported Commands
- `gitter init`
- `gitter add <file>`
- `gitter commit -m <message>`
- `gitter status`
- `gitter log`
- `gitter branch [<name>]`
- `gitter help`
- `gitter help <command>`

### Example usage
`$ gitter init`

Initialized empty Gitter repository

`$ echo "hello" > file.txt`
`$ gitter add file.txt`

Staged file.txt

`$ gitter commit -m "initial commit"`

Committed as <hash>

`$ gitter status`

Working tree clean

`$ gitter log`

commit <hash>

Author: anonymous

Message: initial commit

`$ gitter branch`

`* main`

`feature`