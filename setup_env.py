#!/usr/bin/env python3
"""
Cross-platform environment setup for the CKM treasure hunt notebooks.

Works on Windows, Linux, and macOS by using Python's built-in venv module.
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    print("[run]", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd) if cwd else None)


def venv_python_path(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def default_notebook(project_root: Path) -> str:
    # Prefer fortytwo if present, otherwise fall back to CKM_triangle_hunt.
    preferred = ["fortytwo.ipynb", "CKM_triangle_hunt.ipynb"]
    for name in preferred:
        if (project_root / name).exists():
            return name
    return preferred[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Set up the CKM notebook environment in a local "
            "virtual environment."
        )
    )
    parser.add_argument(
        "--venv",
        default=".venv",
        help="Virtual environment folder name (default: .venv)",
    )
    parser.add_argument(
        "--requirements",
        default="requirements.txt",
        help="Path to requirements file (default: requirements.txt)",
    )
    parser.add_argument(
        "--kernel-name",
        default="ckm-hunt",
        help="Jupyter kernel name to register (default: ckm-hunt)",
    )
    parser.add_argument(
        "--display-name",
        default="Python (ckm-hunt)",
        help='Jupyter kernel display name (default: "Python (ckm-hunt)")',
    )
    parser.add_argument(
        "--no-kernel",
        action="store_true",
        help="Skip Jupyter kernel registration",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Launch Jupyter Notebook after setup",
    )
    parser.add_argument(
        "--notebook",
        default=None,
        help="Notebook to open when using --run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    project_root = Path(__file__).resolve().parent
    venv_dir = project_root / args.venv
    req_file = project_root / args.requirements

    if not req_file.exists():
        print(f"[error] requirements file not found: {req_file}")
        return 1

    print(f"[info] Project root: {project_root}")
    print(f"[info] OS: {platform.system()} {platform.release()}")

    # 1) Create virtual environment
    run([sys.executable, "-m", "venv", str(venv_dir)], cwd=project_root)

    py = venv_python_path(venv_dir)
    if not py.exists():
        print(f"[error] venv python not found: {py}")
        return 1

    # 2) Install dependencies
    run(
        [
            str(py),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "setuptools",
            "wheel",
        ]
    )
    run([str(py), "-m", "pip", "install", "-r", str(req_file)])

    # 3) Register Jupyter kernel (optional)
    if not args.no_kernel:
        run(
            [
                str(py),
                "-m",
                "ipykernel",
                "install",
                "--user",
                "--name",
                args.kernel_name,
                "--display-name",
                args.display_name,
            ]
        )

    print("[ok] Environment setup complete.")
    print(f"[ok] Virtual environment: {venv_dir}")

    # 4) Optionally run Jupyter Notebook
    if args.run:
        nb = args.notebook or default_notebook(project_root)
        nb_path = project_root / nb
        if not nb_path.exists():
            print(f"[error] notebook not found: {nb_path}")
            return 1
        print(f"[info] Launching notebook: {nb}")
        run(
            [str(py), "-m", "jupyter", "notebook", str(nb_path)],
            cwd=project_root,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
