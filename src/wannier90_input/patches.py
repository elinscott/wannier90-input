"""Additional information required to patch the xml file."""

fields = {
    "unit_cell_cart": 'list[Coordinate] = Field(description="Unit cell in cartesian coordinates", '
    "min_length=3, max_length=3)",
    "kpoints": 'list[FractionalCoordinate] = Field(default_factory=list, description="k-points in '
    'relative crystallographic units")',
    "atoms_cart": 'list[AtomCart] | None = Field(None, description="Positions of atoms in '
    'Cartesian coordinates")',
    "atoms_frac": 'list[AtomFrac] | None = Field(None, description="Positions of atoms in '
    'fractional coordinates")',
    "shell_list": 'list[int] = Field(default_factory=list, description="Which shells to use in '
    'finite difference formula")',
    "nnkpts": "list[NearestNeighborKpoint] = Field(default_factory=list, "
    'description="Explicit list of nearest-neighbour k-points")',
    "projections": 'list[Projection] = Field(default_factory=list, description="Projections for '
    'the Wannier functions")',
    "exclude_bands": 'list[int] = Field(default_factory=list, description="List of bands to '
    'exclude from the calculation")',
    "select_projections": 'list[int] = Field(default_factory=list, description="List of '
    'projections to use in Wannierisation")',
    "dis_spheres": 'list[DisentanglementSphere] = Field(default_factory=list, description="List of '
    'centres and radii, for disentanglement only in spheres")',
    "slwf_centres": 'list[CentreConstraint] = Field(default_factory=list, description="The centres '
    'to which the objective WFs are to be constrained")',
    "wannier_plot_list": 'list[int] = Field(default_factory=list, description="List of WF to '
    'plot")',
    "kpoint_path": "list[tuple[SpecialPoint, SpecialPoint]] = Field(default_factory=list, "
    'description="K-point path for the interpolated band structure")',
    "bands_plot_project": 'list[int] = Field(default_factory=list, description="WF to project the '
    'band structure onto")',
    "bands_plot_dim": 'Annotated[int, Field(ge=1, le=3)] = Field(3, description="Dimension of the '
    'system")',
    "translation_centre_frac": 'FractionalCoordinate | None = Field(None, description="Centre of '
    'the translation vector")',
}

types = {
    "mp_grid": "tuple[int, int, int]",
}

exclude = ["devel_flag"]
