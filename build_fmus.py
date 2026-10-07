"""Build models/*.py into fmus/*.fmu. Run with:  .\\.venv\\Scripts\\python.exe build_fmus.py"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
for script in sorted((ROOT / "models").glob("*.py")):
    subprocess.run([Path(sys.executable).parent / "pythonfmu", "build", "-f", script, "-d", ROOT / "fmus"], check=True)
