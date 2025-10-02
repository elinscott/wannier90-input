"""Pydantic models for various `Wannier90` input parameters."""

import textwrap
from enum import Enum
from typing import Annotated, Any, Literal

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

    center: FractionalCoordinate = Field(
        ..., description="Center of the sphere (in crystallographic coordinates)"
    )
    radius: float = Field(..., description="Radius of the sphere (inverse Angstrom)")

    def __str__(self) -> str:
        return f"{','.join(map(str, self.center))} {self.radius}"


class CentreConstraint(BaseModel):
    """Wannier90 slwf_centres input parameter."""

    number: int = Field(..., description="Wannier function index")
    center: FractionalCoordinate = Field(
        ...,
        description="Centre on which to constrain the Wannier function (fractional coordinates)",
    )

    def __str__(self) -> str:
        return f"{self.number} {','.join(map(str, self.center))}"


class SpecialPoint(BaseModel):
    """Wannier90 kpoint_path input parameter."""

    name: str = Field(..., description="Name of the special point")
    coordinates: FractionalCoordinate = Field(
        ..., description="Coordinates of the special point (fractional coordinates)"
    )

    def __str__(self) -> str:
        return f"{self.name} {','.join(map(str, self.coordinates))}"


class NearestNeighborKpoint(BaseModel):
    """Wannier90 nnkpts input parameter."""

    kpoint_number: int
    neighbor_kpoint_number: int
    reciprocal_lattice_vector: Annotated[list[int], Field(min_length=3, max_length=3)]

    def __str__(self) -> str:
        return (
            f"{self.kpoint_number} {self.neighbor_kpoint_number} "
            f"{' '.join(map(str, self.reciprocal_lattice_vector))}"
        )


class AngularMomentum(Enum):
    """Angular momentum options for Wannier90 projections."""

    s = 0
    p = 1
    d = 2
    f = 3
    sp = -1
    sp2 = -2
    sp3 = -3
    sp3d = -4
    sp3d2 = -5


labels_to_mr: dict[str, tuple[int, int | None]] = {
    "s": (0, None),
    "p": (1, None),
    "pz": (1, 1),
    "px": (1, 2),
    "py": (1, 3),
    "d": (2, None),
    "dz2": (2, 1),
    "dxz": (2, 2),
    "dyz": (2, 3),
    "dx2-y2": (2, 4),
    "dxy": (2, 5),
    "f": (3, None),
    "fz3": (3, 1),
    "fxz2": (3, 2),
    "fyz2": (3, 3),
    "fz(x2-y2)": (3, 4),
    "fxyz": (3, 5),
    "fx(x2-3y2)": (3, 6),
    "fy(3x2-y2)": (3, 7),
    "sp": (-1, None),
    "sp-1": (-1, 1),
    "sp-2": (-1, 2),
    "sp2": (-2, None),
    "sp2-1": (-2, 1),
    "sp2-2": (-2, 2),
    "sp2-3": (-2, 3),
    "sp3": (-3, None),
    "sp3-1": (-3, 1),
    "sp3-2": (-3, 2),
    "sp3-3": (-3, 3),
    "sp3-4": (-3, 4),
    "sp3d": (-4, None),
    "sp3d-1": (-4, 1),
    "sp3d-2": (-4, 2),
    "sp3d-3": (-4, 3),
    "sp3d-4": (-4, 4),
    "sp3d-5": (-4, 5),
    "sp3d2": (-5, None),
    "sp3d2-1": (-5, 1),
    "sp3d2-2": (-5, 2),
    "sp3d2-3": (-5, 3),
    "sp3d2-4": (-5, 4),
    "sp3d2-5": (-5, 5),
    "sp3d2-6": (-5, 6),
}


class QuantumNumbers(BaseModel):
    """BaseModel that represents the `ang_mtm` information in Wannier90 projections."""

    angular: AngularMomentum = Field(
        ..., description="Angular momentum quantum number of the projection"
    )
    mᵣ: list[int] | None = Field(None, description="Magnetic quantum numbers of the projection")
    model_config = {"frozen": True}

    @model_validator(mode="after")
    def check_l_mᵣ_consistency(self) -> "QuantumNumbers":
        """Check that the provided mᵣ values are consistent with the angular momentum."""
        if self.mᵣ is None:
            return self
        if self.angular.value >= 0:
            # Atomic orbitals
            for mᵣ in self.mᵣ:
                if mᵣ <= 0 or mᵣ > 2 * self.angular.value + 1:
                    raise ValueError(
                        f"Invalid mᵣ={mᵣ} for l={self.angular.value}. Must have 0 < mᵣ <= 2l + 1."
                    )
        else:
            # Hybrid orbitals
            for mᵣ in self.mᵣ:
                if mᵣ <= 0 or mᵣ > -1 * self.angular.value + 1:
                    raise ValueError(
                        f"Invalid mᵣ={mᵣ} for l={self.angular.value}. "
                        "Must have 0 < mᵣ <= {-1 * self.angular.value + 1}"
                    )
        return self

    def __str__(self) -> str:
        if self.mᵣ is None:
            return self.angular.name.lower()
        else:
            return f"{self.angular.name.lower()},mr=" + ",".join([str(x) for x in self.mᵣ])

    @classmethod
    def from_string(cls, ang_mtm: str) -> "QuantumNumbers":
        """Create a QuantumNumbers object from a Wannier90 ang_mtm input string."""
        if ";" in ang_mtm:
            raise ValueError(
                "Multiple angular momenta channels in one line is not supported."
                " Please provide them as separate lines."
            )

        if ang_mtm in labels_to_mr:
            # Any of the predefined labels e.g. "s", "pz", "sp3d2-1", etc.
            l_int, mr = labels_to_mr[ang_mtm]
            return cls(angular=AngularMomentum(l_int), mᵣ=[mr] if mr is not None else None)
        elif "," in ang_mtm:
            # e.g. "l=0,mr=..."
            l_str, mr_str = ang_mtm.split(",", 1)
            mrs = [int(s) for s in mr_str[3:].split(",")]
        elif ang_mtm.startswith("l="):
            # e.g. "l=0"
            l_str = ang_mtm
            mrs = None
        else:
            raise ValueError("Invalid angular momentum string format.")

        if l_str.startswith("l="):
            l_obj = AngularMomentum(int(l_str[2:]))
        else:
            l_obj = AngularMomentum[l_str]
        return cls(angular=l_obj, mᵣ=mrs)

    def number_of_orbitals(self) -> int:
        """Return the number of orbitals within this projection."""
        if self.mᵣ is None:
            if self.angular.value >= 0:
                return 2 * self.angular.value + 1
            else:
                return -1 * self.angular.value + 1
        else:
            return len(self.mᵣ)


