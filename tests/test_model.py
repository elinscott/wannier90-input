"""Test wannier90_input models."""

import importlib

import numpy as np
import pytest

from wannier90_input.models import versions
from wannier90_input.models.parameters import AngularMomentum, Projection, L
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
    assert inp.num_wann == num_wann  # type: ignore[attr-defined]

    # Defined via a validaotr
    assert inp.num_bands == num_wann  # type: ignore[attr-defined]

    # A default value
    assert inp.projections[0].radial == 1  # type: ignore[attr-defined]


@pytest.mark.parametrize("input_str", ["l=0", "s", "l=1", "p", "pz", "px", "py",
                 "l=2", "d", "dxy", "dxz", "dyz", "dx2-y2", "dz2",
                 "l=3", "f", "fz3", "fxz2", "fyz2", "fz(x2-y2)", "fxyz", "fx(x2-3y2)", "fy(3x2-y2)",
                 "l=-1", "sp", "sp-1", "sp-2",
                 "l=-2", "sp2", "sp2-1", "sp2-2", "sp2-3",
                 "l=-3", "sp3", "sp3-1", "sp3-2", "sp3-3", "sp3-4",
                 "l=-4", "sp3d", "sp3d-1", "sp3d-2", "sp3d-3", "sp3d-4", "sp3d-5",
                 "l=-5", "sp3d2", "sp3d2-1", "sp3d2-2", "sp3d2-3", "sp3d2-4", "sp3d2-5", "sp3d2-6",
                 "l=2,mr=1,2,4", "f,mr=7"])
def test_angular_momentum(input_str: str) -> None:
    """Test the creation of an angular momentum object from various valid strings."""
    a = AngularMomentum.from_string(input_str)

    # For simple cases, check that `l` is correct
    if a.mᵣ is None and not input_str.startswith("l="):
        assert a.l == L[input_str]
        assert str(a) == input_str


def test_projections() -> None:
    """Test the creation of a Projections object."""
    proj = Projection(fractional_site=[0.5, 0.5, 0.5], ang_mtm="sp3")
    assert proj.fractional_site == [0.5, 0.5, 0.5]
    assert str(proj.ang_mtm) == "sp3"
    assert proj.z_axis == (0, 0, 1)  # Default value
    assert proj.x_axis == (1, 0, 0)  # Default value
    assert proj.radial == 1  # Default value

@pytest.mark.parametrize("proj_str", ["Cu:l=0", "c=0,0,0:l=1,mr=1:z=1,1,1", "Fe:dyz(u,d)[1,0,0]"])
def test_projection_from_string(proj_str: str) -> None:
    """Test the creation of a Projections object from various valid strings."""
    proj = Projection.from_string(proj_str)
    assert isinstance(proj, Projection)
