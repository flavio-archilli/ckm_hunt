# CKM treasure hunt

## One-command cross-platform setup (Windows, Linux, macOS)

Run this from the project folder:

```bash
python setup_env.py
```

This will:

- create a local virtual environment in `.venv`
- install all dependencies from `requirements.txt`
- register a Jupyter kernel named `ckm-hunt`

To set up and immediately launch a notebook:

```bash
python setup_env.py --run --notebook fortytwo.ipynb
```

If your system uses `python3` instead of `python`, replace `python` with `python3`.

## Manual setup (optional)

### 1) Create the virtual environment

```bash
python -m venv .venv
```

### 2) Activate it

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Windows (cmd):

```bat
.venv\Scripts\activate.bat
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3) Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Register the notebook kernel

```bash
python -m ipykernel install --user --name ckm-hunt --display-name "Python (ckm-hunt)"
```

### 5) Launch Jupyter

```bash
jupyter notebook fortytwo.ipynb
```

If you use VS Code, open the notebook and select the `Python (ckm-hunt)` kernel.
