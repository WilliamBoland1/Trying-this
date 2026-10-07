"""Run OspSystemStructure.xml with config.py, then check the test force made it around the loop.

Run with:  .\\.venv\\Scripts\\python.exe run_simulation.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from libcosimpy.CosimEnums import CosimVariableCausality
from libcosimpy.CosimExecution import CosimExecution
from libcosimpy.CosimLogging import CosimLogLevel, log_output_level
from libcosimpy.CosimObserver import CosimObserver

import config

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"

# Each box's x, y, n signals in loop order. The placeholders only copy, so all should end at the test force.
LOOP = [
    ("environment", "tau_env_x tau_env_y tau_env_n"),
    ("hull", "north east psi"),
    ("kalman_filter", "north_hat east_hat psi_hat"),
    ("dp_controller", "tau_cmd_x tau_cmd_y tau_cmd_n"),
    ("thrust_allocation", "tau_alloc_x tau_alloc_y tau_alloc_n"),
    ("thruster_dynamics", "tau_thr_x tau_thr_y tau_thr_n"),
    ("hull", "tau_thr_x tau_thr_y tau_thr_n"),           # back at the hull: loop closed
    ("kalman_filter", "tau_thr_x tau_thr_y tau_thr_n"),  # side branch
]


def simulate():
    RESULTS.mkdir(exist_ok=True)
    for old in [*RESULTS.glob("*.csv"), *RESULTS.glob("*.yaml")]:
        old.unlink()

    log_output_level(CosimLogLevel.WARNING)  # the default level prints every FMI call
    execution = CosimExecution.from_osp_config_file(osp_path=str(ROOT / "OspSystemStructure.xml"))

    variables = {(info.name.decode(), v.name.decode()): (info.index, v)
                 for info in execution.slave_infos() for v in execution.slave_variables(info.index)}
    for sim, values in config.PARAMETERS.items():
        for name, value in values.items():
            index, var = variables[sim, name]  # KeyError = typo in config.py
            execution.real_initial_value(index, var.reference, float(value))
    missing = [f"{sim}.{name}" for (sim, name), (_, var) in variables.items()
               if var.causality == CosimVariableCausality.PARAMETER.value and name not in config.PARAMETERS.get(sim, {})]
    if missing:
        raise SystemExit(f"Set these in config.py: {', '.join(missing)}")

    execution.add_observer(observer=CosimObserver.create_to_dir(log_dir=str(RESULTS)))  # one CSV per simulator
    if not execution.simulate_until(target_time=int(config.DURATION * 1e9)):  # libcosim time is in nanoseconds
        raise RuntimeError("simulation failed, see the libcosim log above")


if __name__ == "__main__":
    simulate()
    logs = {sim: pd.read_csv(next(RESULTS.glob(f"{sim}_*.csv")), index_col="Time") for sim, _ in LOOP}
    signals = pd.DataFrame({f"{sim}.{var}": logs[sim][var] for sim, names in LOOP for var in names.split()})

    x = signals.iloc[:, ::3]  # the x-channel of each box
    print(x.head(10).to_string())
    x.loc[:1.0].plot(subplots=True, drawstyle="steps-post", figsize=(7, 10), title="force_x travelling around the loop")
    plt.savefig(RESULTS / "trace.png", dpi=150)

    want = list(config.PARAMETERS["environment"].values()) * len(LOOP)
    bad = [f"{name} = {got}, expected {w}" for (name, got), w in zip(signals.iloc[-1].items(), want) if got != w]
    print("\nNOT connected:\n  " + "\n  ".join(bad) if bad else f"\nAll {len(want)} signals OK")
    raise SystemExit(1 if bad else 0)
