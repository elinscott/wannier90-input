"""Test wannier90_input models."""

import importlib

import numpy as np
import pytest

from wannier90_input.models import versions
from wannier90_input.models.parameters import Projection
from wannier90_input.models.template import Wannier90InputTemplate


def models() -> list[type[Wannier90InputTemplate]]:
    """Load all models."""
    models = []
    for version in versions:
        # Load the model from wannier90_input.models.<version>
        model = importlib.import_module(f"wannier90_input.models.{version}").Wannier90Input
        assert issubclass(model, Wannier90InputTemplate)
        models.append(model)
    return models


@pytest.mark.parametrize("model", models())
def test_wannier90_input(model: type[Wannier90InputTemplate]) -> None:
    """Test the creation of an entire Wannier90 input file."""
    num_wann = 10
    inp = model(
        num_wann=num_wann,
        unit_cell_cart=np.identity(3),
        mp_grid=[3, 3, 3],
        atoms_frac=[{"symbol": "O", "position": [0, 0, 0]}],
        projections=[{"site": "O", "ang_mtm": "sp3"}],
    )

    # Test a direct argument
    assert inp.num_wann == num_wann  #type: ignore[attr-defined]

    # Defined via a validaotr
    assert inp.num_bands == num_wann  #type: ignore[attr-defined]

    # A default value
    assert inp.projections[0].radial == 1  #type: ignore[attr-defined]



def test_projections() -> None:
    """Test the creation of a Projections object."""
    proj = Projection(fractional_site=[0.5, 0.5, 0.5], ang_mtm="sp3")
    assert proj.fractional_site == [0.5, 0.5, 0.5]
    assert proj.ang_mtm == "sp3"
    assert proj.zaxis == (0, 0, 1)  # Default value
    assert proj.xaxis == (1, 0, 0)  # Default value
    assert proj.radial == 1  # Default value
