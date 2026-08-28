# Security Policy

## Supported Versions

Only the latest released version receives security updates.

| Version | Supported |
| ------- | --------- |
| 1.0.x   | Yes       |
| 0.x     | No        |

## Reporting a Vulnerability

This project follows a 90 day disclosure timeline.

Please report security issues privately, through either channel:

- GitHub's [private vulnerability reporting](https://github.com/libranet/autoread-dotenv/security/advisories/new)
  (Security tab -> Report a vulnerability), or
- email to <security@libranet.eu>.

Include:

- a description of the issue
- the steps you took to create the issue,
- affected versions
- and if known, mitigations for the issue

Our team will acknowledge your report within 3 working days, keep you updated on
progress, and credit you in the advisory unless you prefer to stay anonymous.

Please do not open a public issue or pull request for a suspected vulnerability.

## Threat model

`autoread-dotenv` runs from `sitecustomize` on every interpreter startup and reads a
`.env` file into the process environment. Its inputs are treated as **developer-controlled
configuration, not attacker-controlled input**:

- **`AUTOREAD_DOTENV_PATH`** is used verbatim as the path to the `.env` file, with no
  sanitisation, traversal checks or confinement to the project root. This is by design: the
  variable exists for the developer or operator deploying the application (global installs,
  containers, editable mounts) to point at a `.env` outside the `sys.prefix` layout. Anyone
  who can set this environment variable for a Python process can already set arbitrary
  environment variables for that process directly, and typically run arbitrary code in it,
  so path traversal and "load an unexpected file" are **out of scope** - there is no
  privilege boundary being crossed.

- **The `.env` file contents** are parsed by `python-dotenv`; `interpolate=True` means
  `${VAR}` references are expanded from the existing environment. The file is expected to be
  under the same trust boundary as the project's source code. A `.env` an attacker can write
  is equivalent to source code an attacker can write.

- **`AUTOREAD_ENFORCE_DOTENV`** only toggles whether `.env` values override pre-existing
  environment variables. Both settings are safe; neither widens the trust boundary.

What *is* in scope: this package must never crash an interpreter it is loaded into
(hence "warn, never raise"), and must not leak `.env` contents into warnings, logs or
tracebacks. Warnings emitted by this package intentionally contain only file paths and
exception types, never file contents or variable values.
