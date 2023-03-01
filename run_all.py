from pathlib import Path
from subprocess import run

import sys

root = Path.cwd()
for script in root.glob('day*/day*.py'):
    print(f'========= Running {script}')
    path = Path(script)
    completed = run([sys.executable, path.name], cwd=path.parent)
    print()
    if completed.returncode != 0:
        break
