#!/usr/bin/env python3
"""Generate RST files for internal API documentation.

Execution steps:
- Scan the ridgeplot source directory for internal modules (prefixed with _)
- Generate organized hierarchical RST documentation structure
- Each RST file includes module description and appropriate directives
"""

from __future__ import annotations

import importlib
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

PATH_ROOT_DIR = Path(__file__).parents[3]
PATH_TO_SRC = PATH_ROOT_DIR / "src/ridgeplot"
PATH_TO_DOCS = PATH_ROOT_DIR / "docs/api/internal"

MODULE_DESCRIPTIONS = {
    "ridgeplot": "Main ridgeline plotting module.",
    "ridgeplot._ridgeplot": "Core implementation of ridgeline plots.",
    "ridgeplot._figure_factory": "Factory functions for creating ridgeline plots.",
    "ridgeplot._hist": "Histogram generation and binning utilities.",
    "ridgeplot._kde": "Kernel density estimation implementation.",
    "ridgeplot._types": "Type definitions and validation.",
    "ridgeplot._utils": "General utility functions.",
    "ridgeplot._missing": "Missing value handling utilities.",
    "ridgeplot._version": "Version information.",
    "ridgeplot._color": "Color management and utilities.",
    "ridgeplot._color.colorscale": "Continuous colorscale generation and handling.",
    "ridgeplot._color.css_colors": "Standard CSS color definitions and mappings.",
    "ridgeplot._color.interpolation": "Color interpolation and gradient utilities.",
    "ridgeplot._color.utils": "Color manipulation and conversion functions.",
    "ridgeplot._obj": "Object-oriented implementations.",
    "ridgeplot._obj.traces": "Trace implementations for different plot types.",
    "ridgeplot._obj.traces.area": "Area trace for density visualizations.",
    "ridgeplot._obj.traces.bar": "Bar trace for histogram visualizations.",
    "ridgeplot._obj.traces.base": "Base classes for trace implementations.",
    "ridgeplot._vendor": "Third-party vendored utilities.",
    "ridgeplot._vendor.more_itertools": "Additional iteration utilities.",
}


def find_internal_modules(base_path: Path) -> Iterator[tuple[str, Path]]:
    """Find all internal modules and their paths."""
    for item in base_path.rglob("*.py"):
        if item.name.startswith("__"):
            continue

        rel_path = item.relative_to(base_path)
        mod_parts = list(rel_path.parent.parts)
        if rel_path.name != "__init__.py":
            mod_parts.append(rel_path.stem)

        if not any(part.startswith("_") and not part.startswith("__") for part in mod_parts):
            continue

        module_name = ".".join(mod_parts)
        yield module_name, item


def get_module_description(full_module_name: str) -> str:
    """Get the module description."""
    try:
        module = importlib.import_module(full_module_name)
        docstring = module.__doc__
        if docstring:
            return docstring.strip().split("\n")[0]
    except (ImportError, AttributeError):
        pass

    return MODULE_DESCRIPTIONS.get(full_module_name, "Internal module utilities.")


def generate_module_rst(module_name: str, submodules: list[str] | None = None) -> str:
    """Generate RST content for a module."""
    full_module_name = f"ridgeplot.{module_name}"
    description = get_module_description(full_module_name)

    content = [
        full_module_name,
        "=" * len(full_module_name),
        "",
        description,
        "",
    ]

    if submodules:
        content.extend(
            [
                ".. toctree::",
                "   :maxdepth: 1",
                "",
            ]
        )
        for submod in sorted(submodules):
            rel_path = submod.replace(module_name + ".", "")
            content.append(f"   {rel_path}")
        content.append("")

    content.extend([f".. automodule:: {full_module_name}", "   :private-members:", ""])

    return "\n".join(content)


def organize_modules(modules: list[str]) -> dict[str, list[str]]:
    """Organize modules into a hierarchical structure."""
    hierarchy = defaultdict(list)

    for module in modules:
        parts = module.split(".")
        if len(parts) > 1:
            parent = parts[0].lstrip("_")
            hierarchy[parent].append(module)
        else:
            clean_name = module.lstrip("_")
            hierarchy[clean_name] = []

    return dict(hierarchy)


def write_rst_file(output_dir: Path, module_name: str, content: str) -> None:
    """Write RST content to file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    clean_name = module_name.lstrip("_")
    parts = clean_name.split(".")

    if len(parts) > 1:
        *dir_parts, filename = parts
        current_dir = output_dir
        for part in dir_parts:
            current_dir = current_dir / part
            current_dir.mkdir(exist_ok=True)
        filepath = current_dir / f"{filename}.rst"
    else:
        filepath = output_dir / f"{clean_name}.rst"

    filepath.write_text(content)
    print(f"Generated {filepath.relative_to(PATH_TO_DOCS)}")


def clean_directory(path: Path) -> None:
    """Clean directory recursively."""
    if path.exists():
        for item in sorted(path.glob("**/*"), reverse=True):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                item.rmdir()


def main() -> None:
    """Generate RST files for all internal modules."""
    for dir_name in ["color", "obj", "vendor", "_color", "_obj", "_vendor"]:
        dir_path = PATH_TO_DOCS / dir_name
        if dir_path.exists():
            clean_directory(dir_path)
            dir_path.rmdir()

    for rst_file in PATH_TO_DOCS.glob("*.rst"):
        rst_file.unlink()

    PATH_TO_DOCS.mkdir(parents=True, exist_ok=True)
    modules = [name for name, _ in find_internal_modules(PATH_TO_SRC)]
    hierarchy = organize_modules(modules)

    for module_name, submodules in hierarchy.items():
        content = generate_module_rst(module_name, submodules)
        write_rst_file(PATH_TO_DOCS, module_name, content)

        for submod in submodules:
            subcontent = generate_module_rst(submod)
            write_rst_file(PATH_TO_DOCS, submod, subcontent)


if __name__ == "__main__":
    main()
