"""Test wannier90_input models."""

import numpy as np

from wannier90_input.models.latest import Wannier90Input
from wannier90_input.models.parameters import Projection


def test_wannier90_input() -> None:
    """Test the creation of an entire Wannier90 input file."""
    num_wann = 10
    inp = Wannier90Input(num_wann=num_wann,
                         unit_cell_cart=np.identity(3),
                         mp_grid=[3, 3, 3],
                         atoms_frac=[dict(symbol='O', position=[0, 0, 0])],
                         projections=[{'site': 'O', 'ang_mtm': 'sp3'}])
    assert inp.num_wann == num_wann  # A direct argument
    assert inp.num_bands == num_wann  # Defined via a validator
    assert inp.projections[0].radial == 1  # A default value

def test_projections() -> None:
    """Test the creation of a Projections object."""
    proj = Projection(fractional_site=[0.5, 0.5, 0.5], ang_mtm='sp3')
    assert proj.fractional_site == [0.5, 0.5, 0.5]
    assert proj.ang_mtm == 'sp3'
    assert proj.zaxis == (0, 0, 1)  # Default value
    assert proj.xaxis == (1, 0, 0)  # Default value
    assert proj.radial == 1  # Default value
