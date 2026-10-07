"""DP controller: commanded force (body frame) from estimated state and setpoint."""
from pythonfmu import Fmi2Slave, Fmi2Causality, Real


class DPController(Fmi2Slave):
    description = "Placeholder: commanded force = estimated position"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for name in ("north_hat", "east_hat", "psi_hat", "u_hat", "v_hat", "r_hat",
                     "north_ref", "east_ref", "psi_ref"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.input))
        for name in ("tau_cmd_x", "tau_cmd_y", "tau_cmd_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.output))

    def do_step(self, current_time, step_size):
        # TODO: replace with a PD/PID law on the setpoint error
        self.tau_cmd_x, self.tau_cmd_y, self.tau_cmd_n = self.north_hat, self.east_hat, self.psi_hat
        return True
