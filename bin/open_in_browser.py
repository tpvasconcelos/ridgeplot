#!/usr/bin/env python
from __future__ import annotations

import sys
import webbrowser
from pathlib import Path
from urllib.request import pathname2url


def main() -> None:
    path_abs = Path(sys.argv[1]).resolve().as_posix()
    path_url = pathname2url(path_abs)
    webbrowser.open(f"file://{path_url}")


if __name__ == "__main__":
    main()
