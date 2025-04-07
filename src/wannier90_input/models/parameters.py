import textwrap
from typing import Annotated

from pydantic import BaseModel, Field, model_validator

Fraction = Annotated[float, Field(ge=0.0, le=1.0)]
FractionalCoordinate = Annotated[list[Fraction], Field(min_length=3, max_length=3)]
Coordinate = Annotated[list[float], Field(min_length=3, max_length=3)]


class AtomFrac(BaseModel):
    """One entry in the Wannier90 atoms_frac input parameter."""

    symbol: str = Field(..., description="Atomic symbol")
    position: FractionalCoordinate = Field(..., description="Fractional coordinates of the atom")

    def __str__(self) -> str:
        return f"{self.symbol} {' '.join(map(str, self.position))}"


class AtomCart(BaseModel):
    """One entry in the Wannier90 atoms_cart input parameter."""

    symbol: str = Field(..., description="Atomic symbol")
    position: Coordinate = Field(..., description="Cartesian coordinates of the atom")

    def __str__(self) -> str:
        return f"{self.symbol} {' '.join(map(str, self.position))}"


class DisentanglementSphere(BaseModel):
    """Wannier90 dis_spheres input parameter."""

    center: FractionalCoordinate = Field(...,
                                         description="Center of the sphere (in crystallographic coordinates)")
    radius: float = Field(..., description="Radius of the sphere (inverse Angstrom)")

    def __str__(self):
        return f"{','.join(map(str, self.center))} {self.radius}"


class CentreConstraint(BaseModel):
    """Wannier90 slwf_centres input parameter."""

    number: int = Field(..., description="Wannier function index")
    center: FractionalCoordinate = Field(
        ..., description="Centre on which to constrain the Wannier function (fractional coordinates)")

    def __str__(self):
        return f"{self.number} {','.join(map(str, self.center))}"


class SpecialPoint(BaseModel):
    """Wannier90 kpoint_path input parameter."""

    name: str = Field(..., description="Name of the special point")
    coordinates: FractionalCoordinate = Field(
        ..., description="Coordinates of the special point (fractional coordinates)")

    def __str__(self):
        return f"{self.name} {','.join(map(str, self.coordinates))}"


class Projection(BaseModel):
    fractional_site: FractionalCoordinate | None = Field(
        None, description="Site of the projection (fractional coordinates)")
    cartesian_site: Coordinate | None = Field(
        None, description="Cartesian coordinates of the projection")
    site: str | None = Field(None, description="Site of the projection (by atom label)")
    ang_mtm: str = Field(..., description="Angular momentum of the projection")
    zaxis: tuple[int, int, int] = Field((0, 0, 1), description="z-axis for the projection")
    xaxis: tuple[int, int, int] = Field((1, 0, 0), description="x-axis for the projection")
    radial: int = Field(1, description="Radial component of the projection")
    zona: float = Field(
        1.0, description="the value of Z/a for the radial part of the atomic orbital")

    @model_validator(mode="before")
    def check_mutual_exclusivity(cls, values):
        fractional_site = values.get('fractional_site')
        cartesian_site = values.get('cartesian_site')
        site = values.get('site')
        provided_fields = [field for field in [
            fractional_site, cartesian_site, site] if field is not None]
        if len(provided_fields) > 1:
            raise ValueError(
                "Only one of 'fractional_site', 'cartesian_site', or 'site' can be provided.")
        if len(provided_fields) == 0:
            raise ValueError(
                "At least one of 'fractional_site', 'cartesian_site', or 'site' must be provided.")
        return values

    def __str__(self):
        if self.fractional_site is not None:
            site_str = 'f=' + ','.join([str(x) for x in self.fractional_site])
        elif self.cartesian_site is not None:
            site_str = 'c=' + ','.join([str(x) for x in self.cartesian_site])
        else:
            site_str = self.site
        return f"{site_str}:{self.ang_mtm}:[{','.join([str(x) for x in self.zaxis])}]:[{','.join([str(x) for x in self.xaxis])}]:{self.radial}:{self.zona}"


parameter_models: list[type[BaseModel]] = [
    AtomFrac,
    AtomCart,
    Projection,
    DisentanglementSphere,
    CentreConstraint,
    SpecialPoint,
    Projection
]

other_imports = [
    "Coordinate",
    "FractionalCoordinate",
]


import_parameter_models = "\n".join(textwrap.wrap(
    "from wannier90_input.models.parameters import (" + ", ".join(
        [model.__name__ for model in parameter_models] + other_imports) + ")",
    width=120, subsequent_indent="    "))
