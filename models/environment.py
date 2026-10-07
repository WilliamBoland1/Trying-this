"""Environment: wind, wave and current loads on the vessel (body frame)."""
from pythonfmu import Fmi2Slave, Fmi2Causality, Fmi2Variability, Real


class Environment(Fmi2Slave):
    description = "Placeholder: outputs constant environmental forces set as parameters"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for name in ("force_x", "force_y", "moment_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.parameter,
                                        variability=Fmi2Variability.tunable))
        for name in ("tau_env_x", "tau_env_y", "tau_env_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.output))

    def do_step(self, current_time, step_size):
        # TODO: replace with real wind, wave and current models
        self.tau_env_x, self.tau_env_y, self.tau_env_n = self.force_x, self.force_y, self.moment_n
        return True
