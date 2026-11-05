"""The package installs, imports, and describes itself consistently."""

import tomllib
from importlib.metadata import version
from pathlib import Path

import tollgate

PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def declared_version() -> str:
    """Read the version from pyproject.toml without going through the installed package."""
    with PYPROJECT.open("rb") as handle:
        return str(tomllib.load(handle)["project"]["version"])


def test_version_matches_pyproject() -> None:
    # Two places state the version; this is what stops them drifting apart.
    assert tollgate.__version__ == declared_version()


def test_installed_metadata_matches_the_source() -> None:
    # Fails if the tests are running against a stale install instead of this checkout.
    assert version("tollgate") == tollgate.__version__


def test_public_surface_is_only_the_version() -> None:
    # A growing __all__ without tests behind it is how an unchecked API appears.
    assert tollgate.__all__ == ["__version__"]


def test_package_ships_type_information() -> None:
    # Without the PEP 561 marker, users' type checkers silently treat tollgate as untyped.
    assert Path(tollgate.__file__).with_name("py.typed").is_file()
