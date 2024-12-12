"""Tests for generate_internal_api_rst.py script."""

from __future__ import annotations

from pathlib import Path

from cicd.scripts.generate_internal_api_rst import (
    clean_directory,
    find_internal_modules,
    generate_module_rst,
    get_module_description,
    organize_modules,
)


def test_organize_modules() -> None:
    """Test basic module organization."""
    modules = ["_color.utils", "_color.css_colors", "_hist", "_kde", "_color.interpolation"]
    hierarchy = organize_modules(modules)

    assert "color" in hierarchy
    assert len(hierarchy["color"]) == 3
    assert "_color.utils" in hierarchy["color"]
    assert "_color.css_colors" in hierarchy["color"]
    assert "_color.interpolation" in hierarchy["color"]
    assert "hist" in hierarchy
    assert hierarchy["hist"] == []
    assert "kde" in hierarchy
    assert hierarchy["kde"] == []


def test_generate_module_rst_with_submodules() -> None:
    """Test RST generation for module with submodules."""
    content = generate_module_rst("_color", ["_color.utils", "_color.css_colors"])

    assert "ridgeplot._color" in content
    assert ".. toctree::" in content
    assert "utils" in content
    assert "css_colors" in content
    assert ".. automodule:: ridgeplot._color" in content
    assert ":private-members:" in content


def test_find_internal_modules(tmp_path: Path) -> None:
    """Test finding internal modules."""
    test_dir = tmp_path / "src" / "ridgeplot"
    test_dir.mkdir(parents=True)
    (test_dir / "__init__.py").touch()
    (test_dir / "_test.py").write_text("# Test module")
    color_dir = test_dir / "_color"
    color_dir.mkdir()
    (color_dir / "__init__.py").touch()
    (color_dir / "utils.py").write_text("# Utils module")

    modules = list(find_internal_modules(test_dir))
    module_names = [name for name, _ in modules]

    assert "_test" in module_names
    assert "_color.utils" in module_names
    assert len(modules) == 2
    assert all(isinstance(path, Path) for _, path in modules)
    assert all(path.exists() for _, path in modules)


def test_clean_directory(tmp_path: Path) -> None:
    """Test directory cleaning."""
    test_dir = tmp_path / "clean_test"
    test_dir.mkdir()

    (test_dir / "test.rst").touch()
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "nested.rst").touch()

    clean_directory(test_dir)
    assert not (test_dir / "test.rst").exists()
    assert not (test_dir / "subdir").exists()
    assert not list(test_dir.glob("**/*"))


def test_get_module_description() -> None:
    """Test getting module descriptions."""
    assert get_module_description("ridgeplot._color") == "Color management and utilities."
    assert get_module_description("ridgeplot._unknown") == "Internal module utilities."
    assert (
        get_module_description("ridgeplot._color.utils")
        == "Color manipulation and conversion functions."
    )
