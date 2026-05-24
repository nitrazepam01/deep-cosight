import sys
from pathlib import Path

pydeps = Path(__file__).resolve().parents[1] / "pydeps"
sys.path.insert(0, str(pydeps))

from yt_dlp import main

if __name__ == "__main__":
    main()
