"""Custom __str__ method for the Wannier90Input class."""

from __future__ import annotations


def custom_str(model: Wannier90Input) -> str:
    """Return the model formatted as Wannier90 expects it"""
    # Iterate over the fields
    lines: list[str] = []
    for name, field in model.model_fields.items():
        # Only print non-default values
        if not field.is_required() and getattr(model, name, None) == field.default:
            continue

        if name in ['projections', 'unit_cell_cart', 'atoms_frac', 'atoms_cart', 'dis_spheres',
                    'shell_list', 'kpoints', 'nnkpts', 'select_projections', 'slwf_centres', 'wannier_plot_list',
                    'kpoint_path', 'bands_plot_project']:
            if name in ['unit_cell_cart']:
                units = 'ang'
            else:
                units = None
            if name in ['projections']:
                to_remove = ''
            else:
                to_remove = '[],'
            lines += _block_str(name, model, units, to_remove)
        elif name in ["mp_grid"]:
            lines += _list_keyword_str(name, model)
        elif name in ['exclude_bands']:
            lines += _list_keyword_str(name, model, join_with=',')
        else:
            lines += _keyword_str(name, model)

    return "\n".join(lines).replace("\n\n\n","\n\n").strip('\n')


indent = ' '

def _sanitize(string: str, to_remove: str):
    for char in to_remove:
        string = string.replace(char, "")
    return string

def _block_str(name: str, model: Wannier90Input, units: str | None = None, to_remove=',[]') -> list[str]:
    content = getattr(model, name)
    if content == []:
        return []
    unit_list = [indent + units] if units else []

    return ["", f"begin {name}"] + unit_list + [indent + _sanitize(str(x), to_remove) for x in content] + [f"end {name}", ""]

def _keyword_str(name: str, model: Wannier90Input) -> list[str]:
    return [f"{name} = {getattr(model, name)}"] if getattr(model, name) is not None else []

def _list_keyword_str(name: str, model: Wannier90Input, join_with: str = ' ') -> list[str]:
    value = getattr(model, name)
    assert isinstance(value, (list, tuple))
    return [f"{name} = " + join_with.join([str(x) for x in value])] if value else []
