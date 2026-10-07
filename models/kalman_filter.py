"""Kalman filter: estimates position and velocity from measured position and applied thrust."""
from pythonfmu import Fmi2Slave, Fmi2Causality, Real


class KalmanFilter(Fmi2Slave):
    description = "Placeholder: estimated position = measured position, estimated velocity = 0"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for name in ("north_meas", "east_meas", "psi_meas",
                     "tau_thr_x", "tau_thr_y", "tau_thr_n"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.input))
        for name in ("north_hat", "east_hat", "psi_hat", "u_hat", "v_hat", "r_hat"):
            setattr(self, name, 0.0)
            self.register_variable(Real(name, causality=Fmi2Causality.output))

    def do_step(self, current_time, step_size):
        # TODO: replace with a Kalman filter (tau_thr feeds the prediction step)
        self.north_hat, self.east_hat, self.psi_hat = self.north_meas, self.east_meas, self.psi_meas
        self.u_hat = self.v_hat = self.r_hat = 0.0
        return True
