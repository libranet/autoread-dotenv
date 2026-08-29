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

## `AUTOREAD_DOTENV_QUIET`

Suppress every warning `autoread-dotenv` emits. When truthy, [`entrypoint()`](reference/index.md)
installs a process-wide `ignore` filter for the
[`AutoreadDotenvWarning`](reference/warnings.md) category before it does anything else.

- **Default:** `0` (false) - warnings are shown.
- **True values:** `1`, `true`, `yes` (case-insensitive).
- **False values:** `0`, `false`, `no`, `""` (empty).
- **Anything else:** treated as false, *and a warning is emitted* (typo guard) - so a
  misspelled value like `AUTOREAD_DOTENV_QUIET=ture` still warns once.
- **Read by:** [`entrypoint()`](reference/index.md), parsed via
  [`str_to_bool()`](reference/utils.md); the name lives in
  `autoread_dotenv.utils.AUTOREAD_DOTENV_QUIET_VAR`.

```bash
export AUTOREAD_DOTENV_QUIET=1
```

This is the blunt instrument: it hides the missing-`.env` notice together with the genuine
misconfiguration warnings (`python-dotenv` not installed, an unreadable `.env`, a typo'd
boolean elsewhere). Reach for it when the process legitimately runs without a `.env` and you
have accepted that trade-off; otherwise prefer removing the cause (see below).

## Silencing warnings

`autoread-dotenv` never raises for a configuration problem - it emits a warning and records
the reason in [`last_load_status`](reference/status.md). Every one of those warnings uses the
category [`AutoreadDotenvWarning`](reference/warnings.md) (a subclass of `UserWarning`),
re-exported as `autoread_dotenv.AutoreadDotenvWarning`.

### From Python (tests, programmatic callers)

Filter the category directly:

```python
import warnings
from autoread_dotenv import AutoreadDotenvWarning

warnings.filterwarnings("ignore", category=AutoreadDotenvWarning)
```

```toml
# pytest resolves the category itself, so the dotted path works here
[tool.pytest.ini_options]
filterwarnings = ["ignore::autoread_dotenv.warnings.AutoreadDotenvWarning"]
```

Note the timing: `entrypoint()` runs from `sitecustomize` at interpreter startup, *before* any
of your code. An in-process `filterwarnings()` call therefore only affects a later, manual
`entrypoint()` invocation - it cannot retroactively silence the startup pass. Use the options
in the next section for that.

### At startup

Set [`AUTOREAD_DOTENV_QUIET=1`](#autoread_dotenv_quiet). It is read at the very top of
`entrypoint()`, so it covers the startup pass that an in-process `filterwarnings()` call
misses:

```bash
export AUTOREAD_DOTENV_QUIET=1
```

`PYTHONWARNINGS` and `-W` are *not* an option here: they **cannot** name
`AutoreadDotenvWarning`. The interpreter parses warning filters before `site` puts
`site-packages` on `sys.path`, so a third-party category cannot be imported yet and the whole
filter is silently dropped (`Invalid -W option ignored: invalid module name:
'autoread_dotenv'`). Only built-in categories resolve there, so the closest `PYTHONWARNINGS`
equivalent is the much broader `ignore::UserWarning`.

### Better: remove the cause

The most common warning is the missing-`.env` notice. Rather than muting it, point the loader
at a file that exists - an empty `.env` is enough - or set `AUTOREAD_DOTENV_PATH`:

```bash
touch "$PWD/.env"
# or
export AUTOREAD_DOTENV_PATH=/etc/myapp/production.env
```

The remaining warnings (`python-dotenv` not installed, an unreadable `.env`, a typo'd boolean)
signal genuine misconfiguration and are worth leaving on.

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
