"""Pydantic models for the input of Wannier90."""

from wannier90_input.models.latest import Wannier90Input

# being explicit about exports is important!
__all__ = [
    "Wannier90Input",
]
