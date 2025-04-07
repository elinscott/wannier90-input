from wannier90_input.models import Wannier90Input

def test_wannier90_input():
    inp = Wannier90Input(num_wann=10, num_bands=20)
    assert inp.num_wann == 10
    assert inp.num_bands == 20
