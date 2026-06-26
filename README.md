# lumed_andor

`lumed_andor` is a Python wrapper and PyQt GUI for controlling Andor cameras through the vendor SDK.

Current package scope includes:

- ctypes-based wrapper around core Andor SDK camera control calls
- PyQt widget for camera connection, configuration, and acquisition
- acquisition helpers for FVB, single-track, multi-track, random-track, and image modes
- plotting helpers for acquired spectra and images
- TOML import and export for camera settings

## Platform and runtime requirements

Current implementation assumes a Linux host with the Andor SDK installed in standard local paths:

- shared library at `/usr/local/lib/libandor.so`
- initialization files under `/usr/local/etc/andor`
- desktop environment capable of running a PyQt5 GUI

These paths are currently hardcoded in `src/lumed_andor/andor_control.py`.

## Installation

Project uses modern Python packaging and dependency management with [uv](https://github.com/astral-sh/uv).

### Runtime install from repository

```sh
git clone git@github.com:lumed-mtl/lumed_andor.git
cd lumed_andor
uv sync --no-dev
```

### Developer install

```sh
git clone git@github.com:lumed-mtl/lumed_andor.git
cd lumed_andor
uv sync
```

The default `uv sync` workflow installs the package plus the `dev` dependency group.

## Running the GUI

The package exposes a module entry point through `python -m lumed_andor`.

```sh
uv run python -m lumed_andor
```

## Development conventions

Development and contributions follow these conventions:

- **Versioning:** [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH)
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) (for example `feat:`, `fix:`, `chore:`)
- **Branching:** [Conventional Branching](https://conventional-branch.github.io/) with short descriptive names such as `fix/andor-sdk-init` or `chore/modernize-python-tooling`
- **Dependency management:** [uv](https://github.com/astral-sh/uv)
- **Linting and formatting:** [ruff](https://docs.astral.sh/ruff/)
- **Type checking:** [ty](https://github.com/hynek/ty)
- **Testing:** [pytest](https://docs.pytest.org/)

Typical development commands:

```sh
uv run ruff check .
uv run ruff format .
uv run ty .
uv run pytest
```

## Branch flow and merge strategy

This repository uses a simple solo-maintainer branch model.

- `main` serves as the stable release branch.
- `dev` serves as the integration branch for ongoing work.
- Short-lived work branches follow Conventional Branch naming, branch from `dev`, merge back into `dev` when complete, and are deleted afterward.
- Pull requests are optional and are not part of the normal integration flow.

Preferred history policy:

- Non-fast-forward merge commits are the default for integrating completed work branches into `dev`.
- Non-fast-forward merges are also preferred when promoting `dev` into `main` at release boundaries.
- Rebase is not the default integration mechanism when preserving the original branch timeline is more valuable than maintaining a fully linear graph.
- Squash merges are reserved for very small or noisy branches whose intermediate commits have little long-term value.
- For feature, refactor, and modernization branches, preserving branch-local commit history is preferred over squash.

## Notes on packaging and SDK coupling

Python dependencies are managed in `pyproject.toml`, but camera access still depends on the external Andor SDK runtime being installed on the host system. Reproducible Python environments do not remove that external system requirement.
