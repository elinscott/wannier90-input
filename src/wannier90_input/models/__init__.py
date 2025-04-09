"""Pydantic models for Wannier90 input files."""

from pathlib import Path

directory = Path(__file__).parent
versions = ["latest"] + [v.name[:-3] for v in directory.glob("sha_*.py")]
