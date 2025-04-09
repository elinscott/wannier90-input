"""Test wannier90_input models."""

import pytest

import numpy as np
from typing import Type
import importlib

from wannier90_input.models import versions
from wannier90_input.models.template import Wannier90InputTemplate
from wannier90_input.models.parameters import Projection

def models() -> list[Type[Wannier90InputTemplate]]:
    """Load all models."""
    from wannier90_input.models import versions

    models = []
    for version in versions:
        # Load the model from wannier90_input.models.<version>
        model = importlib.import_module(f"wannier90_input.models.{version}").Wannier90Input
        assert issubclass(model, Wannier90InputTemplate)
        models.append(model)
    return models


@pytest.mark.parametrize("model", models())
def test_wannier90_input(model: Type[Wannier90InputTemplate]) -> None:
    """Test the creation of an entire Wannier90 input file."""
    num_wann = 10
    inp = model(
        num_wann=num_wann,
        unit_cell_cart=np.identity(3),
        mp_grid=[3, 3, 3],
        atoms_frac=[{"symbol": "O", "position": [0, 0, 0]}],
        projections=[{"site": "O", "ang_mtm": "sp3"}],
    )
    assert inp.num_wann == num_wann  # A direct argument
    assert inp.num_bands == num_wann  # Defined via a validator
    assert inp.projections[0].radial == 1  # A default value


def test_projections() -> None:
    """Test the creation of a Projections object."""
    proj = Projection(fractional_site=[0.5, 0.5, 0.5], ang_mtm="sp3")
    assert proj.fractional_site == [0.5, 0.5, 0.5]
    assert proj.ang_mtm == "sp3"
    assert proj.zaxis == (0, 0, 1)  # Default value
    assert proj.xaxis == (1, 0, 0)  # Default value
    assert proj.radial == 1  # Default value