class Projection(BaseModel):
    """Wannier90 projections input parameter."""

    fractional_site: FractionalCoordinate | None = Field(
        None, description="Site of the projection (fractional coordinates)"
    )
    cartesian_site: Coordinate | None = Field(
        None, description="Cartesian coordinates of the projection"
    )
    site: str | None = Field(None, description="Site of the projection (by atom label)")
    ang_mtm: QuantumNumbers = Field(..., description="Angular momentum of the projection")
    z_axis: tuple[int, int, int] = Field((0, 0, 1), description="z-axis for the projection")
    x_axis: tuple[int, int, int] = Field((1, 0, 0), description="x-axis for the projection")
    radial: int = Field(1, description="Radial component of the projection")
    z_on_a: float = Field(
        1.0, description="the value of Z/a for the radial part of the atomic orbital"
    )
    spin: Literal["u", "d", "u,d", None] = Field(
        None, description="Optional projection onto spin channels for non-collinear calculations"
    )
    quant_dir: tuple[int, int, int] | None = Field(
        None, description="Quantization axis for non-collinear calculations"
    )

    @model_validator(mode="before")
    @classmethod
    def check_mutual_exclusivity(cls, values: dict[str, str | None]) -> dict[str, str | None]:
        """Check that only one of the site fields is provided."""
        fractional_site = values.get("fractional_site")
        cartesian_site = values.get("cartesian_site")
        site = values.get("site")
        provided_fields = [
            field for field in [fractional_site, cartesian_site, site] if field is not None
        ]
        if len(provided_fields) > 1:
            raise ValueError(
                "Only one of 'fractional_site', 'cartesian_site', or 'site' can be provided."
            )
        if len(provided_fields) == 0:
            raise ValueError(
                "At least one of 'fractional_site', 'cartesian_site', or 'site' must be provided."
            )
        return values

    @model_validator(mode="before")
    @classmethod
    def allow_string_ang_mtm(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Allow ang_mtm to be provided as a string."""
        ang_mtm = values.get("ang_mtm")
        if isinstance(ang_mtm, str):
            values["ang_mtm"] = QuantumNumbers.from_string(ang_mtm)
        return values

    @classmethod
    def from_string(cls, proj_str: str) -> "Projection":
        """Create a Projection object from a string."""
        if proj_str.startswith("c="):
            site_arg = "cartesian_site"
        elif proj_str.startswith("f="):
            site_arg = "fractional_site"
        else:
            site_arg = "site"

        # Dealing with non-":"-separated arguments associated with non-collinear calculations
        kwargs: dict[str, Any] = {}
        if proj_str.endswith("]"):
            proj_str, quant_dir_str = proj_str.rsplit("[", 1)
            kwargs["quant_dir"] = quant_dir_str[:-1].split(",")
        if proj_str.endswith(")"):
            proj_str, spin_str = proj_str.rsplit("(", 1)
            kwargs["spin"] = spin_str[:-1]

        for key, value in zip(
            [site_arg, "ang_mtm", "z_axis", "x_axis", "radial", "z_on_a"],
            proj_str.split(":"),
            strict=False,
        ):
            if key != "ang_mtm":
                if "=" in value:
                    _, value = value.split("=", 1)
                if "," in value:
                    value = value.split(",")  # type: ignore
            kwargs[key] = value

        return cls(**kwargs)

    def __str__(self) -> str:
        if self.fractional_site is not None:
            site_str = "f=" + ",".join([str(x) for x in self.fractional_site])
        elif self.cartesian_site is not None:
            site_str = "c=" + ",".join([str(x) for x in self.cartesian_site])
        elif self.site is not None:
            site_str = self.site
        else:
            raise ValueError(
                "No site information found. This should have been prevented by the validator..."
            )

        content = (
            f"{site_str}:{self.ang_mtm}:[{','.join([str(x) for x in self.z_axis])}]:["
            + f"{','.join([str(x) for x in self.x_axis])}]:{self.radial}:{self.z_on_a}"
        )

        if self.spin is not None:
            content += f"({self.spin})"
        if self.quant_dir is not None:
            content += f"[{','.join(map(str, self.quant_dir))}]"

        return content


parameter_models: list[type[BaseModel]] = [
    AtomFrac,
    AtomCart,
    Projection,
    DisentanglementSphere,
    CentreConstraint,
    SpecialPoint,
    Projection,
    NearestNeighborKpoint,
]

other_imports = [
    "Coordinate",
    "FractionalCoordinate",
]


import_parameter_models = "\n".join(
    textwrap.wrap(
        "from wannier90_input.models.parameters import ("
        + ", ".join([model.__name__ for model in parameter_models] + other_imports)
        + ")",
        width=120,
        subsequent_indent="    ",
    )
)
