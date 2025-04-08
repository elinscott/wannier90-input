"""Additional information required to patch the xml file."""

fields = {
    "unit_cell_cart": 'list[Coordinate] = Field(description="Unit cell in cartesian coordinates", '
    'min_length=3, max_length=3)',
    "kpoints": 'list[FractionalCoordinate] = Field(default_factory=list, description="k-points in '
    'relative crystallographic units")',
    "atoms_cart": 'list[AtomCart] | None = Field(None, description="Positions of atoms in '
    'Cartesian coordinates")',
    "atoms_frac": 'list[AtomFrac] | None = Field(None, description="Positions of atoms in '
    'fractional coordinates")',
    "shell_list": 'list[int] = Field(default_factory=list, description="Which shells to use in '
    'finite difference formula")',
    "nnkpts": 'list[NearestNeighborKpoint] = Field(default_factory=list, '
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
    "kpoint_path": 'list[tuple[SpecialPoint, SpecialPoint]] = Field(default_factory=list, '
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

allow_none = ["dis_win_min", "dis_win_max", "dis_froz_min", "dis_froz_max",
              "fermi_energy_min", "fermi_energy_max", "one_dim_axis", "kpoints",
              "slwf_num"]

exclude = ["devel_flag"]

defaults = {
    "num_bands": -1,  # This will be overwritten by the validator
    "gamma_only": False,
    "spinors": False,
    "search_shells": 36,
    "skip_B1_tests": False,
    "kmesh_tol": 1e-6,
    "higher_order_n": 1,
    "postproc_setup": False,
    "auto_projections": False,
    "translate_home_cell": False,
    "write_xyz": False,
    "write_vdw_data": False,
    "write_hr_diag": False,
    "num_iter": 100,
    "num_cg_steps": 5,
    "conv_window": 3,
    "conv_tol": 1e-10,
    "precond": False,
    "conv_noise_amp": -1.0,
    "conv_noise_num": 3,
    "num_dump_cycles": 100,
    "num_print_cycles": 1,
    "write_r2mn": False,
    "num_guide_cycles": 1,
    "num_no_guide_iter": 0,
    "trial_step": 2.0,
    "fixed_step": -999.0,
    "symmetrize_eps": 1e-3,
    "wannier_plot": False,
    "bands_plot": False,
    "fermi_surface_plot": False,
    "write_hr": False,
    "write_rmn": False,
    "write_bvec": False,
    "write_tb": False,
    "hr_cutoff": 0.0,
    "dist_cutoff": 1000.0,
    "dist_cutoff_mode": 'three_dim',
    "write_u_matrices": False,
    "transport": False,
    "higher_order_nearest_shells": False,
    "restart": "default",
    "iprint": 1,
    "wvfn_formatted": False,
    "timing_level": 1,
    "optimisation": 3,
    "dis_froz_proj": False,
    "dis_proj_min": 0.01,
    "dis_proj_max": 0.95,
    "dis_num_iter": 200,
    "dis_mix_ratio": 0.5,
    "dis_conv_tol": 1e-10,
    "dis_conv_window": 3,
    "dis_spheres_num": 0,
    "dis_spheres_first_wann": 1,
    "guiding_centres": False,
    "use_bloch_phases": False,
    "site_symmetry": False,
    "slwf_constrain": False,
    "slwf_lambda": 0.0,
    "wannier_plot_supercell": 2,
    "wannier_plot_radius": 3.5,
    "wannier_plot_scale": 1.0,
    "wannier_plot_spinor_phase": True,
    "bands_num_points": 100,
    "fermi_surface_num_points": 50,
    "fermi_energy": 0.0,
    "fermi_energy_step": 0.01,
    "hr_plot": False,
    "use_ws_distance": True,
    "ws_distance_tol": 1e-5,
    "ws_search_size": 2,
    "tran_win_min": -3.0,
    "tran_win_max": 3.0,
    "tran_energy_step": 0.01,
    "tran_num_bb": 0,
    "tran_num_ll": 0,
    "tran_num_rr": 0,
    "tran_num_cc": 0,
    "tran_num_lc": 0,
    "tran_num_cr": 0,
    "tran_num_cell_ll": 0,
    "tran_num_cell_rr": 0,
    "tran_num_bandc": 0,
    "tran_write_ht": False,
    "tran_read_ht": False,
    "tran_use_same_lead": False,
    "tran_group_threshold": 0.15}
