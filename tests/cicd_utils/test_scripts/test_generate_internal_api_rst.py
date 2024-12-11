#!/usr/bin/env python3
"""Tests for generate_internal_api_rst.py script."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Import script directly
SCRIPT_PATH = Path(__file__).parents[3] / "cicd_utils/cicd/scripts/generate_internal_api_rst.py"
sys.path.append(str(SCRIPT_PATH.parent))

from generate_internal_api_rst import (
    generate_module_rst,
    organize_modules,
)


def test_organize_modules() -> None:
    """Test basic module organization."""
    modules = ["_color.utils", "_color.css_colors", "_hist", "_kde"]
    hierarchy = organize_modules(modules)
    
    assert "color" in hierarchy
    assert len(hierarchy["color"]) == 2
    assert "_color.utils" in hierarchy["color"]
    assert "hist" in hierarchy


def test_generate_module_rst() -> None:
    """Test RST content generation."""
    content = generate_module_rst("_color", ["_color.utils", "_color.css_colors"])
    
    assert "ridgeplot._color" in content
    assert ".. toctree::" in content
    assert "utils" in content
    assert "css_colors" in content