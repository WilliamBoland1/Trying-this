"""Values for one run. run_simulation.py sets them on the FMUs, so changes need no rebuild."""
DURATION = 10.0  # [s]

PARAMETERS = {  # {simulator in OspSystemStructure.xml: {FMU parameter: value}}
    "environment": {"force_x": 1.0, "force_y": 2.0, "moment_n": 3.0},     # test force [N, N, Nm]
    "hull": {"mass": 6.0e6, "inertia_z": 2.0e9},                           # [kg, kg m^2]
    "dp_controller": {"north_ref": 0.0, "east_ref": 0.0, "psi_ref": 0.0},  # setpoint [m, m, rad]
    "thruster_dynamics": {"time_constant": 2.0},                           # [s]
}
