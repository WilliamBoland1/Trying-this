# DP vessel co-simulation

Simulates a ship that holds its position with thrusters (dynamic positioning, DP). Each part of the ship is its own FMU, and the parts are connected in a loop:

```
environment -> hull -> kalman_filter -> dp_controller -> thrust_allocation -> thruster_dynamics -> hull
```

For now every part is a placeholder that passes its input straight on. A test force from `environment` travels around the whole loop, which proves every connection works.

## Get started

Needs Python 3.11. Commands are for Windows PowerShell, run from this folder.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe build_fmus.py       # creates fmus/
.\.venv\Scripts\python.exe run_simulation.py   # creates results/, ends with "All 24 signals OK"
```

`fmus/` and `results/` are not in git. The two scripts above create them.

## Files

| File | What it does |
|---|---|
| `models/` | One Python class per part. Its `do_step` is the logic. |
| `build_fmus.py` | Turns each model into an FMU. |
| `OspSystemStructure.xml` | Which output feeds which input, and the step size (0.1 s). |
| `config.py` | Run length and every parameter value. |
| `run_simulation.py` | Runs it, saves CSVs and `trace.png` to `results/`, and checks the loop. |

## Changing things

- **A value:** edit `config.py` and run again.
- **A part's logic:** edit `models/<part>.py`, then run `build_fmus.py` and run again.
- **A new input, output or parameter:** rebuild, then wire it in the XML (inputs/outputs) or add it to `config.py` (parameters).

## Good to know

- Each connection adds one step (0.1 s) of delay.
- The FMUs run on this venv's Python, so packages a model imports must be installed there.
- SI units. Position is in NED. Forces are in the body frame (x forward, y starboard, N bow to starboard).
