#!/usr/bin/env python3
"""Repository entry point for the D4 five-class face vector."""

from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from face_vector import main  # noqa: E402

if __name__ == "__main__":
    main()
