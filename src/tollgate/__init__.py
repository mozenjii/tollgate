"""tollgate: an OpenAI-compatible gateway that earns the right to use a cheaper model.

Nothing is served yet. The package exists so that the lint, type, test and coverage gates
run against real installed code from the first commit, rather than being switched on later
against a codebase that has already drifted from them.

The package root exports only the version; code is imported from the module that owns it.
Keeping the root that small means nothing reaches the public surface without a test behind it.
"""

__all__ = ["__version__"]

__version__ = "0.0.0"
"""The released version.

Still ``0.0.0`` on purpose: nothing is released. It must equal the version in
``pyproject.toml``; a test enforces that, so the two can never disagree.
"""
