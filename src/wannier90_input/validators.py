
def set_default_num_bands(values):
    if "num_bands" not in values:
        values["num_bands"] = values["num_wann"]
    return values

def set_default_slwf_num(values):
    if "slwf_num" not in values:
        values["slwf_num"] = values["num_wann"]
    return values

def atoms_frac_xor_cart(cls, values):
    if values.atoms_frac and values.atoms_cart:
        raise ValueError("Specify either atoms_frac or atoms_cart, not both.")
    if not values.atoms_frac and not values.atoms_cart:
        raise ValueError("Specify either atoms_frac or atoms_cart.")
    return values

before_validators = [set_default_num_bands, set_default_slwf_num]

after_validators = [atoms_frac_xor_cart]
