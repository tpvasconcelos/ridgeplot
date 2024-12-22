from __future__ import annotations

from pathlib import Path


def test_packaged_installed() -> None:
    """Assert that ridgeplot has been properly installed and isn't simply under
    the current working directory."""
    import ridgeplot

    # By definition, if a module has a __path__ attribute, it is a package.
    assert hasattr(ridgeplot, "__path__")
    pkg_path = list(ridgeplot.__path__)
    assert len(pkg_path) == 1
    package_path = Path(pkg_path[0])
    assert package_path.exists()
    assert package_path.is_dir()
    assert package_path.name == "ridgeplot"
    assert Path.cwd().resolve() != package_path.parent.resolve()


def test_public_api() -> None:
    from ridgeplot import __all__ as public_api

    assert set(public_api) == {"ridgeplot", "list_all_colorscale_names", "__version__"}
