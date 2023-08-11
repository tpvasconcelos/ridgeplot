#!/usr/bin/env python
from pathlib import Path

# isort: split
from utils import ToxEnvMarkers, run_subprocess


def main() -> None:
    tems = ToxEnvMarkers()
    env_tag = f"{tems.PY_PYTHON_VERSION}-{tems.PY_SYS_PLATFORM}"
    popen_args = [
        "pip-compile-multi",
        "--upgrade",
        f"--out-ext={env_tag}.txt",
        "--directory=requirements/",
        "--autoresolve",
        "--backtracking",
        "--allow-unsafe",
    ]
    run_subprocess(popen_args)
    for reqs_txt in Path("requirements/").glob(f"*{env_tag}.txt"):
        locked_path = Path("requirements/locked").joinpath(reqs_txt.name)
        print(f"Moving {reqs_txt} to {locked_path}")
        reqs_txt.replace(locked_path)


if __name__ == "__main__":
    main()
