"""Thruster dynamics: the force the thrusters actually deliver on the hull."""
from pythonfmu import Fmi2Slave, Fmi2Causality, Fmi2Variability, Real


class ThrusterDynamics(Fmi2Slave):
    description = "Placeholder: delivered force = allocated force"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_constant = 0.0  # value comes from config.py
        self.register_variable(Real("time_constant", causality=Fmi2Causality.parameter,
                                    variability=Fmi2Variability.tunable))
        for name in ("tau_alloc_x", "tau_alloc_y", "tau_alloc_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.input))
        for name in ("tau_thr_x", "tau_thr_y", "tau_thr_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.output))

    def do_step(self, current_time, step_size):
        # TODO: replace with thrust lag and azimuth rate limits
        self.tau_thr_x, self.tau_thr_y, self.tau_thr_n = self.tau_alloc_x, self.tau_alloc_y, self.tau_alloc_n
        return True
