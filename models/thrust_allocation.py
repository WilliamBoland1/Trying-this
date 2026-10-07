"""Thrust allocation (thruster controller): distributes the commanded force over the thrusters."""
from pythonfmu import Fmi2Slave, Fmi2Causality, Real


class ThrustAllocation(Fmi2Slave):
    description = "Placeholder: passes the commanded force through"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for name in ("tau_cmd_x", "tau_cmd_y", "tau_cmd_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.input))
        for name in ("tau_alloc_x", "tau_alloc_y", "tau_alloc_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.output))

    def do_step(self, current_time, step_size):
        # TODO: replace with the real allocation
        self.tau_alloc_x, self.tau_alloc_y, self.tau_alloc_n = self.tau_cmd_x, self.tau_cmd_y, self.tau_cmd_n
        return True
