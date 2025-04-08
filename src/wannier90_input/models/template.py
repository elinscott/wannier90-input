"""Base model for the input of different versions of `Wannier90`."""

from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import Self


class Wannier90InputTemplate(BaseModel):
    """Base model for the input of different versions of `Wannier90`."""

    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode='before')
    @classmethod
    def set_default_num_bands(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Set the default num_bands to num_wann if not provided."""
        if "num_bands" not in values:
            values["num_bands"] = values["num_wann"]
        return values

    @model_validator(mode='after')
    def atoms_frac_xor_cart(self) -> Self:
        """Ensure that either atoms_frac or atoms_cart is specified, but not both."""
        if getattr(self, 'atoms_frac', None) and getattr(self, 'atoms_cart', None):
            raise ValueError("Specify either atoms_frac or atoms_cart, not both.")
        if not getattr(self, 'atoms_frac', None) and not getattr(self, 'atoms_cart', None):
            raise ValueError("Specify either atoms_frac or atoms_cart.")
        return self

    @classmethod
    def from_str(cls, string: str) -> "Wannier90InputTemplate":
        """Convert a string to a Wannier90Input Model instance."""
        raise NotImplementedError()


    def __str__(self) -> str:
        """Return the model formatted as Wannier90 expects it."""
        # Iterate over the fields
        lines: list[str] = []
        for name, field in self.model_fields.items():
            # Only print non-default values
            if not field.is_required() and getattr(self, name, None) == field.default:
                continue

            if name in ['projections', 'unit_cell_cart', 'atoms_frac', 'atoms_cart', 'dis_spheres',
                        'shell_list', 'kpoints', 'nnkpts', 'select_projections', 'slwf_centres',
                        'wannier_plot_list', 'kpoint_path', 'bands_plot_project']:
                if name in ['unit_cell_cart']:
                    units = 'ang'
                else:
                    units = None
                if name in ['projections']:
                    to_remove = ''
                else:
                    to_remove = '[],'
                lines += _block_str(name, self, units, to_remove)
            elif name in ["mp_grid"]:
                lines += _list_keyword_str(name, self)
            elif name in ['exclude_bands']:
                lines += _list_keyword_str(name, self, join_with=',')
            else:
                lines += _keyword_str(name, self)

        return "\n".join(lines).replace("\n\n\n", "\n\n").strip('\n')


indent = ' '


def _sanitize(string: str, to_remove: str) -> str:
    for char in to_remove:
        string = string.replace(char, "")
    return string


def _block_str(name: str, model: BaseModel, units: str | None = None,
               to_remove: str = ',[]') -> list[str]:
    content = getattr(model, name)
    # Only print non-empty blocks
    if content == []:
        return []
    unit_list = [indent + units] if units else []

    return ["", f"begin {name}"] + unit_list + \
        [indent + _sanitize(str(x), to_remove) for x in content] + [f"end {name}", ""]


def _keyword_str(name: str, model: BaseModel) -> list[str]:
    return [f"{name} = {getattr(model, name)}"] if getattr(model, name) is not None else []


def _list_keyword_str(name: str, model: BaseModel, join_with: str = ' ') -> list[str]:
    value = getattr(model, name)
    if not isinstance(value, list | tuple):
        raise TypeError(f"Expected list or tuple for {name}, got {type(value)}")
    return [f"{name} = " + join_with.join([str(x) for x in value])] if value else []

