"""Hull: 3-DOF vessel motion. Position in NED, velocity in the body frame."""
from pythonfmu import Fmi2Slave, Fmi2Causality, Fmi2Variability, Real


class Hull(Fmi2Slave):
    description = "Placeholder: copies the environment force to the position outputs"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for name in ("mass", "inertia_z"):  # values come from config.py
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.parameter,
                                        variability=Fmi2Variability.tunable))
        for name in ("tau_env_x", "tau_env_y", "tau_env_n",
                     "tau_thr_x", "tau_thr_y", "tau_thr_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.input))
        for name in ("north", "east", "psi", "u", "v", "r"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.output))

    def do_step(self, current_time, step_size):
        # TODO: replace with 3-DOF dynamics driven by tau_env + tau_thr.
        # For now the position outputs only trace the environment signal, and
        # tau_thr is ignored so the feedback loop cannot add up.
        self.north, self.east, self.psi = self.tau_env_x, self.tau_env_y, self.tau_env_n
        self.u = self.v = self.r = 0.0
        return True
