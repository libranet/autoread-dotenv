# Configuration

[TOC]

`autoread-dotenv` is configured through a small set of environment variables.

Because this package runs from `sitecustomize` on every interpreter startup and its job is to
*load* your `.env` file, the variables that control **how** and **whether** that load happens
cannot themselves be read from `.env` - by the time `.env` is parsed it is already too late,
and for the path variable it would be circular. Set these through your shell, service manager,
container runtime, CI configuration, or a tool like `direnv` instead.

None of the variables below have any effect when placed inside the `.env` file.

## `AUTOREAD_DOTENV_PATH`

Absolute path to the `.env` file to load. When set, it is used verbatim and the
`sys.prefix`-based discovery is skipped entirely.

- **Default:** unset - the file is discovered at `<project-root>/.env`, where `<project-root>`
  is `sys.prefix`, or its parent when `sys.prefix` ends in `.venv`.
- **Accepted values:** any filesystem path.
- **Read by:** [`get_expected_dotenv_path()`](reference/utils.md) (the name lives in
  `autoread_dotenv.utils.AUTOREAD_DOTENV_PATH_VAR`).

Use it for layouts that do not follow the in-project-virtualenv convention - global installs,
containers, editable mounts, and similar:

```bash
export AUTOREAD_DOTENV_PATH=/etc/myapp/production.env
```

The value is used as-is: no path-traversal check, no confinement to the project root. This is
deliberate - the variable is developer/operator-set configuration, not attacker-controlled
input. See [security.md](security.md) for the full threat model.

## `AUTOREAD_ENFORCE_DOTENV`

Whether values from `.env` override variables that are already present in the environment.
Maps directly to the `override=` argument of `python-dotenv`'s `load_dotenv()`.

- **Default:** `1` (true) - `.env` wins over pre-existing variables.
- **True values:** `1`, `true`, `yes` (case-insensitive).
- **False values:** `0`, `false`, `no`, `""` (empty).
- **Anything else:** treated as false, *and a warning is emitted* (typo guard).
- **Read by:** [`entrypoint()`](reference/index.md), parsed via
  [`str_to_bool()`](reference/utils.md).

Set it to `0` when the surrounding environment (CI secrets, systemd `Environment=`, container
`-e` flags, ...) should take precedence over the file:

```bash
export AUTOREAD_ENFORCE_DOTENV=0
```

## Silencing warnings

`autoread-dotenv` never raises for a configuration problem - it emits a warning and records
the reason in [`last_load_status`](reference/status.md). Every one of those warnings uses the
category [`autoread_dotenv.warnings.AutoreadDotenvWarning`](reference/warnings.md) (a subclass
of `UserWarning`), so you can suppress *only* this package without muting unrelated
`UserWarning`s from the rest of your app:

```bash
# environment (before the interpreter starts, like the variables above)
export PYTHONWARNINGS="ignore::autoread_dotenv.warnings.AutoreadDotenvWarning"

# one-off invocation
python -W "ignore::autoread_dotenv.warnings.AutoreadDotenvWarning" -m myapp
```

```python
# from code, before autoread_dotenv.entrypoint() runs
import warnings
from autoread_dotenv.warnings import AutoreadDotenvWarning

warnings.filterwarnings("ignore", category=AutoreadDotenvWarning)
```

```toml
# pytest
[tool.pytest.ini_options]
filterwarnings = ["ignore::autoread_dotenv.warnings.AutoreadDotenvWarning"]
```

This is all-or-nothing: it silences the missing-`.env` notice together with the genuine
misconfiguration warnings (`python-dotenv` not installed, an unreadable `.env`, a typo'd
boolean). Prefer narrowing by message with `warnings.filterwarnings(..., message=...)` if you
only want to hide one of them.

## Setting variables outside `.env`

Any mechanism that populates the environment *before* the Python process starts works:

```bash
# interactive shell / ~/.bashrc / ~/.zshenv
export AUTOREAD_DOTENV_PATH=/etc/myapp/production.env

# one-off invocation
AUTOREAD_ENFORCE_DOTENV=0 python -m myapp
```

```ini
# systemd unit
[Service]
Environment=AUTOREAD_ENFORCE_DOTENV=0
```

```dockerfile
# Dockerfile
ENV AUTOREAD_ENFORCE_DOTENV=0
# ... or at runtime:  docker run -e AUTOREAD_ENFORCE_DOTENV=0 myimage
```

## Related behaviour

- **Interpolation.** `autoread-dotenv` calls `load_dotenv(..., interpolate=True)`, so values in
  `.env` may reference other variables with `${OTHER_VAR}`. If `OTHER_VAR` is not defined in
  `.env`, it is resolved from the surrounding environment - another way the outside environment
  feeds into the loaded values.
- **Interpreter-level variables.** `PYTHONPATH`, `PYTHONWARNINGS`, and the other
  `PYTHON*`/interpreter variables must be set before the interpreter starts. `sitecustomize`
  (and therefore `autoread-dotenv`) runs too late to apply them, regardless of whether they are
  in `.env`. See the notes at the top of `.env.template`.
- **Querying the outcome.** After startup, `autoread_dotenv.last_load_status` (a
  [`LoadStatus`](reference/status.md)) reports what happened. It is not configuration, but it is
  the companion to the variables above when debugging a load.
