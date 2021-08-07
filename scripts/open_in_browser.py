import sys
import webbrowser
from pathlib import Path
from urllib.request import pathname2url

path_abs: str = Path(sys.argv[1]).resolve().as_posix()
path_url = pathname2url(path_abs)

webbrowser.open(f"file://{path_url}")
