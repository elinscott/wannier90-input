import numpy as np

from wannier90_input.models.latest import Wannier90Input


def test_wannier90_input():
    """Test the creation of an entire Wannier90 input file."""
    num_wann = 10
    inp = Wannier90Input(num_wann=num_wann,
                         unit_cell_cart=np.identity(3),
                         mp_grid=[3, 3, 3],
                         atoms_frac=[dict(symbol='O', position=[0, 0, 0])],
                         projections=[{'site': 'O', 'ang_mtm': 'sp3'}])
    assert inp.num_wann == 10  # A direct argument
    assert inp.num_bands == 10  # Defined via a validator
    assert inp.projections[0].radial == 1  # A default value
